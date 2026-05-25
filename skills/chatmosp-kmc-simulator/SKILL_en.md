# Skill: chatmosp-kmc-simulator (Bilingual Version)

## 🌐 语言匹配规则 / Language Matching Rules

**重要提示 / IMPORTANT**: 根据用户输入的语言，选择合适的SKILL.md版本并匹配输出语言。
**IMPORTANT**: Based on the language of user input, select the appropriate SKILL.md version and match the output language.

### 语言匹配流程 / Language Matching Process

1. **用户输入中文 / User inputs Chinese**:
   - 阅读SKILL.md（中文版）/ Read SKILL.md (Chinese version)
   - 使用中文输出回复 / Output response in Chinese

2. **用户输入英文 / User inputs English**:
   - 阅读SKILL_en.md（双语对照版）/ Read SKILL_en.md (Bilingual version)
   - 使用英文输出回复 / Output response in English

### 语言识别标准 / Language Recognition Standard

- 如果用户输入中包含中文字符，则识别为中文输入
- If user input contains Chinese characters, recognize as Chinese input
- 否则识别为英文输入
- Otherwise recognize as English input

---

## 📖 术语定义 / Terminology Definitions

**MOSP (Multiscale Operando Simulation Package)** - Multiscale Operando simulation package
- Multiscale simulation system for metal catalyst surface reactions
- Integrates structure generation and kinetic simulation

**MSR (Multiscale Structure Reconstruction)** - Multiscale Structure Reconstruction model
- Metal cluster structure generation based on Wulff construction
- Calculate equilibrium morphology with different crystal face ratios

**KMC (Kinetic Monte Carlo)** - Kinetic Monte Carlo model
- Simulate kinetic processes of surface reactions
- Calculate kinetic parameters such as TOF and coverage

---

## 📋 技能概览 / Overview

**技能名称 / Skill Name**: `chatmosp-kmc-simulator`  
**技能类型 / Skill Type**: KMC Computation Engine  
**核心职责 / Core Responsibility**: Kinetic Monte Carlo Simulation  

### 技能定位 / Skill Positioning
KMC模拟器是ChatMOSP系统的动力学计算引擎，负责：  
The KMC simulator is the kinetic calculation engine of the ChatMOSP system, responsible for:

1. **KMC模拟执行 / KMC Simulation Execution**: 执行催化剂表面反应动力学模拟  
   Execute catalyst surface reaction kinetics simulation
2. **资源保护机制 / Resource Protection Mechanism**: 4000万步警告和自动资源保护  
   40 million steps warning and automatic resource protection
3. **长时间运行管理 / Long-running Process Management**: 进度监控和检查点恢复  
   Progress monitoring and checkpoint recovery
4. **结果分析与可视化 / Result Analysis and Visualization**: 提取TOF、覆盖度、反应路径  
   Extract TOF, coverage, reaction paths

### 核心安全特性 / Core Security Features
- ⚠️ **4000万步警告 / 40 Million Steps Warning**: 当KMC步数超过4000万时发出警告  
  Warn when KMC steps exceed 40 million
- ✅ **资源保护 / Resource Protection**: 自动监控内存和CPU使用  
  Automatically monitor memory and CPU usage
- 🔄 **检查点机制 / Checkpoint Mechanism**: 定期保存进度，支持中断恢复  
  Periodically save progress, support interruption recovery
- 📊 **进度报告 / Progress Reporting**: 实时监控模拟进度  
  Real-time monitoring of simulation progress

## 🎯 核心功能 / Core Functions

### 1. KMC模拟执行 / KMC Simulation Execution
- 调用 mosp-for-chatMOSP KMC引擎 / Call mosp-for-chatMOSP KMC engine
- 准备KMC输入文件（KMC-input.json）/ Prepare KMC input file (KMC-input.json)
- 管理长时间运行的计算 / Manage long-running computations
- 捕获动力学数据 / Capture kinetic data

