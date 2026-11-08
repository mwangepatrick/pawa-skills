import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / 'scripts' / 'lookup.py'


class LookupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        spec = importlib.util.spec_from_file_location('lookup', SCRIPT)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
        self.cache = self.root / 'snapshot.json'

    def put(self, name, text=''):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def fixture(self):
        self.put('repo/.git/HEAD', 'ref: refs/heads/main')
        self.put('repo/App/App.csproj', '<Project><ItemGroup><ProjectReference Include="../Data/Data.csproj" /><Reference Include="Legacy"><HintPath>../../dlls/Legacy.dll</HintPath></Reference><PackageReference Include="Npgsql" Version="8.0" /></ItemGroup></Project>')
        self.put('repo/Data/Data.csproj', '<Project/>')
        self.put('other/Data/Data.csproj', '<Project/>')
        self.put('repo/nested/.git', 'gitdir: /elsewhere')
        self.put('repo/nested/Nested.csproj', '<Project/>')
        self.put('repo/App/Rules.cs', 'namespace Pawa.App;\n// class Fake {}\npublic partial class RetryRules {}\npublic record RetryResult(int Count);\npublic interface IRetry {}\n')
        self.put('repo/App/bin/Generated.cs', 'class IgnoreMe {}')
        self.put('repo/App/node_modules/Ignore.cs', 'class IgnoreMe {}')
        return self.mod.build([self.root], self.cache)

    def test_duplicate_projects_and_nested_repositories_keep_full_paths(self):
        data = self.fixture()
        self.assertEqual(2, len([p for p in data['projects'] if p['name'] == 'Data']))
        nested = next(p for p in data['projects'] if p['name'] == 'Nested')
        self.assertEqual(str(self.root / 'repo/nested'), nested['repository'])

    def test_dependency_kinds_and_reverse_consumers(self):
        data = self.fixture()
        rows = self.mod.dependencies(data, 'Data.csproj', incoming=True)
        self.assertEqual(1, len(rows))
        self.assertEqual('project', rows[0]['kind'])
        self.assertEqual({'project', 'dll', 'package'}, {e['kind'] for e in data['edges']})

    def test_lexical_types_are_scoped_and_ignore_comments_and_outputs(self):
        data = self.fixture()
        rows = self.mod.find(data, 'Retry', 'symbol', scope='repo/App')
        self.assertEqual({'RetryRules', 'RetryResult', 'IRetry'}, {r['name'] for r in rows})
        self.assertEqual(2, next(r['line'] for r in rows if r['name'] == 'RetryRules') - 1)
        self.assertEqual([], self.mod.find(data, 'IgnoreMe', 'symbol'))
        self.assertEqual([], self.mod.find(data, 'Fake', 'symbol'))

    def test_snapshot_marks_changed_and_deleted_matches(self):
        data = self.fixture()
        path = self.root / 'repo/App/Rules.cs'
        path.write_text('namespace Changed; class RetryRules {}', encoding='utf-8')
        row = self.mod.find(data, 'RetryRules', 'symbol')[0]
        self.assertEqual('changed', row['source_state'])
        path.unlink()
        self.assertEqual('missing', self.mod.find(data, 'RetryRules', 'symbol')[0]['source_state'])

    def test_missing_root_is_reported_without_erasing_previous_snapshot(self):
        self.fixture()
        before = self.cache.read_bytes()
        with self.assertRaises(ValueError):
            self.mod.build([self.root / 'missing'], self.cache)
        self.assertEqual(before, self.cache.read_bytes())

    def test_strings_are_not_type_declarations(self):
        self.put('App.csproj', '<Project/>')
        self.put('Types.cs', 'namespace Real;\nclass Valid { string text = "class Bogus {}"; }\n')
        data = self.mod.build([self.root], self.cache)
        self.assertEqual(['Valid'], [r['name'] for r in data['symbols']])

    def test_agent_review_snapshots_do_not_compete_with_live_projects(self):
        self.fixture()
        for folder in ('.silent-lan', '.pawa-repo-manager', '.superpowers'):
            self.put(folder + '/snapshot/Shadow.csproj', '<Project/>')
            self.put(folder + '/snapshot/Shadow.cs', 'class Shadow {}')
        data = self.mod.build([self.root], self.cache)
        self.assertEqual([], self.mod.find(data, 'Shadow', 'project'))
        self.assertEqual([], self.mod.find(data, 'Shadow', 'symbol'))

    def test_invalid_manifest_is_reported_and_other_projects_remain_queryable(self):
        self.fixture()
        self.put('repo/Empty.csproj', '')
        data = self.mod.build([self.root], self.cache)
        self.assertEqual(1, len(data['errors']))
        self.assertTrue(self.mod.find(data, 'RetryRules', 'symbol'))

    def test_missing_reference_is_reported_as_declared_not_existing(self):
        self.put('App.csproj', '<Project><ItemGroup><ProjectReference Include="Missing/Missing.csproj" /></ItemGroup></Project>')
        data = self.mod.build([self.root], self.cache)
        self.assertEqual('missing', data['edges'][0]['target_state'])

    def test_cli_bounds_output_and_does_not_refresh_on_query(self):
        self.fixture()
        before = self.cache.read_bytes()
        result = subprocess.run([sys.executable, str(SCRIPT), '--cache', str(self.cache), 'find', 'Retry', '--limit', '1'], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(3, output['total_matches'])
        self.assertEqual(1, len(output['results']))
        self.assertEqual(before, self.cache.read_bytes())

    def test_cli_returns_partial_scan_status_for_invalid_manifest(self):
        self.put('Empty.csproj', '')
        result = subprocess.run([sys.executable, str(SCRIPT), '--cache', str(self.cache), 'index', '--roots', str(self.root)], capture_output=True, text=True)
        self.assertEqual(2, result.returncode, result.stderr)
        self.assertEqual(1, json.loads(result.stdout)['counts']['errors'])

    def test_record_loop_variables_are_not_types_and_type_search_uses_names(self):
        self.put('App.csproj', '<Project/>')
        self.put('DataSyncService.cs', 'namespace Sync;\nclass DataSyncService { void Run() { foreach (var record in records) { } } }\nrecord UploadRow(int Id);\nclass AnotherType {}')
        data = self.mod.build([self.root], self.cache)
        self.assertEqual({'DataSyncService', 'UploadRow', 'AnotherType'}, {r['name'] for r in data['symbols']})
        self.assertEqual(['DataSyncService'], [r['name'] for r in self.mod.find(data, 'DataSyncService')])


if __name__ == '__main__':
    unittest.main()
