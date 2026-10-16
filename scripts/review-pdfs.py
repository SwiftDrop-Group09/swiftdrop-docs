"""Check PDF export dimensions/page counts and make local visual-review previews."""
from pathlib import Path
import json, sys, re
ROOT = Path(__file__).resolve().parents[1]
if (ROOT/'.validation-tools/python').exists():
    sys.path.insert(0,str(ROOT/'.validation-tools/python'))
import pymupdf

out=ROOT/'.validation-tools/pdf-review'
out.mkdir(parents=True,exist_ok=True)
manifest=json.loads((ROOT/'design/diagrams/manifest.json').read_text(encoding='utf-8'))
results=[]
for rel,expected in [('design/diagrams/architecture/swiftdrop-architecture.pdf',1),('design/diagrams/swiftdrop-design-baseline.pdf',len(manifest))]:
    document=pymupdf.open(ROOT/rel)
    assert len(document)==expected,(rel,len(document),expected)
    assert all(len(page.get_text().strip())>70 for page in document),f'Empty PDF page in {rel}'
    if expected > 1:
        for index,record in enumerate(manifest):
            text=document[index].get_text()
            assert record['diagramId'] in text,f'Mismatched diagram page {index+1}'
            if record['source'].endswith('.puml'):
                source=(ROOT/record['source']).read_text(encoding='utf-8')
                title=re.search(r'^title (.+)',source,re.M).group(1).split('—')[0].strip()
                assert title in text,f'Missing activity content on page {index+1}: {title}'
    preview_pages=[0] if expected==1 else [2,28,32]
    for n in preview_pages:
        document[n].get_pixmap(matrix=pymupdf.Matrix(0.9,0.9)).save(out/f'{Path(rel).stem}-page-{n+1}.png')
    results.append({'file':rel,'pages':len(document),'sizePoints':list(document[0].rect),'result':'PASS'})
print(json.dumps(results,indent=2))