### 2. 资源保护与警告 / Resource Protection and Warnings
```
步数监控 → 超过阈值警告 → 用户确认 → 继续执行
Step monitoring → Threshold warning → User confirmation → Continue execution
                      ↓
                  用户取消 → 保存检查点 → 安全停止
                 User cancel → Save checkpoint → Safe stop
```

### 3. 进度监控与报告 / Progress Monitoring and Reporting
- 实时显示模拟进度 / Real-time display of simulation progress
- 预估剩余时间 / Estimate remaining time
- 自动生成进度报告 / Automatically generate progress reports
- 检查点保存和恢复 / Checkpoint saving and recovery

### 4. 结果处理与分析 / Result Processing and Analysis
- 解析TOF（周转频率）数据 / Parse TOF (Turnover Frequency) data
- 提取表面覆盖度信息 / Extract surface coverage information
- 生成反应路径分析 / Generate reaction path analysis
- 创建可视化图表（覆盖度图等）/ Create visual charts (coverage graphs, etc.)

---

## 🚀 快速开始：KMC计算正确流程 / Quick Start: KMC Calculation Correct Process

### 前提条件 / Prerequisites:
- MSR任务已完成，生成了ini.xyz结构文件 / MSR task completed, ini.xyz structure file generated
- input.json包含完整的KMC参数 / input.json contains complete KMC parameters

### 步骤1：准备KMC任务目录 / Step 1: Prepare KMC Task Directory
```bash
# 命名规则：{MSR任务名}_KMC{步数}/ / Naming rule: {MSR_task_name}_KMC{steps}/
mkdir -p OUTPUT/Pd_CO9_O18_473K_101325Pa_R50_KMC2000/INPUT
mkdir -p OUTPUT/Pd_CO9_O18_473K_101325Pa_R50_KMC2000/OUTPUT
```

### 步骤2：准备输入文件 / Step 2: Prepare Input Files
```bash
# 复制结构文件 / Copy structure file
cp OUTPUT/Pd_CO9_O18_473K_101325Pa_R50/ini.xyz OUTPUT/Pd_CO9_O18_473K_101325Pa_R50_KMC2000/

# 准备input.json（从MOSP_database复制并修改）
# Prepare input.json (copy from MOSP_database and modify)
# 必需字段 / Required fields: nspecies, nproducts, nevents, s1, s2, p1, e1-e7, li
```

### 步骤3：KMC参数交互确认 / Step 3: KMC Parameter Interactive Confirmation
（详见下方"🔄 KMC参数交互确认流程"部分）
/ (See "🔄 KMC Parameter Interactive Confirmation Process" section below)

### 步骤4：展示参数给用户确认 / Step 4: Show Parameters for User Confirmation
（详见下方"🔄 KMC参数交互确认流程"部分）
/ (See "🔄 KMC Parameter Interactive Confirmation Process" section below)

### 步骤5：运行KMC / Step 5: Run KMC
```bash
# KMC运行指令（注意：输出目录不需要添加OUTPUT前缀）
# KMC run command (Note: output directory does not need OUTPUT prefix)
python3 ../../kmc_standalone.py \
  --xyz OUTPUT/{任务目录名}/ini.xyz \
  --json OUTPUT/{任务目录名}/input.json \
  --out-dir {任务目录名}

# 说明：kmc_standalone.py会自动添加OUTPUT前缀
# Note: kmc_standalone.py will automatically add OUTPUT prefix
# 例如 / Example: --out-dir Pt_CO60_O40_800K_500Pa_R20_KMC2000
# 实际输出 / Actual output: OUTPUT/Pt_CO60_O40_800K_500Pa_R20_KMC2000/OUTPUT/
```

### 步骤6：检查KMC输出并重新绘制图像 / Step 6: Check KMC Output and Regenerate Plots

**应用场景 / Application Scenario**：
- 用户提交了较长时间的KMC任务 / User submitted a long KMC task
- 询问agent任务是否结束 / Asking agent if task has ended
- agent检查发现任务结束 / Agent checks and finds task has ended
- 检查KMC任务目录是否存在coverage.png和tof.png / Check if coverage.png and tof.png exist in KMC task directory
- 如果不存在，运行绘图脚本重新生成 / If not exist, run plotting script to regenerate

