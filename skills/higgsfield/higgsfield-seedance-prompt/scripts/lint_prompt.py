#!/usr/bin/env python3
"""Lint a Seedance prompt against the job settings, using rules from the audited Higgsfield Bible v2.

Usage: lint_prompt.py PROMPT.txt [PROMPT2.txt ...] --job job.json [--json]
job.json: {"model": "seedance-2.0", "duration_s": 15, "aspect": "9:16", "resolution": "1080p",
           "references": ["@hero", "@product"], "audio_reference": false}
Exit 1 when any error-severity finding exists. Local, read-only, no network.
A PASS means the prompt is structurally consistent; it does not mean the generation will look right.
"""
import argparse
import json
import re
import sys
from pathlib import Path

RULES = {
    'M00': {'title': 'model not in the recorded limits table', 'cite': '[A05.L02 t=01:41] [A05.L02 t=01:38]'},
    'M01': {'title': 'resolution not recorded for this model', 'cite': '[A10.L04 t=01:56–02:08] [A01.L05 frames t=00:05] [A05.L11 t=00:00]'},
    'M02': {'title': 'aspect ratio not recorded for this model', 'cite': '[A01.L05 frames t=00:05]'},
    'R00': {'title': 'references used but no ACTIVE REFERENCES / REFERENCE DEFINITIONS block', 'cite': '[A16.L01 frames t=01:30] [A15.L03 article]'},
    'R01': {'title': '@tag must be declared, attached and used', 'cite': '[A16.L01 frames t=01:30] [A16.L01 frames t=01:40] [A01.L03 t=05:10-05:26] [A10.L04 t=00:06–00:36]'},
    'R03': {'title': 'reference line should state its scope (… only / NOT inherited)', 'cite': '[A01.L05 cue recreate-1b] [A15.L03 article] [A10.L01 frames t=00:35]'},
    'R06': {'title': 'state/emotion described by negation (model may read "not crying" as "crying")', 'cite': '[A02.L07 t=00:33-00:48] [A16.L02 t=03:19] [A16.L05 t=00:57]'},
    'R08': {'title': 'duration over the recorded model limit', 'cite': '[A05.L02 t=01:41] [A05.L02 t=01:38]'},
    'R09': {'title': 'timed segments must start at 0, be contiguous and end at the job duration', 'cite': '[A16.L04 frames t=00:26] [A01.L09 frames t=02:55] [A10.L04 cue cue-scene-2]'},
    'R10': {'title': 'declared shot/cut count must match the SHOT/CUT blocks (cuts = shots - 1)', 'cite': '[A15.L03 article] [A15.L09 t=01:18] [A15.L05 frames t=00:45]'},
    'R11': {'title': '"no timecodes" format mode but timecodes present', 'cite': '[A01.L05 cue recreate-1b] [A01.L07 cue recreate-2-1c]'},
    'R12': {'title': 'CUT line should give lens (mm) or FOV (°)', 'cite': '[A06.L10 frames t=01:45] [A01.L05 cue recreate-1b] [A10.L05 cue cue-scene-3]'},
    'R14': {'title': 'camera speed as a vague word without numbers', 'cite': '[A16.L02 t=01:04] [A16.L03 t=02:44] [A02.L14 t=00:26-00:36] [PB.36]'},
    'R18': {'title': 'match cut without explicit EXACTLY-matching pose', 'cite': '[A16.L04 t=00:24] [A16.L04 t=00:35] [A06.L14 t=00:53]'},
    'R19': {'title': 'dialogue present but no "No subtitles"', 'cite': '[A08.L04 frames t=01:30] [A16.L02 frames t=01:22] [A10.L01 frames t=00:35]'},
    'R20': {'title': 'dialogue present but no lip-sync line', 'cite': '[A15.L06 article]'},
    'R21': {'title': 'AUDIO block missing, or "No music" while an audio reference is attached', 'cite': '[A10.L04 t=01:26–01:46] [A06.L13 t=04:05] [A08.L04 cue cue-l4-fungal]'},
    'R22': {'title': 'style prefix differs between prompts of one project (label per-scene changes "override")', 'cite': '[A06.L10 t=02:02] [A06.L12 t=02:15] [A10.L01 frames t=00:35]'},
    'R24': {'title': 'malformed hex colour (AI-written hex can be mistyped)', 'cite': '[A09.L03 t=01:59–02:04] [A09.L03 cue c3j]'},
    'R27': {'title': 'vague headcount; state "Exactly N named characters"', 'cite': '[A16.L01 frames t=01:30] [A01.L07 cue recreate-2-1c]'},
    'R30': {'title': 'aspect/duration written in the prompt contradicts the job settings', 'cite': '[A16.L01 frames t=01:40] [A09.L08 frames t=00:40] [A09.L06 cue c6a]'},
}

