# Skill: chatmosp-file-organizer (Bilingual Version)

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

**技能名称 / Skill Name**: `chatmosp-file-organizer`
**技能类型 / Skill Type**: Intelligent File System Manager
**核心职责 / Core Responsibility**: Standard Directory Structure Creation, Intelligent Task Naming, Secure File Operations

### 技能定位 / Skill Positioning
文件组织器是chatMOSP系统的文件系统管家,负责:
The file organizer is the file system manager of the chatMOSP system, responsible for:

1. **智能任务命名 / Intelligent Task Naming**: 根据任务类型生成标准化的任务名称(MSR/KMC不同格式)
   Generate standardized task names based on task type (different formats for MSR/KMC)
2. **标准目录创建 / Standard Directory Creation**: 按照MSR和KMC的标准目录结构创建任务文件夹
   Create task folders according to MSR and KMC standard directory structures
3. **安全文件操作 / Secure File Operations**: 防止路径遍历攻击,确保所有操作在安全范围内
   Prevent path traversal attacks, ensure all operations are within safe boundaries
4. **路径逻辑管理 / Path Logic Management**: 管理MSR和KMC任务的不同路径逻辑
   Manage different path logics for MSR and KMC tasks

### 安全第一原则 / Security First Principle
- ✅ **路径遍历防护 / Path Traversal Protection**: 自动检测并清理 `../` 等危险字符
  Automatically detect and clean dangerous characters like `../`
- ✅ **白名单路径 / Whitelist Paths**: 所有操作限制在 `mosp-for-chatMOSP/OUTPUT/` 内
  All operations restricted to `mosp-for-chatMOSP/OUTPUT/`
- ✅ **TaskNameValidator**: 防御性任务名称验证,支持新命名格式
  Defensive task name validation, supports new naming formats
- ✅ **权限检查 / Permission Checking**: 确保有适当的文件读写权限
  Ensure appropriate file read/write permissions

## 🎯 核心功能 / Core Functions

### 1. 智能任务名称生成 / Intelligent Task Name Generation
根据任务类型生成标准化的任务名称:
Generate standardized task names based on task type:

#### 1.1 MSR任务命名规则 / MSR Task Naming Rules
**格式 / Format**: `{金属}_{气体分压}_{温度}K_{压强}Pa_R{尺寸}`
**示例 / Example**: `Pd_CO9_O18_473K_100000Pa_R50`

**参数说明 / Parameter Description**:
- **金属 / Metal**: Pd, Pt, Au等金属元素符号 / Metal element symbols like Pd, Pt, Au
- **气体分压 / Gas Partial Pressure**: 多个气体用`_`连接,气体后面跟着分压(CO9表示CO分压为9)
  Multiple gases connected with `_`, gas followed by partial pressure (CO9 means CO partial pressure is 9)
- **温度 / Temperature**: 数值+K(如473K,默认500K) / Value+K (e.g., 473K, default 500K)
- **压强 / Pressure**: 数值+Pa(如100000Pa,默认101325Pa) / Value+Pa (e.g., 100000Pa, default 101325Pa)
- **尺寸 / Size**: R+数值(如R50表示50Å,默认R20) / R+value (e.g., R50 means 50Å, default R20)

#### 1.2 KMC任务命名规则 / KMC Task Naming Rules

**⚠️ 重要：KMC任务必须在对应的MSR任务目录下创建子目录**
**⚠️ IMPORTANT: KMC tasks MUST create subdirectories under corresponding MSR task directories**

**格式 / Format**: `KMC_{步数}steps` 或 `KMC_{温度}K_{压强}Pa_{步数}steps`
**推荐格式 / Recommended Format**：`KMC_{步数}steps`（简洁明了，因为温度压强等信息已经在MSR目录名中 / Concise and clear, as temperature and pressure info is already in MSR directory name）

**示例 / Examples**: 
- 简化版 / Simplified：`KMC_5000000steps`
- 详细版 / Detailed：`KMC_473K_101325Pa_5000000steps`

**参数说明 / Parameter Description**:
- **步数 / Steps**: 数值+steps（如5000000steps，默认1000000steps）
- **温度 / Temperature**: （可选/Optional）数值+K（如473K）
- **压强 / Pressure**: （可选/Optional）数值+Pa（如101325Pa）

**KMC目录位置 / KMC Directory Location**：
```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/KMC_{步数}steps/
```

**示例 / Example**：
```
mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_101325Pa_R50/KMC_5000000steps/
```

### 2. 标准目录结构创建 / Standard Directory Structure Creation