**检查时机 / Check Timing**：KMC运行结束后 / After KMC run completes

**检查内容 / Check Content**：
1. 检查OUTPUT文件夹是否存在rec_cov.data、rec_event.data、rec_site_spc.data文件 / Check if rec_cov.data, rec_event.data, rec_site_spc.data files exist in OUTPUT folder
2. 比较预期步数和实际运行步数是否一致 / Compare expected steps with actual run steps
3. 检查KMC任务目录是否存在coverage.png和tof.png / Check if coverage.png and tof.png exist in KMC task directory
4. 如果图像不存在，运行绘图脚本重新生成 / If plots don't exist, run plotting script to regenerate

**文件位置说明 / File Location Description**：
- 数据文件位置 / Data file location：KMC任务目录/OUTPUT/（rec_cov.data、rec_event.data、rec_site_spc.data）
- 图像文件位置 / Plot file location：KMC任务目录/（coverage.png、tof.png）

**检查与绘图命令 / Check and Plot Commands**：
```bash
# 定义KMC任务目录 / Define KMC task directory
KMC_TASK_DIR="KMC任务目录"
KMC_OUTPUT="$KMC_TASK_DIR/OUTPUT"

# 检查数据文件是否存在 / Check if data files exist
if [ ! -f "$KMC_OUTPUT/rec_cov.data" ] || [ ! -f "$KMC_OUTPUT/rec_event.data" ] || [ ! -f "$KMC_OUTPUT/rec_site_spc.data" ]; then
  echo "❌ KMC数据文件不存在，KMC模拟可能未开始或未成功完成"
  echo "❌ KMC data files not found, KMC simulation may not have started or completed successfully"
  exit 1
fi

# 检查KMC是否成功结束：比较预期步数和实际运行步数
# Check if KMC completed successfully: compare expected steps with actual run steps
EXPECTED_STEPS=$(grep -E "^[0-9]+\s+! Num of steps" "$KMC_TASK_DIR/INPUT/input.txt" | awk '{print $1}')
ACTUAL_STEPS=$(tail -n 1 "$KMC_OUTPUT/rec_event.data" | awk '{print $2}')

if [ "$EXPECTED_STEPS" != "$ACTUAL_STEPS" ]; then
  echo "❌ KMC模拟未成功完成 / KMC simulation did not complete successfully"
  echo "  预期步数 / Expected steps: $EXPECTED_STEPS"
  echo "  实际运行步数 / Actual steps: $ACTUAL_STEPS"
  echo "请检查KMC运行日志，确认错误原因 / Please check KMC run log to identify the error"
  exit 1
fi

echo "✅ KMC已成功完成（步数 / Steps：$ACTUAL_STEPS）"

# 检查图像文件是否存在 / Check if plot files exist
if [ -f "$KMC_TASK_DIR/coverage.png" ] && [ -f "$KMC_TASK_DIR/tof.png" ]; then
  echo "✅ KMC输出图像已存在 / KMC output plots already exist"
  echo "  Coverage plot: $KMC_TASK_DIR/coverage.png"
  echo "  TOF plot: $KMC_TASK_DIR/tof.png"
else
  echo "⚠️ KMC输出图像不存在，正在重新生成... / KMC output plots not found, regenerating..."
  
  # 运行绘图脚本 / Run plotting script
  python3 ../../utils/plot_kmc_data.py "$KMC_OUTPUT"
  
  echo "✅ 图像已重新生成 / Plots regenerated successfully"
  echo "  Coverage plot: $KMC_TASK_DIR/coverage.png"
  echo "  TOF plot: $KMC_TASK_DIR/tof.png"
fi
```

