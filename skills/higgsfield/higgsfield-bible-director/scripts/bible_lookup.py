#!/usr/bin/env python3
"""Read selected Bible v2 sections without loading the full source. No network or writes.

IDs: course `A01`; lesson `A01.03` (every v2 bullet citing [A01.L03 ...], grouped by subsection);
cross-course / prompt-bank / video-only / contradiction / diff sections `B1`..`F9` (### headings).
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SOURCE_SCOPE = '171 lessons + 46 prompt-bank + 16 course pages; article + audio + visual; audited notes'
LESSON_CITE = re.compile(r'\[(A\d{2})\.L(\d{2})\b')


def _block_end(headings, pos, content):
    level = len(headings[pos][1])
    return next((h.start() for h in headings[pos + 1:] if len(h[1]) <= level), len(content))


def _lesson_sections(course_id, text):
    """Collect each cited bullet (with its ### label) under every lesson it cites."""
    lessons, label = {}, ''
    for line in text.splitlines():
        if line.startswith('### '):
            label = line[4:].strip()
            continue
        cited = {f'{c}.{n}' for c, n in LESSON_CITE.findall(line) if c == course_id}
        for lesson_id in cited:
            groups = lessons.setdefault(lesson_id, {})
            groups.setdefault(label, []).append(line.strip())
    return {
        lesson_id: '\n'.join(f'### {lbl}\n' + '\n'.join(lines) for lbl, lines in groups.items())
        for lesson_id, groups in lessons.items()
    }


def load_sections(source=None, provenance=None):
    source = Path(source or SKILL_ROOT / 'references/bible-snapshot.md')
    provenance = Path(provenance or SKILL_ROOT / 'references/provenance.json')
    data = source.read_bytes()
    if hashlib.sha256(data).hexdigest() != json.loads(provenance.read_text())['source_sha256']:
        raise ValueError('Bible snapshot changed; refresh provenance before using this index.')
    content = data.decode('utf-8')
    headings = list(re.finditer(r'(?m)^(#{2,4}) (.+)$', content))
    sections = {}

    def add(section_id, title, text):
        if section_id in sections:
            raise ValueError(f'Duplicate ID: {section_id}')
        sections[section_id] = {'id': section_id, 'title': title, 'text': text}

    for pos, match in enumerate(headings):
        level, title = len(match[1]), match[2]
        course = re.match(r'(A\d{2})\b(?!\.)', title)
        other = re.match(r'([B-F]\d+(?:\.\d+)?)(?:[.\s—:]|$)', title)
        if level == 2 and course:
            text = content[match.start():_block_end(headings, pos, content)].strip()
            add(course[1], title, text)
            for lesson_id, lesson_text in sorted(_lesson_sections(course[1], text).items()):
                add(lesson_id, f'{lesson_id} (bullets citing {lesson_id.replace(".", ".L")})', lesson_text)
        elif level == 3 and other:
            add(other[1], title, content[match.start():_block_end(headings, pos, content)].strip())
    return sections


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--section', action='append', default=[], help='Exact ID; repeat to retrieve several.')
    parser.add_argument('--list', action='store_true', help='List section IDs and titles.')
    parser.add_argument('--search', help='Find matching section titles or text.')
    parser.add_argument('--limit', type=int, default=8, help='Maximum search matches, default 8.')
    parser.add_argument('--json', action='store_true', help='Machine-readable output.')
    args = parser.parse_args(argv)
    if not args.section and not args.list and not args.search:
        parser.error('Choose --section, --list, or --search.')
    if args.limit < 1:
        parser.error('--limit must be positive.')
    try:
        sections = load_sections()
        unknown = [sid for sid in args.section if sid not in sections]
        if unknown:
            raise ValueError('Unknown section IDs: ' + ', '.join(unknown))
        selected = list(dict.fromkeys(args.section))
        if args.list:
            selected.extend(sid for sid in sections if sid not in selected)
        if args.search:
            query = args.search.casefold()
            # Prefer leaf matches to returning a whole course for a single lesson match.
            matches = [sid for sid, row in sections.items() if query in row['text'].casefold()]
            matches.sort(key=lambda sid: (len(sections[sid]['text']), sid))
            selected.extend(sid for sid in matches[:args.limit] if sid not in selected)
        rows = [dict(sections[sid]) for sid in selected]
        if args.list or args.search:
            for row in rows:
                if row['id'] not in args.section:
                    row.pop('text')
        if args.json:
            print(json.dumps({'source_scope': SOURCE_SCOPE, 'sections': rows}, ensure_ascii=False, indent=2))
        else:
            print('Source: Bible v2.0; audited course notes (prices/UI as recorded), not current API documentation.\n')
            for row in rows:
                print(row.get('text', row['title']) + '\n')
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
