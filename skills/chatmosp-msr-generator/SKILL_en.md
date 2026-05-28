# Skill: chatmosp-msr-generator (Bilingual Version)

## 🌐 语言匹配规则 / Language Matching Rules

**重要提示 / IMPORTANT**: 根据用户输入的语言,选择合适的SKILL.md版本并匹配输出语言。
**IMPORTANT**: Based on the language of user input, select the appropriate SKILL.md version and match the output language.

### 语言匹配流程 / Language Matching Process

1. **用户输入中文 / User inputs Chinese**:
   - 阅读SKILL.md(中文版)/ Read SKILL.md (Chinese version)
   - 使用中文输出回复 / Output response in Chinese

2. **用户输入英文 / User inputs English**:
   - 阅读SKILL_en.md(双语对照版)/ Read SKILL_en.md (Bilingual version)
   - 使用英文输出回复 / Output response in English

### 语言识别标准 / Language Recognition Standard

- 如果用户输入中包含中文字符,则识别为中文输入
- If user input contains Chinese characters, recognize as Chinese input
- 否则识别为英文输入
- Otherwise recognize as English input

---

## ⚠️ 重要提示:必须进行参数确认 / IMPORTANT: Parameter Confirmation is MANDATORY

**在执行任何MSR计算之前,必须遵守以下流程:**
**Before executing any MSR calculation, the following process MUST be followed:**

### 📋 必须遵守的执行流程 / Mandatory Execution Process

```
用户请求MSR计算 → 调用parameter-builder构建参数 → ⚠️ 展示参数给用户确认 ⚠️ → 用户确认参数 → 执行MSR计算
User Request MSR → Call parameter-builder to build parameters → ⚠️ Display parameters for user confirmation ⚠️ → User confirms parameters → Execute MSR calculation
```

### ❌ 禁止直接执行计算 / DO NOT Execute Calculation Directly

**在执行MSR计算之前,必须完成以下步骤:**
**Before executing MSR calculation, you MUST complete the following steps:**

1. **必须调用parameter-builder技能 / MUST call parameter-builder skill**:使用parameter-builder构建参数,不要手动构建参数 / Use parameter-builder to build parameters, do not manually build parameters
2. **必须展示参数给用户确认 / MUST display parameters for user confirmation**:无论用户请求多么明确,都必须展示参数并等待用户确认 / No matter how clear the user request is, you MUST display parameters and wait for user confirmation
3. **必须等待用户确认 / MUST wait for user confirmation**:只有用户明确选择"确认"后,才能执行MSR计算 / Only after user explicitly selects "Confirm" can you execute MSR calculation

### 🔧 参数确认流程 / Parameter Confirmation Process

当parameter-builder构建参数后,会展示参数和5个选项:
When parameter-builder builds parameters, it will display parameters and 5 options:

1. **确认 / Confirm** - 使用这些参数继续执行MSR计算 / Proceed with these parameters for MSR calculation
2. **修改 / Modify** - 调整特定参数(如温度、压强、团簇半径、气体组成等) / Adjust specific parameters (e.g., temperature, pressure, cluster radius, gas composition)
3. **对比 / Compare** - 运行多个条件进行对比(如多个温度、压强或团簇尺寸) / Run multiple conditions for comparison (e.g., multiple temperatures, pressures, or cluster sizes)
4. **切换计算模式 / Switch Calculation Mode** - 切换到KMC动力学模拟 / Switch to KMC kinetic simulation
5. **取消任务,更换体系 / Cancel and Change System** - 更换金属或气体体系 / Change metal or gas system

**只有用户选择"确认"(选项1)后,才能执行MSR计算!**
**Only after user selects "Confirm" (Option 1) can you execute MSR calculation!**

### ⚠️ 禁止行为 / Prohibited Actions

- ❌ **禁止**直接执行MSR计算,不经过parameter-builder / **DO NOT** execute MSR calculation directly without parameter-builder
- ❌ **禁止**跳过参数展示和确认步骤 / **DO NOT** skip parameter display and confirmation step
- ❌ **禁止**假设用户已经了解默认参数,不需要确认 / **DO NOT** assume user knows default parameters and skip confirmation

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

**技能名称 / Skill Name**: `chatmosp-msr-generator`
**技能类型 / Skill Type**: MSR Calculation Engine
**核心职责 / Core Responsibility**: Metal Cluster Structure Generation Calculation

---

## 🚀 快速开始:MSR计算正确流程 / Quick Start: MSR Calculation Correct Process

### 使用已有代码(不写新代码)/ Use Existing Code (Do Not Write New Code):
```bash
# MSR计算命令 / MSR calculation command
python3 mosp-for-chatMOSP/utils/msr.py --json path/to/input.json --output path/to/output/
```

### 📝 参数准备流程(重要)/ Parameter Preparation Process (Important):

