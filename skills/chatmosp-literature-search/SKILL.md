# Skill: chatmosp-literature-search

## 🎯 技能简介

从学术文献中搜索和提取MSR/KMC参数。当MOSP_database中没有匹配的参数时，使用此技能从文献中获取参数。

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

---

## 📋 输入与输出

### 输入

- **金属元素**（必需）：Pd, Pt, Au, Cu, Ni等
- **气体体系**（必需）：CO+O2, H2+CO2, CO+H2等
- **温度范围**（可选）：例如 300-500K
- **压力范围**（可选）：例如 1-10 atm

### 输出

- **参数表格**，包含：
  - 表面能（各晶面）
  - 吸附能（各晶面 + 各气体）
  - 相互作用矩阵
  - **参数来源**（DOI、文献标题）
  - **参数完整性评分**（1-10分）

---

## 🔄 工作流程

### 整体流程图

```
输入（金属 + 气体） → 期刊搜索 → 文章检索 → 参数提取 → 参数验证 → 输出（参数表格）
```

### 流程说明

**步骤1：期刊搜索**（按优先级）
- 第1层：顶刊（Science, Nature, JACS, Angewandte Chemie等）
- 第2层：开放获取期刊（Nature Communications, Science Advances, PNAS等）
- 第3层：预印本平台（arXiv, ChemRxiv等）

**步骤2：文章检索**（3个阶段）
- 阶段1：摘要检索（确认相关性）
- 阶段2：正文检索（查找参数表格）
- 阶段3：SI检索（补充参数）

**步骤3：参数提取**
- 提取表面能
- 提取吸附能
- 提取相互作用矩阵

**步骤4：参数验证**
- 检查完整性
- 检查合理性
- 检查一致性

**步骤5：输出结果**
- 展示参数表格
- 提供参数来源
- 提供完整性评分

---

## ⚠️ 重要限制与机制

### 超时机制

**总搜索时间限制**：5分钟

**单篇文章检索限制**：2分钟

**超时处理**：
- 如果总时间超过5分钟，立即停止搜索
- 返回已找到的参数（即使不完整）
- 向用户说明情况

### 降级方案

**如果搜索了5篇文章还没有找到完整参数**：

1. 向用户说明情况：
   ```
   我已经搜索了5篇文献，但未能找到完整的参数。
   以下是找到的部分参数：
   - 表面能：✅ 已找到
   - 吸附能：❌ 未找到
   - 相互作用矩阵：❌ 未找到
   
   建议选项：
   1. 使用相似金属的参数作为参考
   2. 提供已知参数来源（DOI或文献标题）
   3. 使用默认/测试参数
   ```

2. 提供替代方案

---

## 📚 期刊搜索平台优先级

### 第1层：顶刊（优先但可能无法获取）

**期刊列表**：
- Science (science.org)
- Nature (nature.com)
- JACS (Journal of the American Chemical Society)
- Angewandte Chemie
- PRL (Physical Review Letters)
- JCP (Journal of Chemical Physics)

**获取策略**：
- 检查是否有机构订阅（通过DOI解析）
- 遇到API限制或访问受限 → 直接跳到第2层
- 无法获取 → 跳过，进入第2层
- 可以获取 → 检索摘要 → 正文 → SI

**重要**：不要浪费时间在无法访问的资源上，优先搜索开放获取资源。

### 第2层：完全开放获取期刊（推荐）

**期刊列表**：
- Nature Communications (nature.com/ncomms)
- Science Advances (science.org/journal/sciadv)
- PNAS (pnas.org)
- ACS Central Science
- Chemical Science (RSC)

**优势**：
- 完全免费，无需订阅
- 质量高，参数可信
- SI通常包含完整数据

### 第3层：预印本平台（最后选择）

**平台列表**：
- arXiv (arxiv.org)
- ChemRxiv (chemrxiv.org)
- bioRxiv (biorxiv.org)

**注意事项**：
- 未经过同行评审
- 参数可能不准确
- 需要用户确认

---

## 🔧 期刊搜索工具选择

### ⚠️ 重要提示：工具选择

**不要使用web_fetch**：
- ❌ 期刊网站常有访问限制（403错误、CAPTCHA验证）
- ❌ web_fetch容易失败
- ❌ 无法执行JavaScript，无法获取动态加载的内容

**优先使用openclaw_browser**：
- ✅ 支持JavaScript渲染
- ✅ 支持登录态
- ✅ 支持交互操作
- ✅ 更适合期刊网站访问

**降级方案**：
- ✅ 如果openclaw_browser不可用，可以尝试opencli CLI工具
- 📖 详细指南：参考 `web-tools-guide` 技能文档

---

## 🔍 详细文献检索流程

### 1. 期刊选择与检索

**期刊分类**：