#### 2.1 MSR任务标准目录结构 / MSR Task Standard Directory Structure
```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/          # MSR任务根目录 / MSR task root directory
├── faceinfo.txt                 # MSR输出:晶面信息 / MSR output: crystal face information
├── ini.xyz                      # MSR输出:真实团簇文件,用于KMC计算 / MSR output: real cluster file for KMC calculation
├── {msr_task_name}_cluster.xyz  # MSR输出:用于绘图的结构文件(表面原子已分类) / MSR output: structure file for drawing (surface atoms classified)
├── rotation.gif                 # paint.py生成:旋转动画 / paint.py generated: rotation animation
├── structure.png                # paint.py生成:结构图 / paint.py generated: structure diagram
├── parameter_analysis.md        # MSR输出:参数分析文档 / MSR output: parameter analysis document
├── paint.py                     # 绘图脚本 / Drawing script
├── input.json                   # MSR参数文件 / MSR parameter file
└── metadata.json                # 任务元数据 / Task metadata
```

**MSR任务文件说明 / MSR Task File Description**:
1. **ini.xyz** - 真实团簇结构文件,包含所有原子信息,用于KMC计算 / Real cluster structure file containing all atomic information, used for KMC calculation
2. **{task_name}_cluster.xyz** - 绘图用结构文件,表面原子已按晶面分类,便于可视化 / Drawing structure file with surface atoms classified by crystal plane, easy for visualization

**可视化生成命令 / Visualization Generation Command**:
```bash
python3 utils/paint.py OUTPUT/{task_name}/{task_name}_cluster.xyz \
  --output OUTPUT/{task_name}/structure.png \
  --gif OUTPUT/{task_name}/rotation.gif
```

#### 2.2 KMC任务标准目录结构 / KMC Task Standard Directory Structure

**⚠️ 重要：KMC任务目录必须在对应的MSR任务目录下创建**
**⚠️ IMPORTANT: KMC task directories MUST be created under corresponding MSR task directories**

**目录结构 / Directory Structure**：
```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/              # MSR任务根目录 / MSR task root directory
├── faceinfo.txt                 # MSR输出：晶面信息 / MSR output: crystal face information
├── ini.xyz                      # MSR输出：真实团簇文件（用于KMC计算）/ MSR output: real cluster file (for KMC calculation)
├── {msr_task_name}_cluster.xyz  # MSR输出：绘图用结构文件 / MSR output: structure file for drawing
├── structure.png                # MSR输出：结构图 / MSR output: structure diagram
├── rotation.gif                 # MSR输出：旋转动画 / MSR output: rotation animation
├── input.json                   # MSR参数文件 / MSR parameter file
└── KMC_{步数}steps/              # KMC任务目录（在MSR目录下）/ KMC task directory (under MSR directory)
    ├── input.json               # KMC输入参数文件（必须！）/ KMC input parameter file (required!)
    ├── ini.xyz                  # 结构文件（复制自MSR）/ Structure file (copied from MSR)
    ├── coverage.csv             # KMC输出：覆盖度数据 / KMC output: coverage data
    ├── coverage.png             # KMC输出：覆盖度图 / KMC output: coverage diagram
    ├── run.log                  # KMC输出：运行日志 / KMC output: run log
    ├── site_tof.csv             # KMC输出：位点TOF数据 / KMC output: site TOF data
    ├── tof.csv                  # KMC输出：TOF数据 / KMC output: TOF data
    ├── tof.png                  # KMC输出：TOF图 / KMC output: TOF diagram
    ├── INPUT/                   # 空目录，KMC代码自动填充 / Empty directory, KMC code automatically fills
    │   ├── events.txt           # KMC自动生成：反应事件 / KMC auto-generated: reaction events
    │   ├── input.txt            # KMC自动生成：输入文件 / KMC auto-generated: input file
    │   ├── LI.txt               # KMC自动生成：Langmuir-Isotherm参数 / KMC auto-generated: Langmuir-Isotherm parameters
    │   ├── products.txt         # KMC自动生成：产物信息 / KMC auto-generated: product information
    │   └── species.txt          # KMC自动生成：物种信息 / KMC auto-generated: species information
    └── OUTPUT/                  # 空目录，KMC代码自动输出 / Empty directory, KMC code automatically outputs
        ├── rec_cov.data         # KMC自动输出：覆盖度记录 / KMC auto-output: coverage records
        ├── rec_event.data       # KMC自动输出：事件记录 / KMC auto-output: event records
        └── ...                  # 其他输出文件 / Other output files
```

**示例 / Example**：
```
mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_101325Pa_R50/
├── ini.xyz                      # MSR输出 / MSR output
├── Pd_CO9_O18_473K_101325Pa_R50_cluster.xyz  # MSR输出 / MSR output
├── structure.png                # MSR输出 / MSR output
├── rotation.gif                 # MSR输出 / MSR output
├── input.json                   # MSR参数文件 / MSR parameter file
└── KMC_5000000steps/            # KMC任务目录 / KMC task directory
    ├── input.json               # KMC输入参数文件 / KMC input parameter file
    ├── ini.xyz                  # 结构文件（复制自MSR）/ Structure file (copied from MSR)
    ├── coverage.csv             # KMC输出 / KMC output
    ├── tof.csv                  # KMC输出 / KMC output
    ├── INPUT/                   # KMC输入目录 / KMC input directory
    └── OUTPUT/                  # KMC输出目录 / KMC output directory
```