**绘图脚本说明 / Plotting Script Description**：
- 脚本位置 / Script location：mosp-for-chatMOSP/utils/plot_kmc_data.py
- 功能 / Function：读取rec_cov.data、rec_event.data、rec_site_spc.data文件，生成图像和CSV文件 / Read rec_cov.data, rec_event.data, rec_site_spc.data files, generate plots and CSV files
- 图像保存位置 / Plot save location：KMC任务目录（与kmc_standalone.py一致）/ KMC task directory (consistent with kmc_standalone.py)
- CSV文件保存位置 / CSV save location：KMC任务目录/OUTPUT/

**生成的文件 / Generated Files**：
- coverage.png - 覆盖率随时间变化的图像（保存在KMC任务目录）/ Coverage evolution over time (saved in KMC task directory)
- tof.png - TOF随时间变化的图像（保存在KMC任务目录）/ TOF evolution over time (saved in KMC task directory)
- coverage.csv - 覆盖率数据（保存在OUTPUT目录）/ Coverage data (saved in OUTPUT directory)
- tof.csv - TOF数据（保存在OUTPUT目录）/ TOF data (saved in OUTPUT directory)
- site_tof.csv - 位点TOF数据（保存在OUTPUT目录）/ Site TOF data (saved in OUTPUT directory)

**注意事项 / Notes**：
- 无需重新运行KMC模拟 / No need to re-run KMC simulation
- 绘图脚本会自动识别反应事件（如CO+O）/ Plotting script automatically identifies reaction events (e.g., CO+O)
- 如果数据文件不存在，说明KMC模拟未成功完成，需要检查运行日志 / If data files don't exist, KMC simulation did not complete successfully, need to check run log

**常见问题 / FAQ**：
- Q: 为什么图像在KMC任务目录，而不是OUTPUT目录？/ Why are plots in KMC task directory, not OUTPUT directory?
- A: 这是kmc_standalone.py的设计，图像保存在KMC任务目录，数据文件保存在OUTPUT目录 / This is kmc_standalone.py design, plots saved in KMC task directory, data files saved in OUTPUT directory

- Q: 如果KMC模拟未成功完成怎么办？/ What if KMC simulation did not complete successfully?
- A: 检查KMC运行日志，确认错误原因，修复后重新运行KMC / Check KMC run log, identify error, fix and re-run KMC

---

## ⚠️ KMC执行前检查清单 / KMC Pre-Execution Checklist

在运行KMC之前，**必须**确认以下项目全部完成：
Before running KMC, **must** confirm all the following items are completed:

### 📁 目录结构检查 / Directory Structure Check
- [ ] KMC任务目录已创建 / KMC task directory created
- [ ] INPUT/文件夹已创建 / INPUT/ folder created
- [ ] OUTPUT/文件夹已创建 / OUTPUT/ folder created
- [ ] ini.xyz文件已复制到KMC任务目录 / ini.xyz file copied to KMC task directory
- [ ] input.json文件已创建在KMC任务目录（不是INPUT/下）/ input.json file created in KMC task directory (not under INPUT/)

### 📄 input.json必需字段检查 / input.json Required Fields Check

**顶层必需字段 / Top-level Required Fields:**
- [ ] Element（金属元素 / Metal element）
- [ ] Lattice constant（晶格常数 / Lattice constant）
- [ ] Crystal structure（晶体结构 / Crystal structure）
- [ ] Temperature（温度 / Temperature）
- [ ] Pressure（压力 / Pressure）
- [ ] flag_MSR: false
- [ ] flag_KMC: true
- [ ] KMC（KMC参数对象 / KMC parameter object）

**KMC部分必需字段 / KMC Section Required Fields:**
- [ ] nLoop（模拟步数 / Simulation steps）
- [ ] nspecies（物种数量 / Number of species）
- [ ] nproducts（产物数量 / Number of products）
- [ ] nevents（反应事件数 / Number of reaction events）
- [ ] s1, s2（物种定义 / Species definitions）
- [ ] p1（产物定义 / Product definition）
- [ ] e1-e7（反应事件定义 / Reaction event definitions）
- [ ] li（晶格相互作用矩阵 / Lattice interaction matrix）