#### 步骤1:准备input.json文件 / Step 1: Prepare input.json File
在运行MSR计算之前,必须准备完整的input.json文件。
Before running MSR calculation, you must prepare a complete input.json file.

### ⚠️ Large Cluster Calculation Time Warning / 大尺寸团簇计算时间提醒

When cluster radius ≥50Å, calculation time is long. You MUST warn the user before execution:

```
⚠️ Calculation Time Warning / 计算时间提醒：
Current cluster radius is {R}Å, estimated calculation time is approximately {estimated_minutes} minutes.
(Reference: radius 50Å takes about 20 minutes, larger radius takes longer)
Running multiple tasks simultaneously may increase time.
Continue with MSR calculation?
```

**Time Reference / 时间参考**:
- Radius 50Å (~11,000 atoms): about 20 minutes
- Radius 65Å (~35,000 atoms): about 60 minutes or longer
- Larger radius → cubic growth in atom count → significantly longer calculation time

**Note / 注意**: If user selects multiple conditions (e.g., multiple temperatures), each condition requires separate calculation, total time multiplies.

**推荐方法**:调用`chatmosp-parameter-builder`技能来准备参数。
**Recommended Method**: Call `chatmosp-parameter-builder` skill to prepare parameters.

示例:准备Pd在473K下的参数 → 调用parameter-builder技能 → 自动查找MOSP_database → 自动计算气体熵 / Example: Prepare parameters for Pd at 473K → call parameter-builder skill → auto-search MOSP_database → auto-calculate gas entropy
- CO在473K的熵值 = 0.002356 eV/K / CO entropy at 473K = 0.002356 eV/K
- O₂在473K的熵值 = 0.002446 eV/K / O₂ entropy at 473K = 0.002446 eV/K

#### 步骤2:气体熵自动计算 / Step 2: Automatic Gas Entropy Calculation
**重要**:`parameter-builder`技能会根据温度自动计算气体熵值。
**Important**: `parameter-builder` skill will automatically calculate gas entropy based on temperature.

**⚠️ 详细计算指令请参考 / For detailed calculation instructions, refer to:`chatmosp-parameter-builder/SKILL_en.md` Section 6.4**

气体熵计算公式 / Gas Entropy Calculation Formula:
```
S(eV/K) = (a × T^b) / 96485
```

支持的气体 / Supported Gases:
- H2, N2, O2, CO2, CO, NO, H2O

**计算示例 / Calculation Example**:
```
CO at 1000K / CO在1000K:
- a = 85.142, b = 0.147
- S = (85.142 × 1000^0.147) / 96485 = 0.002482 eV/K
```

**⚠️ 关键原则:MSR和KMC的气体熵值必须一致!**
**⚠️ KEY PRINCIPLE: MSR and KMC gas entropy values MUST be consistent!**
- MSR参数 / MSR Parameters: Gas1_S, Gas2_S
- KMC参数 / KMC Parameters: s1.S_gas, s2.S_gas
- 两者必须使用相同的计算方法和值 / Both must use the same calculation method and values

#### 步骤3:验证参数完整性 / Step 3: Validate Parameter Completeness
确保input.json包含所有必需的MSR参数:
Ensure input.json contains all required MSR parameters:
- Element, Temperature, Pressure
- Gas1_name, Gas1_pp, Gas1_S(气体熵 / gas entropy)
- Gas2_name, Gas2_pp, Gas2_S(气体熵 / gas entropy)
- Radius, nFaces, Face1/2/3参数 / parameters

#### ⚠️ 常见错误:直接复制example文件 / Common Error: Directly Copying example File
**错误做法**:直接复制`MOSP_database/Pd-COoxidation.json`而不调整气体熵。只修改温度但Gas1_S和Gas2_S还是原来温度的值，没有重新计算。
**Wrong Approach**: Directly copying `MOSP_database/Pd-COoxidation.json` without adjusting gas entropy. Only changing temperature but Gas1_S and Gas2_S remain at the original temperature values, not recalculated.

**正确做法**:使用parameter-builder技能准备参数，它会根据新温度自动重新计算气体熵。
**Correct Approach**: Use parameter-builder skill to prepare parameters; it will automatically recalculate gas entropy based on the new temperature.

#### 步骤4:运行MSR计算 ⚠️ 关键步骤 / Step 4: Run MSR Calculation ⚠️ Critical Step

**执行命令 / Execution Command**:
```bash
cd mosp-for-chatMOSP
python3 utils/msr.py --json OUTPUT/{task_name}/input.json --output OUTPUT/{task_name}/
cd -
```

**执行前检查 / Pre-execution Checks**:
- ✅ input.json ready (Steps 1-3 completed) / input.json已准备完整
- ✅ Gas entropy calculated at current temperature / 气体熵已根据当前温度计算
- ✅ User confirmed parameters / 用户已确认参数