**开放获取期刊**（无需付费）：
- Nature Communications
- Science Advances
- PNAS (Proceedings of the National Academy of Sciences)
- ACS Central Science
- Chemical Science

**付费期刊**（需要访问权限）：
- Science
- Nature
- JACS (Journal of the American Chemical Society)
- Angewandte Chemie

---

### 2. 单个期刊检索流程

**步骤1：构建搜索关键词**

根据体系构建搜索关键词：

**✅ 正确格式：**
```
"关键词1" AND "关键词2" AND "关键词3"
```

**示例：**
- 示例1：Cu团簇在一氧化碳氧化环境下 → 搜索 `"Cu" AND "CO oxidation"`
- 示例2：Pd团簇在CO氧化环境下 → 搜索 `"Pd" AND "CO oxidation"`
- 示例3：Pt团簇在氢气环境下 → 搜索 `"Pt" AND "H2"`

**⚠️ 重要提示：禁止使用错误的格式！**

**❌ 错误格式（禁止使用）：**
```
Pd CO oxidation
```
**问题：** 空格分隔的格式会导致搜索结果不准确，搜索系统会将整个短语作为一个关键词搜索，而不是分别搜索"Pd"和"CO oxidation"两个关键词。

**✅ 正确格式（必须使用）：**
```
"Pd" AND "CO oxidation"
```
**优点：** 每个关键词用双引号包裹，用AND连接，确保搜索系统正确理解关键词的含义，返回更准确的搜索结果。

**步骤2：使用openclaw_browser访问期刊网站**

- 访问期刊的搜索页面
- 输入搜索关键词
- 搜索结果默认按相关性排列

**步骤3：获取前10个搜索结果**

- 只检查前10个结果（相关性最高）
- 输出前10名的文献名称、DOI、摘要（可选）

---

### 3. 初步筛选（基于题目）

**筛选标准**：
1. **反应气氛体系匹配**：必须是相同的反应气氛（如CO氧化、水汽变换等）
2. **金属体系匹配**：必须是相同的金属（如Pd、Pt、Cu等），排除合金体系

**筛选结果**：
- 输出被筛选后的文献列表
- 标注每篇文献的筛选理由

---

### 4. 用户交互

**询问用户选择**：

请选择下一步操作：
1. **仔细检查这些被筛选的全部文章** - 对所有被筛选的文章进行详细检查
2. **仔细检查某一篇文章** - 只检查用户指定的某一篇文章
3. **换成另一期刊检索** - 放弃当前期刊，换另一个期刊

---

### 5. 详细检查文章内容

**检查流程**：

**步骤1：检查文章正文**
- 确认是相同的金属体系
- 确认是相同的反应气氛
- 检查正文是否包含参数表格

**步骤2：如果没有参数，下载SI**
- 参数只可能存在于文字和表格中，不会出现在图像中
- 下载SI文件（PDF格式）

**步骤3：检查SI文件**
- 搜索关键词：Table, Supplementary Table, S1, S2等
- 提取参数表格

---

### 6. 参数提取与确认

**步骤1：提取参数**

从文章正文或SI中提取以下参数：
- 表面能（各晶面）
- 吸附能（各晶面 + 各气体）
- 相互作用矩阵
- 参数来源（DOI、文献标题）

**步骤2：向用户展示参数**

```
📊 从文献中提取到以下参数：

【文献信息】
- 标题：xxx
- DOI：xxx
- 期刊：xxx

【参数表格】
- 表面能：...
- 吸附能：...
- 相互作用矩阵：...

【参数完整性评分】
- 评分：8/10
- 说明：参数较完整，可以使用
```

**步骤3：询问用户是否使用**

请选择：
1. **使用这些参数** - 将参数传递给chatmosp-parameter-builder
2. **拒绝，继续检索** - 继续检索下一篇文章
3. **取消任务** - 结束文献检索

---

### 7. 一个期刊检索失败的处理

**情况**：一个期刊的前10篇被筛选的文章都没找到参数

**询问用户**：

```
⚠️ 在{期刊名称}的前10篇相关文章中未找到参数

请选择：
1. **更换期刊** - 换另一个期刊继续检索
2. **取消任务** - 如果所有期刊都没有，建议更换体系或用户提供参数
```

---

### 8. 所有期刊检索失败的处理

**情况**：所有期刊都检索完毕，仍未找到参数

**建议用户**：
1. 更换金属或气体体系
2. 用户自己提供参数
3. 取消任务

---

## 🔍 文章检索流程

### 阶段1：摘要检索（免费，快速）

**目的**：确认文章相关性

**检索内容**：
1. 金属元素是否匹配
2. 反应环境是否匹配（气体、温度范围）
3. 研究类型是否匹配（表面催化、团簇）