### ✅ 检查命令 / Check Commands
```bash
# 检查目录结构 / Check directory structure
ls -la KMC任务目录/

# 检查input.json顶层字段 / Check input.json top-level fields
cat KMC任务目录/input.json | jq 'keys'

# 检查KMC部分字段 / Check KMC section fields
cat KMC任务目录/input.json | jq '.KMC | keys'
```

### ⚠️ 常见错误及解决方案 / Common Errors and Solutions

| 错误信息 / Error Message | 原因 / Cause | 解决方案 / Solution |
|---------|------|----------|
| `missing top-level field 'Lattice constant'` | input.json缺少必需的顶层字段 / input.json missing required top-level field | 从MOSP_database复制完整模板，不要手动创建 / Copy complete template from MOSP_database, do not create manually |
| `INPUT/ or OUTPUT/ directory not found` | 缺少INPUT/OUTPUT文件夹 / Missing INPUT/OUTPUT folders | 执行步骤1创建文件夹 / Execute step 1 to create folders |
| `ini.xyz not found` | ini.xyz文件不存在或位置错误 / ini.xyz file does not exist or in wrong location | 从MSR任务目录复制ini.xyz到KMC任务目录 / Copy ini.xyz from MSR task directory to KMC task directory |

---

### KMC参数来源 / KMC Parameter Sources:
1. **从MOSP_database复制 / Copy from MOSP_database**:
   - `MOSP_database/Pd-COoxidation.json`
   - `MOSP_database/Pt-COoxidation.json`

2. **根据用户输入调整 / Adjust based on user input**:
   - nLoop: 用户指定的步数 / User-specified steps
   - T: 温度 / Temperature
   - 其他参数从example继承 / Other parameters inherited from example

3. **不使用MSR的input.json / Do not use MSR's input.json**:
   - MSR参数不完整，缺少KMC必需字段 / MSR parameters incomplete, missing required KMC fields
   - KMC需要独立的完整参数配置 / KMC requires independent complete parameter configuration

---

## 🔄 KMC参数交互确认流程 / KMC Parameter Interactive Confirmation Process

### 流程 / Process:
```
用户请求KMC → 准备完整参数 → 展示参数模板 → 用户确认 → 运行KMC
User requests KMC → Prepare complete parameters → Show parameter template → User confirmation → Run KMC
```

### 参数展示模板 / Parameter Display Template:

```markdown
📊 KMC参数已准备好，请确认： / KMC parameters are ready, please confirm:

【基本信息 / Basic Information】
- 任务类型 / Task Type: KMC (动力学蒙特卡洛模拟 / Kinetic Monte Carlo Simulation)
- 反应 / Reaction: CO氧化反应 (2CO + O2 → 2CO2) / CO oxidation reaction
- 温度 / Temperature: 473 K (200°C)
- 压力 / Pressure: 101325 Pa (1 atm)
- 气体分压 / Gas Partial Pressure: CO 9%, O2 18%

【团簇信息 / Cluster Information】(来自MSR结果 / From MSR results)
- 金属元素 / Metal Element: Pd
- 团簇半径 / Cluster Radius: 50 Å
- 原子数量 / Number of Atoms: 3,888 个 / atoms
- 晶体结构 / Crystal Structure: FCC (面心立方 / Face-centered cubic)
- MSR任务目录 / MSR Task Directory: Pd_CO9_O18_473K_101325Pa_R50

【模拟参数 / Simulation Parameters】
- 模拟步数 / Simulation Steps: 5,000,000 步 / steps
- 记录间隔 / Record Interval: 每10,000步记录一次 / Record every 10,000 steps
- 物种数量 / Number of Species: 5 种 / types
- 反应事件 / Reaction Events: 14 种 / types

【物种定义 / Species Definition】
- s1: CO (反应物 / Reactant)
- s2: O2 (反应物 / Reactant)
- s3: O (中间体 / Intermediate)
- s4: CO2 (产物 / Product)
- s5: 空位 / Vacancy

【产物定义 / Product Definition】
- p1: CO2 (事件X, Y生成 / Generated by event X, Y)

【反应机制 / Reaction Mechanism】(简要说明 / Brief description)
- CO吸附、脱附、扩散 / CO adsorption, desorption, diffusion
- O2解离、扩散 / O2 dissociation, diffusion
- CO + O → CO2

【输出设置 / Output Settings】
- KMC任务目录 / KMC Task Directory: Pd_CO9_O18_473K_101325Pa_R50/KMC_5000000steps/
- 生成文件 / Generated Files: input.json, 输出文件等 / output files, etc.

请选择 / Please select:
1. ✅ 确认 - 使用这些参数继续执行KMC模拟 / Confirm - Use these parameters to continue KMC simulation
2. ✏️ 修改 - 调整模拟步数或其他参数(如温度、压强、气体组成等) / Modify - Adjust simulation steps or other parameters (e.g., temperature, pressure, gas composition)
3. 📊 对比 - 运行多个条件进行对比(如多个温度、压强) / Compare - Run multiple conditions for comparison (e.g., multiple temperatures, pressures)
4. 🔄 切换计算模式 - 切换到MSR结构计算 / Switch calculation mode - Switch to MSR structure calculation
5. ❌ 取消任务，更换体系 - 更换金属或气体体系 / Cancel task, change system - Change metal or gas system

建议 / Suggestions:
- 如果想快速测试，可以先运行较少步数(如100,000步) / For quick testing, run fewer steps first (e.g., 100,000 steps)
- 500万步可以获得更准确的统计数据，但耗时更长 / 5 million steps yield more accurate statistics but take longer

请回复您的选择(数字1-5或关键词)，或告诉我要修改的参数。 / Please reply with your choice (number 1-5 or keyword), or tell me the parameters to modify.
```
## 🔧 技术实现 / Technical Implementation

