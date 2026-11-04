import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { createHash } from 'node:crypto';
import { cp, mkdir, mkdtemp, readFile, realpath, rm, stat, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { promisify } from 'node:util';
import { fileURLToPath, pathToFileURL } from 'node:url';
import test from 'node:test';

const execFileAsync = promisify(execFile);
const actualPackageRoot = fileURLToPath(new URL('../', import.meta.url));
const wrapperSource = fileURLToPath(new URL('../scripts/site.mjs', import.meta.url));

function publicationKey(sourceRoot) {
  return `framework-${createHash('sha256').update(sourceRoot).digest('hex').slice(0, 12)}`;
}

function optionValue(args, option) {
  return args[args.indexOf(option) + 1];
}

async function loadRendererHelper(t) {
  const configured = process.env.GOVSTACK_SITE_RENDERER;
  if (configured && !path.isAbsolute(configured)) {
    throw new Error('GOVSTACK_SITE_RENDERER must be absolute for renderer integration tests');
  }
  const rendererRoot = configured
    ? path.normalize(configured)
    : path.resolve(actualPackageRoot, '..', '..', 'govstack-specification-site');
  const helperPath = path.join(rendererRoot, 'scripts', 'publication.mjs');
  let available = false;
  try {
    available = (await stat(helperPath)).isFile();
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
  }
  if (!available) {
    if (configured) throw new Error(`Renderer helper not found at ${helperPath}`);
    t.skip(`renderer integration checkout not available at ${rendererRoot}`);
    return undefined;
  }
  const helper = await import(pathToFileURL(helperPath).href);
  assert.equal(typeof helper.resolveBuild, 'function', `${helperPath} must export resolveBuild`);
  return { resolveBuild: helper.resolveBuild, rendererRoot: await realpath(rendererRoot) };
}

async function write(pathname, contents = '') {
  await mkdir(path.dirname(pathname), { recursive: true });
  await writeFile(pathname, contents);
}

async function fixture({ prerequisites = ['metadata.yml', 'authors.yml', 'toc.yml'] } = {}) {
  const scratch = await mkdtemp(path.join(os.tmpdir(), 'bb-template-site-wrapper-'));
  const workspace = path.join(scratch, 'workspace');
  const repoRoot = path.join(workspace, 'bb-template');
  const packageRoot = path.join(repoRoot, 'specification-site');
  const wrapper = path.join(packageRoot, 'scripts', 'site.mjs');
  const fallbackRenderer = path.join(workspace, 'govstack-specification-site');
  const outsideCwd = path.join(scratch, 'outside-cwd');
  const result = path.join(scratch, 'renderer-result.json');

  await mkdir(outsideCwd, { recursive: true });
  await mkdir(path.dirname(wrapper), { recursive: true });
  await cp(wrapperSource, wrapper);
  for (const prerequisite of prerequisites) await write(path.join(repoRoot, prerequisite), `${prerequisite}\n`);

  return {
    scratch,
    repoRoot,
    packageRoot,
    wrapper,
    fallbackRenderer,
    outsideCwd,
    result,
    async stubRenderer(rendererRoot = fallbackRenderer, { scalar = false } = {}) {
      await write(
        path.join(rendererRoot, 'scripts', 'site.mjs'),
        `import { writeFile } from 'node:fs/promises';\nawait writeFile(process.env.STUB_RESULT, JSON.stringify({ argv: process.argv.slice(2), cwd: process.cwd() }));\n`,
      );
      if (scalar) {
        await write(path.join(rendererRoot, 'scripts', 'api-references.mjs'));
        await write(path.join(rendererRoot, 'src', 'components', 'ReferenceContent.astro'));
      }
      return rendererRoot;
    },
    async run(args, env = {}) {
      const childEnv = { ...process.env, STUB_RESULT: result, ...env };
      if (!Object.hasOwn(env, 'GOVSTACK_SITE_RENDERER')) delete childEnv.GOVSTACK_SITE_RENDERER;
      return execFileAsync(process.execPath, [wrapper, ...args], {
        cwd: outsideCwd,
        env: childEnv,
      });
    },
    async output() {
      return JSON.parse(await readFile(result, 'utf8'));
    },
  };
}

test('resolves source, output, and sibling renderer independently of cwd', async (t) => {
  const site = await fixture();
  t.after(() => rm(site.scratch, { recursive: true, force: true }));
  await site.stubRenderer();

  await site.run(['check', '--base', '/sample/', '--unofficial', '--port', '4321']);
  const canonicalRoot = await realpath(site.repoRoot);
  const canonicalRenderer = await realpath(site.fallbackRenderer);
  const output = path.join(canonicalRenderer, 'dist', publicationKey(canonicalRoot));
  const invocation = (await site.output()).argv;

  assert.deepEqual(invocation, [
    'check',
    '--profile',
    'framework',
    '--source',
    canonicalRoot,
    '--output',
    output,
    '--base',
    '/sample/',
    '--unofficial',
    '--port',
    '4321',
  ]);
});

test('uses an absolute GOVSTACK_SITE_RENDERER override', async (t) => {
  const site = await fixture();
  t.after(() => rm(site.scratch, { recursive: true, force: true }));
  const override = await site.stubRenderer(path.join(site.scratch, 'renderer-override'));

  await site.run(['build'], { GOVSTACK_SITE_RENDERER: override });
  const canonicalRoot = await realpath(site.repoRoot);
  const canonicalRenderer = await realpath(override);

  assert.deepEqual((await site.output()).argv.slice(0, 7), [
    'build',
    '--profile',
    'framework',
    '--source',
    canonicalRoot,
    '--output',
    path.join(canonicalRenderer, 'dist', publicationKey(canonicalRoot)),
  ]);
});

test('accepts an absolute external output override', async (t) => {
  const site = await fixture();
  t.after(() => rm(site.scratch, { recursive: true, force: true }));
  await site.stubRenderer();
  const output = path.join(site.scratch, 'preview-output');

  await site.run(['preview', '--output', output]);

  const invocation = (await site.output()).argv;
  assert.equal(optionValue(invocation, '--output'), output);
});

test('rejects relative output overrides before renderer invocation', async (t) => {
  const site = await fixture();
  t.after(() => rm(site.scratch, { recursive: true, force: true }));
  await site.stubRenderer();

  await assert.rejects(site.run(['preview', '--output', 'preview-output']), (error) => {
    assert.match(error.stderr, /--output must be an absolute path/);
    return true;
  });
  await assert.rejects(readFile(site.result), { code: 'ENOENT' });
});

test('default and external outputs satisfy the real renderer separation contract', async (t) => {
  const renderer = await loadRendererHelper(t);
  if (!renderer) return;
  const site = await fixture();
  t.after(() => rm(site.scratch, { recursive: true, force: true }));
  await site.stubRenderer();

  await site.run(['check']);
  let invocation = (await site.output()).argv;
  assert.doesNotThrow(() => renderer.resolveBuild({
    profile: 'framework',
    sourceRoot: optionValue(invocation, '--source'),
    distDir: optionValue(invocation, '--output'),
  }));

  await site.run(['preview', '--output', path.join(site.scratch, 'external-output')]);
  invocation = (await site.output()).argv;
  assert.doesNotThrow(() => renderer.resolveBuild({
    profile: 'framework',
    sourceRoot: optionValue(invocation, '--source'),
    distDir: optionValue(invocation, '--output'),
  }));
});

test('the real renderer rejects output beneath the consumer source', async (t) => {
  const renderer = await loadRendererHelper(t);
  if (!renderer) return;
  const site = await fixture();
  t.after(() => rm(site.scratch, { recursive: true, force: true }));
  const canonicalRoot = await realpath(site.repoRoot);

  assert.throws(() => renderer.resolveBuild({
    profile: 'framework',
    sourceRoot: canonicalRoot,
    distDir: path.join(canonicalRoot, 'specification-site', 'dist'),
  }), /Source, generated workspace, and output must not overlap/);
});

test('the complete test kit runs outside the renderer sibling layout with an absolute override', async (t) => {
  if (process.env.GOVSTACK_WRAPPER_PORTABILITY_CHILD === '1') return;
  const renderer = await loadRendererHelper(t);
  if (!renderer) return;
  const scratch = await mkdtemp(path.join(os.tmpdir(), 'bb-template-site-portability-'));
  t.after(() => rm(scratch, { recursive: true, force: true }));
  const copiedPackage = path.join(scratch, 'isolated', 'building-block', 'specification-site');
  const outsideCwd = path.join(scratch, 'outside-cwd');
  await cp(actualPackageRoot, copiedPackage, { recursive: true });
  await mkdir(outsideCwd, { recursive: true });
  await assert.rejects(
    stat(path.join(scratch, 'isolated', 'govstack-specification-site')),
    { code: 'ENOENT' },
  );

  const standaloneEnv = {
    ...process.env,
    GOVSTACK_WRAPPER_PORTABILITY_CHILD: '1',
  };
  delete standaloneEnv.GOVSTACK_SITE_RENDERER;
  await execFileAsync(process.execPath, [path.join(copiedPackage, 'test', 'site.test.mjs')], {
    cwd: outsideCwd,
    env: standaloneEnv,
  });

  await execFileAsync(process.execPath, [path.join(copiedPackage, 'test', 'site.test.mjs')], {
    cwd: outsideCwd,
    env: {
      ...process.env,
      GOVSTACK_SITE_RENDERER: renderer.rendererRoot,
      GOVSTACK_WRAPPER_PORTABILITY_CHILD: '1',
    },
  });
});

test('rejects a relative GOVSTACK_SITE_RENDERER override', async (t) => {
  const site = await fixture();
  t.after(() => rm(site.scratch, { recursive: true, force: true }));

  await assert.rejects(
    site.run(['generate'], { GOVSTACK_SITE_RENDERER: '../renderer' }),
    (error) => {
      assert.match(error.stderr, /GOVSTACK_SITE_RENDERER must be an absolute path/);
      return true;
    },
  );
});

test('fails before renderer invocation when framework sources are incomplete', async (t) => {
  const site = await fixture({ prerequisites: ['metadata.yml', 'toc.yml'] });
  t.after(() => rm(site.scratch, { recursive: true, force: true }));
  await site.stubRenderer();

  await assert.rejects(site.run(['check']), (error) => {
    assert.match(error.stderr, /authors\.yml/);
    assert.match(error.stderr, /framework-format sources/);
    return true;
  });
  await assert.rejects(readFile(site.result), { code: 'ENOENT' });
});

test('reports a missing shared renderer entry point', async (t) => {
  const site = await fixture();
  t.after(() => rm(site.scratch, { recursive: true, force: true }));

  await assert.rejects(site.run(['preview']), (error) => {
    assert.match(error.stderr, /Shared renderer entry point not found/);
    assert.match(error.stderr, /GOVSTACK_SITE_RENDERER/);
    return true;
  });
});

test('configured API references require native Scalar renderer support', async (t) => {
  const site = await fixture();
  t.after(() => rm(site.scratch, { recursive: true, force: true }));
  await site.stubRenderer();
  await write(path.join(site.repoRoot, 'api-references.yml'), 'references: []\n');

  await assert.rejects(site.run(['check']), (error) => {
    assert.match(error.stderr, /predates native Scalar reference support/);
    assert.match(error.stderr, /Upgrade to a published renderer revision/);
    return true;
  });
  await assert.rejects(readFile(site.result), { code: 'ENOENT' });
});

test('configured API references run with native Scalar renderer support', async (t) => {
  const site = await fixture();
  t.after(() => rm(site.scratch, { recursive: true, force: true }));
  await site.stubRenderer(site.fallbackRenderer, { scalar: true });
  await write(path.join(site.repoRoot, 'api-references.yml'), 'references: []\n');

  await site.run(['generate']);

  assert.equal((await site.output()).argv[0], 'generate');
});

test('forwards every supported renderer command', async (t) => {
  const site = await fixture();
  t.after(() => rm(site.scratch, { recursive: true, force: true }));
  await site.stubRenderer();

  for (const command of ['generate', 'build', 'check', 'preview', 'check-built', 'test-served']) {
    await site.run([command]);
    assert.equal((await site.output()).argv[0], command);
  }
});

test('rejects commands and options outside the wrapper interface', async (t) => {
  const site = await fixture();
  t.after(() => rm(site.scratch, { recursive: true, force: true }));
  await site.stubRenderer();

  await assert.rejects(site.run(['dev']), (error) => {
    assert.match(error.stderr, /Unsupported command: dev/);
    return true;
  });
  await assert.rejects(site.run(['check', '--source', '/tmp/other']), (error) => {
    assert.match(error.stderr, /Unknown option '--source'/);
    return true;
  });
});
