# Coding Standards — Auto-Affi

- **Primary language**: Python 3.12+
- **Frontend**: Next.js 15 + TypeScript 5+ (ops console)
- **Last updated**: 2026-05-12

---

## 1. Python

### 1.1 Tools (enforced ใน CI)
- **Formatter**: `black` (line-length=100)
- **Linter**: `ruff` (rules: E, F, W, I, B, UP, SIM, RUF; ignore E501 ถ้า black แตะแล้ว)
- **Type checker**: `mypy` strict mode บน `src/`
- **Secret scan**: `gitleaks`
- **Import sort**: `ruff --select I` (replaces isort)

### 1.2 Style
- 4-space indent, no tabs
- Use `from __future__ import annotations` ใน module ที่มี forward ref
- Prefer `dataclass` / `pydantic.BaseModel` สำหรับ structured data
- Use type hint ทุก function signature (mypy strict)
- f-string เท่านั้น สำหรับ string formatting (no `%` no `.format()`)
- `pathlib.Path` แทน `os.path`

### 1.3 Naming
- `snake_case` สำหรับ function / variable / module
- `PascalCase` สำหรับ class
- `SCREAMING_SNAKE` สำหรับ module-level constants
- Private = leading underscore (`_helper`)
- ห้าม single-letter เว้นแต่ index loop (`i`, `j`)

### 1.4 Project Structure
```
src/auto_affi/
  agents/        # one module per agent: scout.py, strategist.py, ...
  adapters/      # one per external API: shopee.py, kie.py, eleven.py, ...
  workflows/     # Temporal workflows + activities
  pipeline/      # Editor + Hyperframe + ffmpeg utilities
  wiki/          # retrieval, write, tier mgmt
  schemas/       # pydantic models for cross-boundary data
  ops/           # CLI + ops console backend
  config/        # settings, secrets loader
  observability/ # OTel + Langfuse integration
tests/
  fixtures/
  golden_traces/
  unit/ integration/ e2e/
```

### 1.5 Comments
- Default = ไม่เขียน comment (อ่าน code เอาเอง)
- เขียนเมื่อ: hidden constraint, subtle invariant, workaround, surprising behavior
- ห้ามอธิบาย "what" (ใส่ชื่อตัวแปรให้ดี); เขียน "why" เท่านั้น
- ห้าม `# TODO` without Linear issue link
- ห้าม `# removed` / `# old code` (ลบไปเลย — git track history)

### 1.6 Function Discipline
- ฟังก์ชันยาว > 50 บรรทัด = แตก
- Argument > 5 ตัว = pass dataclass/Model แทน
- No mutable default args
- Async function ที่ทำ I/O ต้อง `await` ทุกตัว, ห้าม sync inside async

### 1.7 Error Handling
- Custom exception class ภายใต้ `src/auto_affi/exceptions.py` (no generic `Exception` raise)
- Catch exception ที่กว้างที่สุดที่ "เข้าใจวิธีจัดการ" — ห้าม `except: pass`
- Re-raise พร้อม context (`raise NewError(...) from err`)
- Boundary validation = pydantic; internal trust ตามกฎ "trust internal code"

### 1.8 Logging
- ใช้ `structlog` (JSON output) + OTel attribute
- Levels: `DEBUG` (dev only), `INFO` (events), `WARNING` (recoverable), `ERROR` (action needed), `CRITICAL` (page on-call)
- ห้าม log secret / API key / PII (auto-redact filter enforced)
- ทุก log มี: `trace_id`, `agent`, `tool`, `cost_usd`, `latency_ms` field

### 1.9 Testing
- `pytest` + `pytest-asyncio`
- Test file = `test_<module>.py` mirror `src/` structure
- Coverage ≥ 70% บน `adapters/` + `workflows/`
- Use fixtures, ไม่ duplicate setup
- VCR cassette สำหรับ vendor API
- Deterministic seed สำหรับ random / time

### 1.10 Performance
- Avoid premature optimize; profile ก่อน optim
- Async-by-default สำหรับ I/O
- DB query: ห้าม N+1; ใช้ `select_related` / batched fetch
- Embeddings cache local LRU + persistent pgvector

---

