import { createRequire } from 'node:module';
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
let require = createRequire(import.meta.url);
try { require.resolve('puppeteer'); } catch { require = createRequire(path.join(root, '.validation-tools', 'package.json')); }
const puppeteer = require('puppeteer');
const bundle = path.join(path.dirname(require.resolve('mermaid/package.json')), 'dist/mermaid.min.js');
const candidates = [process.env.CHROME_PATH, 'C:/Program Files/Google/Chrome/Application/chrome.exe', '/usr/bin/chromium', '/usr/bin/google-chrome'].filter(Boolean);
const executablePath = candidates.find(p => existsSync(p));
if (!executablePath) throw new Error('Set CHROME_PATH to an installed Chromium/Chrome executable');
const browser = await puppeteer.launch({executablePath, headless:true, args:['--no-sandbox','--disable-dev-shm-usage']});
const out = path.join(root, '.validation-tools/rendered');
mkdirSync(out, {recursive:true});
const committedExports = path.join(root, 'design/diagrams/generated');
mkdirSync(committedExports, {recursive:true});
const results = [];
const ignored = new Set(['.git','.validation-tools','node_modules','.venv']);
function files(dir) {
  return readdirSync(dir, {withFileTypes:true}).flatMap(e => ignored.has(e.name) ? [] : e.isDirectory() ? files(path.join(dir,e.name)) : [path.join(dir,e.name)]);
}
const all = files(root);
const page = await browser.newPage();
await page.setViewport({width:2000,height:1400,deviceScaleFactor:1});
await page.setContent('<!doctype html><html><body></body></html>');
await page.addScriptTag({path:bundle});
await page.evaluate(() => mermaid.initialize({startOnLoad:false, securityLevel:'strict', theme:'neutral', maxTextSize:100000, flowchart:{htmlLabels:false, useMaxWidth:false}, sequence:{useMaxWidth:false}, er:{useMaxWidth:false}}));
let n=0;
async function render(source, label, target) {
  let result;
  try { result = await page.evaluate(async ({source,id}) => {
    const {svg}=await mermaid.render(id,source);
    return svg;
  }, {source,id:`diagram${++n}`});
  } catch (error) { throw new Error(`Render failed for ${label}: ${error.message}`); }
  writeFileSync(target,result);
  results.push({source:label,sourceSha256:createHash('sha256').update(source.replaceAll('\r\n','\n').trim()).digest('hex'),artifact:path.relative(root,target).replaceAll('\\','/'),result:'PASS'});
}
try {
  for (const f of all.filter(f=>f.endsWith('.mmd'))) {
    await render(readFileSync(f,'utf8'),path.relative(root,f).replaceAll('\\','/'),f.replace(/\.mmd$/,'.svg'));
  }
  for (const f of all.filter(f=>f.endsWith('.md'))) {
    let i=0;
    for (const match of readFileSync(f,'utf8').matchAll(/```mermaid\s*\n([\s\S]*?)```/g)) {
      const rel=path.relative(root,f).replaceAll('\\','/');
      const target=path.join(committedExports,`${rel.replaceAll('/','-').replace(/\.md$/,'')}-${++i}.svg`);
      await render(match[1],`${rel}#mermaid-${i}`,target);
    }
  }
  const jar = process.env.PLANTUML_JAR || path.join(root,'.validation-tools/plantuml.jar');
  if (!existsSync(jar)) throw new Error('Set PLANTUML_JAR or download PlantUML into .validation-tools');
  const puml = all.filter(f=>f.endsWith('.puml'));
  for (const source of puml) {
    const processResult = spawnSync('java',['-Dfile.encoding=UTF-8','-jar',jar,'-tsvg','-charset','UTF-8','-failfast2',source],{encoding:'utf8'});
    if (processResult.status !== 0) throw new Error(`${source}: ${processResult.stderr || processResult.stdout}`);
    const svg=source.replace(/\.puml$/,'.svg');
    if (!existsSync(svg) || /Syntax Error/i.test(readFileSync(svg,'utf8'))) throw new Error(`Invalid PlantUML: ${source}`);
    results.push({source:path.relative(root,source).replaceAll('\\','/'),sourceSha256:createHash('sha256').update(readFileSync(source,'utf8').replaceAll('\r\n','\n').trim()).digest('hex'),artifact:path.relative(root,svg).replaceAll('\\','/'),result:'PASS'});
  }
  const svg=readFileSync(path.join(root,'design/diagrams/architecture/architecture.svg'),'utf8');
  const pdfPage=await browser.newPage();
  await pdfPage.setContent(`<!doctype html><html><head><style>@page{size:594mm 420mm;margin:12mm}body{font-family:Arial,sans-serif;margin:0;color:#122235}h1{font-size:22px;margin:0 0 8px}p{font-size:12px;margin:0 0 8px}svg{display:block;width:100% !important;height:350mm !important;max-width:100%}</style></head><body><h1>SwiftDrop — Proposed Architecture 2.0</h1><p>16 October 2026 · React all roles · Flutter Customer and Courier · Team sign-off pending</p>${svg}<p>Three APIs + YARP + Worker · Four isolated logical databases on one PostgreSQL instance · Delivery hosts GraphQL/SSE · Merchant owns webhook signing/attempts</p></body></html>`);
  await pdfPage.pdf({path:path.join(root,'design/diagrams/architecture/swiftdrop-architecture.pdf'),preferCSSPageSize:true,printBackground:true});
  await pdfPage.close();
  writeFileSync(path.join(out,'render-results.json'),JSON.stringify(results,null,2)+'\n');
  writeFileSync(path.join(root,'design/diagrams/manifest.json'),JSON.stringify(results,null,2)+'\n');
  const indexResult = spawnSync(process.env.PYTHON || 'python',[path.join(root,'scripts/index-diagrams.py')],{encoding:'utf8'});
  if (indexResult.status !== 0) throw new Error(indexResult.stderr || indexResult.stdout);
  const finalManifest = JSON.parse(readFileSync(path.join(root,'design/diagrams/manifest.json'),'utf8'));
  const packetPage = await browser.newPage();
  const pages = finalManifest.map(record => {
    const content=readFileSync(path.join(root,record.artifact),'utf8');
    return `<section><h2>${record.diagramId} — Proposed 2.0</h2><p>${record.source} · ${record.requirementIds.join(', ')} · Owner/review pending</p>${content}</section>`;
  }).join('');
  await packetPage.setContent(`<!doctype html><html><head><style>@page{size:594mm 420mm;margin:10mm}body{font-family:Arial,sans-serif;margin:0;color:#122235}section{break-after:page;height:390mm;box-sizing:border-box}section:last-child{break-after:auto}h2{font-size:22px;margin:0 0 8px}p{font-size:13px;margin:0 0 8px}section>svg{display:block;width:100% !important;height:364mm !important;max-width:100%}</style></head><body>${pages}</body></html>`);
  await packetPage.pdf({path:path.join(root,'design/diagrams/swiftdrop-design-baseline.pdf'),preferCSSPageSize:true,printBackground:true});
  await packetPage.close();
  console.log(`PASS: ${results.length} diagrams rendered; architecture PDF regenerated. Visual review remains separate.`);
} finally { await browser.close(); }
