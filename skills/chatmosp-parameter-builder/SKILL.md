# Skill: chatmosp-parameter-builder

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

## ⚠️ 重要提示:必须进行参数确认

**在执行任何MSR/KMC任务之前,必须遵守以下流程:**

### 📋 必须遵守的执行流程

```
用户输入 → 参数构建 → ⚠️ 展示参数给用户确认 ⚠️ → 用户选择确认/修改 → 执行计算
```

### ❌ 禁止跳过参数确认步骤

**无论用户请求多么明确,都必须展示参数并等待用户确认!**

**原因**:
1. 用户可能不了解默认参数的具体值
2. 用户可能希望修改某些参数(如温度、压力、团簇尺寸)
3. 参数确认是确保计算符合用户意图的关键步骤

### 📊 参数确认的5个选项

当参数构建完成后,必须向用户展示参数并提供以下5个选项:

1. **确认** - 使用这些参数继续
2. **修改** - 调整特定参数(例如:温度、压力、团簇半径、气体组成)
3. **对比** - 运行多个条件进行对比(例如:多个温度、压强或团簇尺寸)
4. **切换计算模式** - 在MSR和KMC之间切换
5. **取消任务,更换体系** - 更换金属或气体体系

### 🔧 参数展示格式

**必须使用以下格式展示参数:**

#### MSR参数展示格式

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

#### KMC参数展示格式

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

---

## 📏 参数单位说明

### MSR参数单位

#### 基本参数
| 参数名 | 单位 | 说明 |
|--------|------|------|
| **Element** | 无单位 | 金属元素符号(Pd, Pt, Au等) |
| **Lattice constant** | Å(埃) | 晶格常数 |
| **Crystal structure** | 无单位 | 晶体结构类型(FCC, BCC, HCP) |
| **Pressure** | Pa | 系统压力 |
| **Temperature** | K | 温度(开尔文) |

#### 团簇参数
| 参数名 | 单位 | 说明 |
|--------|------|------|
| **Radius** | Å(埃) | 团簇半径 |

#### 气体参数
| 参数名 | 单位 | 说明 |
|--------|------|------|
| **Gas_name** | 无单位 | 气体名称(CO, O2, H2等) |
| **Gas_pp** | %(百分比) | 气体分压百分比 |
| **Gas_S** | eV/K | 气体熵值 |
| **Gas_type** | 无单位 | 吸附类型(Associative/Dissociative) |

#### 晶面参数
| 参数名 | 单位 | 说明 |
|--------|------|------|
| **Face.index** | 无单位 | 晶面密勒指数(100, 110, 111等) |
| **Face.gamma** | eV/Å2 | 表面能 |
| **Face.E_ads** | eV | 吸附能 |
| **Face.S_ads** | eV/K | 吸附熵 |
| **Face.w** | eV | 相互作用矩阵元 |

### KMC参数单位

#### 模拟参数
| 参数名 | 单位 | 说明 |
|--------|------|------|
| **nLoop** | 无单位(步数) | KMC模拟步数 |
| **record_int** | 无单位(步数) | 记录间隔(步数) |
| **nspecies** | 无单位 | 物种数量 |
| **nproducts** | 无单位 | 产物数量 |
| **nevents** | 无单位 | 反应事件数量 |

#### 物种参数
| 参数名 | 单位 | 说明 |
|--------|------|------|
| **mass** | amu(原子质量单位) | 分子质量 |
| **PP_ratio** | %(百分比) | 分压比例 |
| **S_ads** | eV/K | 吸附熵 |
| **S_gas** | eV/K | 气体熵 |
| **Ea_diff** | eV | 扩散活化能 |
| **sticking** | 无单位 | 粘附系数(0-1之间) |
| **E_ads_para** | eV | 吸附能参数 |

#### 反应事件参数
| 参数名 | 单位 | 说明 |
|--------|------|------|
| **BEP_para** | eV | BEP关系参数 |
| **li** | eV | 晶格相互作用矩阵 |

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

## 🎯 参数构建原则

### ⚠️ 核心原则:MSR和KMC参数完全分离

