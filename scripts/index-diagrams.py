"""Enrich the rendered manifest and regenerate the diagram/review index."""
from pathlib import Path
import json, os, re
ROOT = Path(__file__).resolve().parents[1]
base = ROOT / 'design/diagrams'
manifest = json.loads((base/'manifest.json').read_text(encoding='utf-8'))
flows = {
 'google-login': ('UC-04',['FR-C02','NFR-05','NFR-08'],['GoogleLogin','LinkGoogle']),
 'customer-booking': ('UC-01',['FR-C04','FR-C05','NFR-10','NFR-11'],['EstimateFee','CreateParcel']),
 'merchant-order': ('UC-02',['FR-M03','FR-M04','FR-M06','FR-M07','NFR-10'],['SubmitMerchantOrder','GetMerchantOrder','MerchantDashboard']),
 'courier-status-notification': ('UC-03',['FR-R02','FR-R03','FR-R04','FR-C06','FR-M05','NFR-11'],['UpdateDeliveryStatus','CompleteDeliveryWithProof','DispatchWebhook','ParcelEvents']),
 'assignment-proof': ('UC-03',['FR-D02','FR-D03','FR-D04','FR-R03'],['AssignCourier','CompleteDeliveryWithProof']),
 'webhook-delivery': ('UC-03',['FR-M05','NFR-07','NFR-12','NFR-13'],['DispatchWebhook','ListWebhookAttempts']),
 'refresh-session': ('UC-04',['FR-C01','NFR-05'],['Refresh','Logout']),
 'merchant-onboarding': ('Supporting',['FR-M01','FR-M02','FR-A03'],['RegisterMerchant','SetMerchantStatus']),
 'assignment-workload': ('Supporting',['FR-D01','FR-D02','FR-D03','FR-D04','FR-D05'],['ListParcels','AssignCourier','CourierWorkload','ZoneSummary'])
}
def link(p):
    return os.path.relpath(ROOT/p,base).replace('\\','/')
rows=[]
for n,record in enumerate(manifest,1):
    source=record['source']; path=source.split('#')[0]; stem=Path(path).stem
    prefix='SEQ' if '/sequence/' in path else 'ACT' if '/activity/' in path else 'DIA'
    scenario,ids,ops=flows.get(stem,('Cross-cutting',[],[]))
    if '/er/' in path:
        ids=['NFR-14','FR-C01','FR-C04','FR-M05','NFR-11']
    elif '/use-cases/' in path or path.startswith('requirements/srs'):
        ids=['FR-C04','FR-M04','FR-R02','FR-C02']
    elif not ids:
        ids=['NFR-14','NFR-15','NFR-16']
    diagram_id=f'{prefix}-{stem}' if prefix != 'DIA' else f'DIA-{n:02}'
    record.update({'diagramId':diagram_id,'version':'2.0','useCase':scenario,'requirementIds':ids,'operationIds':ops,'owner':'Unassigned','reviewDate':None,'approval':'Pending','relatedDecisions':'DEC-01–DEC-12 as applicable'})
    rows.append(f'| {diagram_id} | {scenario}; {", ".join(ids)} | [{source}]({link(path)}) | [SVG]({link(record["artifact"])}) | 2.0 | Unassigned | Pending |')
(base/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
text='''# Diagram Index and Sign-Off Register

> Proposed baseline 2.0 · 16 October 2026 · All named owners/review dates pending

Editable sources and rendered SVGs below follow the same [use-case narratives](../../requirements/use-case-specifications.md), [REST operations](../../api/rest-api.md), [gRPC](../../api/grpc-services.md), [state matrix](../../architecture/parcel-state-machine.md), [events](../../integration/event-catalog.md) and [ADR register](../../architecture/decisions/README.md). Machine-readable IDs, requirement/operation mapping, version and review fields live in [manifest.json](manifest.json). All exports are generated, **not approved**. IDs for embedded diagrams identify the source Markdown and mermaid-block number.

## Required assignment coverage

| Workflow | Narrative | Sequence | Formal activity |
|---|---|---|---|
| Customer booking / fee confirmation | UC-01 | [SEQ-customer-booking](sequence/customer-booking.mmd) | [ACT-customer-booking](activity/customer-booking.puml) |
| Merchant secured API order | UC-02 | [SEQ-merchant-order](sequence/merchant-order.mmd) | [ACT-merchant-order](activity/merchant-order.puml) |
| Courier status triggers notifications | UC-03 | [SEQ-courier-status-notification](sequence/courier-status-notification.mmd) | [ACT-courier-status-notification](activity/courier-status-notification.puml) |
| Google OAuth/OIDC login | UC-04 | [SEQ-google-login](sequence/google-login.mmd) | [ACT-google-login](activity/google-login.puml) |

## Source/export inventory

| Diagram ID | Scenario / SRS IDs | Editable source | Rendered artifact | Version | Owner | Review date / approval |
|---|---|---|---|---|---|---|
'''+ '\n'.join(rows)+'''

## PDF and review evidence

[Architecture PDF](architecture/swiftdrop-architecture.pdf) is regenerated from architecture.mmd. [Design diagram packet](swiftdrop-design-baseline.pdf) includes the proposed overview and all rendered diagrams; it is a review export, not a final report with implementation/test evidence. Render checks and visual-review limitations are in [documentation validation](../../testing/documentation-validation.md). Source history preserves the prior baseline at 63d0de2.

For each review record the named reviewer/date/PR and check actor/client, exact endpoint/RPC/event, role/resource guard, version/state/persistence owner, success/invalid/unauthorized/failure branches, outbox timing, retries/dedup and public/private data segregation. API plus owning domain approve; SEC/MSG/UI participate when affected. No sign-off is inferred from a renderer passing. Rebuild using [validation scripts](../../scripts/README.md) after contract/source changes.
'''
(base/'README.md').write_text(text,encoding='utf-8')
print(f'Indexed {len(manifest)} diagrams; approvals remain pending.')
