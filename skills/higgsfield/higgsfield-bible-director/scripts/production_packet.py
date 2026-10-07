#!/usr/bin/env python3
"""Prepare and check local production-plan structure; never approve or call providers."""
import argparse
from datetime import date
import json
import math
from pathlib import Path
import shutil
import sys

MODES = ('cinematic', 'vfx', 'brand', 'faceless', 'game', 'agency', 'auto-affi')
SKILL_ROOT = Path(__file__).resolve().parents[1]


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value >= 0


def init_packet(run_dir, mode):
    run_dir.mkdir(parents=True, exist_ok=False)
    packet = {
        'schema_version': 1, 'run_id': run_dir.name, 'mode': mode,
        'brief': {'objective': '', 'deliverable': ''},
        'facts': [], 'assets': [], 'shots': [],
        'budget': {'currency': '', 'max_cost': None, 'spent_cost': 0, 'max_attempts_per_shot': None},
        'review': {'media_files': [], 'report_file': '', 'checks': [], 'blockers': []},
    }
    (run_dir / 'production-plan.json').write_text(json.dumps(packet, ensure_ascii=False, indent=2) + '\n')
    (run_dir / 'templates').mkdir()
    for file in (SKILL_ROOT / 'assets').glob('*.csv'):
        shutil.copy2(file, run_dir / 'templates' / file.name)
    return {'run_dir': str(run_dir), 'created': 'production-plan.json', 'state': 'draft',
            'execution_permission': 'not_determined; this helper never authorizes generation'}