# As recorded in the courses (not current API docs).
MODELS = {
    'seedance-2.0': {'max_s': 15, 'resolutions': {'480p', '720p', '1080p', '4k'},
                     'aspects': {'auto', '16:9', '9:16', '4:3', '3:4', '1:1', '21:9'}},
    'seedance-2.5': {'max_s': 30, 'resolutions': {'720p'}, 'aspects': {'9:16'}},
}
ASPECTS = {'16:9', '9:16', '21:9', '4:3', '3:4', '1:1'}

HEADERS = sorted([
    'ACTIVE REFERENCES', 'REFERENCE DEFINITIONS', 'CHARACTERS', 'SCENE CONTEXT', 'SCENE', 'LOCATION MAP',
    'LOCATION', 'FIRST FRAME', 'BLOCKING', 'FORMAT MODE', 'OPTICS', 'CAMERA', 'ACTION', 'PERFORMANCE', 'ACTING',
    'PHYSICS', 'LIGHTING', 'COLOR', 'COLOUR', 'AUDIO', 'STYLE PREFIX', 'STYLE', 'POSITIVE LOCKS', 'CONSTRAINTS',
    'TECHNICAL BLOCK', 'TECHNICAL', 'SUBJECT', 'MULTISHOT', 'OUTPUT SETTINGS', 'FORBIDDEN', 'NEGATIVE',
    'CONTINUITY', 'MATERIAL', 'CHARACTER DESIGN', 'PROMPT', 'SFX', 'LAYOUT', 'PRACTICAL VFX', 'SKY', 'FOG', 'WEATHER',
    'REFERENCES', 'SETTING', 'AVOID', 'OUTPUT', 'SOUND',
], key=len, reverse=True)
HEADER_RE = re.compile(r'^\s*(?:—\s*)?(' + '|'.join(map(re.escape, HEADERS)) + r')\b\s*(?:\([^)]*\))?\s*(?:—|:|$)')
SHOT_RE = re.compile(r'^\s*(SHOT|CUT)\s+\d+\s*(?:\(|:|—|–|-)', re.I)
DECLARE = {'ACTIVE REFERENCES', 'REFERENCE DEFINITIONS', 'REFERENCES', 'CHARACTERS'}
# Blocks where "no X" exclusion lists are the taught form, not a negated state.
NEGATION_OK = {'CAMERA', 'CONSTRAINTS', 'FORBIDDEN', 'NEGATIVE', 'AUDIO', 'SOUND', 'AVOID', 'TECHNICAL',
               'TECHNICAL BLOCK', 'OUTPUT SETTINGS', 'OUTPUT', 'STYLE', 'STYLE PREFIX', 'CONTINUITY', 'POSITIVE LOCKS'} | DECLARE
TAG_RE = re.compile(r'(?<![\w.])@[A-Za-z][\w-]*')
RANGE_RE = re.compile(r'(?<![\d.:])(\d+(?:\.\d+)?)\s*s?\s*(?:–|—|-|to)\s*(\d+(?:\.\d+)?)\s*s\b'
                      r'|(?<![\d:])(\d+):(\d{2})\s*(?:–|—|-|to)\s*(\d+):(\d{2})(?![\d:])')