**判断标准**：
- ✅ 匹配 → 进入阶段2
- ❌ 不匹配 → 检索下一篇文章

**示例**：
```
文章标题："CO oxidation on Pd nanoparticles"
摘要内容："We studied CO oxidation on Pd(111) and Pd(100) surfaces..."
判断结果：✅ 匹配（金属=Pd，气体=CO+O2，研究类型=表面催化）
```

### 阶段2：正文检索（需要访问权限）

**目的**：提取MSR/KMC参数

**检索位置**：
1. Methods/Experimental Section - 实验方法和参数
2. Results - 计算结果和参数
3. Tables - 参数表格
4. Figures - 参数图表

**判断标准**：
- 如果正文明确提到参数表格 → 下载SI
- 如果正文没有提到，但文章相关性很高 → 仍然下载SI检查
- 如果正文完全没有提到参数 → 跳过SI，检索下一篇文章

**重要**：正文没提到参数表格不代表没有，如果相关性高应该下载SI检查。

### 阶段3：SI检索（补充信息）

**目的**：获取完整参数

**检索位置**：
1. Supplementary Tables - 完整参数表
2. Supplementary Methods - 详细方法
3. Supplementary Data - 原始数据

**SI文件命名格式**：
- 格式：`si_{first_author}_{year}.pdf`
- 示例：`si_chee_2020.pdf`, `si_ghosh_2022.pdf`
- 如果同一作者同年有多篇文章：`si_smith_2023a.pdf`, `si_smith_2023b.pdf`

---

## 📊 MSR需求的数据清单

### 基本参数

- ✅ 金属元素 - Element (Pd, Pt, Au, Cu等)
- ✅ 温度 - Temperature (K)
- ✅ 压力 - Pressure (Pa)
- ✅ 团簇半径 - Radius (Å)
- ✅ 气体种类 - Gas species (CO, O2, H2等)
- ✅ 气体分压 - Partial pressures (%)

### 表面参数（每个晶面）

- ✅ 表面能 - Surface energy (eV/Å²)
  - (100), (110), (111), (211), (311)等

### 吸附参数（每个晶面 + 每种气体）

- ✅ 吸附能 - Adsorption energy E_ads (eV)
  - 例：CO在Pd(111)的吸附能
  - 例：O2在Pd(100)的吸附能

### 相互作用参数

- ✅ 相互作用矩阵 - Interaction matrix (eV)
  - CO-CO相互作用
  - CO-O相互作用
  - O-O相互作用

### 气体参数

- ✅ 气体熵 - Gas entropy (eV/K)
  - 可通过公式计算（温度依赖）
  - 或从文献中提取

---

## 📝 参数提取方法

### 步骤1：下载SI文件

使用browser工具访问文章页面，下载SI文件。

### 步骤2：转换PDF为文本

```bash
pdftotext si_{author}_{year}.pdf si_{author}_{year}.txt
```

### 步骤3：搜索参数表格

**搜索关键词**：
- Table S, Supplementary Table
- adsorption energy, E_ads, binding energy
- surface energy, γ, surface tension
- interaction parameter, interaction matrix

### 步骤4：读取参数表格

使用read工具读取文本文件，找到参数表格。

### 步骤5：提取参数

从表格中提取参数数值，注意单位转换。

### 步骤6：验证参数

- 检查参数是否在合理范围内
- 检查参数是否符合物理规律
- 检查参数是否一致

---

## 🎯 参数完整性评分标准

### 评分标准（10分制）

| 参数类型 | 分值 | 说明 |
|---------|------|------|
| 表面能 | 2分 | 至少包含(100), (110), (111)三个晶面 |
| 吸附能 | 3分 | 每种气体在各晶面的吸附能 |
| 相互作用矩阵 | 3分 | CO-CO, CO-O, O-O相互作用 |
| 参数来源 | 1分 | DOI、文献标题、作者信息 |
| 参数合理性 | 1分 | 参数在合理范围内，符合物理规律 |

### 完整性等级

- **9-10分**：完整，可直接使用
- **7-8分**：较完整，可以使用，但需要用户确认
- **5-6分**：部分完整，需要补充参数
- **3-4分**：不完整，建议使用替代方案
- **1-2分**：极不完整，不推荐使用

---

**注意**：相互作用参数转换规则已经移到chatmosp-parameter-builder技能中，请参考：
- **chatmosp-parameter-builder/SKILL.md** 的 "#### 2.4 相互作用参数转换" 章节
- **chatmosp-parameter-builder/SKILL_en.md** 的 "#### 2.4 相互作用参数转换 / Interaction Parameter Conversion" 章节

---

## 💡 文献搜索经验教训

### 教训1：关键词选择策略

**问题**：关键词太具体，过滤掉了相关文章

