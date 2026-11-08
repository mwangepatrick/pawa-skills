"""Local Pawa architecture snapshot and bounded queries; Python stdlib only."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import xml.etree.ElementTree as ET

DEFAULT_ROOTS = [r'D:\cp\pp', r'D:\cp\wpf']
EXCLUDED = {
    '.git', '.vs', '.idea', '.vscode', '.codex', '.claude', '.agents',
    '.worktrees', 'node_modules', 'packages', 'bin', 'obj', 'dist', 'build',
    'release', 'staging', 'latest', 'dlls', 'images', '_repo-archives',
    'migrationbackup', '__pycache__', '.venv', 'venv', '.next', 'coverage',
    '.silent-lan', '.pawa-repo-manager', '.superpowers',
}
TYPE = re.compile(r'\b(?:(class|interface|struct|enum)\s+|record\s+(?:(?:class|struct)\s+)?)(?!(?:in|with)\b)(@?[A-Za-z_]\w*)(?=\s*[<(:{;])')
NAMESPACE = re.compile(r'\bnamespace\s+([\w.]+)\s*[;{]')
# A lexical aid, not a C# compiler: masking preserves offsets and line numbers.
MASK = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"{3,}[\s\S]*?"{3,}|@"(?:""|[^"])*"|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')


def normalized(path):
    return os.path.normcase(str(Path(path).resolve()))


def inside(path, parent):
    try:
        Path(path).resolve().relative_to(Path(parent).resolve())
        return True
    except ValueError:
        return False


def stamp(path):
    stat = Path(path).stat()
    return [stat.st_size, stat.st_mtime_ns]


def read_text(path):
    raw = Path(path).read_bytes()
    if raw.startswith((b'\xff\xfe', b'\xfe\xff')):
        return raw.decode('utf-16')
    return raw.decode('utf-8-sig', errors='replace')


def strip_literals(text):
    return MASK.sub(lambda m: ''.join('\n' if c == '\n' else ' ' for c in m[0]), text)


def walk(root, errors):
    def on_error(error):
        errors.append({'path': error.filename, 'error': str(error)})
    for folder, dirs, files in os.walk(root, onerror=on_error, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d.lower() not in EXCLUDED and not Path(folder, d).is_symlink())
        yield Path(folder), sorted(files)


def resolve_reference(project, value):
    if '$(' in value or '*' in value:
        return value, 'unresolved-expression'
    path = (project.parent / value.replace('\\', '/')).resolve()
    return str(path), 'exists' if path.exists() else 'missing'


def build(roots, output):
    roots = list(dict.fromkeys(str(Path(r).resolve()) for r in roots))
    if not roots or any(not Path(r).is_dir() for r in roots):
        raise ValueError('Every requested root must exist; previous snapshot is retained.')
    data = {'version': 1, 'created_utc': datetime.now(timezone.utc).isoformat(),
            'roots': roots, 'repositories': [], 'projects': [], 'edges': [],
            'symbols': [], 'errors': [], 'excluded_directories': sorted(EXCLUDED)}
    candidates = []
    seen = set()
    for root in roots:
        for folder, files in walk(root, data['errors']):
            if normalized(folder) in seen:
                continue
            seen.add(normalized(folder))
            if (folder / '.git').exists():
                data['repositories'].append({'name': folder.name, 'path': str(folder)})
            for name in files:
                path = folder / name
                if path.suffix.lower() in {'.csproj', '.vbproj', '.fsproj'} or name == 'package.json':
                    data['projects'].append({'name': path.stem if name != 'package.json' else folder.name,
                                             'path': str(path), 'directory': str(folder)})
                elif path.suffix.lower() == '.cs' and not name.lower().endswith(('.designer.cs', '.g.cs', '.g.i.cs')):
                    candidates.append(path)
    repo_paths = sorted((Path(r['path']) for r in data['repositories']), key=lambda p: len(p.parts), reverse=True)
    owners = {}
    for project in data['projects']:
        path = Path(project['path'])
        project['repository'] = next((str(r) for r in repo_paths if inside(path, r)), None)
        owners.setdefault(project['directory'], []).append(project['path'])
        try:
            project['stamp'] = stamp(path)
            if path.name == 'package.json':
                package = json.loads(read_text(path))
                project['name'] = package.get('name', project['name'])
                project['kind'] = 'node'
                for kind in ('dependencies', 'devDependencies'):
                    for name, version in package.get(kind, {}).items():
                        data['edges'].append({'source': str(path), 'target': name, 'kind': 'package', 'declared_version': version})
                continue
            project['kind'] = 'dotnet'
            tree = ET.fromstring(read_text(path))
            for elem in tree.iter():
                tag = elem.tag.rsplit('}', 1)[-1]
                if tag in ('AssemblyName', 'RootNamespace', 'TargetFramework', 'TargetFrameworks', 'TargetFrameworkVersion') and elem.text:
                    project[tag] = elem.text.strip()
                if tag not in ('ProjectReference', 'PackageReference', 'Reference'):
                    continue
                value = elem.get('Include') or elem.get('Update')
                if not value:
                    continue
                edge = {'source': str(path), 'target': value, 'kind': 'package' if tag == 'PackageReference' else 'assembly'}
                if tag == 'ProjectReference':
                    edge['kind'] = 'project'
                    edge['target'], edge['target_state'] = resolve_reference(path, value)
                elif tag == 'Reference':
                    hint = next((c.text for c in elem if c.tag.rsplit('}', 1)[-1] == 'HintPath'), None)
                    if hint:
                        edge['kind'] = 'dll'
                        edge['hint_path'], edge['target_state'] = resolve_reference(path, hint)
                edge['item_condition'] = elem.get('Condition')
                data['edges'].append(edge)
        except (OSError, ValueError, ET.ParseError) as error:
            data['errors'].append({'path': str(path), 'error': str(error)})
    for path in candidates:
        try:
            text = strip_literals(read_text(path))
            namespaces = list(NAMESPACE.finditer(text))
            directory = next((str(d) for d in path.parents if str(d) in owners), None)
            for match in TYPE.finditer(text):
                ns = next((n[1] for n in reversed(namespaces) if n.start() < match.start()), '')
                data['symbols'].append({'name': match[2].lstrip('@'), 'namespace_hint': ns,
                                        'kind': match[1] or 'record', 'path': str(path),
                                        'line': text.count('\n', 0, match.start()) + 1,
                                        'projects': owners.get(directory, []), 'stamp': stamp(path)})
        except OSError as error:
            data['errors'].append({'path': str(path), 'error': str(error)})
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    # Build in memory first, then replace atomically. Errors remain visible in metadata.
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=output.parent, delete=False) as handle:
        temporary = Path(handle.name)
        json.dump(data, handle, ensure_ascii=False, separators=(',', ':'))
    try:
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)
    return data


def state(row):
    try:
        return 'unchanged' if stamp(row['path']) == row['stamp'] else 'changed'
    except OSError:
        return 'missing'


def find(data, query, kind='symbol', scope=''):
    rows = data['symbols'] if kind == 'symbol' else data['projects'] if kind == 'project' else data['repositories']
    query = query.casefold()
    scope = scope.replace('\\', '/').casefold()
    result = []
    for row in rows:
        path = row['path'].replace('\\', '/').casefold()
        searchable = row.get('name', '') + ' ' + row.get('namespace_hint', '')
        if kind != 'symbol':
            searchable += ' ' + row['path']
        if query not in searchable.casefold():
            continue
        if scope and scope not in path:
            continue
        item = {k: v for k, v in row.items() if k != 'stamp'}
        if 'stamp' in row:
            item['source_state'] = state(row)
        result.append(item)
    return sorted(result, key=lambda r: (r['name'].casefold() != query, r['name'].casefold(), r['path']))


def dependencies(data, query, incoming=False):
    field = 'target' if incoming else 'source'
    query = query.replace('\\', '/').casefold()
    result = []
    by_path = {p['path']: p for p in data['projects']}
    for edge in data['edges']:
        if query in edge[field].replace('\\', '/').casefold():
            row = dict(edge)
            if row['source'] in by_path:
                row['source_state'] = state(by_path[row['source']])
            result.append(row)
    return result


def default_cache():
    base = Path(os.environ.get('LOCALAPPDATA', Path.home() / '.cache'))
    return base / 'pawalogic' / 'architecture.json'


def summary(data):
    return {k: data[k] for k in ('version', 'created_utc', 'roots')} | {
        'counts': {k: len(data[k]) for k in ('repositories', 'projects', 'symbols', 'edges', 'errors')},
        'limits': 'Snapshot; C# lexical types and nearest-directory project candidates. Verify compile inclusion, conditional references and live call sites. No runtime dependency inference.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', type=Path, default=default_cache())
    sub = parser.add_subparsers(dest='command', required=True)
    index = sub.add_parser('index', help='Explicitly refresh local snapshot (only command that writes).')
    index.add_argument('--roots', nargs='+', default=DEFAULT_ROOTS)
    sub.add_parser('status', help='Snapshot metadata; does not rescan.')
    lookup = sub.add_parser('find')
    lookup.add_argument('query')
    lookup.add_argument('--kind', choices=['symbol', 'project', 'repo'], default='symbol')
    lookup.add_argument('--scope', default='')
    lookup.add_argument('--limit', type=int, choices=range(1, 101), default=12, metavar='1..100')
    deps = sub.add_parser('deps')
    deps.add_argument('query', help='Project path or distinctive path fragment; broad names can match several projects.')
    deps.add_argument('--incoming', action='store_true')
    deps.add_argument('--limit', type=int, choices=range(1, 101), default=12, metavar='1..100')
    args = parser.parse_args()
    try:
        if args.command == 'index':
            data = build(args.roots, args.cache)
            print(json.dumps(summary(data) | {'cache': str(args.cache), 'errors': data['errors'][:12]}, indent=2))
            return 2 if data['errors'] else 0
        if not args.cache.exists():
            raise ValueError('No snapshot. Run index first; queries never rebuild implicitly.')
        data = json.loads(args.cache.read_text(encoding='utf-8'))
        if data.get('version') != 1:
            raise ValueError('Unsupported snapshot version. Refresh with index.')
        if args.command == 'status':
            result = summary(data) | {'errors': data['errors'][:12]}
        else:
            rows = find(data, args.query, args.kind, args.scope) if args.command == 'find' else dependencies(data, args.query, args.incoming)
            result = {'snapshot_utc': data['created_utc'], 'scan_errors': len(data['errors']),
                      'total_matches': len(rows), 'returned': min(len(rows), args.limit),
                      'results': rows[:args.limit], 'note': 'Unchanged checks size/mtime for matched files only. Refresh after additions, renames or branch changes.'}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError) as error:
        print(json.dumps({'error': str(error)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