**执行后验证 / Post-execution Validation**:
```bash
ls -lh OUTPUT/{task_name}/ini.xyz
ls -lh OUTPUT/{task_name}/{task_name}_cluster.xyz
```
- ✅ `ini.xyz` MUST exist and be > 0KB, otherwise MSR failed / 必须存在且>0KB，否则失败
- ✅ `{task_name}_cluster.xyz` MUST exist (for visualization) / 必须存在（用于可视化）
- ⚠️ If missing, report error and suggest retrying with adjusted parameters / 若缺失则报错

### 生成的文件 / Generated Files:
- `ini.xyz` - 优化后的团簇结构(包含所有原子)/ Optimized cluster structure (including all atoms)
- `{task_name}_cluster.xyz` - 可视化用结构文件(表面原子已分类)/ Visualization structure file (surface atoms classified)
- `faceinfo.txt` - 晶面信息统计 / Crystal face information statistics
- `input.json` - MSR参数文件 / MSR parameter file

### ⚠️ 重要说明 / Important Notes:
1. **MSR只负责生成团簇结构**,不包含KMC参数 / **MSR only generates cluster structure**, does not include KMC parameters
2. **不要在MSR的input.json中包含KMC参数** / **Do not include KMC parameters in MSR's input.json**
3. KMC参数由KMC技能单独准备(详见chatmosp-kmc-simulator技能)/ KMC parameters are prepared separately by KMC skill (see chatmosp-kmc-simulator skill)
4. MSR和KMC使用不同的input.json,参数完全分离 / MSR and KMC use different input.json, parameters are completely separated

### MSR→KMC工作流 / MSR→KMC Workflow:
```
MSR计算 → 生成ini.xyz → (如需KMC)→ KMC技能准备独立参数 → KMC计算
MSR calculation → Generate ini.xyz → (if KMC needed) → KMC skill prepares independent parameters → KMC calculation
```

---

### 技能定位 / Skill Positioning
MSR生成器是chatMOSP系统的核心计算引擎,负责:
The MSR generator is the core calculation engine of the chatMOSP system, responsible for:

1. **MOSP引擎调用 / MOSP Engine Invocation**: 执行金属团簇结构生成计算
   Executing metal cluster structure generation calculations

2. **智能重试机制 / Smart Retry Mechanism**: 基于设计文档的失败重试和降级策略
   Failure retry and degradation strategies based on design documentation

3. **参数适配 / Parameter Adaptation**: 将通用参数转换为MOSP引擎特定格式
   Converting general parameters to MOSP engine specific format

4. **结果验证 / Result Validation**: 检查计算收敛性和结果合理性
   Checking calculation convergence and result reasonableness

### 安全与可靠性 / Safety and Reliability
- ✅ **失败重试机制 / Failure Retry Mechanism**: 自动重试失败的计算(最多3次)
  Automatically retry failed calculations (up to 3 times)
- ✅ **智能降级策略 / Smart Degradation Strategy**: 调整参数以帮助收敛
  Adjust parameters to help convergence
- ✅ **资源监控 / Resource Monitoring**: 检查内存和CPU使用情况
  Check memory and CPU usage

## 🎯 核心功能 / Core Functions

### 1. MSR计算执行 / MSR Calculation Execution
- 调用 mosp-for-chatMOSP 引擎 / Call mosp-for-chatMOSP engine
- 准备MSR输入文件(MSR-input.json)/ Prepare MSR input files (MSR-input.json)
- 监控计算过程 / Monitor calculation process
- 捕获计算结果 / Capture calculation results

### 2. 智能重试机制 / Smart Retry Mechanism
```
First failure → Reduce cluster radius and retry
第二次失败 → 增加迭代次数重试
Second failure → Increase iteration count and retry
第三次失败 → 返回详细错误信息
Third failure → Return detailed error information
```

### 3. 参数转换与验证 / Parameter Conversion and Validation
- 验证参数完整性 / Validate parameter completeness
- 转换为MOSP引擎格式 / Convert to MOSP engine format
- 检查参数合理性 / Check parameter reasonableness
- 添加默认值 / Add default values

### 4. 结果处理与解析 / Result Processing and Parsing
- 解析结构文件(.xyz格式)/ Parse structure files (.xyz format)
- 提取能量和收敛信息 / Extract energy and convergence information
- 验证结果有效性 / Verify result validity
- 生成标准化输出 / Generate standardized output

## 🔧 技术实现 / Technical Implementation

### 依赖关系 / Dependencies
- `mosp-for-chatMOSP` - 核心计算引擎(已克隆)/ Core calculation engine (already cloned)
- `chatmosp-file-organizer` - 文件路径管理 / File path management
- `chatmosp-parameter-builder` - 参数验证 / Parameter validation