**解决方案**：
- 先用宽泛关键词搜索（如`"Pd" AND "CO oxidation"`）
- 再用具体关键词筛选（如`"adsorption energy"`）
- 不要只搜索参数名称，要搜索文章主题

### 教训2：DOI优先原则

**问题**：搜索不到目标文章

**解决方案**：
- 优先使用已知的DOI或文章标题
- 如果有DOI，直接访问DOI
- 不要只依赖关键词搜索

### 教训3：多平台搜索

**问题**：单一平台搜索结果有限

**解决方案**：
- 不局限于单一期刊网站
- 搜索多个期刊平台
- 使用开放获取期刊优先

### 教训4：不要浪费时间在无法访问的资源上

**问题**：在访问受限的文章上浪费时间

**解决方案**：
- 遇到API限制或访问受限 → 立即跳到第2层
- 遇到CAPTCHA验证 → 跳过，进入下一层
- 优先搜索开放获取资源

### 教训5：正文没提到参数不代表SI没有

**问题**：正文没有提到参数表格，就跳过了SI

**解决方案**：
- 如果文章相关性很高，仍然下载SI检查
- SI通常包含完整参数表格
- 不要仅根据正文判断

---

## 📋 实际操作示例

### 示例：搜索Pd-CO-O体系参数

**用户输入**：
```
"show me the Pd cluster under atmosphere of CO and O2"
```

**步骤1：提取参数需求**
- 金属：Pd
- 气体：CO, O2
- 需要参数：表面能、吸附能、相互作用矩阵

**步骤2：检查MOSP_database**
```
检查：mosp-for-chatMOSP/MOSP_database/
搜索条件：metal=Pd, gases=[CO, O2]
结果：未找到匹配的example文件
```

**步骤3：启动文献搜索**
```
搜索平台：Nature Communications（开放获取）
搜索关键词："Pd" AND "CO oxidation" AND "adsorption energy"
搜索工具：openclaw_browser
```

**步骤4：找到文章**
```
找到文章："Structural changes in noble metal nanoparticles during CO oxidation"
DOI: 10.1038/s41467-020-16027-9
相关性：✅ 匹配（Pd, CO, O2, 表面催化）
```

**步骤5：下载SI**
```
SI文件：si_chee_2020.pdf (13MB)
保存位置：mosp-for-chatMOSP/literature/Pd_CO_oxidation/
```

**步骤6：提取参数**
```
从Supplementary Table 1提取：
- Pd吸附能（各晶面）
- Pd相互作用参数（各晶面）
- 缺少：表面能数据
```

**步骤7：参数验证**
```
完整性评分：7分（缺少表面能）
处理：搜索其他文献补充表面能
```

**步骤8：展示结果**
```
📊 参数已找到，来源：Nature Communications, 2020
DOI: 10.1038/s41467-020-16027-9

【表面晶面参数】
- ❌ 表面能：未找到，需要补充

【表面吸附参数】（从文献提取）
111 晶面：
  - CO 吸附能：E_ads = -1.734 eV
  - O₂ 吸附能：E_ads = -1.214 eV
100 晶面：
  - CO 吸附能：E_ads = -1.666 eV
  - O₂ 吸附能：E_ads = -1.064 eV
110 晶面：
  - CO 吸附能：E_ads = -1.727 eV
  - O₂ 吸附能：E_ads = -0.960 eV

【相互作用矩阵】（从文献提取，已转换为MSR格式）
  CO-CO：(100) -0.596 eV, (110) -0.318 eV, (111) -1.008 eV
  O-O：(100) -0.768 eV, (110) -0.474 eV, (111) -1.074 eV
  CO-O：(100) -0.600 eV, (110) -0.210 eV, (111) -0.798 eV

⚠️ 注意：缺少表面能数据，建议：
1. 搜索其他文献补充表面能
2. 使用默认表面能值
3. 用户提供已知参数
```

---

## 🔗 与其他技能的协作

### 被以下技能调用

- **chatmosp-parameter-builder**：当MOSP_database中没有匹配参数时，调用此技能

### 调用以下工具

- **openclaw_browser**：期刊网站访问、SI下载
- **pdftotext**：PDF转文本
- **read**：读取文本文件

---

## 📖 参考文档

- **web-tools-guide**：网络工具使用指南
- **chatmosp-parameter-builder**：参数构建器技能
- **MOSP_database**：参数库

---

## 📝 版本历史

| 日期 | 版本 | 说明 |
|------|------|------|
| 2026-05-14 | v1.0 | 初始版本，从chatmosp-parameter-builder中提取 |

---

**技能创建者**：OpenClaw Agent
**创建日期**：2026-05-14
**技能位置**：/root/.openclaw/workspace/skills/chatmosp-literature-search/