**KMC任务关键文件 / KMC Task Key Files**：
1. **input.json** - KMC参数文件，必须包含：温度、压强、步数、物种定义、反应事件等 / KMC parameter file, must include: temperature, pressure, steps, species definitions, reaction events, etc.
2. **ini.xyz** - 团簇结构文件，从MSR输出复制而来 / Cluster structure file, copied from MSR output
3. **coverage.csv** - 覆盖度随时间变化数据 / Coverage data over time
4. **tof.csv** - TOF（转换频率）数据 / TOF (Turnover Frequency) data
```

### 3. 任务类型与路径逻辑 / Task Type and Path Logic

#### 3.1 MSR任务路径 / MSR Task Path
- **固定位置 / Fixed Location**: `mosp-for-chatMOSP/OUTPUT/{msr_task_name}/`
- **关键 / Key**: MSR任务会生成 `ini.xyz` 和 `{task_name}_cluster.xyz` 文件 / MSR tasks generate `ini.xyz` and `{task_name}_cluster.xyz` files
- **注意 / Note**: 不要为MSR任务准备 `ini.xyz` 文件，MSR会生成它 / Do not prepare `ini.xyz` file for MSR tasks, MSR will generate it

#### 3.2 KMC任务路径（两种模式）/ KMC Task Path (Two Modes)
1. **直接KMC任务 / Direct KMC Task**（使用MOSP_database中的结构文件 / Using structure files from MOSP_database）:
   - **位置 / Location**: `mosp-for-chatMOSP/OUTPUT/{kmc_task_name}/`
   - **结构文件来源 / Structure File Source**: Copy from `mosp-for-chatMOSP/MOSP_database/`
   - **适用场景 / Applicable Scenario**: Use when there is no corresponding MSR result

2. **接续KMC任务 / Sequential KMC Task**（使用MSR生成的ini.xyz / Using MSR-generated ini.xyz）:
   - **位置 / Location**: `mosp-for-chatMOSP/OUTPUT/{msr_task_name}/{kmc_task_name}/`
   - **结构文件来源 / Structure File Source**: MSR-generated `ini.xyz` file
   - **推荐做法 / Recommended Practice**: 优先使用MSR生成的 `ini.xyz`，确保一致性 / Prioritize using MSR-generated `ini.xyz` to ensure consistency

### 4. 文件操作安全 / File Operation Security
- **TaskNameValidator类 / TaskNameValidator Class**: 验证新命名格式的合法性 / Validate legality of new naming formats
- **分压格式验证 / Partial Pressure Format Validation**: 支持`CO9_O18`等格式 / Support formats like `CO9_O18`
- **参数提取 / Parameter Extraction**: 从任务名称中提取金属、温度、气体、步数等参数 / Extract metal, temperature, gases, steps, etc. from task names
- **路径白名单 / Path Whitelist**: 严格限制在`mosp-for-chatMOSP/OUTPUT/`范围内 / Strictly restricted to `mosp-for-chatMOSP/OUTPUT/`

## 🔧 技术实现 / Technical Implementation

### 依赖关系 / Dependencies
- **chatmosp-parameter-builder**: 获取任务参数信息 / Get task parameter information
- **chatmosp-input-coordinator**: 获取任务类型信息 / Get task type information

### 执行流程 / Execution Flow
```
接收任务信息 → 识别任务类型 → 生成标准任务名称 → 验证名称安全性 →
Receive task info → Identify task type → Generate standard task name → Validate name security →
创建标准目录结构 → 准备必要文件路径 → 返回目录信息
Create standard directory structure → Prepare necessary file paths → Return directory info
```

## 📝 使用示例 / Usage Examples

### 示例1:MSR任务目录创建 / Example 1: MSR Task Directory Creation
```
输入 / Input: {
    "action": "create_msr_directory",
    "parameters": {
        "metal": "Pd",
        "temperature": "473",
        "gases": ["CO", "O2"],
        "partial_pressures": {"CO": 9, "O2": 18},
        "pressure": "100000",
        "radius": "50"
    }
}

