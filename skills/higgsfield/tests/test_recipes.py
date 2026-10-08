"""Behavioral tests for the recipe ledger (synthetic run ledgers only)."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('recipes', ROOT / 'higgsfield-recipe-ledger/scripts/recipes.py')
recipes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recipes)


def write_ledger(run, entries):
    run.mkdir(parents=True, exist_ok=True)
    (run / 'ledger.jsonl').write_text(''.join(json.dumps(e) + '\n' for e in entries))


class RecipeLedger(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = Path(self.tmp.name)
        self.runs, self.store = t / 'runs', t / 'recipes'
        self.run_a = self.runs / '2026-10-08-serum'
        write_ledger(self.run_a, [
            {'type': 'spend', 'credits': 36, 'label': 'shot01 take1', 'route': 'ui', 'model': 'seedance-2.0'},
            {'type': 'review', 'label': 'shot01 take1', 'verdict': 'REROLL', 'issues': 'thumb merges 3.2s'},
            {'credits': 36, 'label': 'shot01 take2', 'route': 'ui', 'model': 'seedance-2.0'},  # legacy entry, no type
            {'type': 'review', 'label': 'shot01 take2', 'verdict': 'KEEP', 'keep': '0.0-7.5s'},
            {'type': 'spend', 'credits': 36, 'label': 'shot02 take1', 'route': 'ui', 'model': 'seedance-2.0'},
            {'type': 'refund', 'credits': -36, 'label': 'shot02 take1 refunded: edit-style prompt', 'model': 'seedance-2.0'},
            {'type': 'spend', 'credits': 112, 'label': 'shot03 take1', 'route': 'ui', 'model': 'genjutsu-mt'},
            {'type': 'review', 'label': 'shot03 take1', 'verdict': 'FIX-BRIEF', 'issues': 'kept source face'},
        ])
        for name, text in (('prompt.txt', 'ACTIVE REFERENCES:\n@jiab — appearance only.\n'), ('job.json', '{"model": "seedance-2.0"}')):
            (self.run_a / name).write_text(text)

    def tearDown(self):
        self.tmp.cleanup()

    def test_report_costs_and_keeps(self):
        r = recipes.report([self.run_a])
        run = r['runs'][str(self.run_a)]
        self.assertEqual(run['spent'], 220)
        self.assertEqual(run['refunded'], 36)
        self.assertEqual(run['net'], 184)
        self.assertEqual(run['takes'], 4)
        self.assertEqual(run['keeps'], 1)
        self.assertEqual(run['cost_per_keep'], 184)
        seed = r['models']['seedance-2.0']
        self.assertEqual((seed['net'], seed['keeps'], seed['cost_per_keep']), (72, 1, 72))
        self.assertIsNone(r['models']['genjutsu-mt']['cost_per_keep'])

    def test_report_collects_failures(self):
        kinds = sorted(f['kind'] for f in recipes.report([self.run_a])['failures'])
        self.assertEqual(kinds, ['FIX-BRIEF', 'REROLL', 'refund'])

    def test_promote_requires_keep_review(self):
        with self.assertRaises(ValueError):
            recipes.promote(self.store, 'serum-hold', run=self.run_a, label='shot01 take1',
                            prompt=self.run_a / 'prompt.txt', job=self.run_a / 'job.json')
        rec = recipes.promote(self.store, 'serum-hold', run=self.run_a, label='shot01 take2',
                              prompt=self.run_a / 'prompt.txt', job=self.run_a / 'job.json', tags=['product', 'serum'])
        self.assertEqual(rec['status'], 'KEPT')
        self.assertEqual(rec['credits_for_label'], 36)
        self.assertEqual(rec['model'], 'seedance-2.0')
        self.assertEqual(len(rec['prompt_sha256']), 64)
        self.assertTrue((self.store / 'serum-hold/prompt.txt').exists())
        with self.assertRaises(FileExistsError):
            recipes.promote(self.store, 'serum-hold', run=self.run_a, label='shot01 take2', prompt=self.run_a / 'prompt.txt')

    def test_import_needs_human_evidence(self):
        with self.assertRaises(ValueError):
            recipes.promote(self.store, 'old', prompt=self.run_a / 'prompt.txt', evidence='agent thinks it is good')
        rec = recipes.promote(self.store, 'genjutsu-dance', prompt=self.run_a / 'prompt.txt',
                              evidence="human:operator 'ดีมาก' 2026-10-07", credits=112, model='genjutsu-mt')
        self.assertEqual(rec['status'], 'HUMAN-APPROVED')
        self.assertEqual(rec['credits_for_label'], 112)

    def test_failure_needs_cause_and_index_lists_all(self):
        with self.assertRaises(ValueError):
            recipes.add_failure(self.store, 'x', model='genjutsu-mt', symptom='kept face', cause='')
        recipes.add_failure(self.store, 'genjutsu-closeup-face', model='genjutsu-mt', symptom='kept source face',
                            cause='close-up mic singer: source face dominates', tried='3 prompts, 2 ref sets',
                            next_lever='Seedance Edit + face refs', evidence='memory 2026-10-08')
        recipes.promote(self.store, 'genjutsu-dance', prompt=self.run_a / 'prompt.txt',
                        evidence="human:operator 2026-10-07", credits=112, model='genjutsu-mt')
        index = recipes.write_index(self.store).read_text()
        self.assertIn('genjutsu-dance', index)
        self.assertIn('genjutsu-closeup-face', index)
        self.assertEqual([r['name'] for r in recipes.list_recipes(self.store, model='genjutsu-mt')], ['genjutsu-dance'])
        self.assertEqual(recipes.list_recipes(self.store, model='seedance-2.0'), [])


if __name__ == '__main__':
    unittest.main()
