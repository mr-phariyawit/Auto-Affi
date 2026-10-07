#!/usr/bin/env python3
"""Read selected Bible sections without loading the full source. No network or writes."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]


def load_sections():
    source = SKILL_ROOT / 'references/bible-snapshot.md'
    data = source.read_bytes()
    provenance = json.loads((SKILL_ROOT / 'references/provenance.json').read_text())
    if hashlib.sha256(data).hexdigest() != provenance['source_sha256']:
        raise ValueError('Bible snapshot changed; refresh provenance before using this index.')
    content = data.decode('utf-8')
    headings = list(re.finditer(r'(?m)^(#{2,4}) (.+)$', content))
    sections = {}
    for pos, match in enumerate(headings):
        named = re.match(r'(A\d{2}(?:\.\d{2})?|[B-F]\d+)(?:\. | — )', match[2])
        if not named:
            continue
        section_id = named[1]
        if section_id in sections:
            raise ValueError(f'Duplicate ID: {section_id}')
        end = next((h.start() for h in headings[pos + 1:] if len(h[1]) <= len(match[1])), len(content))
        sections[section_id] = {'id': section_id, 'title': match[2], 'text': content[match.start():end].strip()}
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
            print(json.dumps({'source_scope': '171 lesson texts; not all videos watched', 'sections': rows}, ensure_ascii=False, indent=2))
        else:
            print('Source: Bible v1.0; lesson-text synthesis, not current API documentation.\n')
            for row in rows:
                print(row.get('text', row['title']) + '\n')
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
