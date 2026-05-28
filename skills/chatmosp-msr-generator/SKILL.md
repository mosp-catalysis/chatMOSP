# Skill: chatmosp-msr-generator

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

**在执行任何MSR计算之前,必须遵守以下流程:**

### 📋 必须遵守的执行流程

```
用户请求MSR计算 → 调用parameter-builder构建参数 → ⚠️ 展示参数给用户确认 ⚠️ → 用户确认参数 → 执行MSR计算
```

### ❌ 禁止直接执行计算

**在执行MSR计算之前,必须完成以下步骤:**

1. **必须调用parameter-builder技能**:使用parameter-builder构建参数,不要手动构建参数
2. **必须展示参数给用户确认**:无论用户请求多么明确,都必须展示参数并等待用户确认
3. **必须等待用户确认**:只有用户明确选择"确认"后,才能执行MSR计算

### 🔧 参数确认流程

当parameter-builder构建参数后,会展示参数和5个选项:

1. **确认** - 使用这些参数继续执行MSR计算
2. **修改** - 调整特定参数(如温度、压强、团簇半径、气体组成等)
3. **对比** - 运行多个条件进行对比(如多个温度、压强或团簇尺寸)
4. **切换计算模式** - 切换到KMC动力学模拟
5. **取消任务,更换体系** - 更换金属或气体体系

**只有用户选择"确认"(选项1)后,才能执行MSR计算!**

### ⚠️ 禁止行为

- ❌ **禁止**直接执行MSR计算,不经过parameter-builder
- ❌ **禁止**跳过参数展示和确认步骤
- ❌ **禁止**假设用户已经了解默认参数,不需要确认

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

## 🚀 快速开始:MSR计算正确流程

### 使用已有代码(不写新代码):
```bash
# MSR计算命令
python3 mosp-for-chatMOSP/utils/msr.py --json path/to/input.json --output path/to/output/
```

### 📝 参数准备流程(重要):

#### 步骤1:准备input.json文件
在运行MSR计算之前,必须准备完整的input.json文件。

### ⚠️ 大尺寸团簇计算时间提醒

当团簇半径≥50Å时,计算时间较长,执行前必须提醒用户:

```
⚠️ 计算时间提醒：
当前团簇半径为 {R}Å，预计计算时间约 {estimated_minutes} 分钟。
（参考：半径50Å约需20分钟，半径越大时间越长）
同时运行多个任务可能导致用时增加。
是否继续执行MSR计算？
```

**时间参考**:
- 半径50Å（约11000原子）：约20分钟
- 半径65Å（约35000原子）：约60分钟或更长
- 半径越大，原子数立方增长，计算时间显著增加

**注意**：如果用户选择多个条件（如多个温度），每个条件都需要单独计算，总时间会成倍增加。

**推荐方法**:调用`chatmosp-parameter-builder`技能来准备参数。

示例:准备Pd在473K下的参数 → 调用parameter-builder技能 → 自动查找MOSP_database → 自动计算气体熵
- CO在473K的熵值 = 0.002356 eV/K
- O₂在473K的熵值 = 0.002446 eV/K

#### 步骤2:气体熵自动计算
**重要**:`parameter-builder`技能会根据温度自动计算气体熵值。

**⚠️ 详细计算指令请参考:`chatmosp-parameter-builder/SKILL.md` 第4.4节**

气体熵计算公式:
```
S(eV/K) = (a × T^b) / 96485
```

支持的气体:
- H2, N2, O2, CO2, CO, NO, H2O

**计算示例**:
```
CO在1000K的熵值:
- a = 85.142, b = 0.147
- S = (85.142 × 1000^0.147) / 96485 = 0.002482 eV/K
```

**⚠️ 关键原则:MSR和KMC的气体熵值必须一致!**
- MSR参数:Gas1_S, Gas2_S
- KMC参数:s1.S_gas, s2.S_gas
- 两者必须使用相同的计算方法和值

#### 步骤3:验证参数完整性
确保input.json包含所有必需的MSR参数:
- Element, Temperature, Pressure
- Gas1_name, Gas1_pp, Gas1_S(气体熵)
- Gas2_name, Gas2_pp, Gas2_S(气体熵)
- Radius, nFaces, Face1/2/3参数

#### ⚠️ 常见错误:直接复制example文件
**错误做法**:直接复制`MOSP_database/Pd-COoxidation.json`而不调整气体熵。只修改温度但Gas1_S和Gas2_S还是原来温度的值，没有重新计算。

**正确做法**:使用parameter-builder技能准备参数，它会根据新温度自动重新计算气体熵。

#### 步骤4:运行MSR计算 ⚠️ 关键步骤

**执行命令**:
```bash
cd mosp-for-chatMOSP
python3 utils/msr.py --json OUTPUT/{task_name}/input.json --output OUTPUT/{task_name}/
cd -
```

**执行前检查**:
- ✅ input.json 已准备完整（步骤1-3已完成）
- ✅ 气体熵已根据当前温度计算
- ✅ 用户已确认参数