#### 1. MSR任务参数:
- 从MOSP_database文件复制**MSR相关参数**
- **只包含MSR部分**
- **不包含KMC参数**
- MSR的input.json结构:
  ```json
  {
    "Element": "Pd",
    "Temperature": "473",
    "Pressure": "101325",
    "flag_MSR": true,
    "flag_KMC": false,
    "MSR": { ... },
    "Gas": { ... },
    "Adsorption": { ... }
  }
  ```

#### 2. KMC任务参数:
- 从MOSP_database文件复制**完整KMC参数**
- **包含所有必需字段**:
  - nspecies, nproducts, nevents
  - s1, s2(物种定义)
  - p1(产物定义)
  - e1-e7(反应事件)
  - li(晶格相互作用)
- 根据用户输入调整:
  - nLoop: 模拟步数
  - T: 温度
  - gas_pp: 气体分压
  - record_int: 记录间隔
- KMC的input.json结构:
  ```json
  {
    "Element": "Pd",
    "Temperature": "473",
    "flag_MSR": false,
    "flag_KMC": true,
    "KMC": {
      "nLoop": "2000",
      "nspecies": 2,
      "nproducts": 1,
      "nevents": 7,
      "s1": "...",
      "s2": "...",
      "p1": "...",
      "e1": "...",
      "e2": "...",
      "e3": "...",
      "e4": "...",
      "e5": "...",
      "e6": "...",
      "e7": "...",
      "li": [...],
      ...
    }
  }
  ```

#### 3. 参数来源:
- ✅ **MOSP_database/Pd-COoxidation.json** - MSR和KMC完整参数
- ✅ **MOSP_database/Pt-COoxidation.json** - MSR和KMC完整参数
- ✅ **MOSP_database/Au-COoxidation.json** - MSR和KMC完整参数
- ✅ **MOSP_database/Cu-WGSr.json** - MSR和KMC完整参数

#### 4. 参数复制原则:
- **MSR任务**:只复制MSR部分 + Gas + Adsorption,不复制KMC部分
- **KMC任务**:只复制KMC部分 + 必需的基础参数,不复制MSR部分
- **重要**:MSR和KMC参数完全独立,互不影响

---

## 📋 KMC input.json必需字段清单

**⚠️ 重要提示**:KMC input.json必须包含以下所有字段,否则会导致运行失败!

### 顶层必需字段

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| Element | string | 金属元素 | "Pt" |
| Lattice constant | string | 晶格常数(Å) | "3.9239" |
| Crystal structure | string | 晶体结构 | "FCC" |
| Temperature | string | 温度(K) | "850" |
| Pressure | string | 压力(Pa) | "150" |
| flag_MSR | boolean | MSR标志(KMC任务必须为false) | false |
| flag_KMC | boolean | KMC标志(KMC任务必须为true) | true |
| KMC | object | KMC参数对象 | {...} |

### KMC部分必需字段

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| nLoop | string | 总模拟步数 | "20000000" |
| record_int | string | 记录间隔 | "1000" |
| nspecies | number | 物种数量 | 2 |
| nproducts | number | 产物数量 | 1 |
| nevents | number | 反应事件数 | 7 |
| nevents_mob | number | 移动事件数 | 1 |
| s1 | string | 物种1定义(JSON字符串) | "{\"name\": \"CO\", ...}" |
| s2 | string | 物种2定义(JSON字符串) | "{\"name\": \"O\", ...}" |
| p1 | string | 产物1定义(JSON字符串) | "{\"name\": \"CO2\", ...}" |
| e1 | string | 反应事件1(JSON字符串) | "{\"name\": \"CO-ads\", ...}" |
| e2 | string | 反应事件2(JSON字符串) | "{\"name\": \"CO-des\", ...}" |
| e3 | string | 反应事件3(JSON字符串) | "{\"name\": \"O2-ads\", ...}" |
| e4 | string | 反应事件4(JSON字符串) | "{\"name\": \"O2-des\", ...}" |
| e5 | string | 反应事件5(JSON字符串) | "{\"name\": \"CO-diff\", ...}" |
| e6 | string | 反应事件6(JSON字符串) | "{\"name\": \"O-diff\", ...}" |
| e7 | string | 反应事件7(JSON字符串) | "{\"name\": \"CO+O\", ...}" |
| li | array | 晶格相互作用矩阵 | [[-0.187, -0.16], [-0.16, -0.176]] |

### ⚠️ 关键原则

