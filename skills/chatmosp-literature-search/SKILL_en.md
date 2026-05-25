# Skill: chatmosp-literature-search

## 🎯 Skill Overview / 技能简介

Search and extract MSR/KMC parameters from academic literature. When MOSP_database lacks matching parameters, use this skill to obtain parameters from literature.
/ 从学术文献中搜索和提取MSR/KMC参数。当MOSP_database中没有匹配的参数时，使用此技能从文献中获取参数。

## 🌐 Language Matching Rules / 语言匹配规则

**IMPORTANT**: Based on the language of user input, select the appropriate SKILL.md version and match the output language.
/ **重要提示**: 根据用户输入的语言，选择合适的SKILL.md版本并匹配输出语言。

1. **User inputs Chinese / 用户输入中文**:
   - Read SKILL.md (Chinese version) / 阅读SKILL.md（中文版）
   - Output response in Chinese / 使用中文输出回复

2. **User inputs English / 用户输入英文**:
   - Read SKILL_en.md (Bilingual version) / 阅读SKILL_en.md（双语对照版）
   - Output response in English / 使用英文输出回复

---

## 📋 Input & Output / 输入与输出

### Input / 输入

- **Metal element** (required): Pd, Pt, Au, Cu, Ni, etc. / **金属元素**（必需）：Pd, Pt, Au, Cu, Ni等
- **Gas system** (required): CO+O2, H2+CO2, CO+H2, etc. / **气体体系**（必需）：CO+O2, H2+CO2, CO+H2等
- **Temperature range** (optional): e.g., 300-500K / **温度范围**（可选）：例如 300-500K
- **Pressure range** (optional): e.g., 1-10 atm / **压力范围**（可选）：例如 1-10 atm

### Output / 输出

- **Parameter table**, including: / **参数表格**，包含：
  - Surface energy (each facet) / 表面能（各晶面）
  - Adsorption energy (each facet + each gas) / 吸附能（各晶面 + 各气体）
  - Interaction matrix / 相互作用矩阵
  - **Parameter source** (DOI, article title) / **参数来源**（DOI、文献标题）
  - **Parameter completeness score** (1-10) / **参数完整性评分**（1-10分）

---

## 🔄 Workflow / 工作流程

### Overall Flow / 整体流程

```
Input (metal + gas) → Journal Search → Article Retrieval → Parameter Extraction → Parameter Validation → Output (parameter table)
/ 输入（金属 + 气体） → 期刊搜索 → 文章检索 → 参数提取 → 参数验证 → 输出（参数表格）
```

### Step 1: Journal Search (by priority) / 步骤1：期刊搜索（按优先级）

- Layer 1: Top journals (Science, Nature, JACS, Angewandte Chemie, etc.) / 第1层：顶刊（Science, Nature, JACS, Angewandte Chemie等）
- Layer 2: Open access journals (Nature Communications, Science Advances, PNAS, etc.) / 第2层：开放获取期刊（Nature Communications, Science Advances, PNAS等）
- Layer 3: Preprint platforms (arXiv, ChemRxiv, etc.) / 第3层：预印本平台（arXiv, ChemRxiv等）

### Step 2: Detailed Literature Retrieval Process / 步骤2：详细文献检索流程

#### 2.1 Journal Selection and Search / 2.1 期刊选择与检索

**Journal Classification / 期刊分类**：

**Open Access Journals (no payment required) / 开放获取期刊（无需付费）**：
- Nature Communications
- Science Advances
- PNAS (Proceedings of the National Academy of Sciences)
- ACS Central Science
- Chemical Science

**Paid Journals (requires access) / 付费期刊（需要访问权限）**：
- Science
- Nature
- JACS (Journal of the American Chemical Society)
- Angewandte Chemie

---

#### 2.2 Single Journal Search Process / 2.2 单个期刊检索流程

**Step 1: Build Search Keywords / 步骤1：构建搜索关键词**

Based on the system, build search keywords / 根据体系构建搜索关键词：

**✅ Correct Format / ✅ 正确格式：**
```
"keyword1" AND "keyword2" AND "keyword3"
```

**Examples / 示例：**
- Example 1 / 示例1：Cu cluster in CO oxidation environment → search `"Cu" AND "CO oxidation"` / Cu团簇在一氧化碳氧化环境下 → 搜索 `"Cu" AND "CO oxidation"`
- Example 2 / 示例2：Pd cluster in CO oxidation environment → search `"Pd" AND "CO oxidation"` / Pd团簇在CO氧化环境下 → 搜索 `"Pd" AND "CO oxidation"`
- Example 3 / 示例3：Pt cluster in H2 environment → search `"Pt" AND "H2"` / Pt团簇在氢气环境下 → 搜索 `"Pt" AND "H2"`

