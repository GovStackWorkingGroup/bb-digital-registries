import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { realpath, stat } from 'node:fs/promises';
import path from 'node:path';
import { parseArgs } from 'node:util';
import { fileURLToPath } from 'node:url';

const packageRoot = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const sourceRoot = path.dirname(packageRoot);
const commands = new Set(['generate', 'build', 'check', 'preview', 'check-built', 'test-served']);

function publicationKey(canonicalSourceRoot) {
  return `framework-${createHash('sha256').update(canonicalSourceRoot).digest('hex').slice(0, 12)}`;
}

async function isFile(pathname) {
  try {
    return (await stat(pathname)).isFile();
  } catch (error) {
    if (error.code === 'ENOENT') return false;
    throw error;
  }
}

function rendererRoot(env) {
  if (env.GOVSTACK_SITE_RENDERER) {
    if (!path.isAbsolute(env.GOVSTACK_SITE_RENDERER)) {
      throw new Error('GOVSTACK_SITE_RENDERER must be an absolute path');
    }
    return path.normalize(env.GOVSTACK_SITE_RENDERER);
  }
  return path.resolve(packageRoot, '..', '..', 'govstack-specification-site');
}

async function assertFrameworkSource() {
  const required = ['metadata.yml', 'authors.yml', 'toc.yml'];
  const missing = [];
  for (const filename of required) {
    if (!(await isFile(path.join(sourceRoot, filename)))) missing.push(filename);
  }
  if (missing.length) {
    throw new Error(
      `Shared specification rendering is not active: missing framework-format sources ${missing.join(', ')} at ${sourceRoot}. `
      + 'Migrate this legacy GitBook template to the framework format before using this wrapper.',
    );
  }
}

async function assertRenderer(renderer) {
  const entryPoint = path.join(renderer, 'scripts', 'site.mjs');
  if (!(await isFile(entryPoint))) {
    throw new Error(
      `Shared renderer entry point not found at ${entryPoint}. Set GOVSTACK_SITE_RENDERER to an absolute checkout path.`,
    );
  }

  if (await isFile(path.join(sourceRoot, 'api-references.yml'))) {
    const scalarFiles = [
      path.join(renderer, 'scripts', 'api-references.mjs'),
      path.join(renderer, 'src', 'components', 'ReferenceContent.astro'),
    ];
    const missing = [];
    for (const filename of scalarFiles) {
      if (!(await isFile(filename))) missing.push(path.relative(renderer, filename));
    }
    if (missing.length) {
      throw new Error(
        `The configured renderer predates native Scalar reference support and is missing ${missing.join(', ')}. `
        + 'Upgrade to a published renderer revision that includes native Scalar references.',
      );
    }
  }

  return entryPoint;
}

function run(entryPoint, renderer, args, env) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [entryPoint, ...args], {
      cwd: renderer,
      env,
      stdio: 'inherit',
    });
    child.once('error', reject);
    child.once('exit', (code, signal) => {
      if (code === 0) resolve();
      else reject(new Error(`Shared renderer exited with ${signal || code}`));
    });
  });
}

export async function main(args = process.argv.slice(2), env = process.env) {
  const command = args[0];
  if (!commands.has(command)) throw new Error(`Unsupported command: ${command || '(missing)'}`);

  const { values } = parseArgs({
    args: args.slice(1),
    options: {
      base: { type: 'string' },
      output: { type: 'string' },
      unofficial: { type: 'boolean' },
      port: { type: 'string' },
    },
  });

  await assertFrameworkSource();
  const configuredRenderer = rendererRoot(env);
  await assertRenderer(configuredRenderer);
  const renderer = await realpath(configuredRenderer);
  const canonicalSourceRoot = await realpath(sourceRoot);
  if (values.output && !path.isAbsolute(values.output)) {
    throw new Error('--output must be an absolute path');
  }
  const outputRoot = values.output
    ? path.normalize(values.output)
    : path.join(renderer, 'dist', publicationKey(canonicalSourceRoot));
  const entryPoint = path.join(renderer, 'scripts', 'site.mjs');
  const rendererArgs = [
    command,
    '--profile',
    'framework',
    '--source',
    canonicalSourceRoot,
    '--output',
    outputRoot,
  ];
  if (values.base) rendererArgs.push('--base', values.base);
  if (values.unofficial) rendererArgs.push('--unofficial');
  if (values.port) rendererArgs.push('--port', values.port);
  await run(entryPoint, renderer, rendererArgs, env);
}

const invokedPath = process.argv[1] ? await realpath(process.argv[1]) : undefined;
const modulePath = await realpath(fileURLToPath(import.meta.url));
if (invokedPath === modulePath) {
  main().catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