1. **必须从MOSP_database复制模板**:不要手动创建input.json
2. **所有顶层字段都是必需的**:包括Element、Lattice constant、Crystal structure等
3. **气体熵值必须与MSR一致**:s1.S_gas和s2.S_gas必须使用相同的计算方法和值
4. **参数类型要正确**:注意string、number、boolean、object的区别

### ✅ 检查命令

```bash
# 检查顶层字段
cat KMC任务目录/input.json | jq 'keys'

# 检查KMC部分字段
cat KMC任务目录/input.json | jq '.KMC | keys'

# 验证字段完整性
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

## 🔍 参数查询类型

### 1. 查看当前任务参数
**用户意图**:查看当前MSR/KMC任务的具体参数值
**触发词**:`show parameters`, `当前参数`, `this task parameters`, `detailed parameters`
**响应**:读取并展示当前任务的input.json内容

示例响应:
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

### 2. 查看参数文档
**用户意图**:了解参数的含义、范围、默认值
**触发词**:`parameter documentation`, `参数说明`, `parameter types`
**响应**:展示参数类型、说明、示例值表格

### ⚠️ 重要说明
当用户询问"show me the detailed parameters"时,**优先理解为查看当前任务参数**,除非明确要求"参数文档"或"parameter documentation"。

---

## 📋 技能概览

**技能名称**: `chatmosp-parameter-builder`
**技能类型**: 智能参数构建与管理器
**核心职责**: 参数查询、智能补全、气体熵计算、验证生成

### 技能定位
参数构建器是chatMOSP系统的参数智能管理中心,负责:
1. **智能参数补全**:基于MOSP_database搜索+温度替换+气体熵计算的完整参数生成
2. **多源参数查询**:从MOSP_database、user_MOSP_database、历史、推荐源查询计算参数
3. **交互式参数构建**:支持用户调整温度、压力、气体等参数
4. **参数验证与完整性检查**:确保参数格式正确、完整,符合MOSP要求
5. **智能气体熵计算**:基于温度自动计算和调整气体熵值

## 🎯 核心功能

### 1. 智能参数补全系统

#### 1.1 Examples搜索与参数补全流程
当用户输入部分参数时,自动搜索MOSP_database目录并补全完整参数:

```
用户输入 → 提取基本参数(金属、温度) → 搜索MOSP_database匹配文件 →
加载匹配的example文件 → 替换温度参数 → 计算气体熵 → 生成完整input.json
```

#### 1.2 参数补全算法
1. **金属匹配**:精确匹配金属元素(Pd, Pt, Au等)
2. **气体匹配**:气体种类集合匹配(CO+O2 → 匹配CO氧化环境)
3. **MOSP_database搜索**:在`mosp-for-chatMOSP/MOSP_database/`目录中搜索
4. **最佳匹配选择**:选择金属和气体匹配度最高的example文件
5. **参数替换**:保持example中的默认参数,替换用户指定的温度等参数

#### 1.3 默认参数使用逻辑
- **用户指定参数**:优先使用用户明确指定的参数
- **MOSP_database参数**:用户未指定的参数使用MOSP_database中的默认值
- **系统默认值**:上述都没有时使用系统预设默认值

#### 1.4 参数完整性检查与处理

当MOSP_database中找到匹配文件但参数不完整时,需要进行参数完整性检查和处理。

**步骤1:检查参数完整性**

检查以下必需字段是否为空:
- **MSR关键参数**:E_ads(吸附能)、w(相互作用矩阵)、gamma(表面能)
- **MSR次要参数**:Gas1_S、Gas2_S(气体熵,可自动计算)
- **KMC关键参数**:E_ads_para、BEP_para、li(晶格相互作用)

**步骤2:根据缺失参数的重要性决定处理方式**

**情况A：关键参数缺失**（E_ads, w, gamma等）

**步骤1：向用户说明参数缺失情况**
```
{metal}.json缺少关键数据（如吸附能、相互作用矩阵）
```

**步骤2：提供选项供用户选择**

请选择处理方式：
1. **进行文献检索补全（开放获取期刊）** - 优先检索Nature Communications, Science Advances, PNAS, ACS Central Science, Chemical Science等开放获取期刊（无需付费，访问便捷）
2. **进行文献检索补全（付费期刊）** - 检索Science, Nature, JACS, Angewandte Chemie等付费期刊（请确保已付费，拥有访问权限）
3. **直接指定参数** - 如果您已知参数值，可直接输入
4. **取消任务（更换体系）** - 更换金属或气体体系

**步骤3：根据用户选择执行相应操作**
- 选择1或2：调用`chatmosp-literature-search`技能，传递期刊类型（开放获取/付费）
- 选择3：等待用户输入参数值
- 选择4：结束当前任务，询问用户新的金属或气体体系

**情况B:次要参数缺失**(Gas1_S, Gas2_S等)
- 次要参数可自动计算或使用默认值
- 气体熵值:根据温度自动计算(使用气体熵计算公式)
- 向用户说明:`"部分参数将使用默认值或自动计算(如气体熵值)"`

**情况C:用户可提供的参数**
- 询问用户是否有已知的参数值
- 如果用户提供参数 → 使用用户提供的值
- 如果用户不知道 → 调用`chatmosp-literature-search`

**步骤3:参数补全流程**

```
读取MOSP_database文件 → 检查参数完整性 → 识别缺失参数 →
判断参数重要性 → 选择处理方式(文献检索/自动计算/用户输入) →
展示完整参数 → 用户确认
```

**示例:Pd.json缺少关键参数**

```
用户请求:Pd在CO氧化条件下结构

