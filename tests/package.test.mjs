import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { test } from 'node:test';
import assert from 'node:assert/strict';
const read = path => readFileSync(new URL(`../${path}`, import.meta.url), 'utf8');
test('Engineering loads coordination with honest limits and complete responsibilities', () => {
  assert.match(read('skills/engineering/SKILL.md'), /\[Coordinator workflow\]\(\.\.\/\.\.\/references\/engineering\/orchestration\.md\)/);
  const guide = read('references/engineering/orchestration.md');
  for (const role of ['Orchestrator', 'Spec Writer', 'Builder', 'Verification Specialist', 'Code Reviewer', 'Security Reviewer', 'UI Reviewer', 'UX Reviewer', 'Readiness Reviewer']) assert.ok(guide.includes(role), role);
  for (const phrase of ['Classify by consequences, not file count', 'no mandatory classification questionnaire', 'Do not spawn specialist', 'two correction rounds', 'Needs human input', 'Source inspection does not', 'HEAD', 'not installed agents', 'not a publishing Approver']) assert.ok(guide.toLowerCase().includes(phrase.toLowerCase()), phrase);
  assert.match(guide, /Execution depends on the local Claude session/);
  assert.match(guide, /summarize the scope and proceed/);
  assert.match(guide, /Saving and publishing/);
  assert.match(read('references/engineering/specification.md'), /do not add a mandatory approval pause/);
  assert.match(read('references/engineering/orchestration-testing.md'), /not model compliance/);
});
test('Spec Writer has a read-only handoff and Builder is the only other specialist', () => {
  assert.deepEqual(readdirSync(new URL('../agents/', import.meta.url)).sort(), ['builder.md', 'spec-writer.md']);
  const agent = read('agents/spec-writer.md');
  const frontmatter = agent.split('---')[1];
  assert.match(frontmatter, /^name: spec-writer$/m);
  assert.match(frontmatter, /^tools: Read, Grep, Glob$/m);
  assert.match(frontmatter, /^model: inherit$/m);
  assert.match(frontmatter, /^maxTurns: 20$/m);
  assert.match(agent, /If a required instruction file is inaccessible, return blocked/);
  assert.doesNotMatch(frontmatter, /permissionMode|hooks|mcpServers|memory|skills/);
  for (const phrase of ['Do not write even specification files', 'Do not assume you inherit', 'unavailable knowledge', 'UI considerations and UX considerations', 'explicitly planned, not run', 'Never read .env']) {
    assert.ok(agent.includes(phrase), phrase);
  }
  const coordinator = read('references/engineering/orchestration.md');
  assert.match(coordinator, /Invoke the installed namespaced `abacus-studio:spec-writer`/);
  assert.match(coordinator, /If unavailable or denied/);
  assert.match(coordinator, /Wait for its result/);
  assert.match(coordinator, /Only Spec Writer and Builder are installed specialist agents/);
  assert.match(read('skills/engineering/SKILL.md'), /you MUST delegate the specification/);
  assert.match(read('skills/project-knowledge/SKILL.md'), /do not invoke Engineering again/);
  assert.match(coordinator, /Do not paste the agent's full draft into chat by default/);
  assert.match(read('references/client-communication.md'), /aim for 2–4 sentences/);
  assert.match(coordinator, /never collapse them into a single/);
});
test('every bundled skill loads the shared client communication standard', () => {
  const root = new URL('../skills/', import.meta.url);
  const skills = readdirSync(root).filter(name => existsSync(new URL(`${name}/SKILL.md`, root)));
  assert.ok(skills.length > 0);
  for (const name of skills) {
    assert.match(read(`skills/${name}/SKILL.md`), /Read and apply \[Client communication\]\(\.\.\/\.\.\/references\/client-communication\.md\) completely\./, name);
  }
  const standard = read('references/client-communication.md');
  assert.match(standard, /Lead with the outcome/);
  assert.match(standard, /usually be under 100 words, not a rigid limit/);
  assert.match(standard, /user asks for technical details/);
  assert.match(standard, /never overrides permissions, approval requirements/);
  assert.match(standard, /exact commands, SQL, diffs/);
  assert.match(standard, /Never print credentials/);
  assert.match(standard, /short answer is not permission to skip verification/);
  assert.match(standard, /review requested, not approved or live/);
});
test('Builder is scoped to implementation and browser capture is not a visual pass', () => {
  const agent = read('agents/builder.md');
  const frontmatter = agent.split('---')[1];
  assert.match(frontmatter, /^tools: Read, Grep, Glob, Edit, Write, Bash$/m);
  assert.match(frontmatter, /^model: inherit$/m);
  assert.match(frontmatter, /^maxTurns: 40$/m);
  assert.doesNotMatch(frontmatter, /permissionMode|hooks|mcpServers|memory/);
  for (const phrase of ['A plan alone', 'Do not commit', 'subject to host permissions', 'Read captured images', 'not independent verification']) assert.ok(agent.includes(phrase), phrase);
  const engineering = read('skills/engineering/SKILL.md');
  assert.match(engineering, /you MUST then delegate to/);
  assert.match(engineering, /Planning-only work must never invoke Builder/);
  const browser = read('references/engineering/browser-verification.md');
  for (const phrase of ['Capture never auto-installs', 'captured is NOT a visual pass', 'no automatic redaction', 'No personal browser profile', 'do not sandbox the server']) assert.ok(browser.includes(phrase), phrase);
});
test('marketplace installs the existing root plugin without duplicating metadata', () => {
  const marketplace = JSON.parse(read('.claude-plugin/marketplace.json'));
  const plugin = JSON.parse(read('.claude-plugin/plugin.json'));
  assert.equal(marketplace.name, 'abacus-studio-marketplace');
  assert.equal(marketplace.owner.name, 'Abacus');
  assert.equal(marketplace.plugins.length, 1);
  assert.equal(marketplace.plugins[0].name, plugin.name);
  assert.equal(marketplace.plugins[0].version, plugin.version);
  assert.equal(marketplace.plugins[0].description, plugin.description);
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
  assert.equal(manifest.version, '0.18.0');
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
test('menu exposes direct actions and engineering with valid workflow links', () => {
  const root = new URL('../skills/', import.meta.url);
  const commands = readdirSync(root).filter(name => existsSync(new URL(`${name}/SKILL.md`, root))).sort();
  const visible = commands.filter(name => !read(`skills/${name}/SKILL.md`).includes('user-invocable: false'));
  assert.deepEqual(visible, ['connect', 'design', 'disconnect', 'engineering', 'request-publish', 'security', 'setup', 'status', 'submit']);
  assert.match(read('skills/sandbox-database/SKILL.md'), /user-invocable: false/);
  for (const command of commands) {
    const skill = read(`skills/${command}/SKILL.md`);
    if (!['design', 'engineering', 'security', 'project-knowledge', 'sandbox-database'].includes(command)) assert.match(skill, /disable-model-invocation: true/);
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
