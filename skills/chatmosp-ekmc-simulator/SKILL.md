---
name: chatmosp-ekmc-simulator
description: |
  chatMOSP 系统的 EKMC(环境动力学蒙特卡洛)模拟引擎,模拟团簇在反应气氛中的
  形貌演化。调用 generate_ekmc_input.py 一键式流程:读 JSON → 生成 EKMC 输入 →
  通过 Wine 运行 EKMC-main.exe → 用 utils/postprocess_ekmc.py 产出覆盖度图、
  事件统计、迁移分析及结构图/旋转动图。EKMC 需要初始结构(如 MSR 生成的团簇)。
  触发场景:parameter-builder 完成 EKMC 参数构建并经用户确认后由本技能执行。
---

# chatmosp-ekmc-simulator (EKMC)

> Skill created by Sanyang Ye (https://github.com/sanyangye)

> **术语**: 本技能即 **EKMC**(Environmental KMC,环境动力学蒙特卡洛)。模拟团簇在反应气氛中的
> **动态形貌**(原子迁移/形貌演化)。相关概念:
> - **MSR** — 模拟团簇在反应气氛中的**平衡形貌**(静态,无需初始结构)。
> - **RKMC** — 模拟团簇在反应气氛中的**反应活性**(见 `chatmosp-kmc-simulator`,需初始结构)。
> - **EKMC** — 模拟团簇在反应气氛中的**动态形貌**(本技能,需初始结构,如 MSR 团簇)。

## 0. ⚠️ MANDATORY: Output Language Rule

The output language (including internal thinking, tool-call descriptions, all user-facing text, generated file content, and cross-skill handoff notes) MUST mirror the language of the user's most recent message.

**Detection rule**: CJK characters in user's last message → `user_lang = zh`. Otherwise → `en`.

**Read `OUTPUT/{task_name}/context.json` for `user_lang`** before producing any output. If `user_lang == "zh"`, also read `SKILL_cn.md` of this skill for Chinese terminology and phrasing.

**Failure modes prohibited**: Do NOT mix languages. The single source of truth is the user's last message script.

> Full rule: see `input-coordinator` §0.

## 1. Core Responsibilities

1. Check and manage Wine environment (EKMC engine dependency)
2. Check Python dependencies (numpy, pandas, matplotlib, scipy, imageio — for plotting)
3. Prepare EKMC input via the one-stop script (copy template from MOSP_database + user-specified T/P/pp/steps)
4. Run the EKMC engine (`EKMC-main.exe` via Wine) and monitor progress
5. Warn on large step counts
6. Generate coverage / event / migration plots and structure images / rotation GIFs
   (large opaque atoms; continuous coloring ships a standalone colorbar)
7. Regenerate plots on demand if results are unsatisfactory

## 2. Prerequisites

- ✅ Initial structure available (EKMC requires it, e.g. MSR-generated `ini.xyz`)
- ✅ `parameter-builder` has built EKMC parameters (the JSON `EKMC` section)
- ✅ User has confirmed via the 5-option prompt
- ✅ Wine installed (check on first run) — see §3
- ✅ Python deps installed (numpy, pandas, matplotlib, scipy, imageio) — see §3.4
- ✅ `user_lang` written to `context.json` by `input-coordinator`
- ❌ DO NOT bypass `parameter-builder`
- ❌ DO NOT reuse the MSR/RKMC `input.json` — EKMC uses its own `EKMC` section

## 3. Environment Checks (Wine + Python)

> Run BOTH §3.1 (Wine) and §3.4 (Python) before any execution. Prompts follow `user_lang`.

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

### 3.3 Automatic Wine check

- ✅ Installed → proceed
- ⚠️ Missing → prompt install (in `user_lang`)
- ❌ Incompatible → prompt upgrade

### 3.4 Python Dependency Check (MANDATORY, for plotting)

> **Why**: After EKMC completes, `utils/postprocess_ekmc.py` reads the EKMC output and produces coverage/event/migration plots plus structure images and rotation GIFs. Structure GIFs need `imageio`; the structure CN/GCN computation and KDTree neighbor logic rely on `scipy`. Missing packages crash the post-run plotting even though the simulation ran fine.

```bash
python3 -c "import numpy, pandas, matplotlib, scipy, imageio; print('OK')" 2>/dev/null
RC=$?

if [ $RC -ne 0 ]; then
  echo "❌ Python dependencies missing for postprocess_ekmc.py"
  echo "Diagnostic: which python3?"
  which python3
  echo "Fix (PEP 668 systems, e.g. Ubuntu 23.04+, Debian 12+):"
  echo "  cd mosp-for-chatMOSP"
  echo "  python3 -m venv venv && source venv/bin/activate"
  echo "  pip install -r requirements.txt"
  echo "Fix (older systems):"
  echo "  cd mosp-for-chatMOSP && pip install -r requirements.txt"
  exit 1
fi
```

**If the check fails, STOP. Do NOT proceed to §7.** Output the diagnostic in `user_lang`.

Required packages: `numpy`, `pandas`, `matplotlib`, `scipy`, `imageio` (all in `mosp-for-chatMOSP/requirements.txt`).

## 4. Step-Count Warning

When EKMC steps (`nLoop`) are large, warn the user before execution (cost grows with step count and grid size). Use `user_lang`. (Reference scale is similar to RKMC: tens of millions of steps can take many hours.)

```
⚠️ Calculation Time Warning:
Current EKMC steps (nLoop): {N} on a {dim_x}×{dim_y}×{dim_z} grid.
Large step counts / grids take significant time. Continue?
```

## 5. Input Contract (Required fields in the EKMC JSON)

> Reference template: `mosp-for-chatMOSP/MOSP_database/*-EKMC*.json` (e.g. `Pt-CO-EKMC-test.json`).

### Top-level fields

| Field | Type | Description |
|-------|------|-------------|
| Element | string | Metal element |
| Lattice constant | string | Lattice constant (Å) |
| Crystal structure | string | FCC / BCC / HCP |
| Temperature | string | Temperature (K) |
| Pressure | string | Pressure (Pa) |
| EKMC | object | EKMC parameter object |

### EKMC object required fields

| Field | Type | Description |
|-------|------|-------------|
| dim_x / dim_y / dim_z | string | Lattice grid dimensions (cluster size proxy) |
| nLoop | string | Simulation steps |
| record_int | string | Recording interval |
| E_bond | string | Bond energy |
| Ecoh_U0 | string | Cohesive energy base term |
| Ecoh_A1 / Ecoh_t1 | string | Cohesive energy exponential term 1 |
| Ecoh_A2 / Ecoh_t2 | string | Cohesive energy exponential term 2 |
| nspecies | number | Number of species |
| nevents | number | Number of events |
| nevents_mob | number | Number of mobility events |
| s1 ... sN | string | Species definitions (JSON string; includes name/mass/PP_ratio/S_gas/S_ads/sticking/E_ads_para/Ea_diff/is_twosite) |
| e1 ... eM | string | Event definitions (JSON string; type ∈ Adsorption/Desorption/Diffusion, cov_before/cov_after, is_twosite) |
| li | array | Lattice interaction matrix |

> **Difference from RKMC**: RKMC uses the `KMC` section (reaction events with products → reactivity). EKMC uses the `EKMC` section (adsorption/desorption/diffusion → morphology evolution). EKMC has no `products`; it has cohesive-energy terms and per-species diffusion barriers.

## 6. Directory Structure

EKMC task directory naming follows `file-organizer`, using the short-name convention under the MSR parent:

**Format** (same conditions as MSR): `EKMC_{steps}steps`

**Format** (different conditions): `EKMC_{T}K_{P}Pa_{pp}_{steps}steps`

**Example**: `EKMC_10000steps`

EKMC task directory must be under the MSR directory (if started from an MSR cluster).
For EKMC → RKMC chains, RKMC nests under the EKMC directory:

```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/
├── EKMC_{steps}steps/                              ← EKMC task directory (same cond)
│   ├── input.json                                   ← EKMC params (the EKMC section)
│   ├── ini.xyz                                      ← initial structure (from MSR)
│   ├── run.log                                      ← engine log
│   ├── coverage.png                                 ← coverage vs time
│   ├── events.png                                   ← event statistics
│   ├── migration.png                                ← migration analysis (Ea/dE/CN/GCN)
│   ├── structure_cov.png/.gif  + structure_cov_legend.png
│   ├── structure_cn.png/.gif   + structure_cn_colorbar.png
│   ├── structure_gcn.png/.gif  + structure_gcn_colorbar.png
│   ├── EKMC-INPUT/                                  ← engine working dir
│   ├── EKMC-OUTPUT/                                 ← engine raw output
│   │   ├── rec_cov.data / rec_event.data
│   │   ├── final_stru.xyz                           ← evolved structure (for RKMC)
│   │   └── migration_infos.data
│   └── RKMC_{steps}steps/                           ← EKMC → RKMC chain (nested)
│       ├── input.json                               ← RKMC params (independent)
│       ├── ini.xyz                                  ← copied from EKMC-OUTPUT/final_stru.xyz
│       ├── coverage.png / coverage_steps.png
│       ├── tof.png / tof_time.png
│       ├── INPUT/
│       └── OUTPUT/
└── RKMC_{steps}steps/                               ← MSR → RKMC direct (sibling)
    ├── input.json                                   ← RKMC params (independent)
    ├── ini.xyz                                      ← copied from MSR ini.xyz
    ├── coverage.png / coverage_steps.png
    ├── tof.png / tof_time.png
    ├── INPUT/
    └── OUTPUT/
```

> ⚠️ **IMPORTANT**:
> - `EKMC-main.exe` reads `EKMC-INPUT` and writes `EKMC-OUTPUT` (relative paths). The one-stop script sets the engine cwd to `--out-dir` and creates these subdirectories there.
> - Structure images / GIFs do NOT embed a colorbar; continuous coloring (cov/cn/gcn) ships a separate `*_colorbar.png` so one colorbar can be shown alongside many structures.
> - All EKMC figure titles include metal / temperature / pressure / partial pressure / cluster grid size / EKMC steps.
> - `ini.xyz` and `input.json` are also placed at the task root for user visibility (matching RKMC convention).

## 7. Execution Steps (one-stop script)

### 7.1 Step 1: Create EKMC task directory

```bash
# Same conditions as MSR → short name:
mkdir -p OUTPUT/Pt_CO9_O18_473K_101325Pa_R50/EKMC_10000steps

# Different conditions → annotated name:
mkdir -p OUTPUT/Pt_CO9_O18_473K_101325Pa_R50/EKMC_800K_1000Pa_CO100_2000000steps
```

### 7.2 Step 2: Provide the initial structure (required)

```bash
cp OUTPUT/{msr_task_name}/ini.xyz \
   OUTPUT/{msr_task_name}/{ekmc_task_name}/ini.xyz

# Example:
cp OUTPUT/Pt_CO9_O18_473K_101325Pa_R50/ini.xyz \
   OUTPUT/Pt_CO9_O18_473K_101325Pa_R50/EKMC_10000steps/ini.xyz
```

### 7.3 Step 3: Prepare input.json

```bash
# Copy an EKMC template from MOSP_database (do not create manually)
cp mosp-for-chatMOSP/MOSP_database/{metal}-{reaction}-EKMC*.json \
   OUTPUT/{msr_task_name}/{ekmc_task_name}/input.json
# Adjust: Temperature, Pressure, EKMC.nLoop, EKMC.record_int,
#         per-species PP_ratio / S_gas, grid dims dim_x/dim_y/dim_z
```

### 7.4 Step 4: Show parameters for user confirmation

Use `parameter-builder` EKMC parameter display format (5 options).

### 7.5 Step 5: Check Wine + step warning (§3.1, §4)

### 7.6 Step 6: Run the one-stop EKMC pipeline

`generate_ekmc_input.py` does: read JSON → generate input → run `EKMC-main.exe` via Wine → plot. `--out-dir` is the run directory; the script creates `EKMC-INPUT` and `EKMC-OUTPUT` under it and sets the engine cwd there. Images are written to the task root.

```bash
python3 mosp-for-chatMOSP/generate_ekmc_input.py \
  --json   OUTPUT/{msr_task_name}/{ekmc_task_name}/input.json \
  --out-dir OUTPUT/{msr_task_name}/{ekmc_task_name} \
  --xyz    OUTPUT/{msr_task_name}/{ekmc_task_name}/ini.xyz
```

> Image titles are auto-composed from the JSON (metal / T / P / partial pressure / grid size / steps-EKMC).

## 8. Output Files

| File | Location | Description |
|------|----------|-------------|
| coverage.png | task dir | Surface coverage vs time |
| events.png | task dir | Event counts & final statistics |
| migration.png | task dir | Migration barrier / energy / CN / GCN analysis |
| structure_cov.png / .gif (+ _legend.png) | task dir | Structure colored by coverage (grey=bare, red=covered) + standalone legend |
| structure_cn.png / .gif (+ _colorbar.png) | task dir | Structure colored by CN + standalone colorbar |
| structure_gcn.png / .gif (+ _colorbar.png) | task dir | Structure colored by GCN + standalone colorbar |
| rec_cov.data / rec_event.data | EKMC-OUTPUT/ | Engine raw records |
| final_stru.xyz | EKMC-OUTPUT/ | Final evolved structure (ele/x/y/z/cov/cn/gcn) |
| migration_infos.data | EKMC-OUTPUT/ | Per-migration records |
| run.log | task dir | Engine log |

> EKMC outputs describe **morphology evolution** (final structure, migration). For reactivity (TOF), use RKMC (`chatmosp-kmc-simulator`).

## 9. Output Check & Regenerate Plots

After EKMC completes (especially when user asks "is the task done?"), check data files and regenerate plots if missing or unsatisfactory:

```bash
EKMC_OUTPUT="{ekmc_task_dir}/EKMC-OUTPUT"

if [ ! -f "$EKMC_OUTPUT/rec_cov.data" ] || \
   [ ! -f "$EKMC_OUTPUT/rec_event.data" ] || \
   [ ! -f "$EKMC_OUTPUT/final_stru.xyz" ]; then
  echo "❌ EKMC output files missing; the simulation may not have completed."
  exit 1
fi

# Replot only (no re-run). Pass the same title info for consistent figure titles.
python3 mosp-for-chatMOSP/utils/postprocess_ekmc.py "$EKMC_OUTPUT" \
  --title "Pt CO100% 800K 1000Pa grid50x50x50 10000steps-EKMC"
```

> The replot module `utils/postprocess_ekmc.py` is plot-only; use `--img-dir` to direct images to task root. The full pipeline is `generate_ekmc_input.py`.

## 10. Error Handling

> Prompts follow `user_lang` from `context.json`.

| Error | Action |
|-------|--------|
| Wine missing | Prompt install (see §3) |
| `wine` not found at run time | Engine cannot run; install Wine |
| Python `ImportError` (numpy/pandas/matplotlib/scipy/imageio) | See §3.4; fix before proceeding |
| Missing `EKMC` section in JSON | Copy a complete EKMC template from MOSP_database |
| ini.xyz missing | EKMC requires an initial structure; copy from MSR |
| `EKMC-main.exe` non-zero exit | Check `run.log`; verify input files and Wine version |
| Output files missing after run | Engine did not complete; inspect `run.log` |
| Structure GIF skipped | `imageio` not installed (see §3.4) |
| Garbage atoms in final_stru.xyz | EKMC engine uninitialized-memory bug; not harmful to results | postprocess_ekmc filters them automatically; use grid dimensions ≥ 3× cluster radius to avoid |

## 11. Cross-Skill Handoff

- **MSR → EKMC**: MSR produces `ini.xyz` (initial structure). EKMC consumes it for morphology evolution.
- **EKMC → RKMC**: EKMC produces `final_stru.xyz` (evolved structure) in `EKMC-OUTPUT/`. Copy it as `ini.xyz` for RKMC's initial structure. Supports the "EKMC first for morphology evolution, then RKMC for reactivity analysis" chain workflow.
- **EKMC vs RKMC**: both need an MSR initial structure. EKMC → morphology (structure images/GIFs/migration); RKMC → reactivity (TOF/coverage). Route via `input-coordinator` per user intent.
- **Parameter building**: `parameter-builder` builds the `EKMC` section; if temperature changes, recalculate gas entropy consistently with MSR/RKMC.
- **Directory naming**: `file-organizer` creates the `EKMC_{steps}steps` task directory under MSR.
- **`user_lang` from `context.json`**: all user-facing messages follow it (see §0).

## 12. Dependencies

- **mosp-for-chatMOSP** — EKMC engine (`engine/EKMC-main.exe`) + `generate_ekmc_input.py` + `utils/postprocess_ekmc.py`
- **chatmosp-parameter-builder** — EKMC parameter building
- **chatmosp-file-organizer** — `EKMC_{steps}steps` directory creation
- **chatmosp-input-coordinator** — task entry point and `user_lang`
- **chatmosp-kmc-simulator** — sibling skill for reactivity (RKMC)
- **Wine** — required for `EKMC-main.exe`
- **Python packages** — `numpy`, `pandas`, `matplotlib`, `scipy`, `imageio`

## 13. File Structure

```
chatmosp-ekmc-simulator/
├── SKILL.md       # This file (English, loaded by OpenClaw)
└── SKILL_cn.md    # Chinese output reference (read on demand, see §0)
```

## 14. Example

> Output language follows `user_lang`. For Chinese example see `SKILL_cn.md` §14.

```
User: Run EKMC for the Pt cluster under CO at 800K, 1000Pa, 10000 steps

System: [Recognize as EKMC (morphology evolution) → parameter-builder builds EKMC section →
        Show 5-option confirmation → User confirms →
        Environment checks: Wine OK (§3.1) + Python OK (§3.4) →
        Create EKMC_10000steps dir → copy MSR ini.xyz → prepare input.json →
        Run generate_ekmc_input.py (--json/--out-dir/--xyz) →
        Engine runs via Wine → plots generated (coverage/events/migration +
        structure_cov/cn/gcn .png/.gif with standalone colorbars,
        titles include metal/T/P/pp/grid/steps-EKMC) → Display results (in user_lang)]

---

User: Run EKMC first to evolve cluster shape, then RKMC for reactivity

System: [Recognize as EKMC → RKMC chain workflow →
        Run ekmc-simulator first for morphology evolution →
        EKMC produces final_stru.xyz in EKMC-OUTPUT/ →
        Copy final_stru.xyz as ini.xyz for RKMC →
        Switch to kmc-simulator for reactivity → Display TOF/coverage results]
```
