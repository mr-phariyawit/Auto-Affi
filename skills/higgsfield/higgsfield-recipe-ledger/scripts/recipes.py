#!/usr/bin/env python3
"""Recipe ledger: learn from our own Higgsfield runs.

    recipes.py report  [RUN ...]            # default: every runs/*/ledger.jsonl
    recipes.py promote --name N --run RUN --label "shot01 take2" --prompt p.txt [--job j.json] [--manifest m.json] [--tags a,b]
    recipes.py promote --name N --prompt p.txt --evidence "human:<who> <what> <date>" --credits 112 --model genjutsu-mt   # import
    recipes.py fail    --name N --model M --symptom "..." --cause "..." [--tried ...] [--next-lever ...] [--evidence ...]
    recipes.py list    [--model M]
    recipes.py index                         # rewrite recipes/higgsfield/INDEX.md

Ledger lines come from gate_cli (spend/refund; legacy lines without "type" are classified by the sign of
credits) and record_review.py (type=review). A take is joined to its review by an identical --label.
A recipe is promoted only from a KEEP review in a ledger, or imported with explicit human evidence.
A failure is recorded only with its cause — "X failed" alone teaches nothing.
"""
import argparse
import hashlib
import json
import shutil
import sys
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
DEFAULT_STORE = REPO / 'recipes/higgsfield'
DEFAULT_RUNS = REPO / 'runs'


def _entries(run):
    path = Path(run) / 'ledger.jsonl'
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def _kind(entry):
    if entry.get('type'):
        return entry['type']
    credits = entry.get('credits')
    if isinstance(credits, (int, float)):
        return 'refund' if credits < 0 else 'spend'
    return 'other'


def report(runs):
    out = {'runs': {}, 'models': {}, 'failures': []}
    models = defaultdict(lambda: {'spent': 0.0, 'refunded': 0.0, 'takes': 0, 'keeps': 0})
    for run in runs:
        entries = _entries(run)
        label_model = {e.get('label'): e.get('model') for e in entries if _kind(e) == 'spend'}
        r = {'spent': 0.0, 'refunded': 0.0, 'takes': 0, 'keeps': 0, 'verdicts': defaultdict(int)}
        for e in entries:
            kind, model = _kind(e), e.get('model') or label_model.get(e.get('label')) or 'unknown'
            if kind == 'spend':
                r['spent'] += e['credits']
                r['takes'] += 1
                models[model]['spent'] += e['credits']
                models[model]['takes'] += 1
            elif kind == 'refund':
                r['refunded'] += abs(e['credits'])
                models[model]['refunded'] += abs(e['credits'])
                out['failures'].append({'run': str(run), 'label': e.get('label', ''), 'kind': 'refund',
                                        'model': model, 'issues': e.get('label', '')})
            elif kind == 'review':
                r['verdicts'][e['verdict']] += 1
                if e['verdict'] == 'KEEP':
                    r['keeps'] += 1
                    models[model]['keeps'] += 1
                else:
                    out['failures'].append({'run': str(run), 'label': e.get('label', ''), 'kind': e['verdict'],
                                            'model': model, 'issues': e.get('issues', '')})
        r['net'] = r['spent'] - r['refunded']
        r['cost_per_keep'] = round(r['net'] / r['keeps'], 2) if r['keeps'] else None
        r['verdicts'] = dict(r['verdicts'])
        out['runs'][str(run)] = r
    for model, m in models.items():
        m['net'] = m['spent'] - m['refunded']
        m['cost_per_keep'] = round(m['net'] / m['keeps'], 2) if m['keeps'] else None
        out['models'][model] = m
    return out


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def promote(store, name, *, prompt, run=None, label=None, job=None, manifest=None, evidence=None,
            credits=None, model=None, route=None, tags=(), notes=''):
    store, dest = Path(store), Path(store) / name
    if dest.exists():
        raise FileExistsError(f'recipe {name!r} already exists — choose a new name or version it')
    review_entries, spend_entries = [], []
    if run is not None:
        entries = _entries(run)
        review_entries = [e for e in entries if _kind(e) == 'review' and e.get('label') == label]
        if not any(e['verdict'] == 'KEEP' for e in review_entries):
            raise ValueError(f'no KEEP review for {label!r} in {run}/ledger.jsonl — review the take first')
        spend_entries = [e for e in entries if _kind(e) in ('spend', 'refund') and (e.get('label') == label or e.get('label', '').startswith(label + ' '))]
        status = 'KEPT'
    elif evidence and evidence.startswith('human:'):
        status = 'HUMAN-APPROVED'
    else:
        raise ValueError('import needs --evidence "human:<who> <what> <date>" (or promote from a ledger KEEP)')
    first_spend = next((e for e in spend_entries if _kind(e) == 'spend'), {})
    dest.mkdir(parents=True)
    files = {}
    for key, src in (('prompt', prompt), ('job', job), ('manifest', manifest)):
        if src:
            target = dest / Path(src).name
            shutil.copyfile(src, target)
            files[key] = target.name
    recipe = {
        'name': name, 'status': status, 'created_at': datetime.now(UTC).isoformat(),
        'model': model or first_spend.get('model'), 'route': route or first_spend.get('route'),
        'credits_for_label': credits if credits is not None else sum(e['credits'] for e in spend_entries),
        'files': files, 'prompt_sha256': _sha(prompt), 'tags': list(tags), 'notes': notes,
        'source': {'run': str(run) if run else None, 'label': label, 'evidence': evidence,
                   'reviews': review_entries, 'spends': spend_entries},
    }
    (dest / 'recipe.json').write_text(json.dumps(recipe, ensure_ascii=False, indent=2), encoding='utf-8')
    return recipe


