---
name: chatmosp-file-organizer
description: |
  File system manager of the chatMOSP system. Handles MSR / RKMC / EKMC task directory
  creation, intelligent naming (format: metal_partial-pressure_TK_PPa_Rsize),
  safe file operations (path traversal protection, whitelist restrictions).
  Triggers: after parameter-builder builds parameters and user confirms, creates task
  directories; or when downstream tasks need subdirectories under parent directories.
---

# chatmosp-file-organizer

## 1. Core Responsibilities

1. **Intelligent task naming**: generate names for MSR / RKMC / EKMC tasks
2. **Standard directory creation**: standard structures for MSR, RKMC, and EKMC
3. **Chain hierarchy management**: three routes — MSR → RKMC, MSR → EKMC, EKMC → RKMC
4. **Safe file operations**: path traversal protection + whitelist restrictions

## 2. Security First

- ✅ Path traversal protection: auto-clean `../`, `//`, `~` and other dangerous chars
- ✅ Whitelist paths: all operations restricted to `mosp-for-chatMOSP/OUTPUT/`
- ✅ TaskNameValidator: validates task name legality, supports new naming format
- ✅ Permission check: ensure appropriate read/write permissions

Blocked patterns: `..`, `//`, `~`, `/root`, `/etc`, `*.exe`, `*.sh`

Allowed chars: `a-zA-Z0-9_-.Å`

Max path length: 512

## 3. Task Naming Rules

### 3.1 MSR Tasks

**Format**: `{metal}_{gas-pp}_{T}K_{P}Pa_R{size}`

**Example**: `Pd_CO9_O18_473K_101325Pa_R50`

| Field | Rule | Default |
|-------|------|---------|
| Metal | Pd, Pt, Au element symbols | Required |
| Gas partial pressure | Multiple gases joined with `_`, pp follows gas (CO9 = CO 9%) | Required |
| Temperature | Value + K | 500 |
| Pressure | Value + Pa | 101325 |
| Size | R + value (Å) | 20 |

### 3.2 RKMC Tasks

> **IMPORTANT**: RKMC task directory is created as a subdirectory under the parent (MSR or EKMC).

**Format**: `RKMC_{steps}steps`

**Example**: `RKMC_5000000steps`

> Temperature/pressure/gas conditions inherit from parent directory. Only annotate when RKMC conditions differ: `RKMC_{T}K_{P}Pa_{pp}_{steps}steps`.

### 3.3 EKMC Tasks

> **IMPORTANT**: EKMC task directory is created as a subdirectory under MSR.

**Format** (same conditions): `EKMC_{steps}steps`

**Example**: `EKMC_1000000steps`

**Format** (different conditions): `EKMC_{T}K_{P}Pa_{pp}_{steps}steps`

**Example**: `EKMC_800K_1000Pa_CO100_2000000steps`

> Temperature/pressure/gas conditions inherit from MSR parent. Only annotate in the subdirectory name when conditions differ.

## 4. Directory Structure

### 4.1 MSR Task Directory

```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/
├── faceinfo.txt            # Facet info
├── ini.xyz                 # Real cluster (input for RKMC/EKMC)
├── {task_name}_cluster.xyz # Structure for plotting
├── rotation.gif            # Rotation animation
├── structure.png           # Structure image
├── input.json              # MSR parameter file
└── metadata.json           # Task metadata
```

### 4.2 RKMC Task Directory (MSR → RKMC direct)

```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/
└── RKMC_{steps}steps/
    ├── input.json          # RKMC params (independent)
    ├── ini.xyz             # Copied from MSR
    ├── coverage.png        # Coverage vs Time
    ├── coverage_steps.png  # Coverage vs Steps
    ├── tof.png             # TOF vs Time
    ├── tof_time.png        # TOF vs Steps
    ├── INPUT/              # Engine auto-fills
    └── OUTPUT/             # Engine auto-outputs
        ├── rec_cov.data
        ├── rec_event.data
        └── rec_site_spc.data
```

### 4.3 EKMC Task Directory (MSR → EKMC)

