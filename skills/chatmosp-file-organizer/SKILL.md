# Skill: chatmosp-file-organizer

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

## 📖 术语定义

**MOSP (Multiscale Operando Simulation Package)** - 多尺度原位模拟包
- 金属催化剂表面反应的多尺度模拟系统
- 整合结构生成和动力学模拟

**MSR (Multiscale Structure Reconstruction)** - 多尺度结构重构模型
- 基于Wulff构造的金属团簇结构生成
- 计算不同晶面比例的平衡形貌

**KMC (Kinetic Monte Carlo)** - 动力学蒙特卡洛模型
- 模拟表面反应的动力学过程
- 计算TOF、覆盖度等动力学参数

---

## 📋 技能概览

**技能名称**: `chatmosp-file-organizer`  
**技能类型**: 智能文件系统管理器  
**核心职责**: 标准目录结构创建、智能任务命名、安全文件操作  

### 技能定位
文件组织器是chatMOSP系统的文件系统管家，负责：
1. **智能任务命名**：根据任务类型生成标准化的任务名称（MSR/KMC不同格式）
2. **标准目录创建**：按照MSR和KMC的标准目录结构创建任务文件夹
3. **安全文件操作**：防止路径遍历攻击，确保所有操作在安全范围内
4. **路径逻辑管理**：管理MSR和KMC任务的不同路径逻辑

### 安全第一原则
- ✅ **路径遍历防护**：自动检测并清理 `../` 等危险字符
- ✅ **白名单路径**：所有操作限制在 `mosp-for-chatMOSP/OUTPUT/` 内
- ✅ **TaskNameValidator**：防御性任务名称验证，支持新命名格式
- ✅ **权限检查**：确保有适当的文件读写权限

## 🎯 核心功能

### 1. 智能任务名称生成
根据任务类型生成标准化的任务名称：

#### 1.1 MSR任务命名规则
**格式**: `{金属}_{气体分压}_{温度}K_{压强}Pa_R{尺寸}`  
**示例**: `Pd_CO9_O18_473K_100000Pa_R50`

**参数说明**:
- **金属**：Pd, Pt, Au等金属元素符号
- **气体分压**：多个气体用`_`连接，气体后面跟着分压（CO9表示CO分压为9）
- **温度**：数值+K（如473K，默认500K）
- **压强**：数值+Pa（如100000Pa，默认101325Pa）
- **尺寸**：R+数值（如R50表示50Å，默认R20）

#### 1.2 KMC任务命名规则

**⚠️ 重要：KMC任务必须在对应的MSR任务目录下创建子目录**

**格式**: `KMC_{步数}steps` 或 `KMC_{温度}K_{压强}Pa_{步数}steps`
**推荐格式**：`KMC_{步数}steps`（简洁明了，因为温度压强等信息已经在MSR目录名中）

**示例**: 
- 简化版：`KMC_5000000steps`
- 详细版：`KMC_473K_101325Pa_5000000steps`

**参数说明**:
- **步数**：数值+steps（如5000000steps，默认1000000steps）
- **温度**：（可选）数值+K（如473K）
- **压强**：（可选）数值+Pa（如101325Pa）

**KMC目录位置**：
```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/KMC_{步数}steps/
```

**示例**：
```
mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_101325Pa_R50/KMC_5000000steps/
```

### 2. 标准目录结构创建

#### 2.1 MSR任务标准目录结构
```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/          # MSR任务根目录
├── faceinfo.txt                 # MSR输出：晶面信息
├── ini.xyz                      # MSR输出：真实团簇文件，用于KMC计算
├── {msr_task_name}_cluster.xyz  # MSR输出：用于绘图的结构文件（表面原子已分类）
├── rotation.gif                 # paint.py生成：旋转动画
├── structure.png                # paint.py生成：结构图
├── parameter_analysis.md        # MSR输出：参数分析文档
├── paint.py                     # 绘图脚本
├── input.json                   # MSR参数文件
└── metadata.json                # 任务元数据
```

**MSR任务文件说明**：
1. **ini.xyz** - 真实团簇结构文件，包含所有原子信息，用于KMC计算
2. **{task_name}_cluster.xyz** - 绘图用结构文件，表面原子已按晶面分类，便于可视化

