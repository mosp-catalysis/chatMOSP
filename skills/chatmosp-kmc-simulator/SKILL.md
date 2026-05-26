# Skill: chatmosp-kmc-simulator

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

## 🚀 快速开始：KMC计算正确流程

### 前提条件：
- MSR任务已完成，生成了 `ini.xyz` 结构文件
- Wine环境已安装（运行Windows版main.exe必需）

### 步骤1：创建KMC任务目录
```bash
# 命名规则：{MSR任务名}_KMC{步数}/
mkdir -p Pd_CO9_O18_473K_101325Pa_R50_KMC2000/INPUT
mkdir -p Pd_CO9_O18_473K_101325Pa_R50_KMC2000/OUTPUT
```

### 步骤2：准备输入文件（⚠️ 重要！）
```bash
# 文件位置：KMC任务目录/下，不是INPUT/下！

# 复制结构文件（从MSR任务目录）
cp MSR任务目录/ini.xyz KMC任务目录/ini.xyz

# 准备KMC参数input.json（从MOSP_database复制并修改）
# 文件位置：KMC任务目录/input.json
```

### ⚠️ 文件位置说明：
```
正确的目录结构：
KMC任务目录/
├── ini.xyz          ← 在INPUT外面
├── input.json       ← 在INPUT外面
├── INPUT/           ← 运行前应为空
└── OUTPUT/          ← 运行前应为空
```

**重要原因**：
- kmc_standalone.py运行时会清空INPUT/和OUTPUT/目录
- 因此ini.xyz和input.json必须放在INPUT外面
- 运行前确保INPUT/和OUTPUT/目录为空

### 步骤3：准备完整KMC参数
```bash
# 从MOSP_database复制KMC参数模板
cp mosp-for-chatMOSP/MOSP_database/Pd-COoxidation.json KMC任务目录/input.json

# 根据用户输入调整参数（重要字段）：
# - nLoop: 用户指定的步数（如2000）
# - T: 温度
# - gas_pp: 气体分压
# - record_int: 记录间隔

# 必需字段（从example继承）：
# - nspecies: 2 (CO, O₂)
# - nproducts: 1 (CO₂)
# - nevents: 7 (吸附、脱附、扩散、反应)
# - s1, s2: 物种定义
# - p1: 产物定义
# - e1-e7: 反应事件定义
# - li: 晶格相互作用矩阵
```

### 步骤4：展示参数给用户确认
（详见下方"🔄 KMC参数交互确认流程"部分）

### 步骤5：运行KMC

**⚠️ 长步数KMC计算时间提醒**

当KMC步数≥2000万步时，计算时间较长，执行前必须提醒用户：

```
⚠️ 计算时间提醒：
当前KMC步数为 {N} 步，预计计算时间约 {estimated_hours} 小时。
（参考：2000万步约需12小时）
同时运行多个任务可能导致用时增加。
是否继续执行KMC模拟？
```

**时间参考**:
- 2000万步（20M steps）：约12小时
- 4000万步（40M steps）：约24小时或更长
- 步数越多，时间线性增长

**注意**：如果用户选择多个条件（如多个温度），每个条件都需要单独计算，总时间会成倍增加。

```bash
# KMC运行指令（注意：输出目录不需要添加OUTPUT前缀）
python3 ../../kmc_standalone.py \
  --xyz OUTPUT/{任务目录名}/ini.xyz \
  --json OUTPUT/{任务目录名}/input.json \
  --out-dir {任务目录名}

# 说明：kmc_standalone.py会自动添加OUTPUT前缀
# 例如：--out-dir Pt_CO60_O40_800K_500Pa_R20_KMC2000
# 实际输出：OUTPUT/Pt_CO60_O40_800K_500Pa_R20_KMC2000/OUTPUT/
```

### 步骤6：检查KMC输出并重新绘制图像

**应用场景**：
- 用户提交了较长时间的KMC任务
- 询问agent任务是否结束
- agent检查发现任务结束
- 检查KMC任务目录是否存在coverage.png和tof.png
- 如果不存在，运行绘图脚本重新生成

**检查时机**：KMC运行结束后

**检查内容**：
1. 检查OUTPUT文件夹是否存在rec_cov.data、rec_event.data、rec_site_spc.data文件
2. 检查KMC任务目录是否存在coverage.png和tof.png
3. 如果图像不存在，运行绘图脚本重新生成

**文件位置说明**：
- 数据文件位置：KMC任务目录/OUTPUT/（rec_cov.data、rec_event.data、rec_site_spc.data）
- 图像文件位置：KMC任务目录/（coverage.png、tof.png）

