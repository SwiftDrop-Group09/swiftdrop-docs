"""Validate local documentation integrity and design fixtures, not application behavior."""
from pathlib import Path
import re, json, sys, subprocess, tempfile, hashlib
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
local_lib = ROOT / '.validation-tools/python'
if local_lib.exists():
    sys.path.insert(0, str(local_lib))
import yaml
from jsonschema import Draft202012Validator, FormatChecker

errors = []
stats = {}
def check(condition, message):
    if not condition:
        errors.append(message)
def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))
def eligible(p):
    return not any(part in {'.git', '.validation-tools', 'node_modules', '.venv', '__pycache__'} for part in p.relative_to(ROOT).parts)
def no_fences(text):
    return re.sub(r'```[^\n]*\n[\s\S]*?```', '', text)
def anchors(text):
    found = set()
    counts = {}
    for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', no_fences(text), flags=re.M):
        title = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', title)
        slug = re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-')
        count = counts.get(slug, 0)
        found.add(slug + (f'-{count}' if count else ''))
        counts[slug] = count + 1
    return found

markdown = sorted(p for p in ROOT.rglob('*.md') if eligible(p))
links = 0
for p in markdown:
    text = p.read_text(encoding='utf-8')
    check(text.count('```') % 2 == 0, f'{p.relative_to(ROOT)}: unbalanced code fences')
    for match in re.finditer(r'!?\[[^\]]*\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)', no_fences(text)):
        target = match.group(1).strip('<>')
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
            continue
        pathpart, _, anchor = unquote(target).partition('#')
        dest = (p.parent / pathpart.split('?')[0]).resolve() if pathpart else p
        links += 1
        check(dest.exists(), f'{p.relative_to(ROOT)}: missing link {target}')
        if anchor and dest.is_file() and dest.suffix == '.md':
            check(anchor in anchors(dest.read_text(encoding='utf-8')), f'{p.relative_to(ROOT)}: missing anchor {target}')
stats['markdown_files'] = len(markdown)
stats['local_links_and_images'] = links

for p in ROOT.rglob('*.json'):
    if eligible(p):
        try:
            json.loads(p.read_text(encoding='utf-8'))
        except Exception as exc:
            errors.append(f'{p.relative_to(ROOT)}: invalid JSON {exc}')

routes = load('api/contracts/routes.json')
opids = {r['operationId'] for r in routes}
routepairs = {(r['method'], r['path']) for r in routes}
check(len(opids) == len(routes) == len(routepairs), 'Duplicate operation ID or method/path')
for r in routes:
    check(r['path'].startswith(('/api/v1/', '/internal/v1/', '/.well-known/')), f'Unversioned route {r}')
    expected = '| ' + ' | '.join(r[k] for k in ('operationId','method','path','owner','authorization','request','response','success')) + ' |'
    check(expected in (ROOT/'api/rest-api.md').read_text(encoding='utf-8'), f'REST table drift: {r["operationId"]}')
for p in markdown:
    for method, route in re.findall(r'\b(GET|POST|PUT|PATCH|DELETE)\s+(/(?:api/v\d+|internal/v\d+)/[\w/{}/.-]+)', p.read_text(encoding='utf-8')):
        check((method, route.rstrip('.,')) in routepairs, f'{p.relative_to(ROOT)}: undeclared route {method} {route}')
stats['canonical_rest_operations'] = len(routes)

srs = (ROOT/'requirements/srs.md').read_text(encoding='utf-8')
srs_ids = re.findall(r'^\|\s*((?:FR-[CMRDA]|NFR-)\d{2})\s*\|', srs, flags=re.M)
check(len(srs_ids) == 52 and len(set(srs_ids)) == 52, 'SRS must have 52 unique requirement rows')
check(sum(x.startswith('FR-') for x in srs_ids) == 32, 'SRS FR count mismatch')
for rid in ('FR-C08','FR-M06','FR-A06'):
    check(bool(re.search(rf'^\|\s*{rid}\s*\|[^\n]*\bMust\b', srs, flags=re.M)), f'{rid} must be Must')
trace = load('requirements/traceability.json')
cases = load('testing/test-cases.json')
caseids = {c['id'] for c in cases}
check(len(cases) == len(caseids) == 68, 'Test catalog must have 68 unique drafted cases')
check({m['requirementId'] for m in trace} == set(srs_ids) and len(trace) == 52, 'Traceability does not exactly cover SRS')
for m in trace:
    check(set(m['operationIds']) <= opids, f'Unknown operation in trace {m["requirementId"]}')
    check(set(m['testIds']) <= caseids, f'Missing primary case for {m["requirementId"]}')
    check(m['implementationEvidence'] is None, 'Unverified implementation evidence added')
    check(m['requirementId'] in (ROOT/'requirements/requirements-traceability.md').read_text(encoding='utf-8'), 'Trace Markdown drift')