输出 / Output: {
    "success": true,
    "task_type": "MSR",
    "task_name": "Pd_CO9_O18_473K_100000Pa_R50",
    "directory_path": "mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_100000Pa_R50",
    "standard_files": [
        "faceinfo.txt", "ini.xyz", "Pd_CO9_O18_473K_100000Pa_R50_cluster.xyz",
        "rotation.gif", "structure.png", "parameter_analysis.md",
        "paint.py", "input.json", "metadata.json"
    ],
    "visualization_commands": [
        "python3 utils/paint.py OUTPUT/Pd_CO9_O18_473K_100000Pa_R50/Pd_CO9_O18_473K_100000Pa_R50_cluster.xyz --output OUTPUT/Pd_CO9_O18_473K_100000Pa_R50/structure.png",
        "python3 utils/paint.py OUTPUT/Pd_CO9_O18_473K_100000Pa_R50/Pd_CO9_O18_473K_100000Pa_R50_cluster.xyz --gif OUTPUT/Pd_CO9_O18_473K_100000Pa_R50/rotation.gif"
    ]
}
```

### 示例2:KMC任务目录创建 / Example 2: KMC Task Directory Creation
```
输入 / Input: {
    "action": "create_kmc_directory",
    "parameters": {
        "metal": "Pd",
        "temperature": "473",
        "gases": ["CO", "O2"],
        "partial_pressures": {"CO": 9, "O2": 18},
        "pressure": "100000",
        "steps": "200000000",
        "parent_msr_task": null  # 直接KMC任务 / Direct KMC task
    }
}

输出 / Output: {
    "success": true,
    "task_type": "KMC",
    "task_name": "Pd_CO9_O18_473K_100000Pa_200000000steps",
    "directory_path": "mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_100000Pa_200000000steps",
    "required_files": ["input.json", "ini.xyz"],
    "empty_directories": ["INPUT", "OUTPUT"],
    "output_files": [
        "coverage.csv", "coverage.png", "run.log",
        "site_tof.csv", "tof.csv", "tof.png"
    ]
}
```

## 🛠️ 配置选项 / Configuration Options

```yaml
# 技能配置 / Skill Configuration
skill:
  name: "chatmosp-file-organizer"
  version: "2.0.0"
  description: "智能文件系统管理器 - 支持MSR/KMC标准目录结构 / Intelligent File System Manager - Supports MSR/KMC Standard Directory Structures"

# 目录配置 / Directory Configuration
directories:
  mosp_home: "mosp-for-chatMOSP"
  output_root: "mosp-for-chatMOSP/OUTPUT/"
  MOSP_database_dir: "mosp-for-chatMOSP/MOSP_database/"

# 命名配置 / Naming Configuration
naming:
  msr_format: "{metal}_{gases_partial}_{temperature}K_{pressure}Pa_R{radius}"
  kmc_format: "{metal}_{gases}_{temperature}K_{pressure}Pa_{steps}steps"
  gas_separator: "_"
  partial_pressure_format: "{gas}{pressure}"

# 默认参数 / Default Parameters
defaults:
  temperature: "500"
  pressure: "101325"
  radius: "20"
  steps: "1000000"

# 安全配置 / Security Configuration
security:
  enable_path_validation: true
  allowed_paths: ["mosp-for-chatMOSP/OUTPUT/", "mosp-for-chatMOSP/MOSP_database/"]
  forbidden_patterns: ["..", "//", "~", "/root", "/etc", "*.exe", "*.sh"]
  max_path_length: 512
  allowed_characters: "a-zA-Z0-9_-.Å"
```

## 📁 文件结构 / File Structure

```
chatmosp-file-organizer/
├── SKILL.md           # 技能说明文档（中文版）/ Skill documentation (Chinese version)
└── SKILL_en.md        # 技能说明文档（英文版）/ Skill documentation (English version)
```

## 🔄 更新说明 / Update Notes

**版本 2.0.0 (2026-04-27) - 重大更新 / Version 2.0.0 (2026-04-27) - Major Update**:
1. ✅ **支持新的命名规则 / Support New Naming Rules**: MSR和KMC任务使用不同的命名格式 / MSR and KMC tasks use different naming formats
2. ✅ **标准目录结构 / Standard Directory Structure**: MSR(9个标准文件)和KMC(复杂嵌套结构) / MSR (9 standard files) and KMC (complex nested structure)
3. ✅ **智能任务类型识别 / Intelligent Task Type Recognition**: 自动识别MSR和KMC任务并创建对应结构 / Automatically identify MSR and KMC tasks and create corresponding structures
4. ✅ **路径逻辑管理 / Path Logic Management**: 支持直接KMC任务和接续KMC任务 / Supports direct KMC tasks and sequential KMC tasks
5. ✅ **安全增强 / Security Enhancement**: TaskNameValidator支持新格式验证 / TaskNameValidator supports new format validation

**向后兼容性 / Backward Compatibility**:
- 旧版任务名称格式(`{金属}_{温度}K_{时间戳}`)仍然支持 / Old task name format (`{metal}_{temperature}K_{timestamp}`) still supported
- 旧版目录结构可以自动升级到新版 / Old directory structures can be automatically upgraded to new version
- API接口保持兼容,新增可选参数 / API interface remains compatible, new optional parameters added