def check_packet(run_dir, stage):
    packet = json.loads((run_dir / 'production-plan.json').read_text())
    errors, warnings = [], []
    if not isinstance(packet, dict):
        raise ValueError('Packet root must be an object.')

    def require(condition, message):
        if not condition:
            errors.append(message)

    def collection(key):
        rows = packet.get(key)
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            errors.append(f'{key} must be a list of objects.')
            return []
        return rows

    def index(rows, label):
        result = {}
        for row in rows:
            row_id = row.get('id')
            if not nonempty(row_id):
                errors.append(f'{label} needs a nonempty id.')
            elif row_id in result:
                errors.append(f'Duplicate {label} id: {row_id}')
            else:
                result[row_id] = row
        return result

    def local_file(value):
        if not nonempty(value):
            return False
        path = Path(value)
        if not path.is_absolute():
            path = run_dir / path
        return path.is_file()

    require(packet.get('schema_version') == 1, 'schema_version must be 1.')
    require(nonempty(packet.get('run_id')), 'run_id is missing.')
    require(packet.get('mode') in MODES, 'Unsupported mode.')
    brief = packet.get('brief')
    if not isinstance(brief, dict):
        errors.append('brief must be an object.'); brief = {}
    for key in ('objective', 'deliverable'):
        require(nonempty(brief.get(key)), f'brief.{key} is missing.')
    facts, assets, shots = collection('facts'), collection('assets'), collection('shots')
    fact_ids, asset_ids, shot_ids = index(facts, 'fact'), index(assets, 'asset'), index(shots, 'shot')
    for fact in facts:
        require(nonempty(fact.get('claim')), f"Fact {fact.get('id')} has no claim.")
        require(fact.get('status') in ('verified', 'pending', 'outdated'), f"Fact {fact.get('id')} status invalid.")
        if fact.get('status') == 'verified':
            require(nonempty(fact.get('source')), f"Verified fact {fact.get('id')} has no source.")
            require(nonempty(fact.get('verified_by')), f"Verified fact {fact.get('id')} has no verifier.")
            try:
                checked = date.fromisoformat(fact.get('checked_at', ''))
                require(checked <= date.today(), f"Fact {fact.get('id')} check date is in the future.")
            except (ValueError, TypeError):
                errors.append(f"Verified fact {fact.get('id')} checked_at must be YYYY-MM-DD.")
    for asset in assets:
        for key in ('role', 'source', 'version'):
            require(nonempty(asset.get(key)), f"Asset {asset.get('id')} {key} is missing.")
        # URLs are recorded but never fetched. Local files must exist when declared local.
        value = asset.get('source')
        if nonempty(value) and not value.startswith(('https://', 'http://')):
            require(local_file(value), f"Asset {asset.get('id')} local source does not exist.")
    if packet.get('mode') in ('cinematic', 'vfx', 'brand', 'faceless', 'auto-affi'):
        require(bool(shots), 'Media production plans need at least one shot.')
    for shot in shots:
        sid = shot.get('id')
        for key in ('purpose', 'prompt', 'start_state', 'end_state', 'acceptance'):
            require(nonempty(shot.get(key)), f'Shot {sid} {key} is missing.')
        for key, lookup in [('reference_ids', asset_ids), ('claim_ids', fact_ids)]:
            ids = shot.get(key)
            if not isinstance(ids, list) or any(not nonempty(x) for x in ids):
                errors.append(f'Shot {sid} {key} must be a list of nonempty IDs.');continue
            for item_id in ids:
                require(item_id in lookup, f'Shot {sid} refers to unknown {key}: {item_id}')
                if key == 'claim_ids' and item_id in lookup:
                    require(lookup[item_id].get('status') == 'verified', f'Shot {sid} uses unverified claim {item_id}.')
        estimate = shot.get('estimated_cost')
        if estimate is not None:
            require(number(estimate), f'Shot {sid} estimated_cost must be nonnegative finite number.')
        attempts = shot.get('attempts', 0)
        require(isinstance(attempts, int) and not isinstance(attempts, bool) and attempts >= 0,
                f'Shot {sid} attempts must be a nonnegative integer.')
    budget = packet.get('budget')
    if not isinstance(budget, dict):
        errors.append('budget must be an object.');budget = {}
    maximum = budget.get('max_cost')
    spent = budget.get('spent_cost', 0)
    require(number(spent), 'budget.spent_cost must be nonnegative finite number.')
    if maximum is not None:
        require(number(maximum), 'budget.max_cost must be nonnegative finite number.')
        require(nonempty(budget.get('currency')), 'A cost budget needs a currency.')
        missing = [shot.get('id') for shot in shots if not number(shot.get('estimated_cost'))]
        if missing:
            errors.append('Cost budget has incomplete next-call estimates: ' + ', '.join(str(x) for x in missing))
        if number(maximum) and number(spent):
            estimates = sum(shot['estimated_cost'] for shot in shots if number(shot.get('estimated_cost')))
            require(spent + estimates <= maximum, 'Recorded spend plus estimated next calls exceeds budget.')
    else:
        warnings.append('No cost ceiling recorded; cannot infer any spend permission.')
    cap = budget.get('max_attempts_per_shot')
    if cap is not None:
        require(isinstance(cap, int) and not isinstance(cap, bool) and cap > 0, 'Attempt cap must be a positive integer.')
        if isinstance(cap, int) and not isinstance(cap, bool) and cap > 0:
            for shot in shots:
                attempts = shot.get('attempts', 0)
                if isinstance(attempts, int):
                    require(attempts < cap, f"Shot {shot.get('id')} has reached its recorded attempt cap.")
    if stage == 'delivery':
        review = packet.get('review')
        if not isinstance(review, dict):
            errors.append('review must be an object.');review = {}
        media = review.get('media_files')
        require(isinstance(media, list) and bool(media), 'No delivery files recorded.')
        if isinstance(media, list):
            for path in media:
                require(local_file(path), f'Delivery file missing: {path}')
        require(local_file(review.get('report_file')), 'QC report file missing.')
        blockers = review.get('blockers')
        require(isinstance(blockers, list) and not blockers, 'Review has blockers or blockers field is invalid.')
        checks = review.get('checks')
        if not isinstance(checks, list) or any(not isinstance(x, dict) for x in checks):
            errors.append('review.checks must be a list of objects.');checks = []
        seen = set()
        for check in checks:
            dimension = check.get('dimension')
            require(nonempty(dimension) and dimension not in seen, 'Review dimension missing or duplicate.')
            if isinstance(dimension, str):seen.add(dimension)
            require(check.get('status') in ('pass', 'na'), f'Unresolved/uninspected review dimension: {dimension}')
            require(nonempty(check.get('evidence')), f'Review {dimension} needs evidence or NA rationale.')
        required = {'story', 'visual', 'audio', 'delivery'} if packet.get('mode') != 'game' else {'gameplay', 'input', 'performance', 'delivery'}
        if packet.get('mode') == 'agency':required = {'facts', 'scope', 'economics', 'delivery'}
        require(required <= seen, 'Missing review dimensions: ' + ', '.join(sorted(required - seen)))
    return {
        'stage': stage, 'structural_status': 'fail' if errors else 'pass', 'issues': errors, 'warnings': warnings,
        'counts': {'facts': len(facts), 'assets': len(assets), 'shots': len(shots)},
        'limits': ['Recorded source/reviewer fields are declarations, not independent truth verification.',
                   'Local file existence does not verify playback, pixels, audio, rights or clinical/product claims.',
                   'No provider calls, authorization decision, publishing or existing Auto-Affi gate execution.'],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    create = sub.add_parser('init');create.add_argument('--run-dir', type=Path, required=True)
    create.add_argument('--mode', choices=MODES, required=True)
    check = sub.add_parser('check');check.add_argument('--run-dir', type=Path, required=True)
    check.add_argument('--stage', choices=('plan', 'delivery'), default='plan')
    check.add_argument('--write-report', action='store_true')
    args = parser.parse_args(argv)
    try:
        run_dir = args.run_dir.expanduser().resolve()
        report = init_packet(run_dir, args.mode) if args.command == 'init' else check_packet(run_dir, args.stage)
        if args.command == 'check' and args.write_report:
            (run_dir / f'structural-check-{args.stage}.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1 if report.get('structural_status') == 'fail' else 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({'error': str(error), 'structural_status': 'fail'}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
