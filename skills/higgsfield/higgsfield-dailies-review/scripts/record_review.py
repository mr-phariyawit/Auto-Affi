#!/usr/bin/env python3
"""Append a take's review verdict to RUN/ledger.jsonl (same ledger gate_cli writes spends to).

Usage: record_review.py --run RUN --label "shot01 take1" --verdict KEEP|REROLL|FIX-BRIEF|REJECT
                        [--issues "..."] [--keep "1.5-6.0s"] [--report path] [--reviewer name]
KEEP = all critical checks PASS · REROLL = one-off defect, brief works (same prompt) ·
FIX-BRIEF = repeated / brief-caused failure (change one variable) · REJECT = unusable, stop.
"""
import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

VERDICTS = ('KEEP', 'REROLL', 'FIX-BRIEF', 'REJECT')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--run', type=Path, required=True)
    ap.add_argument('--label', required=True)
    ap.add_argument('--verdict', choices=VERDICTS, required=True)
    ap.add_argument('--issues', default='')
    ap.add_argument('--keep', default='', help='keeper range(s), e.g. "1.5-6.0s"')
    ap.add_argument('--report', default='')
    ap.add_argument('--reviewer', default='agent')
    a = ap.parse_args(argv)
    a.run.mkdir(parents=True, exist_ok=True)
    entry = {'type': 'review', 'at': datetime.now(UTC).isoformat(), 'label': a.label, 'verdict': a.verdict,
             'issues': a.issues, 'keep': a.keep, 'report': a.report, 'reviewer': a.reviewer}
    with (a.run / 'ledger.jsonl').open('a', encoding='utf-8') as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + '\n')
    print(json.dumps(entry, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
