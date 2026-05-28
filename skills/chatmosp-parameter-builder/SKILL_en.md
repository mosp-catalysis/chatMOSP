# Skill: chatmosp-parameter-builder (Bilingual Version)

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

**在执行任何MSR/KMC任务之前,必须遵守以下流程:**
**Before executing any MSR/KMC task, the following process MUST be followed:**

### 📋 必须遵守的执行流程 / Mandatory Execution Process

```
用户输入 → 参数构建 → ⚠️ 展示参数给用户确认 ⚠️ → 用户选择确认/修改 → 执行计算
User Input → Parameter Building → ⚠️ Display Parameters for User Confirmation ⚠️ → User Confirms/Modifies → Execute Calculation
```

### ❌ 禁止跳过参数确认步骤 / DO NOT Skip Parameter Confirmation

**无论用户请求多么明确,都必须展示参数并等待用户确认!**
**No matter how clear the user request is, you MUST display parameters and wait for user confirmation!**

**原因 / Reasons:**
1. 用户可能不了解默认参数的具体值 / Users may not know the specific values of default parameters
2. 用户可能希望修改某些参数 / Users may want to modify certain parameters (e.g., temperature, pressure, cluster size)
3. 参数确认是确保计算符合用户意图的关键步骤 / Parameter confirmation is a critical step to ensure the calculation matches user intent

### 📊 参数确认的5个选项 / 5 Parameter Confirmation Options

当参数构建完成后,必须向用户展示参数并提供以下5个选项:
When parameters are built, you MUST display them to the user and provide these 5 options:

1. **确认 / Confirm** - 使用这些参数继续 / Proceed with these parameters
2. **修改 / Modify** - 调整特定参数 / Adjust specific parameters (e.g., temperature, pressure, cluster radius, gas composition)
3. **对比 / Compare** - 运行多个条件进行对比 / Run multiple conditions for comparison (e.g., multiple temperatures, pressures, or cluster sizes)
4. **切换计算模式 / Switch Calculation Mode** - 在MSR和KMC之间切换 / Switch between MSR and KMC
5. **取消任务,更换体系 / Cancel and Change System** - 更换金属或气体体系 / Change metal or gas system

### 🔧 参数展示格式 / Parameter Display Format

⚠️ **展示规则 / Display Rules：必须严格按照下方模板格式展示参数，不得自创格式！**
⚠️ **单位说明 / Unit Note：Gas1_pp/Gas2_pp 是百分比(%)，不是压力值(Pa)。展示时必须带%号！**
⚠️ **IMPORTANT: You MUST use the template format below exactly, do NOT create your own format!**
⚠️ **Unit Note: Gas1_pp/Gas2_pp are percentages (%), NOT pressure values (Pa). MUST display with % sign!**

**必须使用以下格式展示参数 / MUST use the following format to display parameters:**

#### MSR参数展示格式 / MSR Parameter Display Format

**中文版本 / Chinese Version:**
```
📊 MSR参数已准备好,请确认:

【基本信息】
- 金属元素:Pd
- 温度:473 K (200°C)
- 压力:101325 Pa (1 atm)
- 团簇半径:50 Å
- 晶体结构:FCC (面心立方)

【气体环境】
- CO 分压:9%
- O2 分压:18%

【气体熵值】(已自动计算)
- CO 熵值:0.002356 eV/K (473K计算值)
- O2 熵值:0.002446 eV/K (473K计算值)

【表面晶面参数】
- 100 晶面:表面能 0.09 eV/Å2
- 110 晶面:表面能 0.10 eV/Å2
- 111 晶面:表面能 0.08 eV/Å2 (最稳定)

【表面吸附参数】(从input.json的Adsorption字段读取)
100 晶面:
  - CO 吸附能:E_ads = -1.50 eV
  - O2 吸附能:E_ads = -0.80 eV
110 晶面:
  - CO 吸附能:E_ads = -1.45 eV
  - O2 吸附能:E_ads = -0.75 eV
111 晶面:
  - CO 吸附能:E_ads = -1.60 eV
  - O2 吸附能:E_ads = -0.85 eV

【相互作用矩阵】(从input.json读取)
100 晶面:
  CO-CO:0.05 eV
  CO-O:0.03 eV
  O-O:0.04 eV
110 晶面:
  CO-CO:0.06 eV
  CO-O:0.04 eV
  O-O:0.05 eV
111 晶面:
  CO-CO:0.07 eV
  CO-O:0.05 eV
  O-O:0.06 eV

【输出设置】
- 任务目录:Pd_CO9_O18_473K_101325Pa_R50
- 生成文件:input.json, ini.xyz, cluster.xyz, faceinfo.txt, structure.png, rotation.gif

请选择:
1. ✅ 确认 - 使用这些参数继续执行MSR计算
2. ✏️ 修改 - 调整特定参数(如温度、压强、团簇半径、气体组成等)
3. 📊 对比 - 运行多个条件进行对比(如多个温度、压强或团簇尺寸)
4. 🔄 切换计算模式 - 切换到KMC动力学模拟
5. ❌ 取消任务,更换体系 - 更换金属或气体体系

请回复您的选择(数字1-5或关键词),或直接告诉我要修改的参数。
```

**English Version / 英文版本:**
```
📊 MSR Parameters ready, please confirm:

【Basic Information】
- Metal: Pd
- Temperature: 473 K (200°C)
- Pressure: 101325 Pa (1 atm)
- Cluster Radius: 50 Å
- Crystal Structure: FCC (Face-Centered Cubic)

【Gas Environment】
- CO Partial Pressure: 9%
- O2 Partial Pressure: 18%

【Gas Entropy Values】 (Auto-calculated)
- CO Entropy: 0.002356 eV/K (calculated at 473K)
- O2 Entropy: 0.002446 eV/K (calculated at 473K)

【Surface Facet Parameters】
- 100 facet: Surface energy 0.09 eV/Å2
- 110 facet: Surface energy 0.10 eV/Å2
- 111 facet: Surface energy 0.08 eV/Å2 (most stable)

【Surface Adsorption Parameters】 (read from Adsorption field in input.json)
100 facet:
  - CO adsorption energy: E_ads = -1.50 eV
  - O2 adsorption energy: E_ads = -0.80 eV
110 facet:
  - CO adsorption energy: E_ads = -1.45 eV
  - O2 adsorption energy: E_ads = -0.75 eV
111 facet:
  - CO adsorption energy: E_ads = -1.60 eV
  - O2 adsorption energy: E_ads = -0.85 eV

【Interaction Matrix】 (read from input.json)
  CO-CO: 0.05 eV
  CO-O2: 0.03 eV
  O2-O2: 0.04 eV

【Output Settings】
- Task directory: Pd_CO9_O18_473K_101325Pa_R50
- Generated files: input.json, ini.xyz, cluster.xyz, faceinfo.txt, structure.png, rotation.gif

Please select:
1. ✅ Confirm - Proceed with these parameters for MSR calculation
2. ✏️ Modify - Adjust specific parameters (e.g., temperature, pressure, cluster radius, gas composition)
3. 📊 Compare - Run multiple conditions for comparison (e.g., multiple temperatures, pressures, or cluster sizes)
4. 🔄 Switch Calculation Mode - Switch to KMC kinetic simulation
5. ❌ Cancel and Change System - Change metal or gas system

Please reply with your choice (number 1-5 or keyword), or directly tell me the parameters to modify.
```

