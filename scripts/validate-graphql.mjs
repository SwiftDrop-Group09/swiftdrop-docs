import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
let require = createRequire(import.meta.url);
try { require.resolve('graphql'); } catch { require = createRequire(path.join(root, '.validation-tools', 'package.json')); }
const { buildSchema, validateSchema, parse, validate } = require('graphql');
const schema = buildSchema(readFileSync(path.join(root, 'api/contracts/schema.graphql'), 'utf8'));
const errors = validateSchema(schema);
const publicExample = parse(`query { trackParcel(trackingNumber:"example") { status originCity destinationCity lastUpdatedAt timeline { status timestamp label } } }`);
errors.push(...validate(schema, publicExample));
const forbidden = parse(`query { trackParcel(trackingNumber:"example") { recipient { phoneNumber } pickupAddress { street } } }`);
if (!validate(schema, forbidden).length) errors.push(new Error('Unsafe public fields were accepted'));
const publicType = schema.getType('PublicTrackingSummary');
const expected = ['trackingNumber','status','originCity','destinationCity','lastUpdatedAt','timeline'];
if (JSON.stringify(Object.keys(publicType.getFields()).sort()) !== JSON.stringify(expected.sort())) errors.push(new Error('Public projection fields drifted'));
if (errors.length) { console.error(errors.map(e => e.message).join('\n')); process.exit(1); }
console.log('GraphQL: valid SDL and public example; private-field query rejected by schema. Runtime resolver authorization not tested.');