for c in cases:
    check(set(c['requirements']) <= set(srs_ids), f'Unknown requirement in case {c["id"]}')
    check(c['id'] in (ROOT/'testing/test-cases.md').read_text(encoding='utf-8'), f'Missing rendered case {c["id"]}')
    check(c['status'] == 'Drafted' and c['evidence'] is None, f'Unevidenced test claim {c["id"]}')
stats['functional_requirements'] = 32
stats['nonfunctional_requirements'] = 20
stats['drafted_test_cases'] = len(cases)

schema = load('api/contracts/status-changed-v1.schema.json')
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(schema, format_checker=FormatChecker())
event = load('api/contracts/status-changed-v1.example.json')
errors.extend('Event example: '+e.message for e in validator.iter_errors(event))
unsafe = dict(event, pickupAddress='private street')
check(not validator.is_valid(unsafe), 'Event schema accepts unnecessary private address')
canonical = ['Created','Assigned','PickedUp','InTransit','OutForDelivery','Delivered','Failed','Cancelled']
check(schema['properties']['status']['enum'] == canonical, 'Event enum drift')
state = (ROOT/'architecture/parcel-state-machine.md').read_text(encoding='utf-8')
gql = (ROOT/'api/contracts/schema.graphql').read_text(encoding='utf-8')
gql_map = ['CREATED','ASSIGNED','PICKED_UP','IN_TRANSIT','OUT_FOR_DELIVERY','DELIVERED','FAILED','CANCELLED']
for domain, enum in zip(canonical,gql_map):
    check(f'| {domain} | {enum} |' in state and enum in gql, f'State enum mapping drift {domain}')

compose = yaml.safe_load((ROOT/'deployment/compose.yaml').read_text(encoding='utf-8'))
services = compose['services']
check('postgres' in services and not any(s.startswith('postgres-') for s in services), 'Database runtime topology drift')
for service, db in [('identity-service','identity'),('delivery-service','delivery'),('merchant-service','merchant'),('notification-worker','notifications')]:
    env = services[service]['environment']
    check(f'Database=swiftdrop_{db};Username={db}_app;' in env['ConnectionStrings__Database'], f'Wrong DB owner {service}')
    check('healthcheck' in services[service], f'No readiness check {service}')
check('merchant' not in services['notification-worker']['environment']['ConnectionStrings__Database'], 'Worker foreign DB access')
check(not any('redis' in k for k in services), 'Unexpected Redis dependency')
sql = (ROOT/'deployment/postgres/init-databases.sh').read_text(encoding='utf-8')
check(sql.count('CREATE DATABASE swiftdrop_') == 4, 'Bootstrap must create four logical DBs')

with tempfile.TemporaryDirectory(prefix='swiftdrop-proto-') as temp:
    result = subprocess.run([sys.executable,'-m','grpc_tools.protoc','-I',str(ROOT/'api/contracts'),f'--descriptor_set_out={temp}/delivery.pb',str(ROOT/'api/contracts/delivery.proto')],text=True,capture_output=True,env={**__import__('os').environ,'PYTHONPATH':str(local_lib) if local_lib.exists() else __import__('os').environ.get('PYTHONPATH','')})
    check(result.returncode == 0, 'Protobuf compilation: '+result.stderr)
stats['protobuf_compile'] = 'PASS' if result.returncode == 0 else 'FAIL'

manifest_path = ROOT/'design/diagrams/manifest.json'
if manifest_path.exists():
    manifest = load('design/diagrams/manifest.json')
    for record in manifest:
        check((ROOT/record['artifact']).exists(), f'Missing diagram export {record["artifact"]}')
        source, _, fragment = record['source'].partition('#')
        content = (ROOT/source).read_text(encoding='utf-8')
        if fragment:
            blocks = re.findall(r'```mermaid\s*\n([\s\S]*?)```', content)
            content = blocks[int(fragment.removeprefix('mermaid-'))-1]
        check(hashlib.sha256(content.strip().encode()).hexdigest() == record.get('sourceSha256'), f'Stale diagram export: {record["source"]}')
        check(set(record.get('requirementIds',[])) <= set(srs_ids), f'Unknown diagram requirement {record["source"]}')
        check(set(record.get('operationIds',[])) <= opids, f'Unknown diagram operation {record["source"]}')
    stats['rendered_diagrams'] = len(manifest)
else:
    errors.append('Render manifest missing; run render-diagrams.mjs')

result = {'status':'FAIL' if errors else 'PASS','checks':stats,'errors':errors,'scope':'Documentation/design fixtures only; no runtime application tests or team approval'}
print(json.dumps(result, indent=2))
sys.exit(bool(errors))