**⚠️ IMPORTANT: Do NOT use incorrect format! / ⚠️ 重要提示：禁止使用错误的格式！**

**❌ Incorrect Format (DO NOT USE) / ❌ 错误格式（禁止使用）：**
```
Pd CO oxidation
```
**Problem / 问题：** Space-separated format leads to inaccurate search results. The search system treats the entire phrase as a single keyword, rather than searching for "Pd" and "CO oxidation" separately. / 空格分隔的格式会导致搜索结果不准确，搜索系统会将整个短语作为一个关键词搜索，而不是分别搜索"Pd"和"CO oxidation"两个关键词。

**✅ Correct Format (MUST USE) / ✅ 正确格式（必须使用）：**
```
"Pd" AND "CO oxidation"
```
**Advantage / 优点：** Each keyword is wrapped in double quotes and connected with AND, ensuring the search system correctly understands the keywords and returns more accurate search results. / 每个关键词用双引号包裹，用AND连接，确保搜索系统正确理解关键词的含义，返回更准确的搜索结果。

**Step 2: Use openclaw_browser to access journal website / 步骤2：使用openclaw_browser访问期刊网站**

- Access the journal's search page / 访问期刊的搜索页面
- Enter search keywords / 输入搜索关键词
- Search results are sorted by relevance by default / 搜索结果默认按相关性排列

**Step 3: Retrieve top 10 search results / 步骤3：获取前10个搜索结果**

- Only check the top 10 results (highest relevance) / 只检查前10个结果（相关性最高）
- Output top 10 article titles, DOI, abstract (optional) / 输出前10名的文献名称、DOI、摘要（可选）

---

#### 2.3 Initial Screening (based on title) / 2.3 初步筛选（基于题目）

**Screening Criteria / 筛选标准**：
1. **Reaction atmosphere match / 反应气氛体系匹配**：Must be the same reaction atmosphere (e.g., CO oxidation, water-gas shift, etc.) / 必须是相同的反应气氛（如CO氧化、水汽变换等）
2. **Metal system match / 金属体系匹配**：Must be the same metal (e.g., Pd, Pt, Cu, etc.), exclude alloy systems / 必须是相同的金属（如Pd、Pt、Cu等），排除合金体系

**Screening Results / 筛选结果**：
- Output filtered article list / 输出被筛选后的文献列表
- Note screening reason for each article / 标注每篇文献的筛选理由

---

#### 2.4 User Interaction / 2.4 用户交互

**Ask user to select / 询问用户选择**：

Please select next action / 请选择下一步操作：
1. **Carefully check all filtered articles / 仔细检查这些被筛选的全部文章** - Detailed check on all filtered articles / 对所有被筛选的文章进行详细检查
2. **Carefully check a specific article / 仔细检查某一篇文章** - Only check a user-specified article / 只检查用户指定的某一篇文章
3. **Switch to another journal / 换成另一期刊检索** - Abandon current journal, switch to another / 放弃当前期刊，换另一个期刊

---

#### 2.5 Detailed Article Content Check / 2.5 详细检查文章内容

**Check Process / 检查流程**：

**Step 1: Check article main text / 步骤1：检查文章正文**
- Confirm same metal system / 确认是相同的金属体系
- Confirm same reaction atmosphere / 确认是相同的反应气氛
- Check if main text contains parameter tables / 检查正文是否包含参数表格

**Step 2: If no parameters, download SI / 步骤2：如果没有参数，下载SI**
- Parameters only exist in text and tables, not in images / 参数只可能存在于文字和表格中，不会出现在图像中
- Download SI file (PDF format) / 下载SI文件（PDF格式）

**Step 3: Check SI file / 步骤3：检查SI文件**
- Search keywords: Table, Supplementary Table, S1, S2, etc. / 搜索关键词：Table, Supplementary Table, S1, S2等
- Extract parameter tables / 提取参数表格

---

#### 2.6 Parameter Extraction and Confirmation / 2.6 参数提取与确认

**Step 1: Extract parameters / 步骤1：提取参数**

Extract the following parameters from article main text or SI / 从文章正文或SI中提取以下参数：
- Surface energy (each facet) / 表面能（各晶面）
- Adsorption energy (each facet + each gas) / 吸附能（各晶面 + 各气体）
- Interaction matrix / 相互作用矩阵
- Parameter source (DOI, article title) / 参数来源（DOI、文献标题）