#### KMC参数展示格式 / KMC Parameter Display Format

**中文版本 / Chinese Version:**
```
📊 KMC参数已准备好,请确认:

【基本信息】
- 任务类型:KMC (动力学蒙特卡洛模拟)
- 反应:CO氧化反应 (2CO + O2 → 2CO2)
- 温度:473 K (200°C)
- 压力:101325 Pa (1 atm)
- 气体分压:CO 9%, O2 18%

【团簇信息】(来自MSR结果)
- 金属元素:Pd
- 团簇半径:50 Å
- 原子数量:3,888 个
- 晶体结构:FCC (面心立方)
- MSR任务目录:Pd_CO9_O18_473K_101325Pa_R50

【模拟参数】
- 模拟步数:5,000,000 步
- 记录间隔:每10,000步记录一次
- 物种数量:5 种
- 反应事件:14 种

【物种定义】
- s1: CO (反应物)
- s2: O2 (反应物)
- s3: O (中间体)
- s4: CO2 (产物)
- s5: 空位

【产物定义】
- p1: CO2 (事件X, Y生成)

【反应机制】(简要说明)
- CO吸附、脱附、扩散
- O2解离、扩散
- CO + O → CO2

【输出设置】
- KMC任务目录:Pd_CO9_O18_473K_101325Pa_R50/KMC_5000000steps/
- 生成文件:input.json, 输出文件等

请选择:
1. ✅ 确认 - 使用这些参数继续执行KMC模拟
2. ✏️ 修改 - 调整模拟步数或其他参数(如温度、压强、气体组成等)
3. 📊 对比 - 运行多个条件进行对比(如多个温度、压强)
4. 🔄 切换计算模式 - 切换到MSR结构计算
5. ❌ 取消任务,更换体系 - 更换金属或气体体系

建议:
- 如果想快速测试,可以先运行较少步数(如100,000步)
- 500万步可以获得更准确的统计数据,但耗时更长

请回复您的选择(数字1-5或关键词),或告诉我要修改的参数。
```

**English Version / 英文版本:**
```
📊 KMC Parameters ready, please confirm:

【Basic Information】
- Task type: KMC (Kinetic Monte Carlo simulation)
- Reaction: CO oxidation (2CO + O2 → 2CO2)
- Temperature: 473 K (200°C)
- Pressure: 101325 Pa (1 atm)
- Gas partial pressure: CO 9%, O2 18%

【Cluster Information】 (from MSR results)
- Metal: Pd
- Cluster radius: 50 Å
- Number of atoms: 3,888
- Crystal structure: FCC (Face-Centered Cubic)
- MSR task directory: Pd_CO9_O18_473K_101325Pa_R50

【Simulation Parameters】
- Simulation steps: 5,000,000 steps
- Recording interval: every 10,000 steps
- Number of species: 5
- Reaction events: 14

【Species Definitions】
- s1: CO (reactant)
- s2: O2 (reactant)
- s3: O (intermediate)
- s4: CO2 (product)
- s5: vacancy

【Product Definitions】
- p1: CO2 (generated by events X, Y)

【Reaction Mechanism】 (brief description)
- CO adsorption, desorption, diffusion
- O2 dissociation, diffusion
- CO + O → CO2

【Output Settings】
- KMC task directory: Pd_CO9_O18_473K_101325Pa_R50/KMC_5000000steps/
- Generated files: input.json, output files, etc.

Please select:
1. ✅ Confirm - Proceed with these parameters for KMC simulation
2. ✏️ Modify - Adjust simulation steps or other parameters (e.g., temperature, pressure, gas composition)
3. 📊 Compare - Run multiple conditions for comparison (e.g., multiple temperatures, pressures)
4. 🔄 Switch Calculation Mode - Switch to MSR structure calculation
5. ❌ Cancel and Change System - Change metal or gas system

Suggestions:
- For quick testing, you can run fewer steps (e.g., 100,000 steps)
- 5 million steps can obtain more accurate statistical data, but takes longer

Please reply with your choice (number 1-5 or keyword), or tell me the parameters to modify.
```

---

## 📏 参数单位说明 / Parameter Units Description

### MSR参数单位 / MSR Parameter Units

#### 基本参数 / Basic Parameters
| 参数名 / Parameter | 单位 / Unit | 说明 / Description |
|--------|------|------|
| **Element** | 无单位 / Unitless | 金属元素符号 / Metal element symbol (Pd, Pt, Au, etc.) |
| **Lattice constant** | Å(埃) | 晶格常数 / Lattice constant |
| **Crystal structure** | 无单位 / Unitless | 晶体结构类型 / Crystal structure type (FCC, BCC, HCP) |
| **Pressure** | Pa | 系统压力 / System pressure |
| **Temperature** | K | 温度(开尔文)/ Temperature (Kelvin) |

#### 团簇参数 / Cluster Parameters
| 参数名 / Parameter | 单位 / Unit | 说明 / Description |
|--------|------|------|
| **Radius** | Å(埃) | 团簇半径 / Cluster radius |

#### 气体参数 / Gas Parameters
| 参数名 / Parameter | 单位 / Unit | 说明 / Description |
|--------|------|------|
| **Gas_name** | 无单位 / Unitless | 气体名称 / Gas name (CO, O2, H2, etc.) |
| **Gas_pp** | %(百分比) | 气体分压百分比 / Gas partial pressure percentage |
| **Gas_S** | eV/K | 气体熵值 / Gas entropy value |
| **Gas_type** | 无单位 / Unitless | 吸附类型 / Adsorption type (Associative/Dissociative) |

#### 晶面参数 / Surface Parameters
| 参数名 / Parameter | 单位 / Unit | 说明 / Description |
|--------|------|------|
| **Face.index** | 无单位 / Unitless | 晶面密勒指数 / Surface Miller index (100, 110, 111, etc.) |
| **Face.gamma** | eV/Å2 | 表面能 / Surface energy |
| **Face.E_ads** | eV | 吸附能 / Adsorption energy |
| **Face.S_ads** | eV/K | 吸附熵 / Adsorption entropy |
| **Face.w** | eV | 相互作用矩阵元 / Interaction matrix element |