检查Pd.json:
- ✅ 基本信息:Element=Pd, Lattice constant=3.8907, Crystal structure=FCC
- ✅ 表面能:gamma(100)=0.145, gamma(110)=0.152, gamma(111)=0.125
- ❌ 吸附能:E_ads全部为空
- ❌ 相互作用矩阵:w大部分为空

处理方式:
1. 向用户说明:"Pd.json缺少关键数据(吸附能、相互作用矩阵)"
2. 调用chatmosp-literature-search检索Pd CO氧化相关文献
3. 从文献中提取缺失参数
4. 展示完整参数给用户确认
```

### 2. 找不到匹配example时的文献搜索流程

#### 2.1 调用独立技能:chatmosp-literature-search

当MOSP_database中没有找到匹配的参数时,调用`chatmosp-literature-search`技能进行文献搜索。

**调用方式**:
```
调用技能:chatmosp-literature-search
输入参数:
- 金属元素:如 Pd, Pt, Au, Cu等
- 气体体系:如 CO+O2, H2+CO2等
- 温度范围:(可选)
- 压力范围:(可选)
```

**返回结果**:
```
参数表格,包含:
- 表面能(各晶面)
- 吸附能(各晶面 + 各气体)
- 相互作用矩阵
- 参数来源(DOI、文献标题)
- 参数完整性评分(1-10分)
```

#### 2.2 处理返回结果

根据`chatmosp-literature-search`返回的参数完整性评分,决定下一步操作:

**⚠️ 重要：文献搜索后必须计算气体熵！**

文献搜索返回的参数**不包含**气体熵值(Gas_S/S_gas)。无论完整性评分多少，在组装input.json之前，必须根据用户指定的温度自动计算气体熵值：

```
文献搜索返回参数 → 提取E_ads, w, gamma → ✅ 根据温度计算Gas_S/S_gas → 组装完整input.json
```

计算公式: `S(eV/K) = (a × T^b) / 96485`

**完整性评分 9-10分**:
- 参数完整,可直接使用
- ✅ 仍需计算气体熵值
- 展示参数给用户确认

**完整性评分 7-8分**:
- 参数较完整,可以使用
- ✅ 仍需计算气体熵值
- 需要用户确认缺失的参数

**完整性评分 5-6分**:
- 参数部分完整,需要补充
- ✅ 仍需计算气体熵值
- 向用户说明缺失的参数,建议补充方案

**完整性评分 3-4分**:
- 参数不完整,建议使用替代方案
- 如:使用相似金属的参数作为参考

**完整性评分 1-2分**:
- 参数极不完整,不推荐使用
- 建议用户提供已知参数来源或使用默认参数

#### 2.3 详细流程请参考

文献搜索的详细流程、期刊搜索平台优先级、文章检索流程、参数提取方法等内容,请参考:
- **chatmosp-literature-search/SKILL.md**(中文版)
- **chatmosp-literature-search/SKILL_en.md**(英文版)

#### 2.4 相互作用参数转换

**⚠️ 重要说明**:只在接收到文献检索参数时才触发检测和转换,Database自带的参数不会处理(假设已经是正确的格式)。

##### MSR vs KMC定义

**MSR使用"满吸附相互作用"**:
- 定义:满吸附时的总相互作用能
- 数值范围:通常 > 0.5 eV
- 用途:MSR计算

**KMC使用"单个相邻原子相互作用"**:
- 定义:单个相邻吸附原子之间的相互作用
- 数值范围:通常 < 0.3 eV
- 用途:KMC模拟

##### 判断标准

**如果所有相互作用能 < 0.3 eV**:
- 这是KMC格式
- MSR任务需要转换为MSR格式

**如果存在相互作用能 > 0.5 eV**:
- 这是MSR格式
- 不需要转换

**如果一个文献的话,wCO、wO、wCO,O应该一起判定**:
- 不要分开判定
- 如果所有相互作用能 < 0.3 eV → KMC格式
- 如果存在相互作用能 > 0.5 eV → MSR格式

##### 转换公式

**MSR参数 = KMC参数 × 相邻位点数**

**相邻位点数**:
- (100) 晶面:4个相邻位点
- (110) 晶面:2个相邻位点
- (111) 晶面:6个相邻位点

##### 转换时机与流程

**步骤1:判断参数来源**
- Database参数 → 不转换,直接使用
- 文献检索参数 → 进入步骤2

**步骤2:判断参数格式**
- 检测相互作用参数数值
- 如果所有值 < 0.3 eV → KMC格式
- 如果存在值 > 0.5 eV → MSR格式

**步骤3:根据任务类型决定是否转换**

**MSR任务**:
- 如果参数是KMC格式 → 需要转换为MSR格式
- 如果参数是MSR格式 → 不需要转换

**KMC任务**:
- 如果参数是KMC格式 → 不需要转换
- 如果参数是MSR格式 → 需要转换为KMC格式(KMC参数 = MSR参数 ÷ 相邻位点数)

**步骤4:执行转换**
- 根据转换公式计算转换后的值
- 更新参数值

**步骤5:验证转换结果**
- 检查转换后的值是否在合理范围内
- 向用户说明转换过程和结果

##### 转换示例

**示例:Pd CO氧化 - 从文献提取的KMC格式参数**

**原始数据(KMC格式)**:
```
(100) 晶面:wCO-CO = -0.149 eV
(110) 晶面:wCO-CO = -0.159 eV
(111) 晶面:wCO-CO = -0.168 eV
```

**判断**:所有值 < 0.3 eV → KMC格式

**任务类型**:MSR任务

**转换**:
```
(100) 晶面:wCO-CO = -0.149 × 4 = -0.596 eV
(110) 晶面:wCO-CO = -0.159 × 2 = -0.318 eV
(111) 晶面:wCO-CO = -0.168 × 6 = -1.008 eV
```

**转换后(MSR格式)**:
```
(100) 晶面:wCO-CO = -0.596 eV
(110) 晶面:wCO-CO = -0.318 eV
(111) 晶面:wCO-CO = -1.008 eV
```

##### 参数格式标注

在展示参数给用户确认时,应该标注参数格式:
```
【相互作用矩阵】(从文献提取,KMC格式,已转换为MSR格式)
100 晶面:
  CO-CO:-0.596 eV (原始值:-0.149 eV × 4)
  ...