```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/
└── EKMC_{steps}steps/                    ← EKMC task directory
    ├── input.json                        ← EKMC params (independent)
    ├── ini.xyz                           ← Copied from MSR
    ├── coverage.png
    ├── events.png
    ├── migration.png
    ├── structure_cov.png/.gif + structure_cov_legend.png
    ├── structure_cn.png/.gif  + structure_cn_colorbar.png
    ├── structure_gcn.png/.gif + structure_gcn_colorbar.png
    ├── EKMC-INPUT/                       ← Engine working dir
    └── EKMC-OUTPUT/                      ← Engine raw output
        ├── rec_cov.data
        ├── rec_event.data
        ├── final_stru.xyz                ← Evolved structure (for RKMC)
        └── migration_infos.data
```

### 4.4 EKMC → RKMC Chain Directory (nested)

```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/
└── EKMC_{steps}steps/
    ├── ... (EKMC files, same as above)
    └── RKMC_{steps}steps/                 ← RKMC nested under EKMC
        ├── input.json                    ← RKMC params (independent)
        ├── ini.xyz                       ← Copied from EKMC-OUTPUT/final_stru.xyz
        ├── coverage.png / coverage_steps.png
        ├── tof.png / tof_time.png
        ├── INPUT/
        └── OUTPUT/
```

> ⚠️ **Design principle**: RKMC nested under EKMC = RKMC uses EKMC's evolved structure. Sibling = parallel experiment (no dependency).

## 5. Path Logic (Three Routes)

```
ROUTE 1: MSR → RKMC (reactivity)
  OUTPUT/{msr}/RKMC_{steps}/
  ini.xyz source: MSR's ini.xyz

ROUTE 2: MSR → EKMC (morphology)
  OUTPUT/{msr}/EKMC_{steps}/
  ini.xyz source: MSR's ini.xyz

ROUTE 3: MSR → EKMC → RKMC (evolve then analyze)
  OUTPUT/{msr}/EKMC_{steps}/RKMC_{steps}/
  ini.xyz source: EKMC's EKMC-OUTPUT/final_stru.xyz
```

### 5.1 MSR Task Path

- Location: `mosp-for-chatMOSP/OUTPUT/{msr_task_name}/`
- MSR generates `ini.xyz` and `{task_name}_cluster.xyz`
- Do NOT prepare `ini.xyz` for MSR (MSR generates it)

### 5.2 Condition Inheritance

Subdirectory (RKMC / EKMC) naming follows **condition inheritance**:
- Same T/P/pp as parent → short name (`RKMC_{steps}steps` / `EKMC_{steps}steps`)
- Different conditions → annotate differences in subdirectory name
- Missing context resolved by tracing up to parent directory name

## 6. Visualization Commands (MSR)

```bash
# Static structure image
cd mosp-for-chatMOSP && python3 utils/paint.py \
  OUTPUT/{task_name}/{task_name}_cluster.xyz \
  --output OUTPUT/{task_name}/structure.png

# Rotation animation
cd mosp-for-chatMOSP && python3 utils/paint.py \
  OUTPUT/{task_name}/{task_name}_cluster.xyz \
  --gif OUTPUT/{task_name}/rotation.gif
```

See msr-generator §5 (Step 3: Generate visualization).

## 7. Interface Examples

### Create MSR Directory

**Input**:

```json
{
  "action": "create_msr_directory",
  "parameters": {
    "metal": "Pd",
    "temperature": "473",
    "gases": ["CO", "O2"],
    "partial_pressures": {"CO": 9, "O2": 18},
    "pressure": "101325",
    "radius": "50"
  }
}
```

**Output**:

```json
{
  "success": true,
  "task_type": "MSR",
  "task_name": "Pd_CO9_O18_473K_101325Pa_R50",
  "directory_path": "mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_101325Pa_R50",
  "standard_files": [
    "faceinfo.txt", "ini.xyz", "{task_name}_cluster.xyz",
    "rotation.gif", "structure.png", "input.json", "metadata.json"
  ]
}
```

### Create RKMC Directory

**Input**:

```json
{
  "action": "create_rkmc_directory",
  "parameters": {
    "steps": "5000000",
    "parent_task": "Pd_CO9_O18_473K_101325Pa_R50",
    "parent_type": "MSR"
  }
}
```

**Output**:

```json
{
  "success": true,
  "task_type": "RKMC",
  "task_name": "RKMC_5000000steps",
  "directory_path": "mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_101325Pa_R50/RKMC_5000000steps",
  "required_files": ["input.json", "ini.xyz"],
  "empty_directories": ["INPUT", "OUTPUT"],
  "output_files": ["coverage.png", "coverage_steps.png", "tof.png", "tof_time.png"]
}
```

### Create EKMC Directory

**Input**:

```json
{
  "action": "create_ekmc_directory",
  "parameters": {
    "steps": "1000000",
    "parent_task": "Pd_CO9_O18_473K_101325Pa_R50",
    "temperature_override": null,
    "pressure_override": null
  }
}
```

> Non-null `temperature_override` / `pressure_override` appends condition annotation to subdirectory name.

**Output**:

```json
{
  "success": true,
  "task_type": "EKMC",
  "task_name": "EKMC_1000000steps",
  "directory_path": "mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_101325Pa_R50/EKMC_1000000steps",
  "required_files": ["input.json", "ini.xyz"],
  "empty_directories": ["EKMC-INPUT", "EKMC-OUTPUT"],
  "output_files": ["coverage.png", "events.png", "migration.png", "structure_cov.png", "structure_cn.png", "structure_gcn.png"]
}
```

### Create EKMC → RKMC Chain Directory

**Input**:

```json
{
  "action": "create_rkmc_directory",
  "parameters": {
    "steps": "2000000",
    "parent_task": "Pd_CO9_O18_473K_101325Pa_R50/EKMC_1000000steps",
    "parent_type": "EKMC"
  }
}
```

**Output**:

```json
{
  "success": true,
  "task_type": "RKMC",
  "parent_type": "EKMC",
  "task_name": "RKMC_2000000steps",
  "directory_path": "mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_101325Pa_R50/EKMC_1000000steps/RKMC_2000000steps",
  "ini_source": "EKMC-OUTPUT/final_stru.xyz"
}
```

## 8. Route Summary

| Route | Directory Path | ini.xyz Source |
|-------|---------------|----------------|
| MSR → RKMC | `{msr}/RKMC_{steps}/` | MSR `ini.xyz` |
| MSR → EKMC | `{msr}/EKMC_{steps}/` | MSR `ini.xyz` |
| MSR → EKMC → RKMC | `{msr}/EKMC_{steps}/RKMC_{steps}/` | EKMC `final_stru.xyz` |

## 9. Error Handling

| Error | Action |
|-------|--------|
| Path traversal (../) | Reject, return error |
| Illegal characters in task name | TaskNameValidator rejects |
| Directory exists | Ask before overwriting |
| Insufficient permissions | Prompt user to check |
| Path outside whitelist | Reject |
| Parent directory missing | Prompt to create parent first |
| Nested too deep | Limit to max 2 levels (MSR → EKMC → RKMC) |

## 10. Cross-Skill Handoff

- **parameter-builder → this skill**: create directory after parameter confirmation
- **this skill → msr-generator**: invoke MSR after directory creation
- **this skill → kmc-simulator**: invoke RKMC after directory creation
- **this skill → ekmc-simulator**: invoke EKMC after directory creation
- **ekmc-simulator → this skill**: after EKMC completes, if user wants RKMC, create nested RKMC subdirectory under EKMC

## 11. Dependencies

- **chatmosp-parameter-builder** — get task parameters
- **chatmosp-input-coordinator** — get task type and route
- **chatmosp-msr-generator** — MSR calculation receiver
- **chatmosp-kmc-simulator** — RKMC simulation receiver
- **chatmosp-ekmc-simulator** — EKMC simulation receiver

## 12. File Structure

```
chatmosp-file-organizer/
├── SKILL.md       # Chinese version
└── SKILL_en.md    # This file
```