def add_failure(store, name, *, model, symptom, cause, tried='', next_lever='', evidence=''):
    if not cause.strip():
        raise ValueError('a failure needs its cause — "X failed" alone teaches nothing')
    Path(store).mkdir(parents=True, exist_ok=True)
    entry = {'name': name, 'model': model, 'symptom': symptom, 'cause': cause, 'tried': tried,
             'next_lever': next_lever, 'evidence': evidence, 'at': datetime.now(UTC).isoformat()}
    with (Path(store) / 'failures.jsonl').open('a', encoding='utf-8') as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + '\n')
    return entry


def list_recipes(store, model=None):
    rows = [json.loads(p.read_text(encoding='utf-8')) for p in sorted(Path(store).glob('*/recipe.json'))]
    return [r for r in rows if model is None or r.get('model') == model]


def failures(store):
    path = Path(store) / 'failures.jsonl'
    return [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()] if path.exists() else []


def write_index(store):
    store = Path(store)
    store.mkdir(parents=True, exist_ok=True)
    lines = ['# Higgsfield recipes and failures', '',
             'Generated by `skills/higgsfield/higgsfield-recipe-ledger/scripts/recipes.py index`. Do not edit by hand.', '',
             '## Recipes (reuse these first)', '', '| name | status | model | credits | tags | evidence |', '|---|---|---|---|---|---|']
    for r in list_recipes(store):
        ev = r['source'].get('evidence') or f"{r['source'].get('run')} · {r['source'].get('label')}"
        lines.append(f"| [{r['name']}]({r['name']}/recipe.json) | {r['status']} | {r.get('model')} | "
                     f"{r.get('credits_for_label')} | {', '.join(r.get('tags', []))} | {ev} |")
    lines += ['', '## Failures (do not repeat; try the next lever)', '',
              '| name | model | symptom | cause | tried | next lever |', '|---|---|---|---|---|---|']
    for f in failures(store):
        lines.append(f"| {f['name']} | {f['model']} | {f['symptom']} | {f['cause']} | {f['tried']} | {f['next_lever']} |")
    path = store / 'INDEX.md'
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return path


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--store', type=Path, default=DEFAULT_STORE)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('report')
    p.add_argument('runs', nargs='*', type=Path)
    p = sub.add_parser('promote')
    for opt in ('--name', '--prompt'):
        p.add_argument(opt, required=True)
    for opt in ('--run', '--label', '--job', '--manifest', '--evidence', '--model', '--route', '--notes', '--tags'):
        p.add_argument(opt, default=None)
    p.add_argument('--credits', type=float)
    p = sub.add_parser('fail')
    for opt in ('--name', '--model', '--symptom', '--cause'):
        p.add_argument(opt, required=True)
    for opt in ('--tried', '--next-lever', '--evidence'):
        p.add_argument(opt, default='')
    p = sub.add_parser('list')
    p.add_argument('--model')
    sub.add_parser('index')
    a = ap.parse_args(argv)
    try:
        if a.cmd == 'report':
            runs = a.runs or sorted(p.parent for p in DEFAULT_RUNS.glob('*/ledger.jsonl'))
            print(json.dumps(report(runs), ensure_ascii=False, indent=2))
        elif a.cmd == 'promote':
            rec = promote(a.store, a.name, prompt=a.prompt, run=a.run, label=a.label, job=a.job, manifest=a.manifest,
                          evidence=a.evidence, credits=a.credits, model=a.model, route=a.route,
                          tags=[t.strip() for t in (a.tags or '').split(',') if t.strip()], notes=a.notes or '')
            write_index(a.store)
            print(json.dumps({k: rec[k] for k in ('name', 'status', 'model', 'credits_for_label')}, ensure_ascii=False))
        elif a.cmd == 'fail':
            print(json.dumps(add_failure(a.store, a.name, model=a.model, symptom=a.symptom, cause=a.cause, tried=a.tried,
                                         next_lever=a.next_lever, evidence=a.evidence), ensure_ascii=False))
            write_index(a.store)
        elif a.cmd == 'list':
            for r in list_recipes(a.store, a.model):
                print(f"{r['name']}\t{r['status']}\t{r.get('model')}\t{r.get('credits_for_label')}\t{','.join(r.get('tags', []))}")
        elif a.cmd == 'index':
            print(write_index(a.store))
    except (OSError, ValueError) as error:
        print(f'error: {error}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
