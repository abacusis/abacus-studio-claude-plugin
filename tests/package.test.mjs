import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { test } from 'node:test';
import assert from 'node:assert/strict';
const read = path => readFileSync(new URL(`../${path}`, import.meta.url), 'utf8');
test('marketplace installs the existing root plugin without duplicating metadata', () => {
  const marketplace = JSON.parse(read('.claude-plugin/marketplace.json'));
  const plugin = JSON.parse(read('.claude-plugin/plugin.json'));
  assert.equal(marketplace.name, 'abacus-studio-marketplace');
  assert.equal(marketplace.owner.name, 'Abacus');
  assert.equal(marketplace.plugins.length, 1);
  assert.equal(marketplace.plugins[0].name, plugin.name);
  assert.equal(marketplace.plugins[0].source, './');
  assert.match(read('INSTALL.md'), /https:\/\/github.com\/abacusis\/abacus-studio-claude-plugin/);
  assert.match(read('INSTALL.md'), /abacus-studio@abacus-studio-marketplace/);
});
test('migrations require per-file approval and never deliver management credentials', () => {
  const skill = read('references/changes/migrate.md');
  assert.match(skill, /disable-model-invocation: true/);
  assert.match(skill, /migration-preview/);
  assert.match(skill, /migration-apply/);
  assert.match(skill, /setup\/install approval is NOT migration approval/);
  assert.match(skill, /Never retry uncertain outcomes/);
  assert.match(skill, /token.*server-side/);
});
test('Claude package uses one helper authorization without an extra connector', () => {
  const manifest = JSON.parse(read('.claude-plugin/plugin.json'));
  assert.equal(manifest.name, 'abacus-studio');
  assert.equal(manifest.version, '0.11.2');
  const config = JSON.parse(read('.mcp.json'));
  assert.deepEqual(config.mcpServers, {});
  assert.equal(config.mcpServers['studio-local'], undefined);
  assert.equal(config.mcpServers['studio-sync'], undefined);
});
test('autosync is opt-in, independent, and does not claim deployment or review submission',()=>{
  const skill=read('references/legacy-sync.md');
  assert.match(skill,/disable-model-invocation: true/);
  assert.match(skill,/enable_local_sync/);
  assert.match(skill,/only after approval/i);
  assert.match(skill,/sync_workspace.py/);
  assert.match(skill,/does not create a PR/);
  assert.match(skill,/token out of chat, logs and files/);
});
test('setup clones with the secure Git helper and never falls back to snapshots', () => {
  const skill = read('references/workspace/setup.md');
  assert.match(skill, /studio_git.py/);
  assert.match(skill, /NEW folder/);
  assert.match(skill, /Do not fall back to a ZIP/);
  assert.match(skill, /Setup never commits/);
});
test('skill is explicitly invoked, generic, and honest about its limited scope', () => {
  const skill = read('references/workspace/connect.md');
  assert.match(skill, /disable-model-invocation: true/);
  assert.match(skill, /list-apps/);
  assert.match(skill, /workspace-config/);
  assert.match(skill, /needs_configuration/);
  assert.match(skill, /schema_version/);
  assert.match(skill, /does not authorize/);
  for (const fixture of ['private-client-app', 'abacusis/private-client', 'Bearer ', 'service_role_key']) assert.equal(skill.includes(fixture), false);
});
test('menu exposes seven direct actions with valid workflow links', () => {
  const root = new URL('../skills/', import.meta.url);
  const commands = readdirSync(root).filter(name => existsSync(new URL(`${name}/SKILL.md`, root))).sort();
  const visible = commands.filter(name => !read(`skills/${name}/SKILL.md`).includes('user-invocable: false'));
  assert.deepEqual(visible, ['connect', 'design', 'disconnect', 'request-publish', 'setup', 'status', 'submit']);
  assert.match(read('skills/sandbox-database/SKILL.md'), /user-invocable: false/);
  for (const command of commands) {
    const skill = read(`skills/${command}/SKILL.md`);
    if (!['design', 'sandbox-database'].includes(command)) assert.match(skill, /disable-model-invocation: true/);
    for (const match of skill.matchAll(/\]\((\.\.\/\.\.\/references\/[^)]+)\)/g)) {
      assert.equal(existsSync(new URL(`../skills/${command}/${match[1]}`, import.meta.url)), true);
    }
  }
});
test('Setup works directly and Status stays limited to connection access', () => {
  const skill = read('skills/setup/SKILL.md');
  assert.match(skill, /no separate Connect command is required/);
  const setup = read('references/workspace/setup.md');
  assert.match(setup, /list-apps/);
  assert.match(setup, /workspace-config/);
  assert.match(setup, /Browser consent and host-required execution prompts still apply/);
  assert.match(read('references/workspace/status.md'), /get_connection_status/);
});
