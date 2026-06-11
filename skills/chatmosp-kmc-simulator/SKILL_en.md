---
name: chatmosp-kmc-simulator
description: |
  RKMC (Reaction Kinetic Monte Carlo) simulation engine of the chatMOSP system. Invokes
  kmc_standalone.py via Wine to run the Windows main.exe engine, executes
  catalyst surface reaction kinetic simulations, and produces TOF / coverage
  results. Uses utils/plot_kmc_data.py to generate coverage.png, coverage_steps.png,
  tof.png, and tof_time.png (4 images total).
  Triggers: after parameter-builder has built RKMC parameters and the user has
  confirmed via the 5-option prompt, this skill executes the RKMC simulation.
---

# chatmosp-kmc-simulator (RKMC — Reaction Kinetic Monte Carlo)

> Skill created by Sanyang Ye (https://github.com/sanyangye)

> **Terminology**: This skill is **RKMC** (Reaction KMC). It simulates catalyst
> surface reaction **kinetics** (TOF / coverage / reactivity). Related concepts:
> - **MSR** — simulates cluster **equilibrium morphology** under reaction atmosphere (static, no initial structure needed, produces ini.xyz).
> - **RKMC** — simulates cluster **reactivity** under reaction atmosphere (this skill, requires initial structure, focuses on TOF / coverage).
> - **EKMC** — simulates cluster **dynamic morphology** (see `chatmosp-ekmc-simulator`, focuses on morphology evolution / atom migration).
>
> ⚠️ **Directory name unchanged**: the skill directory stays `chatmosp-kmc-simulator`; internally we use the concept RKMC.
> Code / JSON fields / filenames keep `KMC`; only docs distinguish RKMC/EKMC.

## 1. Core Responsibilities

1. Check and manage Wine environment (RKMC engine dependency)
2. Prepare RKMC input files (copy template from MOSP_database + user-specified steps/T/pp)
3. Execute RKMC simulation and monitor progress
4. Warn on large step counts (≥ 20M steps)
5. Generate TOF / coverage plots and CSV data
6. Auto-regenerate plots if missing or on user request

## 2. Prerequisites

- ✅ Initial structure available (MSR-generated `ini.xyz`, or EKMC-evolved `final_stru.xyz`)
- ✅ parameter-builder has built RKMC parameters
- ✅ User has confirmed via the 5-option prompt (see parameter-builder §RKMC display format)
- ✅ Wine environment installed (check on first run, prompt install if missing)
- ✅ Structure file copied to RKMC task directory (if applicable)
- ❌ DO NOT bypass parameter-builder and build RKMC parameters manually
- ❌ DO NOT reuse MSR/EKMC's `input.json` — RKMC must independently prepare complete parameters

## 3. Wine Environment

The RKMC engine is the Windows `main.exe`, requiring Wine to run.

### 3.1 Check Wine

```bash
which wine64 || which wine
```

### 3.2 Install Wine (Ubuntu/Debian)

```bash
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install wine64 wine32
```

### 3.3 Automatic environment check

- ✅ Wine installed → proceed normally
- ⚠️ Wine missing → prompt install instructions
- ❌ Version incompatible → prompt upgrade

## 4. Step-Count Warning

When RKMC steps ≥ 20M, MUST warn user before execution:

```
⚠️ Calculation Time Warning:
Current RKMC steps: {N}, estimated time: ~{estimated_hours} hours.
(Reference: 20M steps ≈ 12 hours, 40M steps ≈ 24+ hours)
Continue with RKMC simulation?
```

| Steps | Estimated time |
|-------|----------------|
| 20M | ~12 hours |
| 40M | ~24 hours or longer |
| More | Linear growth |

> Note: Running multiple conditions multiplies total time.

## 5. Input Contract (Required fields in input.json)

### Top-level fields

| Field | Type | Description |
|-------|------|-------------|
| Element | string | Metal element (Pd, Pt, Au, etc.) |
| Lattice constant | string | Lattice constant (Å) |
| Crystal structure | string | Crystal structure (FCC, BCC, HCP) |
| Temperature | string | Temperature (K) |
| Pressure | string | Pressure (Pa) |
| flag_MSR | boolean | MUST be `false` |
| flag_KMC | boolean | MUST be `true` |
| KMC | object | KMC parameter object |

### KMC object required fields

| Field | Type | Description |
|-------|------|-------------|
| nLoop | string | Simulation steps |
| record_int | string | Recording interval |
| nspecies | number | Number of species |
| nproducts | number | Number of products |
| nevents | number | Number of reaction events |
| nevents_mob | number | Number of mobility events |
| s1 / s2 | string | Species 1/2 definitions (JSON string) |
| p1 | string | Product 1 definition (JSON string) |
| e1 ~ e7 | string | Reaction events 1~7 (JSON string) |
| li | array | Lattice interaction matrix |

> ⚠️ **CRITICAL**: Gas entropy `s1.S_gas` / `s2.S_gas` MUST match MSR's `Gas1_S` / `Gas2_S` (use same formula).

## 6. Directory Structure

RKMC task directory must be under MSR (or EKMC) directory:

```
mosp-for-chatMOSP/OUTPUT/{source_task_name}/
└── RKMC_{steps}steps/             ← RKMC task directory
    ├── input.json                ← outside INPUT/
    ├── ini.xyz                   ← copied from MSR (or EKMC final_stru.xyz)
    ├── coverage.png              ← generated after run
    ├── coverage_steps.png        ← generated after run
    ├── tof.png                   ← generated after run
    ├── tof_time.png              ← generated after run
    ├── INPUT/                    ← should be empty before run
    └── OUTPUT/                   ← populated after run
        ├── rec_cov.data
        ├── rec_event.data
        └── rec_site_spc.data
```

> ⚠️ **Note**:
> - `ini.xyz` and `input.json` MUST be outside `INPUT/` (`kmc_standalone.py` clears `INPUT/OUTPUT`)
> - Ensure `INPUT/` and `OUTPUT/` are empty before running
> - If RKMC starts from EKMC instead of MSR, `{source_task_name}` is the EKMC task directory name; copy `final_stru.xyz` and rename to `ini.xyz`

## 7. Execution Steps

### Step 1: Create RKMC task directory

```bash
mkdir -p OUTPUT/{source_task_name}/RKMC_{steps}steps/INPUT
mkdir -p OUTPUT/{source_task_name}/RKMC_{steps}steps/OUTPUT
```

### Step 2: Copy structure file

```bash
# From MSR:
cp OUTPUT/{msr_task_name}/ini.xyz OUTPUT/{msr_task_name}/RKMC_{steps}steps/ini.xyz

# Or from EKMC (evolved structure):
cp OUTPUT/{ekmc_task_dir}/EKMC-OUTPUT/final_stru.xyz \
   OUTPUT/{ekmc_task_dir}/RKMC_{steps}steps/ini.xyz
```

### Step 3: Prepare input.json

```bash
# Copy template from MOSP_database (do not create manually)
cp mosp-for-chatMOSP/MOSP_database/{metal}-{reaction}.json \
   OUTPUT/{source_task_name}/RKMC_{steps}steps/input.json

# Adjust fields:
# - nLoop: user-specified steps
# - T: user-specified temperature
# - gas_pp: user-specified partial pressures
# - record_int: recording interval
# - s1.S_gas / s2.S_gas: recalculated using parameter-builder §8.1 formula
```

### Step 4: Show parameters for user confirmation

Use parameter-builder §RKMC parameter display format (5 options).

### Step 5: Check Wine + step warning

- Check Wine environment
- Warn when steps ≥ 20M

### Step 6: Execute RKMC

```bash
python3 ../../kmc_standalone.py \
  --xyz OUTPUT/{task_dir}/ini.xyz \
  --json OUTPUT/{task_dir}/input.json \
  --out-dir {task_dir}
```

> Note: pass just the task directory name to `--out-dir` (e.g.
> `{source_task_name}/RKMC_{steps}steps`). The script automatically places it under
> `OUTPUT/`; even if an `OUTPUT/` prefix is accidentally included it is de-duplicated.

## 8. Output Files

| File | Location | Description |
|------|----------|-------------|
| coverage.png | RKMC task dir | Coverage vs Time |
| coverage_steps.png | RKMC task dir | Coverage vs Steps |
| tof.png | RKMC task dir | TOF vs Time |
| tof_time.png | RKMC task dir | TOF vs Steps |
| coverage.csv | OUTPUT/ | Coverage data |
| tof.csv | OUTPUT/ | TOF data |
| site_tof.csv | OUTPUT/ | Site TOF data |
| rec_cov.data | OUTPUT/ | Coverage records (engine raw) |
| rec_event.data | OUTPUT/ | Event records |
| rec_site_spc.data | OUTPUT/ | Site-species records |

### 8.1 Sending Images to User (Feishu)

> ⚠️ **One image per call**: Feishu message tool only supports 1 image per attachment.
> More than one will silently drop. After RKMC completes, MUST send the 4 images
> one at a time with numbered labels.

Send order:

1. Image 1/4: Coverage vs Time — `coverage.png`
2. Image 2/4: Coverage vs Steps — `coverage_steps.png`
3. Image 3/4: TOF vs Time — `tof.png`
4. Image 4/4: TOF vs Steps — `tof_time.png`

Example per message:
```
message(action=send, message="Image 1/4: Coverage vs Time",
         attachments=[{filePath:"...coverage.png", type:"image"}])
```

## 9. Output Check & Auto-Regenerate

After RKMC completes (especially when user asks "is the task done?"), MUST check and regenerate if needed:

```bash
RKMC_TASK_DIR="RKMC task directory"
RKMC_OUTPUT="$RKMC_TASK_DIR/OUTPUT"

# 1. Check data files
if [ ! -f "$RKMC_OUTPUT/rec_cov.data" ] || \
   [ ! -f "$RKMC_OUTPUT/rec_event.data" ] || \
   [ ! -f "$RKMC_OUTPUT/rec_site_spc.data" ]; then
  echo "❌ Data files missing, RKMC may not have completed"
  exit 1
fi

# 2. Check step-count consistency
EXPECTED=$(grep -E "^[0-9]+\s+! Num of steps" "$RKMC_TASK_DIR/INPUT/input.txt" | awk '{print $1}')
ACTUAL=$(tail -n 1 "$RKMC_OUTPUT/rec_event.data" | awk '{print $2}')

if [ "$EXPECTED" != "$ACTUAL" ]; then
  echo "❌ Expected $EXPECTED steps, got $ACTUAL, RKMC did not complete"
  exit 1
fi

# 3. Check plots (4 images), regenerate if missing
if [ -f "$RKMC_TASK_DIR/coverage.png" ] && \
   [ -f "$RKMC_TASK_DIR/coverage_steps.png" ] && \
   [ -f "$RKMC_TASK_DIR/tof.png" ] && \
   [ -f "$RKMC_TASK_DIR/tof_time.png" ]; then
  echo "✅ Plots already exist"
else
  python3 ../../utils/plot_kmc_data.py "$RKMC_OUTPUT"
  echo "✅ Plots regenerated"
fi
```

> Plotting script: `mosp-for-chatMOSP/utils/plot_kmc_data.py`

## 10. Error Handling

| Error | Action |
|-------|--------|
| Step-count mismatch | Check RKMC log; may not have finished |
| Data files missing | RKMC did not complete; check `run.log` |
| Lattice constant missing | Copy complete template from MOSP_database; do not create manually |
| INPUT/OUTPUT dir missing | Create them in Step 1 |
| ini.xyz missing | Copy from MSR or EKMC task directory |
| final_stru.xyz missing (from EKMC) | Confirm EKMC completed successfully first |
| Wine missing | Prompt install instructions |
| RKMC segfault | Wine version incompatible; prompt upgrade |

## 11. Cross-Skill Handoff

- **MSR → RKMC**: After MSR completes, `ini.xyz` is produced. This skill independently fetches complete RKMC parameters from MOSP_database. Do NOT reuse MSR's `input.json`.
- **EKMC → RKMC**: After EKMC completes, `final_stru.xyz` (evolved structure) is produced. Copy it as `ini.xyz` for RKMC's initial structure. Supports the "EKMC first for morphology evolution, then RKMC for reactivity analysis" workflow.
- **Parameter modification**: If user changes temperature, parameter-builder MUST recalculate gas entropy.
- **Long-task query**: When user asks "is the task done?", run §9 check script, regenerate plots if needed.

## 12. Dependencies

- **mosp-for-chatMOSP** — KMC engine (cloned, includes main.exe)
- **chatmosp-parameter-builder** — parameter building and gas entropy
- **chatmosp-file-organizer** — directory creation
- **chatmosp-input-coordinator** — task entry point
- **chatmosp-ekmc-simulator** — EKMC (provides evolved initial structure)
- **Wine** — required for Windows main.exe

## 13. File Structure

```
chatmosp-kmc-simulator/
├── SKILL.md       # Chinese version
└── SKILL_en.md    # This file
```

## 14. Example

```
User: Run RKMC simulation for Pt CO oxidation at 850K, 150Pa, 20M steps

System: [Recognize as RKMC → parameter-builder searches params →
        Show 5-option confirmation → User confirms → Check Wine installed →
        ⚠️ 20M steps ≈ 12 hours, warn user → User confirms again →
        Prepare input.json → Invoke kmc_standalone.py → Monitor progress →
        Check output → Generate 4 images → Send one-by-one → Display results]

---

User: Run EKMC first to evolve cluster morphology, then RKMC for reactivity

System: [Recognize as EKMC → RKMC chain workflow →
        Run ekmc-simulator first for morphology evolution →
        EKMC produces final_stru.xyz → Copy as ini.xyz →
        Run this skill for RKMC (reactivity) → Display TOF/coverage results]
```