NEGATED_STATE = re.compile(r"\b(?:not|never|isn't|doesn't)\s+\w+(?:ing|ed)\b"
                           r'|\bno\s+(?:tears|smil\w*|emotion\w*|expression\w*|fear|anger)\b', re.I)
NUMBERS = {w: i for i, w in enumerate('zero one two three four five six seven eight nine ten eleven twelve'.split())}


def norm_model(name):
    return re.sub(r'[\s_]+', '-', str(name).strip().lower())


def parse(prompt):
    """Return [(line_no, section, text)] where section is the current header or SHOT."""
    rows, section = [], ''
    for n, line in enumerate(prompt.splitlines(), 1):
        header = HEADER_RE.match(line)
        if header:
            section = header[1]
        elif SHOT_RE.match(line):
            section = 'SHOT'
        rows.append((n, section, line))
    return rows


def ranges(text):
    """Segment timecodes only: the first range near the line start ("0.0s to 5.5s —", "SHOT 2 (5–10s):").
    Ranges later in the line (lens locks inside a segment, "1980s–90s") are not segments."""
    m = RANGE_RE.search(text)
    if not m or m.start() > 25:
        return []
    a, b = (float(m[1]), float(m[2])) if m[1] is not None else \
        (int(m[3]) * 60 + int(m[4]), int(m[5]) * 60 + int(m[6]))
    return [(a, b)] if b > a else []


