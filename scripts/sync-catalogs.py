"""Regenerate Markdown catalog tables from the versioned JSON design fixtures."""
from pathlib import Path
import json, re
ROOT = Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))
def replace_table(path, header, rows):
    p = ROOT/path
    text = p.read_text(encoding='utf-8')
    pattern = re.escape(header)+r'\n(?:\|[^\n]*\n)+'
    match = re.search(pattern, text)
    if not match:
        raise ValueError(f'Cannot locate catalog table in {path}')
    columns = header.count('|')-1
    replacement = header+'\n|'+ '|'.join(['---']*columns)+'|\n'+'\n'.join(rows)+'\n'
    p.write_text(text[:match.start()]+replacement+text[match.end():],encoding='utf-8',newline='\n')
def row(cells):
    return '| '+' | '.join(cells)+' |'
routes=load('api/contracts/routes.json')
replace_table('api/rest-api.md', '| Operation ID | Method | Path | Owner | Authentication / resource guard | Input | Output | Success |',[
    row([r[k] for k in ('operationId','method','path','owner','authorization','request','response','success')]) for r in routes
])
trace=load('requirements/traceability.json')
replace_table('requirements/requirements-traceability.md','| Requirement | Capability | Operation IDs / verification | Event | Client/UI | Suggested role | Test | Evidence |',[
    row([m['requirementId'],m['title'],', '.join(m['operationIds']) or 'Cross-cutting acceptance scenario',m['event'],m['client'],m['suggestedOwnerRoles'],', '.join(m['testIds']),'Pending' if m['implementationEvidence'] is None else m['implementationEvidence']]) for m in trace
])
groups=[('Customer','FR-C'),('Merchant','FR-M'),('Courier','FR-R'),('Dispatcher','FR-D'),('Admin','FR-A'),('NFR','NFR-')]
summary=[]
for label,prefix in groups:
    entries=[m for m in trace if m['requirementId'].startswith(prefix)]
    summary.append(row([label,str(len(entries)),str(sum(bool(m['testIds']) for m in entries)),str(sum(m['implementationEvidence'] is not None for m in entries))]))
summary.append(row(['Total',str(len(trace)),str(sum(bool(m['testIds']) for m in trace)),str(sum(m['implementationEvidence'] is not None for m in trace))]))
replace_table('requirements/requirements-traceability.md','| Category | Requirements | Primary test cases drafted | Runtime evidence |',summary)
cases=load('testing/test-cases.json')
replace_table('testing/test-cases.md','| ID | SRS requirement(s) | Preconditions | Steps | Expected result | Status |',[
    row([c['id'],', '.join(c['requirements']),c['preconditions'],c['steps'],c['expected'],c['status']]) for c in cases
])
print(f'Synchronized {len(routes)} routes, {len(trace)} requirement mappings and {len(cases)} test scenarios; no execution statuses changed.')