### KMC参数单位 / KMC Parameter Units

#### 模拟参数 / Simulation Parameters
| 参数名 / Parameter | 单位 / Unit | 说明 / Description |
|--------|------|------|
| **nLoop** | 无单位(步数)/ Unitless (steps) | KMC模拟步数 / KMC simulation steps |
| **record_int** | 无单位(步数)/ Unitless (steps) | 记录间隔(步数)/ Recording interval (steps) |
| **nspecies** | 无单位 / Unitless | 物种数量 / Number of species |
| **nproducts** | 无单位 / Unitless | 产物数量 / Number of products |
| **nevents** | 无单位 / Unitless | 反应事件数量 / Number of reaction events |

#### 物种参数 / Species Parameters
| 参数名 / Parameter | 单位 / Unit | 说明 / Description |
|--------|------|------|
| **mass** | amu(原子质量单位)| 分子质量 / Molecular mass |
| **PP_ratio** | %(百分比) | 分压比例 / Partial pressure ratio |
| **S_ads** | eV/K | 吸附熵 / Adsorption entropy |
| **S_gas** | eV/K | 气体熵 / Gas entropy |
| **Ea_diff** | eV | 扩散活化能 / Diffusion activation energy |
| **sticking** | 无单位 / Unitless | 粘附系数(0-1之间)/ Sticking coefficient (0-1 range) |
| **E_ads_para** | eV | 吸附能参数 / Adsorption energy parameter |

#### 反应事件参数 / Reaction Event Parameters
| 参数名 / Parameter | 单位 / Unit | 说明 / Description |
|--------|------|------|
| **BEP_para** | eV | BEP关系参数 / BEP relationship parameter |
| **li** | eV | 晶格相互作用矩阵 / Lattice interaction matrix |

---

## 📋 KMC input.json必需字段清单 / KMC input.json Required Fields Checklist

**⚠️ 重要提示 / IMPORTANT**: KMC input.json必须包含以下所有字段,否则会导致运行失败!
KMC input.json must contain all the following fields, otherwise execution will fail!

### 顶层必需字段 / Top-level Required Fields

| 字段名 / Field | 类型 / Type | 说明 / Description | 示例 / Example |
|--------|------|------|------|
| Element | string | 金属元素 / Metal element | "Pt" |
| Lattice constant | string | 晶格常数(Å)/ Lattice constant (Å) | "3.9239" |
| Crystal structure | string | 晶体结构 / Crystal structure | "FCC" |
| Temperature | string | 温度(K)/ Temperature (K) | "850" |
| Pressure | string | 压力(Pa)/ Pressure (Pa) | "150" |
| flag_MSR | boolean | MSR标志(KMC任务必须为false)/ MSR flag (must be false for KMC tasks) | false |
| flag_KMC | boolean | KMC标志(KMC任务必须为true)/ KMC flag (must be true for KMC tasks) | true |
| KMC | object | KMC参数对象 / KMC parameter object | {...} |

### KMC部分必需字段 / KMC Section Required Fields

| 字段名 / Field | 类型 / Type | 说明 / Description | 示例 / Example |
|--------|------|------|------|
| nLoop | string | 总模拟步数 / Total simulation steps | "20000000" |
| record_int | string | 记录间隔 / Recording interval | "1000" |
| nspecies | number | 物种数量 / Number of species | 2 |
| nproducts | number | 产物数量 / Number of products | 1 |
| nevents | number | 反应事件数 / Number of reaction events | 7 |
| nevents_mob | number | 移动事件数 / Number of mobility events | 1 |
| s1 | string | 物种1定义(JSON字符串)/ Species 1 definition (JSON string) | "{\"name\": \"CO\", ...}" |
| s2 | string | 物种2定义(JSON字符串)/ Species 2 definition (JSON string) | "{\"name\": \"O\", ...}" |
| p1 | string | 产物1定义(JSON字符串)/ Product 1 definition (JSON string) | "{\"name\": \"CO2\", ...}" |
| e1 | string | 反应事件1(JSON字符串)/ Reaction event 1 (JSON string) | "{\"name\": \"CO-ads\", ...}" |
| e2 | string | 反应事件2(JSON字符串)/ Reaction event 2 (JSON string) | "{\"name\": \"CO-des\", ...}" |
| e3 | string | 反应事件3(JSON字符串)/ Reaction event 3 (JSON string) | "{\"name\": \"O2-ads\", ...}" |
| e4 | string | 反应事件4(JSON字符串)/ Reaction event 4 (JSON string) | "{\"name\": \"O2-des\", ...}" |
| e5 | string | 反应事件5(JSON字符串)/ Reaction event 5 (JSON string) | "{\"name\": \"CO-diff\", ...}" |
| e6 | string | 反应事件6(JSON字符串)/ Reaction event 6 (JSON string) | "{\"name\": \"O-diff\", ...}" |
| e7 | string | 反应事件7(JSON字符串)/ Reaction event 7 (JSON string) | "{\"name\": \"CO+O\", ...}" |
| li | array | 晶格相互作用矩阵 / Lattice interaction matrix | [[-0.187, -0.16], [-0.16, -0.176]] |

### ⚠️ 关键原则 / Key Principles

1. **必须从MOSP_database复制模板 / MUST copy template from MOSP_database**: 不要手动创建input.json / Do not create input.json manually
2. **所有顶层字段都是必需的 / All top-level fields are required**: 包括Element、Lattice constant、Crystal structure等 / Including Element, Lattice constant, Crystal structure, etc.
3. **气体熵值必须与MSR一致 / Gas entropy values must match MSR**: s1.S_gas和s2.S_gas必须使用相同的计算方法和值 / s1.S_gas and s2.S_gas must use same calculation method and values
4. **参数类型要正确 / Parameter types must be correct**: 注意string、number、boolean、object的区别 / Note the difference between string, number, boolean, object

### ✅ 检查命令 / Check Commands

```bash
# 检查顶层字段 / Check top-level fields
cat KMC任务目录/input.json | jq 'keys'

# 检查KMC部分字段 / Check KMC section fields
cat KMC任务目录/input.json | jq '.KMC | keys'

# 验证字段完整性 / Validate field completeness
python3 -c "
import json
with open('KMC任务目录/input.json') as f:
    data = json.load(f)
    required = ['Element', 'Lattice constant', 'Crystal structure', 'Temperature', 'Pressure', 'flag_MSR', 'flag_KMC', 'KMC']
    missing = [k for k in required if k not in data]
    print('Missing fields:', missing if missing else 'None')
"
```

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

**技能名称 / Skill Name**: `chatmosp-parameter-builder`
**技能类型 / Skill Type**: Intelligent Parameter Construction and Management
**核心职责 / Core Responsibility**: Parameter Query, Intelligent Completion, Gas Entropy Calculation, Validation and Generation