### ⚠️ 系统要求 / System Requirements
KMC计算需要Wine环境运行Windows版`mine.exe`引擎：
KMC calculation requires Wine environment to run Windows version `mine.exe` engine:

```bash
# 检查Wine是否已安装 / Check if Wine is installed
which wine

# 如果未安装，请安装：/ If not installed, please install:
sudo apt-get update
sudo apt-get install wine
```

### 自动环境检查 / Automatic Environment Check
系统会自动检查Wine环境：
The system will automatically check the Wine environment:
- ✅ 如果Wine已安装：正常执行KMC计算 / If Wine is installed: Execute KMC calculation normally
- ⚠️ 如果Wine未安装：提示安装指导 / If Wine is not installed: Prompt installation instructions
- ❌ 如果Wine版本不兼容：提示升级 / If Wine version is incompatible: Prompt upgrade

### 依赖关系 / Dependencies
- `mosp-for-chatMOSP` - 核心计算引擎（已克隆）/ Core computation engine (already cloned)
- `chatmosp-file-organizer` - 文件路径管理 / File path management
- `chatmosp-parameter-builder` - 参数验证 / Parameter validation
- **Wine环境 / Wine Environment** - 运行Windows版`mine.exe`（必需）/ Run Windows version `mine.exe` (required)

### 执行流程 / Execution Flow
```
接收参数 → 验证参数 → 准备输入 → 检查Wine环境 → 
Receive params → Validate params → Prepare input → Check Wine environment →
Wine可用 → 执行KMC → 监控进度 → 检查资源 → 收集结果 → 分析数据
Wine available → Execute KMC → Monitor progress → Check resources → Collect results → Analyze data
       ↓
   Wine不可用 → 提示安装指导 → 中止计算
   Wine unavailable → Prompt installation instructions → Abort calculation
       ↓
    4000万步警告 → 用户交互 → 继续/停止
    40M steps warning → User interaction → Continue/Stop
```

## 📝 使用示例 / Usage Examples