**可视化生成命令**：

⚠️ **简化绘图命令（不需要-c site_type）**：
```bash
# 只需要这两个命令，不生成冗余的site_type图像
python3 utils/paint.py OUTPUT/{task_name}/{task_name}_cluster.xyz \
  --output OUTPUT/{task_name}/structure.png

python3 utils/paint.py OUTPUT/{task_name}/{task_name}_cluster.xyz \
  --gif OUTPUT/{task_name}/rotation.gif
```

**说明**：
- 默认按元素着色（简单明了）
- 不需要 `-c site_type` 参数（除非用户明确要求按晶面着色）
- 只生成两个文件：structure.png（静态图）和rotation.gif（旋转动画）
- 不生成 structure_site_type.png（冗余文件）

#### 2.2 KMC任务标准目录结构

**⚠️ 重要：KMC任务目录必须在对应的MSR任务目录下创建**

**目录结构**：
```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/              # MSR任务根目录
├── faceinfo.txt                 # MSR输出：晶面信息
├── ini.xyz                      # MSR输出：真实团簇文件（用于KMC计算）
├── {msr_task_name}_cluster.xyz  # MSR输出：绘图用结构文件
├── structure.png                # MSR输出：结构图
├── rotation.gif                 # MSR输出：旋转动画
├── input.json                   # MSR参数文件
└── KMC_{步数}steps/              # KMC任务目录（在MSR目录下）
    ├── input.json               # KMC输入参数文件（必须！）
    ├── ini.xyz                  # 结构文件（复制自MSR）
    ├── coverage.csv             # KMC输出：覆盖度数据
    ├── coverage.png             # KMC输出：覆盖度图
    ├── run.log                  # KMC输出：运行日志
    ├── site_tof.csv             # KMC输出：位点TOF数据
    ├── tof.csv                  # KMC输出：TOF数据
    ├── tof.png                  # KMC输出：TOF图
    ├── INPUT/                   # 空目录，KMC代码自动填充
    │   ├── events.txt           # KMC自动生成：反应事件
    │   ├── input.txt            # KMC自动生成：输入文件
    │   ├── LI.txt               # KMC自动生成：Langmuir-Isotherm参数
    │   ├── products.txt         # KMC自动生成：产物信息
    │   └── species.txt          # KMC自动生成：物种信息
    └── OUTPUT/                  # 空目录，KMC代码自动输出
        ├── rec_cov.data         # KMC自动输出：覆盖度记录
        ├── rec_event.data       # KMC自动输出：事件记录
        └── ...                  # 其他输出文件
```

**示例**：
```
mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_101325Pa_R50/
├── ini.xyz                      # MSR输出
├── Pd_CO9_O18_473K_101325Pa_R50_cluster.xyz  # MSR输出
├── structure.png                # MSR输出
├── rotation.gif                 # MSR输出
├── input.json                   # MSR参数文件
└── KMC_5000000steps/            # KMC任务目录
    ├── input.json               # KMC输入参数文件
    ├── ini.xyz                  # 结构文件（复制自MSR）
    ├── coverage.csv             # KMC输出
    ├── tof.csv                  # KMC输出
    ├── INPUT/                   # KMC输入目录
    └── OUTPUT/                  # KMC输出目录
```

**KMC任务关键文件**：
1. **input.json** - KMC参数文件，必须包含：温度、压强、步数、物种定义、反应事件等
2. **ini.xyz** - 团簇结构文件，从MSR输出复制而来
3. **coverage.csv** - 覆盖度随时间变化数据
4. **tof.csv** - TOF（转换频率）数据
    └── rec_site_spc.data        # KMC自动输出：位点物种记录