### 技能定位 / Skill Positioning
参数构建器是chatMOSP系统的参数智能管理中心,负责:
The parameter builder is the intelligent parameter management center of the chatMOSP system, responsible for:

1. **智能参数补全 / Intelligent Parameter Completion**: 基于MOSP_database搜索+温度替换+气体熵计算的完整参数生成
   Complete parameter generation based on MOSP_database search + temperature replacement + gas entropy calculation
2. **多源参数查询 / Multi-source Parameter Query**: 从MOSP_database、user_MOSP_database、历史、推荐源查询计算参数
   Query calculation parameters from MOSP_database, user_MOSP_database, history, recommendation sources
3. **交互式参数构建 / Interactive Parameter Construction**: 支持用户调整温度、压力、气体等参数
   Support user adjustment of temperature, pressure, gases and other parameters
4. **参数验证与完整性检查 / Parameter Validation and Completeness Check**: 确保参数格式正确、完整,符合MOSP要求
   Ensure parameter format is correct, complete, and meets MOSP requirements
5. **智能气体熵计算 / Intelligent Gas Entropy Calculation**: 基于温度自动计算和调整气体熵值
   Automatically calculate and adjust gas entropy values based on temperature

## 🔍 Parameter Query Types / 参数查询类型

### 1. View Current Task Parameters / 查看当前任务参数
**User Intent**: View specific parameter values of current MSR/KMC task
**Trigger Words**: `show parameters`, `current parameters`, `this task parameters`, `detailed parameters`
**Response**: Read and display the input.json content of current task

Example Response:
```json
{
  "Element": "Pt",
  "Temperature": "800 K",
  "Pressure": "500 Pa",
  "MSR": {
    "Radius": "20 Å",
    "Gas1": "CO (60%, Associative)",
    "Gas2": "O2 (40%, Dissociative)"
  }
}
```

### 2. View Parameter Documentation / 查看参数文档
**User Intent**: Understand parameter meanings, ranges, default values
**Trigger Words**: `parameter documentation`, `parameter types`, `parameter explanation`
**Response**: Display parameter types, descriptions, example values table

### ⚠️ Important Note / 重要说明
When user asks "show me the detailed parameters", **prioritize understanding as viewing current task parameters**, unless explicitly requesting "parameter documentation".

---

## 🎯 核心功能 / Core Functions

### 1. 智能参数补全系统 / Intelligent Parameter Completion System

#### 1.1 Examples搜索与参数补全流程 / Examples Search and Parameter Completion Process
当用户输入部分参数时,自动搜索MOSP_database目录并补全完整参数:
When user inputs partial parameters, automatically search MOSP_database directory and complete full parameters:

```
用户输入 → 提取基本参数(金属、温度) → 搜索MOSP_database匹配文件 →
User input → Extract basic parameters (metal, temperature) → Search MOSP_database matching files →
加载匹配的example文件 → 替换温度参数 → 计算气体熵 → 生成完整input.json
Load matching example file → Replace temperature parameters → Calculate gas entropy → Generate complete input.json
```

#### 1.2 参数补全算法 / Parameter Completion Algorithm
1. **金属匹配 / Metal Matching**: 精确匹配金属元素(Pd, Pt, Au等) / Exact matching of metal elements (Pd, Pt, Au, etc.)
2. **气体匹配 / Gas Matching**: 气体种类集合匹配(CO+O2 → 匹配CO氧化环境) / Gas type set matching (CO+O2 → match CO oxidation environment)
3. **MOSP_database搜索 / Examples Search**: 在`mosp-for-chatMOSP/MOSP_database/`目录中搜索 / Search in `mosp-for-chatMOSP/MOSP_database/` directory
4. **最佳匹配选择 / Best Match Selection**: 选择金属和气体匹配度最高的example文件 / Select example file with highest metal and gas matching degree
5. **参数替换 / Parameter Replacement**: 保持example中的默认参数,替换用户指定的温度等参数 / Keep default parameters in example, replace user-specified parameters like temperature

#### 1.3 默认参数使用逻辑 / Default Parameter Usage Logic
- **用户指定参数 / User-specified Parameters**: 优先使用用户明确指定的参数 / Prioritize user-explicitly specified parameters
- **MOSP_database参数 / Examples Parameters**: 用户未指定的参数使用MOSP_database中的默认值 / Use default values from MOSP_database for parameters not specified by user
- **系统默认值 / System Default Values**: 上述都没有时使用系统预设默认值 / Use system preset default values when none of the above exist

#### 1.4 参数完整性检查与处理 / Parameter Completeness Check and Handling

当MOSP_database中找到匹配文件但参数不完整时,需要进行参数完整性检查和处理。
/ When a matching file is found in MOSP_database but parameters are incomplete, parameter completeness check and handling is required.

**步骤1:检查参数完整性 / Step 1: Check Parameter Completeness**

检查以下必需字段是否为空 / Check if the following required fields are empty:
- **MSR关键参数 / MSR Key Parameters**: E_ads(吸附能 / adsorption energy)、w(相互作用矩阵 / interaction matrix)、gamma(表面能 / surface energy)
- **MSR次要参数 / MSR Secondary Parameters**: Gas1_S、Gas2_S(气体熵,可自动计算 / gas entropy, can be auto-calculated)
- **KMC关键参数 / KMC Key Parameters**: E_ads_para、BEP_para、li(晶格相互作用 / lattice interaction)

**步骤2:根据缺失参数的重要性决定处理方式 / Step 2: Decide Handling Method Based on Missing Parameter Importance**

**情况A：关键参数缺失 / Case A: Key Parameters Missing**（E_ads, w, gamma等 / etc.）

**步骤1：向用户说明参数缺失情况 / Step 1: Explain Parameter Missing to User**
```
{metal}.json缺少关键数据（如吸附能、相互作用矩阵）
{metal}.json lacks key data (e.g., adsorption energy, interaction matrix)
```

**步骤2：提供选项供用户选择 / Step 2: Provide Options for User Selection**

请选择处理方式 / Please select handling method：
1. **进行文献检索补全（开放获取期刊）/ Literature search completion (Open access journals)** - 优先检索Nature Communications, Science Advances, PNAS, ACS Central Science, Chemical Science等开放获取期刊（无需付费，访问便捷）/ Priority search on open access journals like Nature Communications, Science Advances, PNAS, ACS Central Science, Chemical Science (no payment required, easy access)
2. **进行文献检索补全（付费期刊）/ Literature search completion (Paid journals)** - 检索Science, Nature, JACS, Angewandte Chemie等付费期刊（请确保已付费，拥有访问权限）/ Search paid journals like Science, Nature, JACS, Angewandte Chemie (please ensure you have paid and have access)
3. **直接指定参数 / Directly specify parameters** - 如果您已知参数值，可直接输入 / If you know parameter values, you can input directly
4. **取消任务（更换体系）/ Cancel task (Change system)** - 更换金属或气体体系 / Change metal or gas system

