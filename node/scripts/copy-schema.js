import { copyFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');
const repoRoot = path.resolve(projectRoot, '..');

const source = path.join(repoRoot, 'spec', 'core.schema.json');
const destination = path.join(projectRoot, 'dist', 'schema', 'core.schema.json');

async function copySchema() {
  await mkdir(path.dirname(destination), { recursive: true });
  await copyFile(source, destination);
}

copySchema().catch((error) => {
  console.error(error);
  process.exit(1);
});