**执行后验证**:
```bash
ls -lh OUTPUT/{task_name}/ini.xyz
ls -lh OUTPUT/{task_name}/{task_name}_cluster.xyz
```
- ✅ `ini.xyz` 必须存在且 > 0KB，否则MSR计算失败
- ✅ `{task_name}_cluster.xyz` 必须存在（用于可视化）
- ⚠️ 若文件缺失，返回错误信息并建议调整参数后重试

### 生成的文件:
- `ini.xyz` - 优化后的团簇结构(包含所有原子)
- `{task_name}_cluster.xyz` - 可视化用结构文件(表面原子已分类)
- `faceinfo.txt` - 晶面信息统计
- `input.json` - MSR参数文件

### ⚠️ 重要说明:
1. **MSR只负责生成团簇结构**,不包含KMC参数
2. **不要在MSR的input.json中包含KMC参数**
3. KMC参数由KMC技能单独准备(详见chatmosp-kmc-simulator技能)
4. MSR和KMC使用不同的input.json,参数完全分离

### MSR→KMC工作流:
```
MSR计算 → 生成ini.xyz → (如需KMC)→ KMC技能准备独立参数 → KMC计算
```

---

## 📋 技能概览

**技能名称**: `chatmosp-msr-generator`
**技能类型**: MSR计算引擎
**核心职责**: 金属团簇结构生成计算

### 技能定位
MSR生成器是chatMOSP系统的核心计算引擎,负责:
1. **MOSP引擎调用**:执行金属团簇结构生成计算
2. **智能重试机制**:基于设计文档的失败重试和降级策略
3. **参数适配**:将通用参数转换为MOSP引擎特定格式
4. **结果验证**:检查计算收敛性和结果合理性

### 安全与可靠性
- ✅ **失败重试机制**:自动重试失败的计算(最多3次)
- ✅ **智能降级策略**:调整参数以帮助收敛
- ✅ **资源监控**:检查内存和CPU使用情况

## 🎯 核心功能

### 1. MSR计算执行
- 调用 mosp-for-chatMOSP 引擎
- 准备MSR输入文件(MSR-input.json)
- 监控计算过程
- 捕获计算结果

### 2. 智能重试机制
```
第一次失败 → 减小团簇半径重试
第二次失败 → 增加迭代次数重试
第三次失败 → 返回详细错误信息
```

### 3. 参数转换与验证
- 验证参数完整性
- 转换为MOSP引擎格式
- 检查参数合理性
- 添加默认值

### 4. 结果处理与解析
- 解析结构文件(.xyz格式)
- 提取能量和收敛信息
- 验证结果有效性
- 生成标准化输出

## 🔧 技术实现

### 依赖关系
- `mosp-for-chatMOSP` - 核心计算引擎(已克隆)
- `chatmosp-file-organizer` - 文件路径管理
- `chatmosp-parameter-builder` - 参数验证

### 执行流程
```
接收参数 → 验证参数 → 准备输入文件 → 执行计算 →
监控进度 → 检查收敛 → 解析结果 → 返回标准化输出
           ↓
       失败重试 → 参数调整 → 重新执行
```

### 文件使用逻辑
**重要:正确的文件创建和使用流程**

1. **MSR任务文件流程**:
   - **输入**: `input.json` (参数文件)
   - **MSR生成**: `ini.xyz` - 真实团簇结构文件(包含所有原子信息)
   - **MSR生成**: `{task_name}_cluster.xyz` - 绘图用结构文件(表面原子已按晶面分类)
   - **重要**: `ini.xyz` 是MSR的输出文件,不是输入文件

2. **KMC任务文件流程**:
   - **输入**: `input.json` (参数文件) + `ini.xyz` (MSR生成的结构文件)
   - **KMC生成**: 动力学模拟结果文件
   - **关键**: KMC需要MSR生成的 `ini.xyz` 作为输入

### 可视化生成 / Visualization Generation
MSR计算完成后自动生成可视化图像:
MSR automatically generates visualization images after calculation completion:

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

可视化配置：
- 默认生成静态图(structure.png)和旋转动图(rotation.gif)
- 动图生成建议原子数≤20000（超过时仅生成静态图）

#### 步骤3：向用户展示可视化结果 ⚠️ 重要

**必须执行**：生成图像后，立即向用户展示！

**飞书平台发送示例**：
```json
{
  "action": "send",
  "channel": "feishu",
  "filePath": "/root/.openclaw/workspace/mosp-for-chatMOSP/OUTPUT/{task_name}/structure.png",
  "caption": "{金属} - {气体分压}-{温度}K-{压强}Pa-R{半径}Å"
}
```

**示例标题**：
- `Pt - CO67%-O33%-1000K-1500Pa-R40Å`
- `Pd - CO9%-O18%-473K-101325Pa-R50Å`

**操作要求**：
1. 发送 structure.png 给用户查看
2. 发送 rotation.gif 给用户查看
3. 简要描述结构特征（如："Pd纳米颗粒呈截角八面体，主要暴露(111)晶面"）

## 📝 使用示例

```
用户: 计算Pt纳米颗粒在500K下的团簇结构
系统: [识别为MSR任务 → 查找参数 → 展示确认 → 执行计算 → 展示结构图]
```