**步骤3：根据用户选择执行相应操作 / Step 3: Execute Operation Based on User Selection**
- 选择1或2 / Select 1 or 2：调用`chatmosp-literature-search`技能，传递期刊类型（开放获取/付费）/ Call `chatmosp-literature-search` skill, pass journal type (open access/paid)
- 选择3 / Select 3：等待用户输入参数值 / Wait for user to input parameter values
- 选择4 / Select 4：结束当前任务，询问用户新的金属或气体体系 / End current task, ask user for new metal or gas system

**情况B:次要参数缺失 / Case B: Secondary Parameters Missing**(Gas1_S, Gas2_S等 / etc.)
- 次要参数可自动计算或使用默认值 / Secondary parameters can be auto-calculated or use default values
- 气体熵值:根据温度自动计算(使用气体熵计算公式)/ Gas entropy: auto-calculate based on temperature (using gas entropy calculation formula)
- 向用户说明:`"部分参数将使用默认值或自动计算(如气体熵值)"` / Explain to user: `"Some parameters will use default values or be auto-calculated (e.g., gas entropy)"`

**情况C:用户可提供的参数 / Case C: User-Providable Parameters**
- 询问用户是否有已知的参数值 / Ask user if they have known parameter values
- 如果用户提供参数 → 使用用户提供的值 / If user provides parameters → Use user-provided values
- 如果用户不知道 → 调用`chatmosp-literature-search` / If user doesn't know → Call `chatmosp-literature-search`

**步骤3:参数补全流程 / Step 3: Parameter Completion Process**

```
读取MOSP_database文件 / Read MOSP_database file → 检查参数完整性 / Check parameter completeness → 识别缺失参数 / Identify missing parameters →
判断参数重要性 / Judge parameter importance → 选择处理方式(文献检索/自动计算/用户输入)/ Select handling method (literature search/auto-calculation/user input) →
展示完整参数 / Display complete parameters → 用户确认 / User confirmation
```

**示例:Pd.json缺少关键参数 / Example: Pd.json Lacks Key Parameters**

```
用户请求 / User Request: Pd在CO氧化条件下结构 / Pd structure under CO oxidation conditions

检查Pd.json / Check Pd.json:
- ✅ 基本信息 / Basic Info: Element=Pd, Lattice constant=3.8907, Crystal structure=FCC
- ✅ 表面能 / Surface Energy: gamma(100)=0.145, gamma(110)=0.152, gamma(111)=0.125
- ❌ 吸附能 / Adsorption Energy: E_ads全部为空 / All E_ads are empty
- ❌ 相互作用矩阵 / Interaction Matrix: w大部分为空 / Most w are empty

处理方式 / Handling Method:
1. 向用户说明 / Explain to user: "Pd.json缺少关键数据(吸附能、相互作用矩阵)" / "Pd.json lacks key data (adsorption energy, interaction matrix)"
2. 调用chatmosp-literature-search检索Pd CO氧化相关文献 / Call chatmosp-literature-search to retrieve Pd CO oxidation related literature
3. 从文献中提取缺失参数 / Extract missing parameters from literature
4. 展示完整参数给用户确认 / Display complete parameters to user for confirmation
```

### 2. 找不到匹配example时的文献搜索流程 / Literature Search Process When No Matching Example Found

#### 2.1 调用独立技能:chatmosp-literature-search / Call Independent Skill: chatmosp-literature-search

当MOSP_database中没有找到匹配的参数时,调用`chatmosp-literature-search`技能进行文献搜索。
/ When no matching parameters are found in MOSP_database, call the `chatmosp-literature-search` skill to perform literature search.

**调用方式 / Call Method**:
```
调用技能 / Call Skill: chatmosp-literature-search
输入参数 / Input Parameters:
- 金属元素 / Metal element: 如 Pd, Pt, Au, Cu等 / e.g., Pd, Pt, Au, Cu, etc.
- 气体体系 / Gas system: 如 CO+O2, H2+CO2等 / e.g., CO+O2, H2+CO2, etc.
- 温度范围 / Temperature range: (可选) / (optional)
- 压力范围 / Pressure range: (可选) / (optional)
```

**返回结果 / Return Results**:
```
参数表格 / Parameter Table, 包含 / including:
- 表面能(各晶面)/ Surface energy (each facet)
- 吸附能(各晶面 + 各气体)/ Adsorption energy (each facet + each gas)
- 相互作用矩阵 / Interaction matrix
- 参数来源(DOI、文献标题)/ Parameter source (DOI, article title)
- 参数完整性评分(1-10分)/ Parameter completeness score (1-10 points)
```

#### 2.2 处理返回结果 / Process Return Results

根据`chatmosp-literature-search`返回的参数完整性评分,决定下一步操作:
/ Decide next steps based on the parameter completeness score returned by `chatmosp-literature-search`:

**⚠️ 重要：文献搜索后必须计算气体熵！/ IMPORTANT: Gas entropy MUST be calculated after literature search!**

文献搜索返回的参数**不包含**气体熵值(Gas_S/S_gas)。无论完整性评分多少，在组装input.json之前，必须根据用户指定的温度自动计算气体熵值：
/ Parameters returned by literature search do **NOT** include gas entropy (Gas_S/S_gas). Regardless of completeness score, gas entropy MUST be automatically calculated based on user-specified temperature before assembling input.json:

```
文献搜索返回参数 → 提取E_ads, w, gamma → ✅ 根据温度计算Gas_S/S_gas → 组装完整input.json
Literature search returns → Extract E_ads, w, gamma → ✅ Calculate Gas_S/S_gas based on temperature → Assemble complete input.json
```

计算公式 / Calculation formula: `S(eV/K) = (a × T^b) / 96485`

**完整性评分 9-10分 / Completeness Score 9-10 points**:
- 参数完整,可直接使用 / Parameters complete, ready to use
- ✅ 仍需计算气体熵值 / Still need to calculate gas entropy
- 展示参数给用户确认 / Display parameters for user confirmation

**完整性评分 7-8分 / Completeness Score 7-8 points**:
- 参数较完整,可以使用 / Parameters mostly complete, usable
- ✅ 仍需计算气体熵值 / Still need to calculate gas entropy
- 需要用户确认缺失的参数 / Need user to confirm missing parameters

**完整性评分 5-6分 / Completeness Score 5-6 points**:
- 参数部分完整,需要补充 / Parameters partially complete, need supplement
- ✅ 仍需计算气体熵值 / Still need to calculate gas entropy
- 向用户说明缺失的参数,建议补充方案 / Explain missing parameters to user, suggest supplement solutions