### English Usage
```python
from skill_updated import ChatMOSPKMCSimulatorBilingual

simulator = ChatMOSPKMCSimulatorBilingual()

# Execute KMC simulation for Pt at 500K
result = simulator.execute({
    "action": "execute_kmc_simulation",
    "parameters": {
        "Element": "Pt",
        "Temperature": "500",
        "KMC": {
            "nLoop": "1000000",
            "record_int": "1000",
            "temperature": "500",
            "pressure": "101325"
        },
        "task_directory": "mosp-for-chatMOSP/OUTPUT/Pt_500K_12345"
    }
})

if result["success"]:
    print(f"✅ Simulation ID: {result.get('simulation_id', '')}")
    print(f"📊 Estimated duration: {result.get('estimated_duration', 0):.1f}s")
else:
    print(f"❌ Error: {result.get('error', '')}")
```

### Chinese Usage / 中文使用示例
```python
from skill_updated import ChatMOSPKMCSimulatorBilingual

simulator = ChatMOSPKMCSimulatorBilingual()

# 为Pt在500K下执行KMC模拟
result = simulator.execute({
    "action": "execute_kmc_simulation",
    "parameters": {
        "Element": "Pt",
        "Temperature": "500",
        "KMC": {
            "nLoop": "1000000",
            "record_int": "1000",
            "temperature": "500",
            "pressure": "101325"
        },
        "task_directory": "mosp-for-chatMOSP/OUTPUT/Pt_500K_12345"
    }
})

if result["success"]:
    print(f"✅ 模拟ID: {result.get('simulation_id', '')}")
    print(f"📊 预计持续时间: {result.get('estimated_duration', 0):.1f}秒")
else:
    print(f"❌ 错误: {result.get('error', '')}")
```

### Warning Example / 警告示例
```python
# When steps exceed 40 million, warning is issued
result = simulator.execute({
    "action": "execute_kmc_simulation",
    "parameters": {
        "Element": "Pd",
        "Temperature": "600",
        "KMC": {
            "nLoop": "50000000",  # 50 million steps - exceeds warning threshold
            "record_int": "1000"
        }
    }
})

if result.get("warning_issued", False):
    print(f"⚠️ WARNING: {result.get('warning_message', '')}")
    print(f"Steps: {result.get('step_count', 0):,}")
    print(f"Threshold: {result.get('threshold', 0):,}")
    # User confirmation required before proceeding
```

## 🌐 语言支持 / Language Support

### 支持的操作语言 / Supported Action Languages
- **中文关键词**: 执行, 验证, 检查, 估计, 状态, 停止
- **英文关键词**: execute, validate, check, estimate, status, stop

### 配置语言 / Configuration Languages
- **config.json**: 中文配置，包含4000万步警告等安全配置
- **config_en.json**: 英文配置，包含双语警告信息和资源保护设置

### 重要功能双语支持 / Key Feature Bilingual Support
1. **40 Million Steps Warning / 4000万步警告**: 双语警告信息
2. **Resource Monitoring / 资源监控**: 内存/CPU使用监控和警告
3. **Progress Reporting / 进度报告**: 实时进度更新（双语）
4. **Error Messages / 错误信息**: 双语错误提示和故障排除

## 🔧 配置选项 / Configuration Options

### config.json (中文配置)
```json
{
  "skill": {
    "name": "chatmosp-kmc-simulator",
    "version": "1.0.0",
    "description": "ChatMOSP KMC模拟器（动力学蒙特卡洛模拟）"
  },
  "computation": {
    "max_steps": 100000000,
    "warning_threshold_steps": 40000000
  }
}
```

### config_en.json (英文配置)
```json
{
  "skill": {
    "name": "chatmosp-kmc-simulator",
    "version": "1.0.0",
    "description": "ChatMOSP KMC Simulator (Kinetic Monte Carlo Simulation)"
  },
  "computation": {
    "max_steps": 100000000,
    "warning_threshold_steps": 40000000
  },
  "warning_messages": {
    "en": {
      "step_threshold_warning": "WARNING: KMC step count exceeds {threshold} steps..."
    }
  }
}
```

### 主要配置参数 / Main Configuration Parameters
- `computation.warning_threshold_steps`: 警告阈值步数（默认4000万）
- `computation.timeout_hours`: 超时时间（默认24小时）
- `resources.memory_warning_threshold_mb`: 内存警告阈值（默认4096MB）
- `results.generate_plots`: 是否生成图表（默认true）