**Step 2: Display parameters to user / 步骤2：向用户展示参数**

```
📊 Extracted parameters from literature / 从文献中提取到以下参数：

【Article Information / 文献信息】
- Title / 标题：xxx
- DOI：xxx
- Journal / 期刊：xxx

【Parameter Table / 参数表格】
- Surface energy / 表面能：...
- Adsorption energy / 吸附能：...
- Interaction matrix / 相互作用矩阵：...

【Parameter Completeness Score / 参数完整性评分】
- Score / 评分：8/10
- Description / 说明：Parameters relatively complete, can be used / 参数较完整，可以使用
```

**Step 3: Ask user whether to use / 步骤3：询问用户是否使用**

Please select / 请选择：
1. **Use these parameters / 使用这些参数** - Pass parameters to chatmosp-parameter-builder / 将参数传递给chatmosp-parameter-builder
2. **Reject, continue search / 拒绝，继续检索** - Continue searching next article / 继续检索下一篇文章
3. **Cancel task / 取消任务** - End literature search / 结束文献检索

---

#### 2.7 Handling One Journal Search Failure / 2.7 一个期刊检索失败的处理

**Situation / 情况**：No parameters found in top 10 filtered articles of one journal / 一个期刊的前10篇被筛选的文章都没找到参数

**Ask user / 询问用户**：

```
⚠️ No parameters found in top 10 relevant articles of {Journal Name} / 在{期刊名称}的前10篇相关文章中未找到参数

Please select / 请选择：
1. **Switch journal / 更换期刊** - Switch to another journal to continue search / 换另一个期刊继续检索
2. **Cancel task / 取消任务** - If all journals have been searched, suggest changing system or user providing parameters / 如果所有期刊都没有，建议更换体系或用户提供参数
```

---

#### 2.8 Handling All Journals Search Failure / 2.8 所有期刊检索失败的处理

**Situation / 情况**：All journals have been searched, still no parameters found / 所有期刊都检索完毕，仍未找到参数

**Suggest user / 建议用户**：
1. Change metal or gas system / 更换金属或气体体系
2. User provides parameters themselves / 用户自己提供参数
3. Cancel task / 取消任务

---

### Step 3: Article Retrieval (3 stages) / 步骤3：文章检索（3个阶段）

- Stage 1: Abstract retrieval (confirm relevance) / 阶段1：摘要检索（确认相关性）
- Stage 2: Main text retrieval (find parameter tables) / 阶段2：正文检索（查找参数表格）
- Stage 3: SI retrieval (supplement parameters) / 阶段3：SI检索（补充参数）

### Step 3: Parameter Extraction / 步骤3：参数提取

- Extract surface energy / 提取表面能
- Extract adsorption energy / 提取吸附能
- Extract interaction matrix / 提取相互作用矩阵

### Step 4: Parameter Validation / 步骤4：参数验证

- Check completeness / 检查完整性
- Check reasonability / 检查合理性
- Check consistency / 检查一致性

### Step 5: Output Results / 步骤5：输出结果

- Display parameter table / 展示参数表格
- Provide parameter source / 提供参数来源
- Provide completeness score / 提供完整性评分

---

## ⚠️ Important Constraints & Mechanisms / ⚠️ 重要限制与机制

### Timeout Mechanism / 超时机制

**Total search time limit**: 5 minutes / **总搜索时间限制**：5分钟

**Single article retrieval limit**: 2 minutes / **单篇文章检索限制**：2分钟

**Timeout handling** / **超时处理**:
- If total time exceeds 5 minutes, stop search immediately / 如果总时间超过5分钟，立即停止搜索
- Return found parameters (even if incomplete) / 返回已找到的参数（即使不完整）
- Explain situation to user / 向用户说明情况

### Fallback Plan / 降级方案

**If 5 articles searched without complete parameters** / **如果搜索了5篇文章还没有找到完整参数**:

1. Explain situation to user / 向用户说明情况:
   ```
   I have searched 5 articles but could not find complete parameters.
   / 我已经搜索了5篇文献，但未能找到完整的参数。
   
   Found partial parameters: / 找到的部分参数：
   - Surface energy: ✅ Found / 表面能：✅ 已找到
   - Adsorption energy: ❌ Not found / 吸附能：❌ 未找到
   - Interaction matrix: ❌ Not found / 相互作用矩阵：❌ 未找到
   
   Suggested options: / 建议选项：
   1. Use parameters from similar metal as reference / 使用相似金属的参数作为参考
   2. Provide known parameter source (DOI or article title) / 提供已知参数来源（DOI或文献标题）
   3. Use default/test parameters / 使用默认/测试参数
   ```

