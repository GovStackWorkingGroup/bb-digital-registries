# Digital Registries specification site

This thin wrapper uses the shared GovStack renderer. The repository root is the
source; generated output goes to the renderer-owned `dist/framework-<source-hash>` directory, separate from the source.

Use Node 24.11 or later and a renderer checkout containing native Scalar support:

```sh
export GOVSTACK_SITE_RENDERER=/absolute/path/to/govstack-specification-site
npm --prefix "$GOVSTACK_SITE_RENDERER" ci --ignore-scripts
npm --prefix specification-site run check -- --base /bb-digital-registries/ --unofficial
npm --prefix specification-site run preview -- --base /bb-digital-registries/ --unofficial --port 4339
```

Run the preview with the same base used for the build. Existing output containing
obsolete HTML is preserved, so use the renderer CLI with a fresh absolute `--output`
directory when removing published routes.

Root `api-references.yml` connects Consultation, Write, and their illustrative
contracts to the pages in `toc.yml`. OpenAPI and its local dependencies remain
the source of truth. The site adds no API requirements or domain model.

`npm test` checks the wrapper; `npm run check` runs the shared renderer's test,
build, output, and HTTP checks. The wrapper rejects a renderer that would
silently ignore native API references.

The fork's site-check and preview workflows use the shared build-only action.
Before hosted activation, publish the reviewed renderer change and set the
repository variable `GOVSTACK_SITE_RENDERER_REF` to its exact full commit. The
workflow checks that value, the checked-out commit, and native Scalar support.
It does not follow a renderer branch. The previous renderer pin lacks this
feature and is deliberately rejected rather than producing an incomplete site.

Only the existing preview workflow deploys output, retaining its fork-only,
unofficial-preview policy. The wrapper and site-check workflow do not deploy.
The template's `specification-site/` directory is the source for this wrapper;
renderer implementation and dependencies stay in the shared renderer.
