# MOSP Software Requirement

chatMOSP **does not include** the MOSP computation engine. It only provides conversational control interfaces (skill documents). You must install the MOSP engine separately to perform calculations.

## Required Components

### MOSP for chatMOSP (Required)

- **Repository**: [mosp-for-chatMOSP](https://github.com/mosp-catalysis/mosp-for-chatMOSP)
- **Function**: Core computation engine (MSR structure generation + KMC kinetic simulation)
- **License**: GNU GPL v3 — same as the original [MOSP](https://github.com/MOSP-catalysis/MOSP)

### chatMOSP (This Repository)

- **Function**: Conversational skill documents for controlling MOSP via natural language
- **License**: GNU GPL v3

## Installation Order

```
1. Install MOSP for chatMOSP (computation capability)
2. Install chatMOSP skills (conversational capability)
3. Restart OpenClaw
```

## MOSP Software Structure

After installing MOSP for chatMOSP, you should have:

```
mosp-for-chatMOSP/
├── engine/               # Computation engine (Windows executables)
│   ├── main.exe          # KMC engine
│   └── *.dll             # Dependencies
├── MOSP_database/        # Parameter database (JSON files)
├── utils/                # Python utility scripts
│   ├── msr.py            # MSR structure generator
│   ├── paint.py          # Visualization (static + rotation GIF)
│   └── plot_kmc_data.py  # KMC result plotting
├── kmc_standalone.py     # KMC entry script
├── requirements.txt      # Python dependencies
└── install.sh            # Installation script
```

## How chatMOSP Skills Call MOSP

```
User command → chatMOSP skill → Parse parameters → Call MOSP engine → Return results
```

Specific execution paths:
1. **MSR calculation**: `python3 mosp-for-chatMOSP/utils/msr.py input.json OUTPUT_DIR/`
2. **KMC simulation**: `python3 mosp-for-chatMOSP/kmc_standalone.py --xyz ... --json ... --out-dir ...`
3. **Visualization**: `python3 mosp-for-chatMOSP/utils/paint.py cluster.xyz --output structure.png`

## FAQ

### Q: Skills installed but MOSP calculations don't run
**Cause**: MOSP for chatMOSP engine not installed.  
**Fix**: Install from [mosp-for-chatMOSP](https://github.com/mosp-catalysis/mosp-for-chatMOSP) first.

### Q: Linux/macOS error "cannot run main.exe"
**Cause**: Wine not installed.  
**Fix**: `sudo apt install wine` (Ubuntu/Debian) or `brew install wine` (macOS).

### Q: Python dependency errors
**Fix**: `pip3 install -r mosp-for-chatMOSP/requirements.txt`

## License

Both chatMOSP and MOSP for chatMOSP are licensed under **GNU GPL v3**, consistent with the original MOSP software by Yi Gao's Group.

## Contact

**Yi Gao's Group** — [https://www.x-mol.com/groups/gao_yi](https://www.x-mol.com/groups/gao_yi)