**检查与绘图命令**：
```bash
# 定义KMC任务目录
KMC_TASK_DIR="KMC任务目录"
KMC_OUTPUT="$KMC_TASK_DIR/OUTPUT"

# 检查数据文件是否存在
if [ ! -f "$KMC_OUTPUT/rec_cov.data" ] || [ ! -f "$KMC_OUTPUT/rec_event.data" ] || [ ! -f "$KMC_OUTPUT/rec_site_spc.data" ]; then
  echo "❌ KMC数据文件不存在，KMC模拟可能未开始或未成功完成"
  exit 1
fi

# 检查KMC是否成功结束：比较预期步数和实际运行步数
EXPECTED_STEPS=$(grep -E "^[0-9]+\s+! Num of steps" "$KMC_TASK_DIR/INPUT/input.txt" | awk '{print $1}')
ACTUAL_STEPS=$(tail -n 1 "$KMC_OUTPUT/rec_event.data" | awk '{print $2}')

if [ "$EXPECTED_STEPS" != "$ACTUAL_STEPS" ]; then
  echo "❌ KMC模拟未成功完成"
  echo "  预期步数: $EXPECTED_STEPS"
  echo "  实际运行步数: $ACTUAL_STEPS"
  echo "请检查KMC运行日志，确认错误原因"
  exit 1
fi

echo "✅ KMC已成功完成（步数：$ACTUAL_STEPS）"

# 检查图像文件是否存在
if [ -f "$KMC_TASK_DIR/coverage.png" ] && [ -f "$KMC_TASK_DIR/tof.png" ]; then
  echo "✅ KMC输出图像已存在"
  echo "  Coverage plot: $KMC_TASK_DIR/coverage.png"
  echo "  TOF plot: $KMC_TASK_DIR/tof.png"
else
  echo "⚠️ KMC输出图像不存在，正在重新生成..."
  
  # 运行绘图脚本
  python3 ../../utils/plot_kmc_data.py "$KMC_OUTPUT"
  
  echo "✅ 图像已重新生成"
  echo "  Coverage plot: $KMC_TASK_DIR/coverage.png"
  echo "  TOF plot: $KMC_TASK_DIR/tof.png"
fi
```

**绘图脚本说明**：
- 脚本位置：mosp-for-chatMOSP/utils/plot_kmc_data.py
- 功能：读取rec_cov.data、rec_event.data、rec_site_spc.data文件，生成图像和CSV文件
- 图像保存位置：KMC任务目录（与kmc_standalone.py一致）
- CSV文件保存位置：KMC任务目录/OUTPUT/

**生成的文件**：
- coverage.png - 覆盖率随时间变化的图像（保存在KMC任务目录）
- tof.png - TOF随时间变化的图像（保存在KMC任务目录）
- coverage.csv - 覆盖率数据（保存在OUTPUT目录）
- tof.csv - TOF数据（保存在OUTPUT目录）
- site_tof.csv - 位点TOF数据（保存在OUTPUT目录）

**注意事项**：
- 无需重新运行KMC模拟
- 绘图脚本会自动识别反应事件（如CO+O）
- 如果数据文件不存在，说明KMC模拟未成功完成，需要检查运行日志

**常见问题**：
- Q: 为什么图像在KMC任务目录，而不是OUTPUT目录？
- A: 这是kmc_standalone.py的设计，图像保存在KMC任务目录，数据文件保存在OUTPUT目录

- Q: 如果KMC模拟未成功完成怎么办？
- A: 检查KMC运行日志，确认错误原因，修复后重新运行KMC

---

## ⚠️ KMC执行前检查清单

在运行KMC之前，**必须**确认以下项目全部完成：

### 📁 目录结构检查
- [ ] KMC任务目录已创建
- [ ] INPUT/文件夹已创建
- [ ] OUTPUT/文件夹已创建
- [ ] ini.xyz文件已复制到KMC任务目录
- [ ] input.json文件已创建在KMC任务目录（不是INPUT/下）

### 📄 input.json必需字段检查

**顶层必需字段：**
- [ ] Element（金属元素）
- [ ] Lattice constant（晶格常数）
- [ ] Crystal structure（晶体结构）
- [ ] Temperature（温度）
- [ ] Pressure（压力）
- [ ] flag_MSR: false
- [ ] flag_KMC: true
- [ ] KMC（KMC参数对象）

**KMC部分必需字段：**
- [ ] nLoop（模拟步数）
- [ ] nspecies（物种数量）
- [ ] nproducts（产物数量）
- [ ] nevents（反应事件数）
- [ ] s1, s2（物种定义）
- [ ] p1（产物定义）
- [ ] e1-e7（反应事件定义）
- [ ] li（晶格相互作用矩阵）

### ✅ 检查命令
```bash
# 检查目录结构
ls -la KMC任务目录/

# 检查input.json顶层字段
cat KMC任务目录/input.json | jq 'keys'

# 检查KMC部分字段
cat KMC任务目录/input.json | jq '.KMC | keys'
```

### ⚠️ 常见错误及解决方案

| 错误信息 | 原因 | 解决方案 |
|---------|------|----------|
| `missing top-level field 'Lattice constant'` | input.json缺少必需的顶层字段 | 从MOSP_database复制完整模板，不要手动创建 |
| `INPUT/ or OUTPUT/ directory not found` | 缺少INPUT/OUTPUT文件夹 | 执行步骤1创建文件夹 |
| `ini.xyz not found` | ini.xyz文件不存在或位置错误 | 从MSR任务目录复制ini.xyz到KMC任务目录 |

---

### KMC参数来源：
1. **从MOSP_database复制**：
   - `MOSP_database/Pd-COoxidation.json`
   - `MOSP_database/Pt-COoxidation.json`

