# chatMOSP

Conversational control of MOSP catalytic reaction simulations via OpenClaw skills. Make catalytic reaction calculations as simple as chatting!

## Overview

chatMOSP is a collection of seven OpenClaw skills that enable natural-language control of MOSP (Multiscale Operando Simulation Package) calculations. The system follows a **document-driven architecture** — each skill is a pair of Markdown instruction documents (Chinese + English) that guide an AI assistant through parameter construction, structure generation, kinetic simulation (both reaction and environmental), and result visualization.

KMC has been refined into two specialized skills: **chatmosp-kmc-simulator (RKMC)** for reaction kinetics (TOF/coverage), and **chatmosp-ekmc-simulator (EKMC)** for environmental morphology evolution (atom migration/diffusion).

**Key principle**: The AI reads `SKILL.md` documents as operation guides and executes calculations step-by-step using shell commands, file operations, and user interaction. No Python skill code is invoked; all computation is performed by the MOSP engine directly.

## Skills

| Skill | Description |
|-------|-------------|
| **chatmosp-input-coordinator** | Task recognition and routing. Identifies MSR, KMC, or parameter query tasks from user input. |
| **chatmosp-parameter-builder** | Parameter construction with auto-calculation. Builds `input.json` from MOSP_database templates or literature search. Auto-calculates gas entropy and converts interaction parameters. |
| **chatmosp-msr-generator** | Multiscale Structure Reconstruction. Generates equilibrium nanoparticle structures via Wulff construction. |
| **chatmosp-kmc-simulator** | Reaction Kinetic Monte Carlo (RKMC). Simulates surface reaction dynamics and computes TOF, coverage, etc. |
| **chatmosp-ekmc-simulator** | Environmental Kinetic Monte Carlo (EKMC). Simulates cluster morphology evolution under reaction atmosphere via migration/diffusion events. |
| **chatmosp-literature-search** | Literature parameter extraction. Searches academic journals for adsorption energies, interaction parameters, surface energies, and EKMC-specific parameters (E_bond, Ecoh, Ea_diff) when MOSP_database lacks matching data. |
| **chatmosp-file-organizer** | File and directory management. Organizes output files, generates visualizations, and manages MOSP_database. |

## Prerequisites

- **MOSP for chatMOSP** — the computation engine. Install from [mosp-for-chatMOSP](https://github.com/mosp-catalysis/mosp-for-chatMOSP) first.
- **OpenClaw** v0.10.0+ — the AI agent framework.
- **Python 3.8+** with numpy, matplotlib (used by MOSP utilities, not by chatMOSP skills themselves).
- **Linux/macOS**: Wine is required to run the KMC engine (`main.exe`).

## Installation

### Step 1: Install MOSP for chatMOSP

```bash
git clone https://github.com/mosp-catalysis/mosp-for-chatMOSP.git
cd mosp-for-chatMOSP
bash install.sh
```

### Step 2: Install chatMOSP Skills

```bash
git clone https://github.com/mosp-catalysis/chatMOSP.git
cp -r chatMOSP/skills/* ~/.openclaw/workspace/skills/
```

Or use the install script:

```bash
cd chatMOSP && bash install.sh
```

### Step 3: Verify

Restart OpenClaw. You should be able to give natural-language commands like:

- "生成一个Pt55团簇" / "Generate a Pt55 cluster"
- "运行CO氧化KMC模拟" / "Run CO oxidation KMC simulation"

## Workflow

```
User input → chatmosp-input-coordinator (task recognition)
    ├── MSR task → chatmosp-parameter-builder → chatmosp-msr-generator → visualization
    ├── RKMC task → chatmosp-parameter-builder → chatmosp-kmc-simulator → visualization
    ├── EKMC task → chatmosp-parameter-builder → chatmosp-ekmc-simulator → visualization
    └── Query task → chatmosp-parameter-builder (display parameters)

Advanced chain (MSR → EKMC → RKMC):
    MSR → chatmosp-ekmc-simulator (morphology evolution) → chatmosp-kmc-simulator (reactivity analysis)
```

## Key Features

- **Gas entropy auto-calculation**: `S(eV/K) = (a × T^b) / 96485` for 7 gases (H₂, N₂, O₂, CO₂, CO, NO, H₂O)
- **Interaction parameter conversion**: Automatic detection and conversion between MSR (per-atom) and KMC (per-bond) formats
- **Bilingual support**: Chinese and English skill documents; AI responds in the user's language
- **Literature search**: When MOSP_database lacks parameters, searches open-access journals via browser tool
- **Mandatory user confirmation**: All parameters must be confirmed before computation begins

## Directory Structure

```
chatMOSP/
├── README.md                       # This file
├── LICENSE                         # GNU GPL v3
├── MOSP-SOFTWARE-REQUIREMENT.md    # MOSP engine dependency details
├── install.sh                      # Installation script
├── .gitignore
└── skills/
    ├── chatmosp-file-organizer/
    │   ├── SKILL.md               # Chinese skill document
    │   └── SKILL_en.md            # English skill document
    ├── chatmosp-input-coordinator/
    ├── chatmosp-kmc-simulator/
    ├── chatmosp-ekmc-simulator/
    ├── chatmosp-literature-search/
    ├── chatmosp-msr-generator/
    └── chatmosp-parameter-builder/
```

## Version Notes

This `EKMC-test` branch adds **chatmosp-ekmc-simulator** (7th skill) and refines KMC into RKMC (reaction) and EKMC (environmental). The `main` branch retains the original 6-skill structure.

## Citation

If you use this software in academic work, please cite:

Ying L, Zhu B,* Gao Y,* "MOSP: A user-interface package for simulating metal nanoparticle's structure and reactivity under operando conditions." *J. Chem. Phys.* **2024**, *161*, 114702. [DOI: 10.1063/5.0226023](https://doi.org/10.1063/5.0226023)

## License

This project is licensed under the **GNU General Public License v3.0** — see the [LICENSE](LICENSE) file for details.

Both chatMOSP skills and the MOSP computation engine use GPL v3, consistent with the original [MOSP](https://github.com/MOSP-catalysis/MOSP) license.

## Contact

**Yi Gao's Group** — [https://www.x-mol.com/groups/gao_yi](https://www.x-mol.com/groups/gao_yi)

## Related Repository

- **[mosp-for-chatMOSP](https://github.com/mosp-catalysis/mosp-for-chatMOSP)** — The MOSP computation engine with MSR/KMC capabilities, parameter database, and visualization utilities.
