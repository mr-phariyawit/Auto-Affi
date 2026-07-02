# Study — CC Workflow Studio (`breaking-brake/cc-wf-studio`)

> 5-subagent deep study of the cloned repo (2026-07-02). Verdict for Auto-Affi at the bottom.

## What it is
A **visual canvas → Markdown compiler** for AI-agent workflows. Tagline: *"You think visually. AI thinks in `.md`.
CC Workflow Studio speaks both."* You draw a node graph on a React-Flow canvas; it exports agent-ready Markdown
(`.claude/skills/<wf>/SKILL.md` + `.claude/agents/*.md`, plus Copilot/Codex/Cursor/Gemini/Roo/Antigravity targets).
It **does not execute** anything — the AI coding agent runs the exported markdown. Published (VS Code Marketplace,
Open VSX, npm). Ext = AGPL-3.0 (v3.35.1); libs `core`/`cli`/`mcp` = MIT (0.x).

## Architecture (pnpm monorepo, 5 packages)
- **`@cc-wf-studio/core`** (MIT, hub, pure/no-I/O) — workflow types, zod schema, validation, migration, and the
  generators: Mermaid flowchart + `.claude/*.md` export + prompt/overview. `resources/workflow-schema.{json,toon}`
  is the AI-facing contract (toon = ~23% fewer tokens).
- **`cc-wf-studio-webview`** (React 19 + **ReactFlow v11** + zustand/zundo undo) — the canvas UI; host-agnostic via a
  `postMessage`/`acquireVsCodeApi` bridge.
- **`cc-wf-studio`** (VSCode extension) — hosts the webview as a CustomEditor for `**/.vscode/workflows/*.json`,
  runs an in-process **HTTP MCP server (default :6282)**, writes exports, Slack share/import.
- **`@cc-wf-studio/cli` (`ccwf`)** — re-hosts the same webview in a browser (HTTP+WS) for SSH/CI; render/validate/
  export/run/preview/canvas/mcp/tour/install-skills.
- **`@cc-wf-studio/mcp` (`ccwf-mcp`)** — stdio MCP server over one workflow file; 6 tools.

## Workflow model
- Source of truth = one **`workflow.json`** at `.vscode/workflows/*.json` (serialized `Workflow` object; max 100 nodes).
- **13 node types**: `start, end, prompt, subAgent, askUserQuestion, ifElse, switch, branch(legacy), skill, mcp,
  subAgentFlow, codex, group`. Edges = `Connection{from,to,fromPort,toPort,condition?}`. **No loop node** (loops =
  back-edges). `mcp` node params are **static/authored**, not runtime-computed.
- **Export shape (VERIFIED — a subagent ran the real generator):** frontmatter + a **Mermaid flowchart** (topology)
  + a **per-node "Details" reference section** the AI reads to execute. `subAgent` nodes become
  `.claude/agents/<name>.md` (frontmatter `name/description/model` + the agent body). SlashCommand frontmatter can
  carry `allowed-tools/model/context/argument-hint/hooks`.

## CLI / MCP usage
```sh
npx @cc-wf-studio/cli validate <wf.json>          # exit 0/1 — CI-friendly
npx @cc-wf-studio/cli render   <wf.json> [-f mermaid]   # md/mermaid to stdout
npx @cc-wf-studio/cli export   <wf.json> --agent claude-code [--overwrite --cwd DIR]
npx @cc-wf-studio/cli run      <wf.json> --launch  # export + spawn `claude` in the out dir
npx @cc-wf-studio/cli preview  <wf.json>           # read-only browser viewer (127.0.0.1)
npx @cc-wf-studio/cli canvas   <wf.json>           # experimental editable browser canvas
npx @cc-wf-studio/mcp --file   <wf.json>           # stdio MCP: AI edits the workflow
```
MCP tools (6): `get_current_workflow, get_workflow_schema (toon), apply_workflow (optimistic-lock revision),
update_nodes (partial), list_available_agents (~/.claude/agents + project), highlight_group_node (canvas-only)`.
No MCP resources. File writes are atomic (sha256 revision). Fully headless/CI-capable.

## VERDICT for Auto-Affi — **SKIP for authoring; optional TRIAL for onboarding diagrams only**
Grounded in reading both repos:
1. **Wrong altitude / lossy export.** Its frontmatter is only `name/description/tools/model/color/memory`. Our
   `.claude/agents/*.md` carry `disallowedTools`, full model IDs (`claude-sonnet-4-6`), bilingual `triggers.en/th`,
   and `reads/writes/wires/tests` contracts — an export would **strip/downgrade** these. Never point `export` at our
   repo root; it would scatter thin `.claude/skills/*` beside our real hand-written commands.
2. **It can't model what our pipeline IS.** Our value = paid API calls + `GatedProducer`/`assert_may_generate` gates
   + verify-before-spend + the STT-verify→reword→regen loop + "video ≥ VO length". Its node model has **no code/op
   node, no loop/retry, no cost gate**; the one executable-ish node (`mcp`) takes static params. A canvas of our
   pipeline would be a pretty-but-lying diagram — which clashes with our PRODUCED-vs-VERIFIED honesty contract.
3. **It runs nothing** (`ccwf run` = export + a hint). Pure GUI+markdown layer over orchestration that already lives
   in our JS ops + AEGIS agents = lossy duplication.

**One cheap, contained experiment (zero risk to `.claude/`):** in a scratch dir, hand-draw ONLY the `aegis-pipeline`
gate chain (or the 5 PGA gates) as a `workflow.json`, `npx @cc-wf-studio/cli render <file> -f mermaid`, keep just the
Mermaid as a `docs/` onboarding diagram — then judge it vs our existing `mermaid-render` + `diagram-first-reflex`
skills. Do NOT run `export`/`run` against the repo root; do NOT adopt its `.claude/skills/*` output.

**Bottom line:** interesting tool, well-engineered, right idea for greenfield agent-skill authoring — but Auto-Affi's
orchestration is code/API/gate-heavy and already richer than its markdown model. Not a fit as an authoring layer.