```

### 3. 气体熵计算系统

#### 3.1 气体熵计算公式

**熵值计算公式**:
```
S(J/K/mol) = a × T(K)^b
S(eV/K) = (a × T^b) / 96485
```

其中:
- a, b 是气体特定的参数
- T 是温度(K)
- 96485 是J到eV的转换因子(1 eV = 96485 J)

#### 3.2 支持的气体参数

| 气体 | a (系数) | b (指数) |
|------|----------|----------|
| H2 | 41.362 | 0.201 |
| N2 | 82.394 | 0.148 |
| O2 | 90.454 | 0.143 |
| CO2 | 76.458 | 0.181 |
| CO | 85.142 | 0.147 |
| NO | 93.121 | 0.143 |
| H2O | 64.234 | 0.18665 |

**注意**:参数通过0~6000K范围拟合获得,无温度范围限制。

#### 3.3 气体熵计算示例

**示例1:CO在473K的熵值**
```
S(J/K/mol) = 85.142 × 473^0.147 = 85.142 × 2.47 = 210.5 J/K/mol
S(eV/K) = 210.5 / 96485 = 0.00218 eV/K
```

**示例2:O2在473K的熵值**
```
S(J/K/mol) = 90.454 × 473^0.143 = 90.454 × 2.41 = 218.2 J/K/mol
S(eV/K) = 218.2 / 96485 = 0.00226 eV/K
```

#### 3.4 MSR和KMC的气体熵字段

**MSR的气体熵字段**:
- Gas1_S: 第一种气体的熵值(eV/K)
- Gas2_S: 第二种气体的熵值(eV/K)

**KMC的气体熵字段**:
- s1.S_gas: 第一种物种的气体熵值(eV/K)
- s2.S_gas: 第二种物种的气体熵值(eV/K)

#### 3.5 气体熵计算验证

验证公式:`S(J/K/mol) ≈ S(eV/K) × 96485`

验证示例:
```
CO在473K:
- S(eV/K) = 0.0972 eV/K
- S(J/K/mol) = 0.0972 × 96485 = 9383 J/K/mol
- 预期值:9375 J/K/mol
- 误差:< 0.1% ✓
```



### 4. 温度替换系统

#### 4.1 温度替换流程

从MOSP_database匹配example文件后,需要根据用户指定的温度更新参数:

**步骤1:读取example中的温度**
```
example文件温度:T_example (如 473K)
```

**步骤2:用户指定温度**
```
用户指定温度:T_user (如 600K)
```

**步骤3:更新温度相关参数**
- 更新温度字段:`Temperature = T_user`
- 更新气体熵值:根据T_user重新计算

**步骤4:保留其他参数**
- 表面能、吸附能、相互作用矩阵等参数保持不变
- 这些参数是温度无关的(在example中已经提供)

#### 4.2 温度替换示例

**示例:Pd-CO-O体系,温度从473K更新到600K**

**更新前(473K)**:
```
Temperature: 473
Gas1_S: 0.002356 eV/K  (CO)
Gas2_S: 0.002446 eV/K  (O2)
```

**更新后(600K)**:
```
Temperature: 600
Gas1_S: 0.002482 eV/K  (CO, 重新计算)
Gas2_S: 0.002539 eV/K  (O2, 重新计算)
```

**验证**:
```
CO在600K的熵值:
S(J/K/mol) = 85.142 × 600^0.147 = 85.142 × 2.56 = 218.0 J/K/mol
S(eV/K) = 218.0 / 96485 = 0.00226 eV/K