2. Provide alternative solutions / 提供替代方案

---

## 🔧 Journal Search Tool Selection / 🔧 期刊搜索工具选择

### ⚠️ Important: Tool Selection / ⚠️ 重要提示：工具选择

**Do NOT use web_fetch** / **不要使用web_fetch**:
- ❌ Journal websites often have access restrictions (403 errors, CAPTCHA verification) / 期刊网站常有访问限制（403错误、CAPTCHA验证）
- ❌ web_fetch prone to failure / web_fetch容易失败
- ❌ Cannot execute JavaScript, cannot get dynamically loaded content / 无法执行JavaScript，无法获取动态加载的内容

**Prioritize openclaw_browser** / **优先使用openclaw_browser**:
- ✅ Supports JavaScript rendering / 支持JavaScript渲染
- ✅ Supports login state / 支持登录态
- ✅ Supports interactive operations / 支持交互操作
- ✅ Better suited for journal website access / 更适合期刊网站访问

**Fallback option** / **降级方案**:
- ✅ If openclaw_browser unavailable, try opencli CLI tool / 如果openclaw_browser不可用，可以尝试opencli CLI工具
- 📖 Detailed guide: Refer to `web-tools-guide` skill document / 详细指南：参考 `web-tools-guide` 技能文档

---

## 📊 MSR Required Data Checklist / 📊 MSR需求的数据清单

### Basic Parameters / 基本参数

- ✅ Metal element - Element (Pd, Pt, Au, Cu, etc.) / 金属元素
- ✅ Temperature - Temperature (K) / 温度
- ✅ Pressure - Pressure (Pa) / 压力
- ✅ Cluster radius - Radius (Å) / 团簇半径
- ✅ Gas species - Gas species (CO, O2, H2, etc.) / 气体种类
- ✅ Partial pressures - Partial pressures (%) / 气体分压

### Surface Parameters (each facet) / 表面参数（每个晶面）

- ✅ Surface energy - Surface energy (eV/Å²) / 表面能
  - (100), (110), (111), (211), (311), etc.

### Adsorption Parameters (each facet + each gas) / 吸附参数（每个晶面 + 每种气体）

- ✅ Adsorption energy - Adsorption energy E_ads (eV) / 吸附能
  - Example: CO adsorption energy on Pd(111) / 例：CO在Pd(111)的吸附能
  - Example: O2 adsorption energy on Pd(100) / 例：O2在Pd(100)的吸附能

### Interaction Parameters / 相互作用参数

- ✅ Interaction matrix - Interaction matrix (eV) / 相互作用矩阵
  - CO-CO interaction / CO-CO相互作用
  - CO-O interaction / CO-O相互作用
  - O-O interaction / O-O相互作用

### Gas Parameters / 气体参数

- ✅ Gas entropy - Gas entropy (eV/K) / 气体熵
  - Can be calculated via formula (temperature dependent) / 可通过公式计算（温度依赖）
  - Or extracted from literature / 或从文献中提取

---

## 🎯 Parameter Completeness Scoring / 🎯 参数完整性评分

### Scoring Criteria (10-point scale) / 评分标准（10分制）

| Parameter Type | Score | Description |
|---------------|-------|-------------|
| Surface energy | 2 points | At least (100), (110), (111) three facets / 至少包含(100), (110), (111)三个晶面 |
| Adsorption energy | 3 points | Adsorption energy of each gas on each facet / 每种气体在各晶面的吸附能 |
| Interaction matrix | 3 points | CO-CO, CO-O, O-O interactions / CO-CO, CO-O, O-O相互作用 |
| Parameter source | 1 point | DOI, article title, author information / DOI、文献标题、作者信息 |
| Parameter reasonability | 1 point | Parameters within reasonable range, physically plausible / 参数在合理范围内，符合物理规律 |

### Completeness Levels / 完整性等级

- **9-10 points**: Complete, ready to use / 完整，可直接使用
- **7-8 points**: Mostly complete, usable but needs user confirmation / 较完整，可以使用，但需要用户确认
- **5-6 points**: Partially complete, needs supplementary parameters / 部分完整，需要补充参数
- **3-4 points**: Incomplete, recommend alternative solutions / 不完整，建议使用替代方案
- **1-2 points**: Very incomplete, not recommended / 极不完整，不推荐使用

---