### 执行流程 / Execution Flow
```
接收参数 → 验证参数 → 准备输入文件 → 执行计算 →
Receive parameters → Validate parameters → Prepare input files → Execute calculation →
监控进度 → 检查收敛 → 解析结果 → 返回标准化输出
Monitor progress → Check convergence → Parse results → Return standardized output
           ↓
       失败重试 → 参数调整 → 重新执行
       Failure retry → Parameter adjustment → Re-execute
```

### 文件使用逻辑 / File Usage Logic
**重要:正确的文件创建和使用流程 / Important: Correct file creation and usage process**

1. **MSR任务文件流程 / MSR Task File Flow**:
   - **输入 / Input**: `input.json` (parameter file)
   - **MSR生成 / MSR Generates**: `ini.xyz` - 真实团簇结构文件(包含所有原子信息) / Real cluster structure file (contains all atomic information)
   - **MSR生成 / MSR Generates**: `{task_name}_cluster.xyz` - 绘图用结构文件(表面原子已按晶面分类) / Drawing structure file (surface atoms classified by crystal plane)
   - **重要 / Important**: `ini.xyz` 是MSR的输出文件,不是输入文件 / `ini.xyz` is an output file of MSR, not an input file

2. **KMC任务文件流程 / KMC Task File Flow**:
   - **输入 / Input**: `input.json` (parameter file) + `ini.xyz` (structure file generated by MSR)
   - **KMC生成 / KMC Generates**: 动力学模拟结果文件 / Kinetic simulation result files
   - **关键 / Key**: KMC需要MSR生成的 `ini.xyz` 作为输入 / KMC requires `ini.xyz` generated by MSR as input

### 可视化生成 / Visualization Generation
MSR计算完成后自动生成可视化图像:
Visualization images are automatically generated after MSR calculation:

**可视化命令执行步骤 / Visualization Command Steps**:

**步骤1:生成静态结构图 / Step 1: Generate Static Structure Image**
```bash
# 生成PNG静态图片 / Generate PNG static image
cd mosp-for-chatMOSP && python3 utils/paint.py OUTPUT/{task_name}/{task_name}_cluster.xyz \
  --output OUTPUT/{task_name}/structure.png
```

**步骤2:生成动态旋转动图 / Step 2: Generate Rotation Animation**
```bash
# 生成GIF动图 / Generate GIF animation
cd mosp-for-chatMOSP && python3 utils/paint.py OUTPUT/{task_name}/{task_name}_cluster.xyz \
  --gif OUTPUT/{task_name}/rotation.gif
```

**重要说明 / IMPORTANT**:
- paint.py每次调用只能生成一种类型的图像(静态图片或动图)
- paint.py can only generate one type of image per call (static image OR animation)
- 需要分两步分别生成静态图片和动图
- Two separate steps are required to generate static image and animation respectively

可视化配置 / Visualization Config:
- 默认生成静态图(structure.png)和旋转动图(rotation.gif) / Default: generate static image and rotation GIF
- 动图生成建议原子数≤20000（超过时仅生成静态图） / Animation recommended for ≤20000 atoms (static only above)

#### 步骤3:向用户展示可视化结果 / Step 3: Present Visualization to User ⚠️ 重要 / IMPORTANT

**必须执行 / MUST DO**:生成图像后,立即向用户展示!
**Must present visualization to user immediately after generation!**

**飞书平台发送示例 / Feishu Platform Send Example**:
```json
{
  "action": "send",
  "channel": "feishu",
  "filePath": "/root/.openclaw/workspace/mosp-for-chatMOSP/OUTPUT/{task_name}/structure.png",
  "caption": "{Element} - {Gas1}%-{Gas2}%-{Temperature}K-{Pressure}Pa-R{Radius}Å"
}
```

**示例标题 / Example Captions**:
- `Pt - CO67%-O33%-1000K-1500Pa-R40Å`
- `Pd - CO9%-O18%-473K-101325Pa-R50Å`

**操作要求 / Requirements**:
1. 发送 structure.png 给用户查看 / Send structure.png to user
2. 发送 rotation.gif 给用户查看 / Send rotation.gif to user
3. 简要描述结构特征 / Briefly describe structural features
   (如:"Pd纳米颗粒呈截角八面体,主要暴露(111)晶面")
   (e.g., "Pd nanoparticle shows truncated octahedron, mainly exposing (111) facets")

## 📝 使用示例 / Usage Examples

### 英文示例 / English Example
```
用户: Generate Pd cluster for CO oxidation at 500K, 101325Pa
系统: [识别为MSR任务 → 查找参数 → 展示确认 → 执行计算 → 展示结构图]
```

### 中文示例 / Chinese Example
```
用户: 计算Pt纳米颗粒在500K下的团簇结构
系统: [识别为MSR任务 → 查找参数 → 展示确认 → 执行计算 → 展示结构图]
```
