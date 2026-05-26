# chatMOSP

Conversational control of MOSP catalytic reaction simulations via OpenClaw skills. Make catalytic reaction calculations as simple as chatting!

## Overview

chatMOSP is a collection of six OpenClaw skills that enable natural-language control of MOSP (Multiscale Operando Simulation Package) calculations. The system follows a **document-driven architecture** — each skill is a pair of Markdown instruction documents (Chinese + English) that guide an AI assistant through parameter construction, structure generation, kinetic simulation, and result visualization.

**Key principle**: The AI reads `SKILL.md` documents as operation guides and executes calculations step-by-step using shell commands, file operations, and user interaction. No Python skill code is invoked; all computation is performed by the MOSP engine directly.

## Skills

| Skill | Description |
|-------|-------------|
| **chatmosp-input-coordinator** | Task recognition and routing. Identifies MSR, KMC, or parameter query tasks from user input. |
| **chatmosp-parameter-builder** | Parameter construction with auto-calculation. Builds `input.json` from MOSP_database templates or literature search. Auto-calculates gas entropy and converts interaction parameters. |
| **chatmosp-msr-generator** | Multiscale Structure Reconstruction. Generates equilibrium nanoparticle structures via Wulff construction. |
| **chatmosp-kmc-simulator** | Kinetic Monte Carlo simulation. Simulates surface reaction dynamics and computes TOF, coverage, etc. |
| **chatmosp-literature-search** | Literature parameter extraction. Searches academic journals for adsorption energies, interaction parameters, and surface energies when MOSP_database lacks matching data. |
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

See the [mosp-for-chatMOSP repository](https://github.com/mosp-catalysis/mosp-for-chatMOSP) for detailed instructions.

### Step 2: Install chatMOSP Skills

```bash
# Clone this repository
git clone https://github.com/mosp-catalysis/chatMOSP.git

# Copy skills to your OpenClaw workspace
cp -r chatMOSP/skills/* ~/.openclaw/workspace/skills/
```

Or use the install script:

```bash
cd chatMOSP
bash install.sh
```

### Step 3: Verify

Restart OpenClaw or wait for skills to auto-load. You should be able to give natural-language commands like:

- "生成一个Pt55团簇" / "Generate a Pt55 cluster"
- "运行CO氧化KMC模拟" / "Run CO oxidation KMC simulation"

## Workflow

```
User input → chatmosp-input-coordinator (task recognition)
    ├── MSR task → chatmosp-parameter-builder → chatmosp-msr-generator → visualization
    ├── KMC task → chatmosp-parameter-builder → chatmosp-kmc-simulator → visualization
    └── Query task → chatmosp-parameter-builder (display parameters)
```

### MSR Example

1. User: "生成Pd团簇在CO氧化环境下"
2. Input-coordinator identifies MSR task
3. Parameter-builder finds `Pd-COoxidation.json` in MOSP_database, auto-calculates gas entropy
4. Parameters displayed for user confirmation
5. MSR generates equilibrium structure
6. Visualization (structure.png + rotation.gif) presented to user

### KMC Example

1. User: "Run KMC simulation for Pt CO oxidation, 20M steps"
2. Input-coordinator identifies KMC task
3. Parameter-builder loads parameters, user confirms
4. KMC simulation runs (20M steps ≈ 12 hours)
5. Results plotted: coverage vs time, TOF vs steps

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
├── LICENSE                         # MIT License
├── MOSP-SOFTWARE-REQUIREMENT.md    # MOSP engine dependency details
├── install.sh                      # Installation script
├── .gitignore
└── skills/
    ├── chatmosp-file-organizer/
    │   ├── SKILL.md               # Chinese skill document
    │   └── SKILL_en.md            # English skill document
    ├── chatmosp-input-coordinator/
    ├── chatmosp-kmc-simulator/
    ├── chatmosp-literature-search/
    ├── chatmosp-msr-generator/
    └── chatmosp-parameter-builder/
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

The MOSP computation engine has a separate academic license. See the [mosp-for-chatMOSP](https://github.com/mosp-catalysis/mosp-for-chatMOSP) repository for details.

## Related Repository

- **[mosp-for-chatMOSP](https://github.com/mosp-catalysis/mosp-for-chatMOSP)** — The MOSP computation engine with MSR/KMC capabilities, parameter database, and visualization utilities.