def lint(prompt, job):
    found = []

    def add(rule, severity, message, line=None):
        found.append({'rule': rule, 'severity': severity, 'message': message, 'line': line, 'cite': RULES[rule]['cite']})

    rows = parse(prompt)
    model_key = norm_model(job.get('model', ''))
    model = MODELS.get(model_key)
    duration = job.get('duration_s')
    aspect = str(job.get('aspect', '')).lower()

    if model is None:
        add('M00', 'error', f"model {job.get('model')!r} unknown; recorded: {', '.join(MODELS)}")
    else:
        res = str(job.get('resolution', '')).lower()
        if res and res not in model['resolutions']:
            add('M01', 'warn', f'{res} not seen for {model_key} in the courses (recorded: {sorted(model["resolutions"])})')
        if aspect and aspect not in model['aspects']:
            add('M02', 'warn', f'{aspect} not seen for {model_key} in the courses')
        if duration is not None and duration > model['max_s']:
            add('R08', 'error', f'{duration}s > recorded max {model["max_s"]}s for {model_key}')

    # References
    declared, used, declare_lines = set(), {}, []
    for n, section, text in rows:
        tags = {t.lower() for t in TAG_RE.findall(text)}
        if section in DECLARE:
            declared |= tags
            if tags:
                declare_lines.append((n, text))
        else:
            for t in tags:
                used.setdefault(t, n)
    attached = {t.lower() for t in job.get('references', [])}
    if (attached or used) and not any(s in DECLARE for _, s, _ in rows):
        add('R00', 'error', 'add an ACTIVE REFERENCES block declaring every @tag and its role')
    elif declare_lines or used:
        for t, n in sorted(used.items()):
            if t not in declared:
                add('R01', 'error', f'{t} used but not declared in ACTIVE REFERENCES', n)
        if 'references' in job:
            for t in sorted(declared - attached):
                add('R01', 'error', f'{t} declared but not attached to the job (Element name must match exactly)')
            for t in sorted(attached - declared - set(used)):
                add('R01', 'warn', f'{t} attached but never declared or used')
        for t in sorted(declared - set(used)):
            add('R01', 'warn', f'{t} declared but not used in the prompt body')
        unscoped = [n for n, text in declare_lines
                    if not re.search(r'\bonly\b|not inherited|reference only|\bcontrols\b', text, re.I)]
        if unscoped:
            add('R03', 'warn', 'state what each reference controls ("appearance only", "NOT inherited") on lines '
                + ', '.join(f'L{n}' for n in unscoped), unscoped[0])

    # Timing
    spans = [(n, a, b) for n, s, t in rows if s != 'OUTPUT SETTINGS' for a, b in ranges(t)]
    lower = prompt.lower()
    if spans:
        if 'no timecodes' in lower:
            add('R11', 'warn', 'remove timecodes or switch FORMAT MODE to "Timed multishot"', spans[0][0])
        spans.sort(key=lambda x: x[1])
        if spans[0][1] != 0:
            add('R09', 'warn', f'first segment starts at {spans[0][1]}s, not 0', spans[0][0])
        for (n1, _, end), (n2, start, _) in zip(spans, spans[1:]):
            if abs(start - end) > 0.05:
                add('R09', 'warn', f'gap/overlap between {end}s and {start}s', n2)
        last = max(b for _, _, b in spans)
        if duration is not None and abs(last - duration) > 0.05:
            add('R09', 'error', f'segments end at {last}s but the job is {duration}s')
        if model and last > model['max_s']:
            add('R08', 'error', f'timecode {last}s > recorded max {model["max_s"]}s')

    shot_lines = [n for n, _, t in rows if SHOT_RE.match(t) and SHOT_RE.match(t)[1].upper() == 'SHOT']
    cut_lines = [n for n, _, t in rows if SHOT_RE.match(t) and SHOT_RE.match(t)[1].upper() == 'CUT']
    blocks = len(shot_lines) or len(cut_lines)
    for m in re.finditer(r'exactly\s+(\w+)\s+shots?(?:\s*(?:and|,)\s*(?:only\s+)?(\w+)\s+cuts?)?', prompt, re.I):
        shots = NUMBERS.get(m[1].lower(), int(m[1]) if m[1].isdigit() else None)
        cuts = NUMBERS.get((m[2] or '').lower(), int(m[2]) if (m[2] or '').isdigit() else None)
        if shots is not None and blocks and shots != blocks:
            add('R10', 'error', f'declares {shots} shots but has {blocks} SHOT/CUT blocks')
        if shots is not None and cuts is not None and cuts != shots - 1:
            add('R10', 'error', f'{shots} shots need {shots - 1} cuts, not {cuts}')

    for n in cut_lines:
        if not re.search(r'\d+\s?mm\b|\d+(?:\.\d+)?\s?°', rows[n - 1][2]):
            add('R12', 'warn', 'add shot size + lens mm or FOV°', n)

    # Language
    for n, section, text in rows:
        cam = text if section == 'CAMERA' else ''
        if not cam and (m := re.search(r'\bcamera\b[^.]*', text, re.I)):
            cam = m[0]  # only the camera clause, not the shot's timecode/lens
        if cam and re.search(r'\b(fast|slow|slowly|quick|quickly|rapid)\b', cam, re.I) \
                and not re.search(r'\d+(?:\.\d+)?\s?(?:m|cm|°|s|mm|x)\b', cam):
            add('R14', 'warn', 'replace speed words with numbers (metres, degrees, seconds, ratios)', n)
        if section not in NEGATION_OK and NEGATED_STATE.search(text):
            add('R06', 'warn', f'describe the state positively: {NEGATED_STATE.search(text)[0]!r}', n)
        if re.search(r'no extra people', text, re.I):
            add('R27', 'warn', 'write "Exactly N named characters" instead', n)
        for token in re.findall(r'(?<![\w&])#([0-9A-Za-z]{3,8})\b', text):
            hexish = sum(c in '0123456789abcdefABCDEF' for c in token) / len(token)
            if hexish >= 0.5 and not re.fullmatch(r'[0-9a-fA-F]{6}|[0-9a-fA-F]{3}', token):
                add('R24', 'warn', f'#{token} is not a valid hex colour', n)
        aspect_ctx = section in ('OUTPUT SETTINGS', 'OUTPUT') or re.search(
            r'aspect|ratio|framing|frame|vertical|horizontal|widescreen|anamorphic|format', text, re.I)
        for a in re.findall(r'(?<![\d:])(\d{1,2}:\d{1,2})(?![\d:])', text) if aspect_ctx else []:
            if a in ASPECTS and aspect and a != aspect and not re.search(r'reproduce[^.]*' + a, text, re.I):
                add('R30', 'error', f'prompt says {a} but the job is {aspect}', n)
        if section in ('OUTPUT SETTINGS', 'OUTPUT') or re.search(r'seconds? total|s total', text, re.I):
            for d in re.findall(r'(\d+(?:\.\d+)?)\s*(?:seconds?|s)\s+total', text, re.I):
                if duration is not None and abs(float(d) - duration) > 0.05:
                    add('R30', 'error', f'prompt says {d}s total but the job is {duration}s', n)

    if re.search(r'match[- ]cut', prompt, re.I) and not re.search(
            r'exactly match|matches exactly|same pose|exact same (?:screen )?(?:position|pose|angle)|identical (?:pose|position)',
            prompt, re.I):
        add('R18', 'error', 'state that the end pose of shot N EXACTLY matches the start of shot N+1')

    dialogue = re.search(r'@[\w-]+[^"\n]{0,40}?(?::|\bsays\b|\bsaid\b)\s*"[^"]+"', prompt)
    if dialogue:
        if 'no subtitle' not in lower:
            add('R19', 'warn', 'dialogue present: add "No subtitles" to AUDIO')
        if not re.search(r'lip[- ]?sync', lower):
            add('R20', 'warn', 'dialogue present: add a lip-sync line (or use VO instead of on-camera speech)')

    if not any(s in ('AUDIO', 'SOUND', 'SFX') for _, s, _ in rows):
        add('R21', 'warn', 'add an AUDIO block (default: "No music. Environmental SFX only.")')
    elif job.get('audio_reference') and re.search(r'no music', lower):
        add('R21', 'warn', 'an audio reference is attached but the prompt says "No music"')
    return found