2. **根据用户输入调整**：
   - nLoop: 用户指定的步数
   - T: 温度
   - 其他参数从example继承

3. **不使用MSR的input.json**：
   - MSR参数不完整，缺少KMC必需字段
   - KMC需要独立的完整参数配置

---

## 📋 技能概览

**技能名称**: `chatmosp-kmc-simulator`  
**技能类型**: KMC计算引擎  
**核心职责**: 动力学蒙特卡洛模拟  

### 技能定位
KMC模拟器是chatMOSP系统的动力学计算引擎，负责：
1. **KMC模拟执行**：执行催化剂表面反应动力学模拟
2. **资源保护机制**：4000万步警告和自动资源保护
3. **结果分析与可视化**：提取TOF、覆盖度、反应路径

### 核心安全特性
- ⚠️ **4000万步警告**：当KMC步数超过4000万时发出警告
- ✅ **资源保护**：自动监控内存和CPU使用
- 📊 **进度报告**：实时监控模拟进度

## 🔄 KMC参数交互确认流程

### 流程：
```
用户请求KMC → 准备完整参数 → 展示参数模板 → 用户确认 → 运行KMC
```
### 参数展示模板：

```markdown
📊 KMC参数已准备好，请确认：

【基本信息】
- 任务类型：KMC (动力学蒙特卡洛模拟)
- 反应：CO氧化反应 (2CO + O2 → 2CO2)
- 温度：473 K (200°C)
- 压力：101325 Pa (1 atm)
- 气体分压：CO 9%, O2 18%

【团簇信息】(来自MSR结果)
- 金属元素：Pd
- 团簇半径：50 Å
- 原子数量：3,888 个
- 晶体结构：FCC (面心立方)
- MSR任务目录：Pd_CO9_O18_473K_101325Pa_R50

【模拟参数】
- 模拟步数：5,000,000 步
- 记录间隔：每10,000步记录一次
- 物种数量：5 种
- 反应事件：14 种

【物种定义】
- s1：CO (反应物)
- s2：O2 (反应物)
- s3：O (中间体)
- s4：CO2 (产物)
- s5：空位

【产物定义】
- p1：CO2 (事件X, Y生成)

【反应机制】(简要说明)
- CO吸附、脱附、扩散
- O2解离、扩散
- CO + O → CO2

【输出设置】
- KMC任务目录：Pd_CO9_O18_473K_101325Pa_R50/KMC_5000000steps/
- 生成文件：input.json, 输出文件等

请选择：
1. ✅ 确认 - 使用这些参数继续执行KMC模拟
2. ✏️ 修改 - 调整模拟步数或其他参数(如温度、压强、气体组成等)
3. 📊 对比 - 运行多个条件进行对比(如多个温度、压强)
4. 🔄 切换计算模式 - 切换到MSR结构计算
5. ❌ 取消任务，更换体系 - 更换金属或气体体系

建议：
- 如果想快速测试，可以先运行较少步数(如100,000步)
- 500万步可以获得更准确的统计数据，但耗时更长

请回复您的选择(数字1-5或关键词)，或告诉我要修改的参数。
```
---

## 🎯 核心功能

### 1. KMC模拟执行
- 调用 mosp-for-chatMOSP KMC引擎
- 准备KMC输入文件（KMC-input.json）
- 捕获动力学数据

### 2. 资源保护与警告
```
步数监控 → 超过阈值警告 → 用户确认 → 继续执行
```

### 3. 结果处理与分析
- 解析TOF（周转频率）数据
- 提取表面覆盖度信息
- 生成反应路径分析
- 创建可视化图表（覆盖度图等）

## 🔧 技术实现

### ⚠️ 系统要求
KMC计算需要Wine环境运行Windows版`main.exe`引擎：

```bash
# 检查Wine是否已安装
which wine

# 如果未安装，请安装：
sudo apt-get update
sudo apt-get install wine
```

### 自动环境检查
系统会自动检查Wine环境：
- ✅ 如果Wine已安装：正常执行KMC计算
- ⚠️ 如果Wine未安装：提示安装指导
- ❌ 如果Wine版本不兼容：提示升级

### 依赖关系
- `mosp-for-chatMOSP` - 核心计算引擎（已克隆）
- `chatmosp-file-organizer` - 文件路径管理
- `chatmosp-parameter-builder` - 参数验证
- **Wine环境** - 运行Windows版`main.exe`（必需）

### 执行流程
```
接收参数 → 验证参数 → 准备输入 → 检查Wine环境 → 
Wine可用 → 执行KMC → 监控进度 → 检查资源 → 收集结果 → 分析数据
       ↓
   Wine不可用 → 提示安装指导 → 中止计算
       ↓
    4000万步警告 → 用户交互 → 继续/停止
```

## 📝 使用示例

```
用户: 对Pt纳米颗粒进行CO氧化KMC模拟，850K，150Pa，2000万步
系统: [识别为KMC任务 → 查找/确认参数 → ⚠️ 2000万步约需12小时，确认继续？→ 执行KMC → 绘制TOF/覆盖度图 → 展示结果]
```