## 2. TypeScript (Ops Console)

### 2.1 Tools
- `eslint` (recommended + typescript-eslint strict)
- `prettier` (default + tailwind plugin)
- `tsc --strict`

### 2.2 Style
- 2-space indent
- Prefer `const` over `let`; never `var`
- Functional React component + hooks
- `interface` for object shape, `type` for union/utility
- No `any` (use `unknown` + narrow)

### 2.3 Naming
- `camelCase` for function/variable
- `PascalCase` for component/type/interface
- File = component PascalCase, util kebab-case

### 2.4 Component Discipline
- Server components default ใน Next.js 15
- Client component เฉพาะที่ใช้ interactivity (`'use client'`)
- shadcn/ui primitives — ห้าม fork unless necessary

---

## 3. Git Hygiene

### 3.1 Branches
- `main` — protected, deploy-ready
- `claude/<feature-slug>` — AI co-dev branches
- `feat/<slug>` / `fix/<slug>` / `docs/<slug>` / `chore/<slug>`

### 3.2 Commit Messages — Conventional Commits
```
<type>(<scope>): <short summary>

<body — optional, why not what>

<footer — Linear issue link>
```
Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `perf`, `build`, `ci`, `revert`

ตัวอย่าง:
```
feat(scout): add Shopee saturation penalty to score

Avoids re-scouting products already promoted in last 7d. Wiki research
showed >40% engagement drop for repeat SKUs.

Closes AEG-123
```

### 3.3 PR Rules
- Title = Conventional Commits format
- Body = Summary + Test plan + Linear link
- Squash merge default
- ≥ 1 approval required
- Block on: lint, unit, integration, golden trace regression

### 3.4 Forbidden
- ❌ `git push --force` to `main`
- ❌ `--no-verify` (skip hooks)
- ❌ commit `.env`, secret, API key, PII
- ❌ direct push to `main` (PR only)

---

## 4. Schema Discipline

### 4.1 Pydantic everywhere ที่ boundary
- All agent input/output = pydantic `BaseModel`
- All Temporal activity input/output = pydantic
- All MCP tool result = pydantic `ToolResult { ok, data, cost_usd, latency_ms, trace_id }`

### 4.2 Schema Evolution
- Additive change OK (new optional field)
- Breaking change = bump version field + adapter shim ≥ 1 release
- Document ใน `docs/si/sdd.md` (Tier 2)

---

## 5. Configuration
- `pydantic-settings` สำหรับ env config
- Secrets ใน Vault / SOPS, **never .env in git**
- Per-env config file: `config/dev.yaml`, `config/staging.yaml`, `config/prod.yaml`
- Override via env var `AUTO_AFFI__<NAMESPACE>__<KEY>`

---

## 6. Documentation
- Public function = docstring (Google style)
- Module top = 1-line purpose docstring
- README ของ subsystem ใน `src/auto_affi/<name>/README.md` ถ้าจำเป็น
- Architecture decision = ADR file ใน `docs/adr/NNNN-title.md` (when needed)

---

## 7. Dependencies
- `pyproject.toml` + `uv` lock file (`uv.lock`)
- Pin major version; allow patch
- Review weekly via Dependabot
- Security advisory subscription on
- ห้าม add dep โดยไม่ approve ใน PR (justify in description)

---

## 8. Security
- Secret scan บน every PR (gitleaks)
- Egress allowlist (no `*.com` glob)
- Input validation ทุก external boundary
- SQL — parameterized only (no f-string SQL)
- Dependency audit weekly

---

## 9. Review Checklist (Reviewer)
- [ ] Linked Linear issue
- [ ] Test added/updated
- [ ] Schema-validated handoff (if cross-boundary)
- [ ] No secret/PII in code or test fixture
- [ ] No `# TODO` without Linear link
- [ ] Logging includes trace_id + cost where applicable
- [ ] Performance — N+1 / unbounded loop check
- [ ] Error path tested
- [ ] If prompt change → eval result attached

---

## 10. Tool Setup (one-liner)
```bash
uv sync
uv run pre-commit install
uv run pytest
```

pre-commit hooks: black, ruff, mypy, gitleaks (fast set only — full set runs in CI)