**Note / 注意**: Interaction parameter conversion rules have been moved to chatmosp-parameter-builder skill, please refer to / 相互作用参数转换规则已经移到chatmosp-parameter-builder技能中，请参考：
- **chatmosp-parameter-builder/SKILL_en.md** section "#### 2.4 Interaction Parameter Conversion / 相互作用参数转换" / **chatmosp-parameter-builder/SKILL_en.md** 的 "#### 2.4 Interaction Parameter Conversion / 相互作用参数转换" 章节
- **chatmosp-parameter-builder/SKILL.md** section "#### 2.4 相互作用参数转换" / **chatmosp-parameter-builder/SKILL.md** 的 "#### 2.4 相互作用参数转换" 章节

---

## 💡 Literature Search Lessons Learned / 💡 文献搜索经验教训

### Lesson 1: Keyword Selection Strategy / 教训1：关键词选择策略

**Problem**: Keywords too specific, filtered out relevant articles / **问题**：关键词太具体，过滤掉了相关文章

**Solution** / **解决方案**:
- Start with broad keywords (e.g., `"Pd" AND "CO oxidation"`) / 先用宽泛关键词搜索（如`"Pd" AND "CO oxidation"`）
- Then filter with specific keywords (e.g., "adsorption energy") / 再用具体关键词筛选（如"adsorption energy"）
- Don't only search parameter names, search article topics / 不要只搜索参数名称，要搜索文章主题

### Lesson 2: DOI Priority Principle / 教训2：DOI优先原则

**Problem**: Cannot find target article / **问题**：搜索不到目标文章

**Solution** / **解决方案**:
- Prioritize using known DOI or article title / 优先使用已知的DOI或文章标题
- If DOI available, access directly / 如果有DOI，直接访问DOI
- Don't rely solely on keyword search / 不要只依赖关键词搜索

### Lesson 3: Multi-platform Search / 教训3：多平台搜索

**Problem**: Single platform search results limited / **问题**：单一平台搜索结果有限

**Solution** / **解决方案**:
- Don't limit to single journal website / 不局限于单一期刊网站
- Search multiple journal platforms / 搜索多个期刊平台
- Prioritize open access journals / 使用开放获取期刊优先

### Lesson 4: Don't Waste Time on Inaccessible Resources / 教训4：不要浪费时间在无法访问的资源上

**Problem**: Wasting time on access-restricted articles / **问题**：在访问受限的文章上浪费时间

**Solution** / **解决方案**:
- Encounter API limits or access restrictions → Immediately jump to Layer 2 / 遇到API限制或访问受限 → 立即跳到第2层
- Encounter CAPTCHA → Skip, proceed to next layer / 遇到CAPTCHA验证 → 跳过，进入下一层
- Prioritize searching open access resources / 优先搜索开放获取资源

### Lesson 5: No Parameter Mention in Main Text Doesn't Mean No Parameter in SI / 教训5：正文没提到参数不代表SI没有

**Problem**: Main text doesn't mention parameter tables, so skipped SI / **问题**：正文没有提到参数表格，就跳过了SI

**Solution** / **解决方案**:
- If article relevance is high, still download SI to check / 如果文章相关性很高，仍然下载SI检查
- SI typically contains complete parameter tables / SI通常包含完整参数表格
- Don't judge based solely on main text / 不要仅根据正文判断

---

## 🔗 Collaboration with Other Skills / 🔗 与其他技能的协作

### Called by / 被以下技能调用

- **chatmosp-parameter-builder**: When MOSP_database lacks matching parameters, calls this skill / 当MOSP_database中没有匹配参数时，调用此技能

### Calls following tools / 调用以下工具

- **openclaw_browser**: Journal website access, SI download / 期刊网站访问、SI下载
- **pdftotext**: PDF to text conversion / PDF转文本
- **read**: Read text files / 读取文本文件

---

## 📖 Reference Documents / 📖 参考文档

- **web-tools-guide**: Web tools usage guide / 网络工具使用指南
- **chatmosp-parameter-builder**: Parameter builder skill / 参数构建器技能
- **MOSP_database**: Parameter database / 参数库

---

## 📝 Version History / 📝 版本历史

| Date | Version | Description |
|------|---------|-------------|
| 2026-05-14 | v1.0 | Initial version, extracted from chatmosp-parameter-builder / 初始版本，从chatmosp-parameter-builder中提取 |

---

**Skill Creator**: OpenClaw Agent / **技能创建者**：OpenClaw Agent
**Creation Date**: 2026-05-14 / **创建日期**：2026-05-14
**Skill Location**: /root/.openclaw/workspace/skills/chatmosp-literature-search/ / **技能位置**：/root/.openclaw/workspace/skills/chatmosp-literature-search/