O2在600K的熵值:
S(J/K/mol) = 90.454 × 600^0.143 = 90.454 × 2.50 = 225.8 J/K/mol
S(eV/K) = 225.8 / 96485 = 0.00234 eV/K

填入参数:
  - MSR: Gas1_S = "0.00226", Gas2_S = "0.00234"
  - KMC: s1.S_gas = "0.00226", s2.S_gas = "0.00234"

⚠️ 检查:MSR和KMC的气体熵值是否一致? ✓
```
```
搜索平台:Nature Communications(开放获取)
搜索关键词:"{metal}" AND "{gas}" AND "adsorption energy"

找到文章列表:
### 5. 参数验证系统
- **格式验证**:确保JSON格式正确,包含所有必需字段
- **范围验证**:温度、压力、团簇尺寸等在合理范围内
- **一致性验证**:气体种类与分压设置一致
- **完整性验证**:MSR和KMC任务的必需参数齐全

## 🔧 技术实现

### 依赖关系
- `literature-review` - 文献搜索(可选,用于User-Examples)
- `chatmosp-file-organizer` - 获取MOSP_database目录路径
- `chatmosp-input-coordinator` - 获取任务类型信息

### 执行流程
```
用户输入 → 参数提取 → MOSP_database搜索 → 参数匹配 → 温度替换 →
气体熵计算 → 参数验证 → 生成input.json → 返回完整参数
```

### 智能参数补全详细流程

#### 场景:用户输入"Pd在CO氧化环境下200摄氏度结构"

1. **参数提取**:
   - 金属: Pd
   - 温度: 200°C → 473K(转换)
   - 气体: ["CO"](推断CO氧化环境需要CO和O2)

