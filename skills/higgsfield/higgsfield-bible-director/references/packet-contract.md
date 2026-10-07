# Local production packet

`production_packet.py` has no provider client and no network calls. It prepares and checks structure, dependency IDs, declared used claims, recorded budgets/attempt caps, and local delivery-file/report existence. It never returns `generation_allowed`, never authorizes expenditure, and never replaces the Auto-Affi generation preflight.

`init` creates a new directory exclusively and refuses an existing directory. It writes a draft `production-plan.json` and copies reusable CSV templates. Empty fields are deliberate inputs, not completed work.

## JSON contract

- `schema_version`: 1; `run_id`: nonempty; `mode`: cinematic/vfx/brand/faceless/game/agency/auto-affi.
- `brief`: nonempty objective and deliverable.
- `facts`: objects with unique `id`, `claim`, and status verified/pending/outdated. A declared verified fact needs source, verified_by, checked_at (ISO date). Independent verification remains the agent's responsibility.
- `assets`: unique id, role, source and version. Local source paths resolve against run directory and must exist; HTTP URLs are recorded without fetching. Observational role and uncertainty belong in optional fields.
- `shots`: unique id, purpose, prompt, start_state, end_state, acceptance, reference_ids and claim_ids lists. IDs must exist; used claims must be declared verified. Unused pending facts do not fail a plan. Media modes require at least one shot. Game and agency planning may use empty shots.
- `budget`: optional max_cost, required nonnegative spent_cost; when a ceiling exists, currency and every next-call estimated_cost are required. The check compares spent plus all next-call estimates to ceiling. Values are in one currency/unit. Optional max_attempts_per_shot is a positive integer; a shot at its cap needs a new decision before another call. Do not include old completed shots as next calls; preserve historical ledger separately.
- `review`: delivery files, report file, blockers, checks. Delivery requires local files, no blockers and resolved dimensions with declared evidence or NA rationale. Media: story/visual/audio/delivery. Game: gameplay/input/performance/delivery. Agency: facts/scope/economics/delivery.

Each review check is `{ "dimension": "visual", "status": "pass", "evidence": "reviewer + file + interval + method" }`. Status issue/not_inspectable fails delivery. An irrelevant dimension can be na with a reason; missing evidence cannot be na simply to obtain pass. Manual declarations are not machine media validation.

```bash
python3 scripts/production_packet.py init --run-dir /absolute/new-run --mode cinematic
python3 scripts/production_packet.py check --run-dir /absolute/run --stage plan --write-report
python3 scripts/production_packet.py check --run-dir /absolute/run --stage delivery --write-report
```

Exit 0 = structurally passed; 1 = identified issues; 2 = invalid input/read failure. Reports preserve limitations. This helper does not create storyboard approvals, read credentials, generate media, or check the current provider model. Keep the existing execution adapter's authorization, model and preflight rules.
