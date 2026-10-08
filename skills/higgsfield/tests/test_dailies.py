"""Behavioral tests for the dailies-review tools on synthetic ffmpeg clips (no real media, no network)."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'higgsfield-dailies-review/scripts'


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


HAVE_FFMPEG = shutil.which('ffmpeg') and shutil.which('ffprobe')


def make_clip(path, segments, audio=True, size='720x1280'):
    """segments: list of (kind, seconds); kind in testsrc|mandel|negate|black|still."""
    sources, n = [], len(segments)
    for kind, sec in segments:
        src = {
            'testsrc': f'testsrc2=s={size}:r=24:d={sec}',
            'mandel': f'mandelbrot=s={size}:r=24,trim=duration={sec}',
            'negate': f'testsrc2=s={size}:r=24:d={sec},negate',
            'black': f'color=black:s={size}:r=24:d={sec}',
            'still': f'testsrc2=s={size}:r=24:d=0.04,loop=loop=-1:size=1,trim=duration={sec},setpts=N/24/TB',
        }[kind]
        sources += ['-f', 'lavfi', '-i', src]
    total = sum(s for _, s in segments)
    cmd = ['ffmpeg', '-v', 'error', '-y', *sources]
    if audio:
        cmd += ['-f', 'lavfi', '-i', f'sine=f=440:d={total}']
    chain = ''.join(f'[{i}:v]' for i in range(n)) + f'concat=n={n}:v=1:a=0[v]'
    cmd += ['-filter_complex', chain, '-map', '[v]']
    if audio:
        cmd += ['-map', f'{n}:a', '-shortest']
    cmd += ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', str(path)]
    subprocess.run(cmd, check=True)
    return path


def status(report, check_id):
    return next(c['status'] for c in report['checks'] if c['id'] == check_id)


@unittest.skipUnless(HAVE_FFMPEG, 'ffmpeg not installed')
class DailiesReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.probe = load('probe_checks')
        cls.frames = load('review_frames')
        cls.record = load('record_review')
        cls.tmp = tempfile.TemporaryDirectory()
        t = Path(cls.tmp.name)
        cls.three = make_clip(t / 'three.mp4', [('testsrc', 2), ('mandel', 2), ('negate', 2)])
        cls.gap = make_clip(t / 'gap.mp4', [('testsrc', 2), ('black', 0.5), ('negate', 2)])
        cls.frozen = make_clip(t / 'frozen.mp4', [('testsrc', 2), ('still', 1.5), ('testsrc', 1)], audio=False)
        cls.prompt3 = t / 'p3.txt'
        cls.prompt3.write_text('SHOT 1 (0.0–2.0s): a.\nSHOT 2 (2.0–4.0s): b.\nSHOT 3 (4.0–6.0s): c.\n')
        cls.prompt2 = t / 'p2.txt'
        cls.prompt2.write_text('SHOT 1 (0.0–3.0s): a.\nSHOT 2 (3.0–6.0s): b.\n')
        cls.oner = t / 'oner.txt'
        cls.oner.write_text('CAMERA: ONE CONTINUOUS TAKE, NO CUTS, NO EDITS.\n')

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def job(self, **kw):
        return {'duration_s': 6, 'aspect': '9:16', 'resolution': '720p', **kw}

    def test_probe_matches_job(self):
        r = self.probe.run_checks(self.three, self.job(), self.prompt3.read_text())
        self.assertEqual(r['probe']['width'], 720)
        for cid in ('T01', 'T02', 'T03', 'T07'):
            self.assertEqual(status(r, cid), 'PASS', (cid, r['checks']))
        self.assertEqual(len(r['cuts']), 2)

    def test_duration_aspect_resolution_mismatch(self):
        r = self.probe.run_checks(self.three, self.job(duration_s=8, aspect='16:9', resolution='1080p'), '')
        self.assertEqual(status(r, 'T01'), 'ISSUE')
        self.assertEqual(status(r, 'T02'), 'ISSUE')
        self.assertEqual(status(r, 'T03'), 'ISSUE')

    def test_cut_count_against_prompt(self):
        self.assertEqual(status(self.probe.run_checks(self.three, self.job(), self.prompt2.read_text()), 'T07'), 'ISSUE')
        self.assertEqual(status(self.probe.run_checks(self.three, self.job(), self.oner.read_text()), 'T07'), 'ISSUE')
        self.assertEqual(status(self.probe.run_checks(self.three, self.job(), ''), 'T07'), 'NA')

    def test_black_gap_is_issue_and_one_transition(self):
        r = self.probe.run_checks(self.gap, self.job(duration_s=4.5), '')
        self.assertEqual(status(r, 'T05'), 'ISSUE')
        self.assertEqual(len(r['cuts']), 1)

    def test_freeze_and_missing_audio(self):
        r = self.probe.run_checks(self.frozen, self.job(duration_s=4.5, audio_expected=True), '')
        self.assertEqual(status(r, 'T06'), 'WARN')
        self.assertEqual(status(r, 'T04'), 'ISSUE')
        self.assertEqual(status(self.probe.run_checks(self.frozen, self.job(duration_s=4.5), ''), 'T04'), 'NA')

    def test_review_frames_outputs(self):
        with tempfile.TemporaryDirectory() as out:
            report = self.probe.run_checks(self.three, self.job(), self.prompt3.read_text())
            ref = Path(out) / 'ref.jpg'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=red:s=400x600', '-frames:v', '1',
                            str(ref)], check=True)
            m = self.frames.extract(self.three, Path(out) / 'frames', report=report, every=1.0, refs=[ref], bursts=[3.0])
            self.assertTrue(m['contact_sheets'])
            self.assertEqual(len(m['cut_pairs']), 2)
            self.assertEqual(len(m['ref_compare']), 4)
            self.assertEqual(len(m['bursts']), 1)
            for group in ('contact_sheets', 'cut_pairs', 'ref_compare', 'bursts', 'first_last'):
                for f in m[group]:
                    self.assertTrue(Path(f).stat().st_size > 0, f)
            rows = (Path(out) / 'frames/index.tsv').read_text().splitlines()
            self.assertGreater(len(rows), 6)

    def test_record_review_appends_ledger(self):
        with tempfile.TemporaryDirectory() as run:
            self.record.main(['--run', run, '--label', 'shot01 take1', '--verdict', 'REROLL',
                              '--issues', 'hand warps at 3.2s', '--report', 'r.json'])
            entry = json.loads((Path(run) / 'ledger.jsonl').read_text().splitlines()[-1])
            self.assertEqual(entry['type'], 'review')
            self.assertEqual(entry['verdict'], 'REROLL')
            with self.assertRaises(SystemExit):
                self.record.main(['--run', run, '--label', 'x', '--verdict', 'GREAT'])


class RubricCitations(unittest.TestCase):
    def test_rubric_citations_exist_in_bible(self):
        import re
        bible = (ROOT / 'higgsfield-bible-director/references/bible-snapshot.md').read_text(encoding='utf-8')
        rubric = (ROOT / 'higgsfield-dailies-review/references/rubric.md').read_text(encoding='utf-8')
        cites = re.findall(r'\[(?:A\d\d\.L\d\d|PB\.\d\d)[^\]]*\]', rubric)
        self.assertGreater(len(cites), 10)
        self.assertEqual([c for c in cites if c not in bible], [])


if __name__ == '__main__':
    unittest.main()