**完整性评分 3-4分 / Completeness Score 3-4 points**:
- 参数不完整,建议使用替代方案 / Parameters incomplete, recommend alternative solutions
- 如:使用相似金属的参数作为参考 / e.g., use parameters from similar metals as reference

**完整性评分 1-2分 / Completeness Score 1-2 points**:
- 参数极不完整,不推荐使用 / Parameters very incomplete, not recommended
- 建议用户提供已知参数来源或使用默认参数 / Suggest user provide known parameter source or use default parameters

#### 2.3 详细流程请参考 / Detailed Process Please Refer To

文献搜索的详细流程、期刊搜索平台优先级、文章检索流程、参数提取方法等内容,请参考:
/ For detailed processes of literature search, journal search platform priorities, article retrieval procedures, parameter extraction methods, please refer to:
- **chatmosp-literature-search/SKILL.md**(中文版 / Chinese version)
- **chatmosp-literature-search/SKILL_en.md**(英文版 / English version)

#### 2.4 相互作用参数转换 / Interaction Parameter Conversion

**⚠️ 重要说明 / IMPORTANT**: 只在接收到文献检索参数时才触发检测和转换,Database自带的参数不会处理(假设已经是正确的格式)。/ Only trigger detection and conversion when receiving literature-retrieved parameters. Database built-in parameters will not be processed (assumed to be in correct format).

##### MSR vs KMC定义 / MSR vs KMC Definitions

**MSR使用"满吸附相互作用" / MSR uses "Full Adsorption Interaction"**:
- 定义:满吸附时的总相互作用能 / Definition: Total interaction energy at full adsorption
- 数值范围:通常 > 0.5 eV / Typical range: > 0.5 eV
- 用途:MSR计算 / Usage: MSR calculation

**KMC使用"单个相邻原子相互作用" / KMC uses "Single Adjacent Atom Interaction"**:
- 定义:单个相邻吸附原子之间的相互作用 / Definition: Interaction between single adjacent adsorbed atoms
- 数值范围:通常 < 0.3 eV / Typical range: < 0.3 eV
- 用途:KMC模拟 / Usage: KMC simulation

##### 判断标准 / Judgment Criteria

**如果所有相互作用能 < 0.3 eV / If all interaction energies < 0.3 eV**:
- 这是KMC格式 / This is KMC format
- MSR任务需要转换为MSR格式 / MSR task requires conversion to MSR format

**如果存在相互作用能 > 0.5 eV / If any interaction energy > 0.5 eV**:
- 这是MSR格式 / This is MSR format
- 不需要转换 / No conversion needed

**如果一个文献的话,wCO、wO、wCO,O应该一起判定 / For one literature source, wCO, wO, wCO,O should be judged together**:
- 不要分开判定 / Do not judge separately
- 如果所有相互作用能 < 0.3 eV → KMC格式 / If all interaction energies < 0.3 eV → KMC format
- 如果存在相互作用能 > 0.5 eV → MSR格式 / If any interaction energy > 0.5 eV → MSR format

##### 转换公式 / Conversion Formula

**MSR参数 = KMC参数 × 相邻位点数 / MSR parameter = KMC parameter × Coordination number**

**相邻位点数 / Coordination Numbers**:
- (100) 晶面:4个相邻位点 / 4 adjacent sites
- (110) 晶面:2个相邻位点 / 2 adjacent sites
- (111) 晶面:6个相邻位点 / 6 adjacent sites

##### 转换时机与流程 / Conversion Timing and Process

**步骤1:判断参数来源 / Step 1: Determine Parameter Source**
- Database参数 → 不转换,直接使用 / Database parameters → No conversion, use directly
- 文献检索参数 → 进入步骤2 / Literature-retrieved parameters → Go to Step 2

**步骤2:判断参数格式 / Step 2: Determine Parameter Format**
- 检测相互作用参数数值 / Check interaction parameter values
- 如果所有值 < 0.3 eV → KMC格式 / If all values < 0.3 eV → KMC format
- 如果存在值 > 0.5 eV → MSR格式 / If any value > 0.5 eV → MSR format

**步骤3:根据任务类型决定是否转换 / Step 3: Decide Conversion Based on Task Type**

**MSR任务 / MSR Task**:
- 如果参数是KMC格式 → 需要转换为MSR格式 / If KMC format → Convert to MSR format
- 如果参数是MSR格式 → 不需要转换 / If MSR format → No conversion needed

**KMC任务 / KMC Task**:
- 如果参数是KMC格式 → 不需要转换 / If KMC format → No conversion needed
- 如果参数是MSR格式 → 需要转换为KMC格式(KMC参数 = MSR参数 ÷ 相邻位点数)/ If MSR format → Convert to KMC format (KMC parameter = MSR parameter ÷ Coordination number)

**步骤4:执行转换 / Step 4: Execute Conversion**
- 根据转换公式计算转换后的值 / Calculate converted values using conversion formula
- 更新参数值 / Update parameter values

**步骤5:验证转换结果 / Step 5: Validate Conversion Results**
- 检查转换后的值是否在合理范围内 / Check if converted values are within reasonable range
- 向用户说明转换过程和结果 / Explain conversion process and results to user

##### 转换示例 / Conversion Example

**示例:Pd CO氧化 - 从文献提取的KMC格式参数 / Example: Pd CO oxidation - KMC format parameters from literature**

**原始数据(KMC格式)/ Original Data (KMC format)**:
```
(100) 晶面:wCO-CO = -0.149 eV
(110) 晶面:wCO-CO = -0.159 eV
(111) 晶面:wCO-CO = -0.168 eV
```

**判断 / Judgment**: 所有值 < 0.3 eV → KMC格式 / All values < 0.3 eV → KMC format

**任务类型 / Task Type**: MSR任务 / MSR task

**转换 / Conversion**:
```
(100) 晶面:wCO-CO = -0.149 × 4 = -0.596 eV
(110) 晶面:wCO-CO = -0.159 × 2 = -0.318 eV
(111) 晶面:wCO-CO = -0.168 × 6 = -1.008 eV
```

**转换后(MSR格式)/ After Conversion (MSR format)**:
```
(100) 晶面:wCO-CO = -0.596 eV
(110) 晶面:wCO-CO = -0.318 eV
(111) 晶面:wCO-CO = -1.008 eV
```

##### 参数格式标注 / Parameter Format Annotation

在展示参数给用户确认时,应该标注参数格式:
/ When displaying parameters for user confirmation, parameter format should be annotated:
```
【相互作用矩阵】(从文献提取,KMC格式,已转换为MSR格式)
/ 【Interaction Matrix】(From literature, KMC format, converted to MSR format)
100 晶面 / 100 facet:
  CO-CO:-0.596 eV (原始值 / original value:-0.149 eV × 4)
  ...
```

### 3. 气体熵计算系统 / Gas Entropy Calculation System

