import { copyFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');
const repoRoot = path.resolve(projectRoot, '..');

const sources = [
  { src: path.join(repoRoot, 'spec', 'core.schema.json'), dest: path.join(projectRoot, 'dist', 'schema', 'core.schema.json') },
  { src: path.join(repoRoot, 'spec', 'ocd-default-spec.ocd'), dest: path.join(projectRoot, 'dist', 'schema', 'ocd-default-spec.ocd') }
];

async function copySchemas() {
  for (const { src, dest } of sources) {
    await mkdir(path.dirname(dest), { recursive: true });
    await copyFile(src, dest);
  }
}

copySchemas().catch((error) => {
  console.error(error);
  process.exit(1);
});