def style_prefix(prompt):
    rows = parse(prompt)
    return '\n'.join(t.strip() for _, s, t in rows if s == 'STYLE PREFIX').strip()


def lint_project(prompts, job):
    """Lint several prompts of one project; adds R22 when style prefixes drift."""
    results = {name: lint(text, job) for name, text in prompts.items()}
    prefixes = {name: style_prefix(text) for name, text in prompts.items()}
    base = next((p for p in prefixes.values() if p), '')
    for name, prefix in prefixes.items():
        if base and prefix and prefix != base and 'override' not in prefix.lower():
            results[name].append({'rule': 'R22', 'severity': 'warn', 'line': None, 'cite': RULES['R22']['cite'],
                                  'message': 'STYLE PREFIX differs from the first prompt; reuse it or label the change "override"'})
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('prompts', nargs='+', type=Path)
    parser.add_argument('--job', required=True, type=Path)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    try:
        job = json.loads(args.job.read_text(encoding='utf-8'))
        prompts = {str(p): p.read_text(encoding='utf-8') for p in args.prompts}
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 2
    results = lint_project(prompts, job)
    errors = sum(f['severity'] == 'error' for fs in results.values() for f in fs)
    warns = sum(f['severity'] == 'warn' for fs in results.values() for f in fs)
    if args.json:
        print(json.dumps({'errors': errors, 'warnings': warns, 'results': results}, ensure_ascii=False, indent=2))
    else:
        for name, findings in results.items():
            print(f'{name}: {"FAIL" if any(f["severity"] == "error" for f in findings) else "PASS"}'
                  f' ({sum(f["severity"] == "error" for f in findings)} errors, {sum(f["severity"] == "warn" for f in findings)} warnings)')
            for f in sorted(findings, key=lambda f: (f['severity'] != 'error', f['line'] or 0)):
                where = f' L{f["line"]}' if f['line'] else ''
                print(f'  {f["severity"].upper():5} {f["rule"]}{where}: {f["message"]}  {f["cite"]}')
        print('Structural lint only: a PASS does not mean the generated video is correct.')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