2. **MOSP_database搜索**:
   - 搜索目录: `mosp-for-chatMOSP/MOSP_database/`
   - 匹配条件: 金属=Pd, 气体包含CO和O2
   - 找到文件: `Pd_CO9_O18_500K_101325Pa_R20.json`

3. **参数加载与替换**:
   - 加载example文件的所有参数
   - 替换温度: 500K → 473K
   - 保持其他参数: 分压(CO9_O18)、压力(101325Pa)、尺寸(R20)

4. **气体熵计算**:
   - 计算CO在473K的熵值
   - 计算O2在473K的熵值
   - 替换原熵值参数

5. **生成完整input.json**:
   - 包含所有必需参数
   - 格式符合MOSP要求
   - 可用于MSR计算

## 📝 使用示例

### 示例1:智能参数补全
```
用户输入: "Pd在CO氧化环境下200摄氏度结构"

系统处理:
1. 提取参数: metal=Pd, temperature=473K, gases=["CO"]
2. 搜索MOSP_database: 找到 Pd_CO9_O18_500K_101325Pa_R20.json
3. 替换温度: 500K → 473K
4. 计算气体熵: CO(473K)=..., O2(473K)=...
5. 输出完整参数:
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

### 示例2:直接KMC参数生成
```
用户输入: "运行Pd的CO氧化KMC模拟,温度473K,200万步"

系统处理:
1. 识别任务类型: KMC
2. 提取参数: metal=Pd, temperature=473K, steps=2000000
3. 搜索MOSP_database: 找到 Pd_CO9_O18_500K_101325Pa_1000000steps.json
4. 替换参数: 温度→473K, 步数→2000000
5. 输出KMC参数文件
```

## 🛠️ 配置选项

```yaml
# 技能配置
skill:
  name: "chatmosp-parameter-builder"
  version: "2.0.0"
  description: "智能参数构建器 - 支持MOSP_database搜索和气体熵计算"

# 参数源配置
parameter_sources:
  MOSP_database_dir: "mosp-for-chatMOSP/MOSP_database/"
  user_MOSP_database_dir: "mosp-for-chatMOSP/user_MOSP_database/"
  history_dir: "mosp-for-chatMOSP/OUTPUT/_history/"

# 智能补全配置
completion:
  enable_MOSP_database_search: true
  gas_entropy_calculation: true
  auto_temperature_conversion: true  # °C → K自动转换
  default_pressure: "101325"
  default_radius: "20"
  default_steps: "1000000"

# 匹配配置
matching:
  metal_weight: 3.0
  temperature_weight: 2.0
  gas_weight: 2.5
  partial_pressure_weight: 1.5

# 气体熵计算配置
gas_entropy:
  enable_calculation: true
  supported_gases: ["H2", "N2", "O2", "CO2", "CO", "NO", "H2O"]
  conversion_factor: 96485  # J/mol·K → eV/K
  validation_tolerance: 0.003  # 3%误差容忍度

# 输出配置
output:
  format: "json"
  include_metadata: true
  include_calculation_log: true
  backup_original: true
```

## 📁 文件结构

```
chatmosp-parameter-builder/
├── SKILL.md           # 技能说明文档（中文版）
└── SKILL_en.md        # 技能说明文档（英文版）
```

## 🌐 语言一致性

### 响应语言策略
1. **自动语言检测**: 根据用户输入自动检测语言
2. **一致性响应**: 英文输入得到英文回复,中文输入得到中文回复
3. **双语支持**: 根据用户语言选择SKILL.md或SKILL_en.md

### 示例
- 英文输入 "Show me the Pd structure" → 英文回复,使用SKILL_en.md
- 中文输入 "生成Pd团簇" → 中文回复,使用SKILL.md

### 关键原则
- 气体熵计算与语言无关,确保科学计算准确性
- 文件保存使用通用JSON格式
## 🔄 更新说明

**版本 2.0 (2026-05) - 文档驱动架构**:
- 技能文档（SKILL.md/SKILL_en.md）作为AI操作指南，不再使用Python代码
- 智能参数补全：基于MOSP_database搜索的完整参数生成流程
- 气体熵自动计算：支持7种气体的温度依赖熵值计算
- 相互作用参数转换：自动检测并转换MSR/KMC格式
- 文献搜索集成：MOSP_database无匹配时自动搜索文献
- 用户确认流程：5选项交互式参数确认