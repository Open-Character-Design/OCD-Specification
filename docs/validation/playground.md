# In-Browser Validator (Preview)

This page will host a browser-based validator powered by the TypeScript implementation. It will run fully client-side: paste YAML/JSON, get diagnostics and normalized output.

## What you'll be able to do
- Paste or upload an OCD document (YAML/JSON)
- Choose validation mode (relaxed/strict)
- See errors, warnings, and normalized output
- Copy results for use in your tools

## Privacy and performance
- Client-side only: no files sent to any server by default
- Large files may be slower in the browser; use CLI for CI/production

## Try it now (coming soon)
This is a preview. Until the embed is ready:
- Python CLI → [Validators (Python)](../integration/python-validator.md)
- JS/TS CLI → [Validators (JS/TS)](../integration/js-ts-validator.md)

## Planned embed target
```html
<!-- Playground mount point (implementation to be added later) -->
<div id="ocd-playground"></div>
```
