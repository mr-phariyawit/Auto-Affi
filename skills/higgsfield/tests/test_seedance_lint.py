"""Behavioral tests for the Seedance prompt linter, using synthetic prompts only."""
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'higgsfield-seedance-prompt/scripts/lint_prompt.py'
BIBLE = ROOT / 'higgsfield-bible-director/references/bible-snapshot.md'

spec = importlib.util.spec_from_file_location('lint_prompt', SCRIPT)
lint_prompt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint_prompt)

JOB = {'model': 'seedance-2.0', 'duration_s': 15, 'aspect': '9:16', 'resolution': '1080p',
       'references': ['@jiab', '@serum'], 'audio_reference': False}

CLEAN = """\
ACTIVE REFERENCES:
@jiab — character appearance only; background NOT inherited.
@serum — product shape and label only.
SCENE CONTEXT: bright bathroom vanity, morning.
FORMAT MODE: Timed multishot.
SHOT 1 (0.0–5.0s): medium shot, 35mm, static. @jiab lifts @serum to chest height.
SHOT 2 (5.0–10.0s): close-up, 85mm, push-in 0.5 m. @jiab taps two drops onto her palm.
SHOT 3 (10.0–15.0s): close-up, 50mm, static. @serum label faces camera, held 2 s.
CAMERA: tripod, push-in 0.5 m over 3 s, no tilt, no rotation.
LIGHTING: soft window key from camera left.
AUDIO: No music. Environmental SFX only. No subtitles.
POSITIVE LOCKS: Exactly one named character. Label text reads "GLOW 10%".
"""


def rules(findings, severity=None):
    return sorted({f['rule'] for f in findings if severity is None or f['severity'] == severity})


def run(prompt, **job):
    return lint_prompt.lint(prompt, {**JOB, **job})