#### 3.1 气体熵计算公式 / Gas Entropy Calculation Formula

**熵值计算公式 / Entropy Calculation Formula**:
```
S(J/K/mol) = a × T(K)^b
S(eV/K) = (a × T^b) / 96485
```

其中 / Where:
- a, b 是气体特定的参数 / are gas-specific parameters
- T 是温度(K)/ is temperature (K)
- 96485 是J到eV的转换因子(1 eV = 96485 J)/ is conversion factor from J to eV (1 eV = 96485 J)

#### 3.2 支持的气体参数 / Supported Gas Parameters

| 气体 / Gas | a (系数 / Coefficient) | b (指数 / Exponent) |
|-----------|------------------------|--------------------|
| H2 | 41.362 | 0.201 |
| N2 | 82.394 | 0.148 |
| O2 | 90.454 | 0.143 |
| CO2 | 76.458 | 0.181 |
| CO | 85.142 | 0.147 |
| NO | 93.121 | 0.143 |
| H2O | 64.234 | 0.18665 |
| NO2 | 93.02 | 0.1668 |

**注意 / Note**:参数通过0~6000K范围拟合获得,无温度范围限制。/ Parameters obtained from 0~6000K range fitting, no temperature range limitation.

#### 3.3 气体熵计算示例 / Gas Entropy Calculation Examples

**示例1:CO在473K的熵值 / Example 1: CO entropy at 473K**
```
S(J/K/mol) = 85.142 × 473^0.147 = 85.142 × 2.47 = 210.5 J/K/mol
S(eV/K) = 210.5 / 96485 = 0.00218 eV/K
```

**示例2:O2在473K的熵值 / Example 2: O2 entropy at 473K**
```
S(J/K/mol) = 90.454 × 473^0.143 = 90.454 × 2.41 = 218.2 J/K/mol
S(eV/K) = 218.2 / 96485 = 0.00226 eV/K
```

#### 3.4 MSR和KMC的气体熵字段 / Gas Entropy Fields for MSR and KMC

**MSR的气体熵字段 / MSR Gas Entropy Fields**:
- Gas1_S: 第一种气体的熵值(eV/K)/ First gas entropy (eV/K)
- Gas2_S: 第二种气体的熵值(eV/K)/ Second gas entropy (eV/K)

**KMC的气体熵字段 / KMC Gas Entropy Fields**:
- s1.S_gas: 第一种物种的气体熵值(eV/K)/ First species gas entropy (eV/K)
- s2.S_gas: 第二种物种的气体熵值(eV/K)/ Second species gas entropy (eV/K)



#### 3.5 Interactive Temperature Modification: Gas Entropy Recalculation / 交互式修改温度后的气体熵重算

**When user selects "Modify" during parameter confirmation and changes temperature, gas entropy MUST be recalculated!**
**当用户在参数确认阶段选择"修改"并改变温度时，必须重新计算气体熵！**

Process / 处理流程:
1. Get the user's new temperature T_new / 获取用户修改后的新温度值
2. Use the formula from §3.1: S = (a × T^b) / 96485 to recalculate entropy for each gas / 使用§3.1公式重新计算每种气体的熵值
3. Update Gas1_S and Gas2_S in input.json / 更新input.json中的Gas1_S和Gas2_S
4. Present updated parameters (including new entropy values) to user / 展示更新后的参数给用户

**Example / 示例**: Temperature change from 500K to 800K / 温度从500K改为800K
- CO: S(500K) = 0.002200 eV/K → S(800K) = 0.002357 eV/K ✅ MUST update / 必须更新
- O2: S(500K) = 0.002285 eV/K → S(800K) = 0.002446 eV/K ✅ MUST update / 必须更新

**Verification / 验证**: Modified entropy values must match formula calculation from §3.1 / 修改后的熵值必须与§3.1公式计算结果一致。


### 4. 温度替换系统 / Temperature Replacement System

#### 4.1 温度替换流程 / Temperature Replacement Process

从MOSP_database匹配example文件后,需要根据用户指定的温度更新参数:
/ After matching example file from MOSP_database, need to update parameters based on user-specified temperature:

**步骤1:读取example中的温度 / Step 1: Read temperature from example**
```
example文件温度 / Example file temperature: T_example (如 473K / e.g., 473K)
```

**步骤2:用户指定温度 / Step 2: User-specified temperature**
```
用户指定温度 / User-specified temperature: T_user (如 600K / e.g., 600K)
```

**步骤3:更新温度相关参数 / Step 3: Update temperature-related parameters**
- 更新温度字段 / Update temperature field: `Temperature = T_user`
- 更新气体熵值 / Update gas entropy: 根据T_user重新计算 / recalculate based on T_user

**步骤4:保留其他参数 / Step 4: Keep other parameters**
- 表面能、吸附能、相互作用矩阵等参数保持不变 / Surface energy, adsorption energy, interaction matrix parameters remain unchanged
- 这些参数是温度无关的(在example中已经提供)/ These parameters are temperature-independent (already provided in example)



### 5. 参数验证系统 / Parameter Validation System

- **格式验证 / Format Validation**: 确保JSON格式正确,包含所有必需字段 / Ensure JSON format is correct, contains all required fields
- **范围验证 / Range Validation**: 温度、压力、团簇尺寸等在合理范围内 / Temperature, pressure, cluster size within reasonable ranges
- **一致性验证 / Consistency Validation**: 气体种类与分压设置一致 / Gas species and partial pressure settings are consistent
- **完整性验证 / Completeness Validation**: MSR和KMC任务的必需参数齐全 / Required parameters for MSR and KMC tasks are complete


### 依赖关系 / Dependencies
- `literature-review` - 文献搜索(可选,用于User-Examples)/ Literature search (optional, for User-Examples)
- `chatmosp-file-organizer` - 获取MOSP_database目录路径 / Get MOSP_database directory path
- `chatmosp-input-coordinator` - 获取任务类型信息 / Get task type information

### 执行流程 / Execution Flow
```
用户输入 → 参数提取 → MOSP_database搜索 → 参数匹配 → 温度替换 →
User input → Parameter extraction → Examples search → Parameter matching → Temperature replacement →
气体熵计算 → 参数验证 → 生成input.json → 返回完整参数
Gas entropy calculation → Parameter validation → Generate input.json → Return complete parameters
```

### 智能参数补全详细流程 / Intelligent Parameter Completion Detailed Process

#### 场景:用户输入"Pd在CO氧化环境下200摄氏度结构" / Scenario: User input "Pd structure under CO oxidation environment at 200°C"

1. **参数提取 / Parameter Extraction**:
   - 金属 / Metal: Pd
   - 温度 / Temperature: 200°C → 473K(转换 / Conversion)
   - 气体 / Gases: ["CO"](推断CO氧化环境需要CO和O2 / Infer CO oxidation environment needs CO and O2)