```

### 3. 任务类型与路径逻辑

#### 3.1 MSR任务路径
- **固定位置**：`mosp-for-chatMOSP/OUTPUT/{msr_task_name}/`
- **关键**：MSR任务会生成 `ini.xyz` 和 `{task_name}_cluster.xyz` 文件
- **注意**：不要为MSR任务准备 `ini.xyz` 文件，MSR会生成它

#### 3.2 KMC任务路径（两种模式）
1. **直接KMC任务**（使用MOSP_database中的结构文件）：
   - **位置**：`mosp-for-chatMOSP/OUTPUT/{kmc_task_name}/`
   - **结构文件来源**：从`mosp-for-chatMOSP/MOSP_database/`复制
   - **适用场景**：没有对应MSR结果时使用

2. **接续KMC任务**（使用MSR生成的ini.xyz）：
   - **位置**：`mosp-for-chatMOSP/OUTPUT/{msr_task_name}/{kmc_task_name}/`
   - **结构文件来源**：MSR生成的`ini.xyz`文件
   - **推荐做法**：优先使用MSR生成的 `ini.xyz`，确保一致性

### 4. 文件操作安全
- **TaskNameValidator类**：验证新命名格式的合法性
- **分压格式验证**：支持`CO9_O18`等格式
- **参数提取**：从任务名称中提取金属、温度、气体、步数等参数
- **路径白名单**：严格限制在`mosp-for-chatMOSP/OUTPUT/`范围内

## 🔧 技术实现

### 依赖关系
- **chatmosp-parameter-builder**：获取任务参数信息
- **chatmosp-input-coordinator**：获取任务类型信息

### 执行流程
```
接收任务信息 → 识别任务类型 → 生成标准任务名称 → 验证名称安全性 → 
创建标准目录结构 → 准备必要文件路径 → 返回目录信息
```

## 📝 使用示例

### 示例1：MSR任务目录创建
```
输入: {
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

输出: {
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

### 示例2：KMC任务目录创建
```
输入: {
    "action": "create_kmc_directory",
    "parameters": {
        "metal": "Pd",
        "temperature": "473",
        "gases": ["CO", "O2"],
        "partial_pressures": {"CO": 9, "O2": 18},
        "pressure": "100000",
        "steps": "200000000",
        "parent_msr_task": null  # 直接KMC任务
    }
}

输出: {
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

## 🛠️ 配置选项

```yaml
# 技能配置
skill:
  name: "chatmosp-file-organizer"
  version: "2.0.0"
  description: "智能文件系统管理器 - 支持MSR/KMC标准目录结构"
  
# 目录配置
directories:
  mosp_home: "mosp-for-chatMOSP"
  output_root: "mosp-for-chatMOSP/OUTPUT/"
  MOSP_database_dir: "mosp-for-chatMOSP/MOSP_database/"
  
# 命名配置
naming:
  msr_format: "{metal}_{gases_partial}_{temperature}K_{pressure}Pa_R{radius}"
  kmc_format: "{metal}_{gases}_{temperature}K_{pressure}Pa_{steps}steps"
  gas_separator: "_"
  partial_pressure_format: "{gas}{pressure}"
  
# 默认参数
defaults:
  temperature: "500"
  pressure: "101325"
  radius: "20"
  steps: "1000000"
  
# 安全配置
security:
  enable_path_validation: true
  allowed_paths: ["mosp-for-chatMOSP/OUTPUT/", "mosp-for-chatMOSP/MOSP_database/"]
  forbidden_patterns: ["..", "//", "~", "/root", "/etc", "*.exe", "*.sh"]
  max_path_length: 512
  allowed_characters: "a-zA-Z0-9_-.Å"
```

## 📁 文件结构

```
chatmosp-file-organizer/
├── SKILL.md           # 技能说明文档（中文版）
└── SKILL_en.md        # 技能说明文档（英文版）
```

## 🔄 更新说明

**版本 2.0.0 (2026-04-27) - 重大更新**：
1. ✅ **支持新的命名规则**：MSR和KMC任务使用不同的命名格式
2. ✅ **标准目录结构**：MSR（9个标准文件）和KMC（复杂嵌套结构）
3. ✅ **智能任务类型识别**：自动识别MSR和KMC任务并创建对应结构
4. ✅ **路径逻辑管理**：支持直接KMC任务和接续KMC任务
5. ✅ **安全增强**：TaskNameValidator支持新格式验证

**向后兼容性**：
- 旧版任务名称格式（`{金属}_{温度}K_{时间戳}`）仍然支持
- 旧版目录结构可以自动升级到新版
- API接口保持兼容，新增可选参数