class SeedanceLint(unittest.TestCase):
    def test_clean_prompt_has_no_findings(self):
        self.assertEqual(run(CLEAN), [])

    def test_tag_used_but_not_declared_is_error(self):
        prompt = CLEAN.replace('label faces camera', 'label faces @mirror')
        self.assertIn('R01', rules(run(prompt), 'error'))

    def test_declared_tag_not_attached_is_error(self):
        self.assertIn('R01', rules(run(CLEAN, references=['@jiab']), 'error'))

    def test_attached_but_unused_tag_is_warning(self):
        found = run(CLEAN, references=['@jiab', '@serum', '@towel'])
        self.assertIn('R01', rules(found, 'warn'))
        self.assertNotIn('R01', rules(found, 'error'))

    def test_references_without_declaration_block_is_error(self):
        prompt = CLEAN.split('SCENE CONTEXT', 1)[1]
        self.assertIn('R00', rules(run('SCENE CONTEXT' + prompt), 'error'))

    def test_duration_over_model_limit(self):
        self.assertIn('R08', rules(run(CLEAN, duration_s=20), 'error'))
        self.assertNotIn('R08', rules(run(CLEAN, duration_s=20, model='seedance-2.5', resolution='720p')))

    def test_timecodes_must_reach_job_duration(self):
        prompt = CLEAN.replace('(10.0–15.0s)', '(10.0–12.0s)')
        self.assertIn('R09', rules(run(prompt), 'error'))

    def test_timecode_gap_is_warning(self):
        prompt = CLEAN.replace('(5.0–10.0s)', '(6.0–10.0s)')
        self.assertIn('R09', rules(run(prompt), 'warn'))

    def test_declared_shot_count_must_match_blocks(self):
        prompt = CLEAN.replace('FORMAT MODE: Timed multishot.', 'FORMAT MODE: Timed multishot, exactly four shots and three cuts.')
        self.assertIn('R10', rules(run(prompt), 'error'))

    def test_no_timecodes_mode_with_timecodes(self):
        prompt = CLEAN.replace('Timed multishot', 'Sequence of cuts, no timecodes')
        self.assertIn('R11', rules(run(prompt)))

    def test_cut_line_needs_lens_or_fov(self):
        prompt = CLEAN + 'CUT 1 — wide shot, slow dolly: @jiab walks in.\n'
        self.assertIn('R12', rules(run(prompt)))
        ok = CLEAN + 'CUT 1 — wide shot, 47°, slow dolly: @jiab walks in.\n'
        self.assertNotIn('R12', rules(run(ok)))

    def test_vague_camera_speed_without_numbers(self):
        prompt = CLEAN.replace('CAMERA: tripod, push-in 0.5 m over 3 s, no tilt, no rotation.', 'CAMERA: fast dramatic push-in.')
        self.assertIn('R14', rules(run(prompt)))
        shot = CLEAN.replace('static. @jiab lifts', 'camera moves fast. @jiab lifts')
        self.assertIn('R14', rules(run(shot)))

    def test_negated_state_outside_camera_block_warns(self):
        prompt = CLEAN.replace('taps two drops onto her palm', 'is not crying while tapping drops')
        self.assertIn('R06', rules(run(prompt), 'warn'))

    def test_camera_exclusions_are_allowed(self):
        self.assertNotIn('R06', rules(run(CLEAN)))

    def test_match_cut_needs_exact_pose_language(self):
        prompt = CLEAN.replace('SHOT 2 (5.0–10.0s):', 'SHOT 2 (5.0–10.0s): match cut from shot 1.')
        self.assertIn('R18', rules(run(prompt), 'error'))
        ok = prompt.replace('match cut from shot 1.', 'match cut: end pose of shot 1 EXACTLY matches this start pose.')
        self.assertNotIn('R18', rules(run(ok)))

    def test_dialogue_needs_no_subtitles_and_lipsync(self):
        prompt = CLEAN.replace('AUDIO: No music. Environmental SFX only. No subtitles.', 'AUDIO: No music.')
        prompt += '@jiab: "Two drops are enough."\n'
        found = rules(run(prompt))
        self.assertIn('R19', found)
        self.assertIn('R20', found)

    def test_music_ban_conflicts_with_attached_audio(self):
        self.assertIn('R21', rules(run(CLEAN, audio_reference=True)))

    def test_missing_audio_block_warns(self):
        prompt = CLEAN.replace('AUDIO: No music. Environmental SFX only. No subtitles.\n', '')
        self.assertIn('R21', rules(run(prompt)))

    def test_invalid_hex_colour(self):
        self.assertIn('R24', rules(run(CLEAN + 'COLOR: accent #D1EF1 and #GG0000.\n')))
        self.assertNotIn('R24', rules(run(CLEAN + 'COLOR: accent #d1fe17.\n')))

    def test_vague_headcount(self):
        self.assertIn('R27', rules(run(CLEAN + 'No extra people.\n')))

    def test_prompt_settings_must_match_job(self):
        self.assertIn('R30', rules(run(CLEAN + 'OUTPUT SETTINGS: 16:9 aspect ratio, 8 seconds total.\n'), 'error'))

    def test_resolution_not_recorded_for_model(self):
        self.assertIn('M01', rules(run(CLEAN, model='seedance-2.5', resolution='1080p'), 'warn'))

    def test_unknown_model_is_error(self):
        self.assertIn('M00', rules(run(CLEAN, model='veo-9'), 'error'))

    def test_sub_ranges_and_decades_are_not_segments(self):
        prompt = CLEAN.replace('SHOT 1 (0.0–5.0s): medium shot, 35mm, static.',
                               'SHOT 1 (0.0–5.0s): medium shot, 35mm, LENS LOCK from 0.0s to 2.5s, 1980s–90s decor.')
        self.assertEqual(run(prompt), [])

    def test_style_prefix_drift_across_project(self):
        a = 'STYLE PREFIX: warm film grain, 24fps.\n' + CLEAN
        b = 'STYLE PREFIX: cold digital look, 60fps.\n' + CLEAN
        results = lint_prompt.lint_project({'a': a, 'b': b}, JOB)
        self.assertEqual(rules(results['a']), [])
        self.assertIn('R22', rules(results['b']))
        c = 'STYLE PREFIX (override): night scene, 24fps.\n' + CLEAN
        self.assertNotIn('R22', rules(lint_prompt.lint_project({'a': a, 'c': c}, JOB)['c']))

    def test_eval_regressions_iteration1(self):
        # "REFERENCES (appearance only):" header is a declaration block
        alt = CLEAN.replace('ACTIVE REFERENCES:', 'REFERENCES (appearance only):')
        self.assertEqual(rules(run(alt), 'error'), [])
        # "SHOT 1 rig:" is a camera note, not a shot block
        rig = CLEAN.replace('FORMAT MODE: Timed multishot.', 'FORMAT MODE: Timed multishot, exactly three shots and two cuts.')
        rig += 'Rig notes: SHOT 1 rig: tripod.\nSHOT 1 rig: tripod, 1.2 m high.\n'
        self.assertNotIn('R10', rules(run(rig)))
        # course phrase "Do not reproduce the reference 1:1" is not an aspect ratio
        self.assertNotIn('R30', rules(run(CLEAN + 'Location is a style reference. Do not reproduce the reference 1:1.\n')))
        self.assertIn('R30', rules(run(CLEAN + 'Framing: 16:9 widescreen.\n')))
        # explicit continuity wording counts as a match-cut spec
        mc = CLEAN.replace('SHOT 2 (5.0–10.0s):', 'SHOT 2 (5.0–10.0s): match cut; the bottle sits at the exact same screen position.')
        self.assertNotIn('R18', rules(run(mc)))

    def test_every_rule_citation_is_in_bible(self):
        bible = BIBLE.read_text(encoding='utf-8')
        cites = [c for rule in lint_prompt.RULES.values() for c in re.findall(r'\[[^\]]+\]', rule['cite'])]
        self.assertTrue(cites)
        self.assertEqual([c for c in cites if c not in bible], [])

    def test_cli_exit_code_and_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            p, j = Path(tmp, 'p.txt'), Path(tmp, 'job.json')
            p.write_text(CLEAN)
            j.write_text(json.dumps(JOB))
            ok = subprocess.run([sys.executable, str(SCRIPT), str(p), '--job', str(j), '--json'], capture_output=True, text=True)
            self.assertEqual(ok.returncode, 0, ok.stderr)
            self.assertEqual(json.loads(ok.stdout)['errors'], 0)
            j.write_text(json.dumps({**JOB, 'duration_s': 20}))
            bad = subprocess.run([sys.executable, str(SCRIPT), str(p), '--job', str(j)], capture_output=True, text=True)
            self.assertEqual(bad.returncode, 1)
            self.assertIn('R08', bad.stdout)


if __name__ == '__main__':
    unittest.main()