2. **MOSP_database搜索 / Examples Search**:
   - 搜索目录 / Search directory: `mosp-for-chatMOSP/MOSP_database/`
   - 匹配条件 / Matching conditions: 金属=Pd, 气体包含CO和O2 / Metal=Pd, gases include CO and O2
   - 找到文件 / Found file: `Pd_CO9_O18_500K_101325Pa_R20.json`

3. **参数加载与替换 / Parameter Loading and Replacement**:
   - 加载example文件的所有参数 / Load all parameters from example file
   - 替换温度 / Replace temperature: 500K → 473K
   - 保持其他参数 / Keep other parameters: 分压(CO9_O18)、压力(101325Pa)、尺寸(R20) / Partial pressures (CO9_O18), pressure (101325Pa), size (R20)

4. **气体熵计算 / Gas Entropy Calculation**:
   - 计算CO在473K的熵值 / Calculate CO entropy at 473K
   - 计算O2在473K的熵值 / Calculate O2 entropy at 473K
   - 替换原熵值参数 / Replace original entropy parameters

5. **生成完整input.json / Generate Complete input.json**:
   - 包含所有必需参数 / Contains all required parameters
   - 格式符合MOSP要求 / Format meets MOSP requirements
   - 可用于MSR计算 / Can be used for MSR calculation

## 📝 使用示例 / Usage Examples

### 示例1:智能参数补全 / Example 1: Intelligent Parameter Completion
```
用户输入 / User input: "Pd在CO氧化环境下200摄氏度结构"

系统处理 / System processing:
1. 提取参数 / Extract parameters: metal=Pd, temperature=473K, gases=["CO"]
2. 搜索MOSP_database / Search MOSP_database: 找到 Pd_CO9_O18_500K_101325Pa_R20.json / Found Pd_CO9_O18_500K_101325Pa_R20.json
3. 替换温度 / Replace temperature: 500K → 473K
4. 计算气体熵 / Calculate gas entropy: CO(473K)=..., O2(473K)=...
5. 输出完整参数 / Output complete parameters:
   {
     "Element": "Pd",
     "Temperature": "473",
     "Pressure": "101325",
     "Gases": ["CO", "O2"],
     "PartialPressures": {"CO": 9, "O2": 18},
     "ClusterRadius": "20",
     "GasEntropies": {...}
   }
```

### 示例2:直接KMC参数生成 / Example 2: Direct KMC Parameter Generation
```
用户输入 / User input: "运行Pd的CO氧化KMC模拟,温度473K,200万步"

系统处理 / System processing:
1. 识别任务类型 / Identify task type: KMC
2. 提取参数 / Extract parameters: metal=Pd, temperature=473K, steps=2000000
3. 搜索MOSP_database / Search MOSP_database: 找到 Pd_CO9_O18_500K_101325Pa_1000000steps.json
4. 替换参数 / Replace parameters: 温度→473K, 步数→2000000 / Temperature→473K, steps→2000000
5. 输出KMC参数文件 / Output KMC parameter file
```

## 🛠️ 配置选项 / Configuration Options

```yaml
# 技能配置 / Skill Configuration
skill:
  name: "chatmosp-parameter-builder"
  version: "2.0.0"
  description: "智能参数构建器 - 支持MOSP_database搜索和气体熵计算 / Intelligent Parameter Builder - Supports MOSP_database search and gas entropy calculation"

# 参数源配置 / Parameter Source Configuration
parameter_sources:
  MOSP_database_dir: "mosp-for-chatMOSP/MOSP_database/"
  user_MOSP_database_dir: "mosp-for-chatMOSP/user_MOSP_database/"
  history_dir: "mosp-for-chatMOSP/OUTPUT/_history/"

# 智能补全配置 / Intelligent Completion Configuration
completion:
  enable_MOSP_database_search: true
  gas_entropy_calculation: true
  auto_temperature_conversion: true  # °C → K自动转换 / °C → K automatic conversion
  default_pressure: "101325"
  default_radius: "20"
  default_steps: "1000000"

# 匹配配置 / Matching Configuration
matching:
  metal_weight: 3.0
  temperature_weight: 2.0
  gas_weight: 2.5
  partial_pressure_weight: 1.5

# 气体熵计算配置 / Gas Entropy Calculation Configuration
gas_entropy:
  enable_calculation: true
  supported_gases: ["H2", "N2", "O2", "CO2", "CO", "NO", "H2O"]
  conversion_factor: 96485  # J/mol·K → eV/K
  validation_tolerance: 0.003  # 3%误差容忍度 / 3% error tolerance

# 输出配置 / Output Configuration
output:
  format: "json"
  include_metadata: true
  include_calculation_log: true
  backup_original: true
```

## 📁 文件结构 / File Structure

```
chatmosp-parameter-builder/
├── SKILL.md           # 技能说明文档（中文版）/ Skill documentation (Chinese version)
└── SKILL_en.md        # 技能说明文档（英文版）/ Skill documentation (English version)
```

## 🌐 语言一致性 / Language Consistency

### 响应语言策略 / Response Language Strategy
1. **自动语言检测 / Automatic Language Detection**: 根据用户输入自动检测语言 / Automatically detect language based on user input
2. **一致性响应 / Consistent Response**: 英文输入得到英文回复,中文输入得到中文回复 / English input gets English reply, Chinese input gets Chinese reply
3. **双语支持 / Bilingual Support**: 根据用户语言选择SKILL.md或SKILL_en.md / Select SKILL.md or SKILL_en.md based on user language

### 示例 / Examples
- 英文输入 "Show me the Pd structure" → 英文回复,使用SKILL_en.md / English reply, use SKILL_en.md
- 中文输入 "生成Pd团簇" → 中文回复,使用SKILL.md / Chinese reply, use SKILL.md

### 关键原则 / Key Principles
- 气体熵计算与语言无关,确保科学计算准确性 / Gas entropy calculation is language-independent, ensuring scientific accuracy
- 文件保存使用通用JSON格式 / File saving uses universal JSON format
## 🔄 更新说明 / Update Notes

**版本 2.0 (2026-05) - 文档驱动架构 / Document-Driven Architecture**:
- 技能文档（SKILL.md/SKILL_en.md）作为AI操作指南，不再使用Python代码 / Skill documents (SKILL.md/SKILL_en.md) serve as AI operation guides, no Python code used
- 智能参数补全 / Intelligent parameter completion based on MOSP_database
- 气体熵自动计算 / Automatic gas entropy calculation for 7 gases
- 相互作用参数转换 / Automatic MSR/KMC interaction parameter conversion
- 文献搜索集成 / Literature search integration when MOSP_database lacks data
- 用户确认流程 / 5-option interactive parameter confirmation