## 🚀 快速开始 / Quick Start

### 1. 初始化技能 / Initialize Skill
```python
from skill_updated import ChatMOSPKMCSimulatorBilingual

# Automatically detect language / 自动检测语言
simulator = ChatMOSPKMCSimulatorBilingual()
print(f"Language: {simulator.language}")
print(f"Skill Name: {simulator.skill_name}")
print(f"Warning Threshold: {simulator.config['computation']['warning_threshold_steps']:,} steps")
```

### 2. 验证参数 / Validate Parameters
```python
# English input validation
result_en = simulator.execute({
    "action": "validate_parameters",
    "parameters": {
        "Element": "Pd",
        "Temperature": "550",
        "KMC": {"nLoop": "5000000", "record_int": "1000"}
    }
})

# Chinese input validation / 中文输入验证
result_zh = simulator.execute({
    "action": "validate_parameters",
    "parameters": {
        "Element": "铂",
        "Temperature": "550",
        "KMC": {"nLoop": "5000000", "record_int": "1000"}
    }
})

if result_en["success"] and result_en["valid"]:
    print("✅ English parameters validated")
if result_zh["success"] and result_zh["valid"]:
    print("✅ 中文参数验证通过")
```

### 3. 检查警告 / Check Warnings
```python
# Check for any warnings based on parameters
result = simulator.execute({
    "action": "check_warnings",
    "parameters": {
        "nLoop": "45000000"  # 45 million steps
    }
})

if result["success"] and result["step_warning"]:
    print("⚠️ Step count warning would be triggered for this simulation")
```

### 4. 执行模拟 / Execute Simulation
```python
# Start KMC simulation
result = simulator.execute({
    "action": "execute_kmc_simulation",
    "parameters": {
        "Element": "Co",
        "Temperature": "400",
        "KMC": {
            "nLoop": "1000000",
            "record_int": "1000",
            "temperature": "400",
            "pressure": "101325"
        },
        "task_directory": "mosp-for-chatMOSP/OUTPUT/Co_400K_101325Pa"
    }
})

if result["success"]:
    print(f"✅ Simulation started: {result.get('simulation_id', '')}")
    print(f"⏱️ Estimated: {result.get('estimated_duration', 0):.1f} seconds")
    
    # Check status
    status = simulator.execute({"action": "get_status"})
    print(f"📊 Status: {status.get('message', '')}")
```

## 🔧 故障排除 / Troubleshooting

### 常见问题 / Common Issues

#### Q: 4000万步警告如何工作？  
**A**: 当KMC步数超过4000万时，系统会发出警告并要求用户确认。  
**A**: When KMC steps exceed 40 million, system issues warning and requires user confirmation.

#### Q: 如何停止长时间运行的模拟？  
**A**: 使用"stop_simulation"操作，系统会保存检查点后安全停止。  
**A**: Use "stop_simulation" action, system saves checkpoint before safe stop.

#### Q: 资源监控包含哪些内容？  
**A**: 内存使用、CPU使用率、磁盘空间，超过阈值会发出警告。  
**A**: Memory usage, CPU utilization, disk space, warnings when thresholds exceeded.

#### Q: 如何切换语言？  
**A**: 系统根据输入自动检测，也可在代码中设置language属性。  
**A**: System automatically detects based on input, can also set language property in code.

#### Q: 模拟失败时会发生什么？  
**A**: 系统会记录错误信息，保存日志，并提供恢复建议。  
**A**: System logs error, saves logs, and provides recovery suggestions.

### 调试模式 / Debug Mode
```python
# Enable detailed logging for debugging
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Test with step count that triggers warning
simulator = ChatMOSPKMCSimulatorBilingual()
test_result = simulator.execute({
    "action": "check_warnings",
    "parameters": {"nLoop": "45000000"}
})
print(f"Warning check: {test_result}")
```

---
*Last Updated: 2026-04-27*  
*Version: 1.0.0*  
*Language Support: zh_CN, en_US*  
*Key Feature: 40 million steps warning mechanism*