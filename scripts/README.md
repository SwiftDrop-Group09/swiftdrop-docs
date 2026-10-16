# Documentation Validation and Rendering

These checks validate local documentation and design fixtures. They do not run application business tests or prove deployment/approval.

Use Python and Node versions supporting the pinned packages in [requirements.txt](requirements.txt) and [package.json](package.json). The recorded run used Python 3.14 and installed package versions; use isolated environments. From the repository root:

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r scripts/requirements.txt
$env:PUPPETEER_SKIP_DOWNLOAD='true'
npm.cmd --prefix scripts ci
$env:CHROME_PATH='C:/Program Files/Google/Chrome/Application/chrome.exe'
$env:PLANTUML_JAR='<path-to-plantuml-1.2026.8.jar>'
node scripts/render-diagrams.mjs
python scripts/sync-catalogs.py
python scripts/review-pdfs.py
node scripts/validate-graphql.mjs
.venv/Scripts/python scripts/validate-docs.py
docker compose --env-file deployment/.env.example -f deployment/compose.yaml --profile application config --quiet
```

For Linux/macOS activate the virtual environment and use its Python; set the same environment variables with the host shell. Install a local Java runtime and obtain PlantUML 1.2026.8 from its official release; do not commit JAR/node_modules/browser binaries. PlantUML renders formal activities; Mermaid renders sequence/ER/context and other diagrams. Render script regenerates SVGs, [manifest](../design/diagrams/manifest.json) and architecture PDF; visually inspect the PDF after each change. For a faster schema/link-only check, use the final two validation commands against existing exports. Docker config uses **placeholder** environment values and never starts containers; actual startup needs generated ignored secrets, real application images and a running daemon.

`sync-catalogs.py` regenerates route/trace/test tables and derives requirement totals from JSON fixtures. `validate-docs.py` checks relative paths/anchors, balanced fences, canonical REST method/path references, exact SRS/trace/test IDs/counts, Must priorities, JSON/event schemas/privacy, state mapping, Compose data ownership and actual protobuf compilation. `validate-graphql.mjs` validates SDL/example and rejects private fields on public tracking at schema level; resolver authorization still needs backend tests. `render-diagrams.mjs` fails on rendering errors, publishes source/export inventory with source hashes, and regenerates the architecture PDF plus a packet of all 33 diagrams. It accepts existing Chromium via CHROME_PATH and uses only local diagram sources. All current Markdown documents, including the remaining-work checklist, are checked for canonical route references.
