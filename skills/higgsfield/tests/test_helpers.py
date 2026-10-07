"""Behavioral tests for local helpers, using isolated synthetic fixtures only."""
import copy
from datetime import date
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'higgsfield-bible-director/scripts'


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lookup = load('bible_lookup')
packet = load('production_packet')


class HelperBehavior(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.run = Path(self.temp.name) / 'test-run'
        packet.init_packet(self.run, 'cinematic')
        (self.run / 'reference.txt').write_text('SYNTHETIC TEST FIXTURE; not a product fact or media.')
        self.base = {
            'schema_version': 1, 'run_id': 'test-run', 'mode': 'cinematic',
            'brief': {'objective': 'synthetic test', 'deliverable': 'test plan'},
            'facts': [{'id': 'F1', 'claim': 'synthetic fixture only', 'status': 'verified',
                       'source': 'reference.txt', 'verified_by': 'test fixture', 'checked_at': date.today().isoformat()}],
            'assets': [{'id': 'A1', 'role': 'test reference', 'source': 'reference.txt', 'version': '1'}],
            'shots': [{'id': 'S1', 'purpose': 'test behavior', 'prompt': 'synthetic test',
                       'start_state': 'closed', 'end_state': 'open', 'acceptance': 'recorded example',
                       'reference_ids': ['A1'], 'claim_ids': ['F1'], 'estimated_cost': 2, 'attempts': 0}],
            'budget': {'currency': 'test credits', 'max_cost': 3, 'spent_cost': 0, 'max_attempts_per_shot': 2},
            'review': {'media_files': [], 'report_file': '', 'checks': [], 'blockers': []},
        }

    def tearDown(self):
        self.temp.cleanup()

    def check(self, data=None, stage='plan'):
        (self.run / 'production-plan.json').write_text(json.dumps(data if data is not None else self.base))
        return packet.check_packet(self.run, stage)

    def test_lookup_covers_171_and_limits_excerpts(self):
        sections = lookup.load_sections()
        lessons = [x for x in sections if x.startswith('A') and '.' in x]
        courses = [x for x in sections if x.startswith('A') and '.' not in x]
        self.assertEqual(len(lessons), 171)
        self.assertEqual(len(courses), 16)
        self.assertIn('A16.04', sections)
        bullets = [l for l in sections['A16.04']['text'].splitlines() if not l.startswith('#')]
        self.assertTrue(bullets)
        self.assertTrue(all('[A16.L04' in l for l in bullets))
        self.assertLess(len(sections['A16.04']['text']), len(sections['A16']['text']))
        self.assertIn('[A16.L05', sections['A16']['text'])

    def test_lesson_index_ignores_other_course_citations(self):
        text = '### rules\n- a [A01.L02 t=00:01] [A03.L02 t=00:02]\n- b [A03.L05 article]\n'
        lessons = lookup._lesson_sections('A01', text)
        self.assertEqual(list(lessons), ['A01.02'])
        self.assertIn('### rules', lessons['A01.02'])

    def test_init_refuses_overwrite(self):
        p = self.run / 'production-plan.json'
        before = p.read_bytes()
        with self.assertRaises(FileExistsError):
            packet.init_packet(self.run, 'vfx')
        self.assertEqual(p.read_bytes(), before)

    def test_valid_plan_is_only_structural(self):
        report = self.check()
        self.assertEqual(report['structural_status'], 'pass')
        self.assertNotIn('generation_allowed', report)
        self.assertTrue(report['limits'])

    def test_unknown_reference_and_missing_local_file_fail(self):
        data = copy.deepcopy(self.base)
        data['shots'][0]['reference_ids'] = ['MISSING']
        self.assertEqual(self.check(data)['structural_status'], 'fail')
        data = copy.deepcopy(self.base)
        data['assets'][0]['source'] = 'does-not-exist.png'
        self.assertEqual(self.check(data)['structural_status'], 'fail')

    def test_pending_claim_only_blocks_if_used(self):
        data = copy.deepcopy(self.base)
        data['facts'][0]['status'] = 'pending'
        self.assertEqual(self.check(data)['structural_status'], 'fail')
        data['shots'][0]['claim_ids'] = []
        self.assertEqual(self.check(data)['structural_status'], 'pass')

    def test_duplicate_ids_fail(self):
        data = copy.deepcopy(self.base)
        data['assets'].append(dict(data['assets'][0]))
        self.assertEqual(self.check(data)['structural_status'], 'fail')

    def test_spent_plus_next_call_budget_and_nan_fail(self):
        data = copy.deepcopy(self.base)
        data['budget']['spent_cost'] = 2
        self.assertEqual(self.check(data)['structural_status'], 'fail')
        data = copy.deepcopy(self.base)
        data['shots'][0]['estimated_cost'] = float('nan')
        self.assertEqual(self.check(data)['structural_status'], 'fail')
        data['shots'][0]['estimated_cost'] = True
        self.assertEqual(self.check(data)['structural_status'], 'fail')

    def test_attempt_limit_fails(self):
        data = copy.deepcopy(self.base)
        data['shots'][0]['attempts'] = 2
        self.assertEqual(self.check(data)['structural_status'], 'fail')

    def test_missing_or_uninspected_delivery_fails(self):
        self.assertEqual(self.check(stage='delivery')['structural_status'], 'fail')
        data = copy.deepcopy(self.base)
        (self.run / 'fake-media.txt').write_text('synthetic file; not playable media')
        (self.run / 'qc.txt').write_text('declared test review only')
        data['review'] = {
            'media_files': ['fake-media.txt'], 'report_file': 'qc.txt', 'blockers': [],
            'checks': [{'dimension': d, 'status': 'pass', 'evidence': 'synthetic declaration only'}
                       for d in ['story', 'visual', 'audio', 'delivery']]}
        declared = self.check(data, 'delivery')
        self.assertEqual(declared['structural_status'], 'pass')
        self.assertIn('Local file existence', declared['limits'][1])
        data['review']['checks'][1]['status'] = 'not_inspectable'
        self.assertEqual(self.check(data, 'delivery')['structural_status'], 'fail')
        data['review']['checks'][1]['status'] = 'pass'
        data['review']['blockers'] = ['wrong SKU']
        self.assertEqual(self.check(data, 'delivery')['structural_status'], 'fail')

    def test_game_delivery_requires_gameplay_and_input(self):
        data = copy.deepcopy(self.base)
        data['mode'] = 'game'
        data['shots'] = []
        self.assertEqual(self.check(data)['structural_status'], 'pass')
        (self.run / 'game.html').write_text('synthetic fixture')
        (self.run / 'qc.txt').write_text('synthetic fixture')
        data['review'] = {
            'media_files': ['game.html'], 'report_file': 'qc.txt', 'blockers': [],
            'checks': [{'dimension': d, 'status': 'pass', 'evidence': 'synthetic declaration only'}
                       for d in ['story', 'visual', 'audio', 'delivery']]}
        self.assertEqual(self.check(data, 'delivery')['structural_status'], 'fail')
        data['review']['checks'] = [{'dimension': d, 'status': 'pass', 'evidence': 'synthetic declaration only'}
                                   for d in ['gameplay', 'input', 'performance', 'delivery']]
        self.assertEqual(self.check(data, 'delivery')['structural_status'], 'pass')


if __name__ == '__main__':
    unittest.main()
