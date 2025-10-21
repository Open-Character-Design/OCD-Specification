## GitHub Wiki Publishing

This folder contains the GitHub Wiki pages for the project. Keep content DRY; link to canonical docs in `docs/`, `spec/`, `examples/`, `grammar/`, `node/`, and `python/`.

Publish steps:

1. Clone the wiki repository (replace with your org/repo):
```bash
git clone https://github.com/your-org/OpenCharacter-Specification.wiki.git
```
2. Copy files into the wiki repo:
```bash
rsync -av --delete documentation/wiki/ OpenCharacter-Specification.wiki/
```
3. Commit and push:
```bash
cd OpenCharacter-Specification.wiki
git add -A
git commit -m "Sync wiki from documentation/wiki"
git push
```

Pages included:
- `Home.md`, `Getting-Started.md`, `Specification.md`, `Schema-Overview.md`, `Trait-Model.md`, `Grammar-OCD.md`
- `Reference-Fields.md`, `Reference-Vocabularies.md`, `Reference-Diagnostics.md`
- `Authoring-Guide.md`, `Examples.md`, `Validators.md`, `Integration-Node.md`, `Integration-Python.md`, `Agents.md`
- `FAQ.md`, `Glossary.md`, `Changelog.md`, `Governance.md`, `Versioning-and-Roadmap.md`, `Contributing.md`, `License.md`


