---
name: chatmosp-kmc-simulator
description: |
  chatMOSP 系统的 RKMC（反应动力学蒙特卡洛）模拟引擎。调用 kmc_standalone.py 通过 Wine
  环境运行 Windows 版 main.exe，执行催化剂表面反应动力学模拟，产出 TOF、覆盖度等
  动力学结果，并通过 utils/plot_kmc_data.py 生成 coverage.png, coverage_steps.png,
  tof.png, tof_time.png 共 4 张图像。
  触发场景：parameter-builder 完成 RKMC 参数构建并经用户确认后，由本技能执行 RKMC 模拟。
---

> **🌐 Language routing / 语言路由**
> Detect the user's language from their latest message.
> - **If the user writes in English** → read `SKILL_en.md` in this same skill
>   directory and follow it as the authoritative instructions; respond in English;
>   you do NOT need to read the rest of this Chinese document.
> - **若用户使用中文** → 继续使用本文件（`SKILL.md`）作为权威指令，并用中文回复。
> Always match the response language to the user's input language.

# chatmosp-kmc-simulator（RKMC — 反应动力学蒙特卡洛）

> Skill created by Sanyang Ye (https://github.com/sanyangye)

> **术语**：本技能即 **RKMC**（Reaction KMC，反应动力学蒙特卡洛）。模拟催化剂表面反应的
> **动力学过程**（TOF/覆盖度/反应活性）。相关概念：
> - **MSR** — 模拟团簇在反应气氛中的**平衡形貌**（静态，无需初始结构，产出 ini.xyz）。
> - **RKMC** — 模拟团簇在反应气氛中的**反应活性**（本技能，需初始结构，关注 TOF/覆盖度）。
> - **EKMC** — 模拟团簇在反应气氛中的**动态形貌**（见 `chatmosp-ekmc-simulator`，关注形貌演化/原子迁移）。
>
> ⚠️ **目录名不变**：skill 目录名保持 `chatmosp-kmc-simulator`，内部概念使用 RKMC。
> 代码/JSON字段/文件名中的 `KMC` 保持不变，仅文档层面区分 RKMC/EKMC。

## 1. 核心职责

1. 检查并管理 Wine 环境（RKMC 引擎依赖）
2. 准备 RKMC 输入文件（从 MOSP_database 复制模板 + 用户指定步数/温度/分压）
3. 执行 RKMC 模拟并监控进度
4. 步数预警（≥ 2000 万步时提醒用户）
5. 生成 TOF、覆盖度图与 CSV 数据
6. 步数不足或失败时自动重新绘图

## 2. 前置条件

- ✅ 初始结构可用（MSR 生成的 `ini.xyz`，或 EKMC 演化后的 `final_stru.xyz`）
- ✅ parameter-builder 已完成 RKMC 参数构建
- ✅ 用户已通过 5 选项确认（详见 parameter-builder §RKMC 参数展示格式）
- ✅ Wine 环境已安装（首次运行时检查并提示安装）
- ✅ 结构文件已复制到 RKMC 任务目录（如适用）
- ❌ 禁止绕过 parameter-builder 手动构建 RKMC 参数
- ❌ 禁止复用 MSR/EKMC 的 input.json——RKMC 必须独立准备完整参数

## 3. Wine 环境

RKMC 引擎是 Windows 版 main.exe，需要 Wine 运行。

### 3.1 检查 Wine

```bash
which wine64 || which wine
```

### 3.2 安装 Wine（Ubuntu/Debian）

```bash
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install wine64 wine32
```

### 3.3 自动环境检查

- ✅ Wine 已安装 → 正常执行
- ⚠️ Wine 未安装 → 提示安装指导
- ❌ 版本不兼容 → 提示升级

## 4. 步数警告

RKMC 步数 ≥ 2000 万时，执行前必须提醒用户：

```
⚠️ 计算时间提醒：
当前 RKMC 步数为 {N} 步，预计计算时间约 {estimated_hours} 小时。
（参考：2000 万步约 12 小时，4000 万步约 24 小时）
是否继续执行 RKMC 模拟？
```

| 步数 | 预计时间 |
|------|----------|
| 2,000 万（20M） | ~12 小时 |
| 4,000 万（40M） | ~24 小时或更长 |
| 更多 | 线性增长 |

注意：选择多个条件（如多温度对比）时，每个条件都要单独计算，总时间成倍增加。

## 5. 输入契约（input.json 必含字段）

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| Element | string | 金属元素（Pd、Pt、Au 等） |
| Lattice constant | string | 晶格常数（Å） |
| Crystal structure | string | 晶体结构（FCC、BCC、HCP） |
| Temperature | string | 温度（K） |
| Pressure | string | 压力（Pa） |
| flag_MSR | boolean | 必须 false |
| flag_KMC | boolean | 必须 true |
| KMC | object | KMC 参数对象 |

### KMC 对象内必含字段

| 字段 | 类型 | 说明 |
|------|------|------|
| nLoop | string | 模拟步数 |
| record_int | string | 记录间隔 |
| nspecies | number | 物种数量 |
| nproducts | number | 产物数量 |
| nevents | number | 反应事件数 |
| nevents_mob | number | 移动事件数 |
| s1 / s2 | string | 物种 1/2 定义（JSON 字符串） |
| p1 | string | 产物 1 定义（JSON 字符串） |
| e1 ~ e7 | string | 反应事件 1~7（JSON 字符串） |
| li | array | 晶格相互作用矩阵 |

> ⚠️ **关键**：气体熵 `s1.S_gas` / `s2.S_gas` 必须与 MSR 的 `Gas1_S` / `Gas2_S` 保持一致（用相同公式计算）。

## 6. 目录结构

RKMC 任务目录必须在 MSR（或 EKMC）目录下：

```
mosp-for-chatMOSP/OUTPUT/{source_task_name}/
└── RKMC_{步数}steps/             ← RKMC 任务目录
    ├── input.json                ← 在 INPUT 外面
    ├── ini.xyz                   ← 从 MSR（或 EKMC final_stru.xyz）复制
    ├── coverage.png              ← 运行后生成
    ├── coverage_steps.png        ← 运行后生成
    ├── tof.png                   ← 运行后生成
    ├── tof_time.png              ← 运行后生成
    ├── INPUT/                    ← 运行前应为空
    └── OUTPUT/                   ← 运行后填充
        ├── rec_cov.data
        ├── rec_event.data
        └── rec_site_spc.data
```

> ⚠️ **注意**：
> - `ini.xyz` 和 `input.json` 必须放在 `INPUT/` 外面（`kmc_standalone.py` 会清空 `INPUT/OUTPUT`）
> - 运行前确保 `INPUT/` 和 `OUTPUT/` 为空
> - 如果 RKMC 的起始结构来自 EKMC（而非 MSR），`{source_task_name}` 为 EKMC 任务目录名，`ini.xyz` 从 EKMC 的 `final_stru.xyz` 复制并重命名即可

## 7. 执行步骤

### 步骤 1：创建 RKMC 任务目录

```bash
mkdir -p OUTPUT/{source_task_name}/RKMC_{步数}steps/INPUT
mkdir -p OUTPUT/{source_task_name}/RKMC_{步数}steps/OUTPUT
```

### 步骤 2：复制结构文件

```bash
# 从 MSR 复制：
cp OUTPUT/{msr_task_name}/ini.xyz OUTPUT/{msr_task_name}/RKMC_{步数}steps/ini.xyz

# 或从 EKMC 复制（演化后结构）：
cp OUTPUT/{ekmc_task_dir}/EKMC-OUTPUT/final_stru.xyz \
   OUTPUT/{ekmc_task_dir}/RKMC_{步数}steps/ini.xyz
```

### 步骤 3：准备 input.json

```bash
# 从 MOSP_database 复制模板（不要手动创建）
cp mosp-for-chatMOSP/MOSP_database/{metal}-{reaction}.json \
   OUTPUT/{source_task_name}/RKMC_{步数}steps/input.json

# 调整字段：
# - nLoop: 用户指定的步数
# - T: 用户指定的温度
# - gas_pp: 用户指定的气体分压
# - record_int: 记录间隔
# - s1.S_gas / s2.S_gas: 用 parameter-builder §8.1 公式重算
```

### 步骤 4：展示参数给用户确认

使用 parameter-builder §RKMC 参数展示格式（5 选项）。

### 步骤 5：检查 Wine + 步数警告

- 检查 Wine 环境
- 步数 ≥ 2000 万时弹窗警告

### 步骤 6：执行 RKMC

```bash
# 从 mosp-for-chatMOSP 根目录执行（推荐）
cd mosp-for-chatMOSP && python3 kmc_standalone.py \
  --xyz OUTPUT/{任务目录}/ini.xyz \
  --json OUTPUT/{任务目录}/input.json \
  --out-dir {任务目录}
```

注意：`--out-dir` 传任务目录名即可（如 `{source_task_name}/RKMC_{步数}steps`）。
脚本会自动放到 `OUTPUT/` 下；即使误带 `OUTPUT/` 前缀也会自动去重，不会产生
`OUTPUT/OUTPUT/` 重复结构。

## 8. 输出文件

| 文件 | 位置 | 说明 |
|------|------|------|
| coverage.png | RKMC 任务目录 | 覆盖度 vs 时间 |
| coverage_steps.png | RKMC 任务目录 | 覆盖度 vs 步数 |
| tof.png | RKMC 任务目录 | TOF vs 时间 |
| tof_time.png | RKMC 任务目录 | TOF vs 步数 |
| coverage.csv | OUTPUT/ | 覆盖率数据 |
| tof.csv | OUTPUT/ | TOF 数据 |
| site_tof.csv | OUTPUT/ | 位点 TOF 数据 |
| rec_cov.data | OUTPUT/ | 覆盖度记录（引擎原始输出） |
| rec_event.data | OUTPUT/ | 事件记录 |
| rec_site_spc.data | OUTPUT/ | 位点物种记录 |

### 8.1 发送图片给用户（飞书）

> ⚠️ **一次只发一张图**：飞书 message 工具每次 attach 只能带 1 张图片，
> 多发会静默丢失。RKMC 完成后必须分 4 次发送，每次标注序号。

发送顺序和内容：

1. 图 1/4：Coverage vs Time（覆盖度 vs 时间） — `coverage.png`
2. 图 2/4：Coverage vs Steps（覆盖度 vs 步数） — `coverage_steps.png`
3. 图 3/4：TOF vs Time（TOF vs 时间） — `tof.png`
4. 图 4/4：TOF vs Steps（TOF vs 步数） — `tof_time.png`

每条消息示例：
```
message(action=send, message="图 1/4：Coverage vs Time",
         attachments=[{filePath:"...coverage.png", type:"image"}])
```

## 9. 输出检查与自动重绘

RKMC 完成后（尤其是用户问"任务是否结束"时），必须检查并按需重绘图像：

```bash
RKMC_TASK_DIR="RKMC 任务目录"
RKMC_OUTPUT="$RKMC_TASK_DIR/OUTPUT"

# 1. 检查数据文件
if [ ! -f "$RKMC_OUTPUT/rec_cov.data" ] || \
   [ ! -f "$RKMC_OUTPUT/rec_event.data" ] || \
   [ ! -f "$RKMC_OUTPUT/rec_site_spc.data" ]; then
  echo "❌ 数据文件不存在，RKMC 模拟可能未完成"
  exit 1
fi

# 2. 检查步数一致性
EXPECTED=$(grep -E "^[0-9]+\s+! Num of steps" "$RKMC_TASK_DIR/INPUT/input.txt" | awk '{print $1}')
ACTUAL=$(tail -n 1 "$RKMC_OUTPUT/rec_event.data" | awk '{print $2}')

if [ "$EXPECTED" != "$ACTUAL" ]; then
  echo "❌ 预期步数 $EXPECTED，实际 $ACTUAL，RKMC 未成功完成"
  exit 1
fi

# 3. 检查图像（4 张），缺失则重绘
if [ -f "$RKMC_TASK_DIR/coverage.png" ] && \
   [ -f "$RKMC_TASK_DIR/coverage_steps.png" ] && \
   [ -f "$RKMC_TASK_DIR/tof.png" ] && \
   [ -f "$RKMC_TASK_DIR/tof_time.png" ]; then
  echo "✅ 图像已存在"
else
  cd mosp-for-chatMOSP && python3 utils/plot_kmc_data.py "$RKMC_OUTPUT"
  echo "✅ 图像已重绘"
fi
```

绘图脚本位置：`mosp-for-chatMOSP/utils/plot_kmc_data.py`

## 10. 错误处理

| 错误 | 处理 |
|------|------|
| 步数不匹配 | 提示用户检查 RKMC 日志，可能未跑完 |
| 数据文件缺失 | RKMC 未成功完成，检查 run.log |
| Lattice constant 缺失 | 从 MOSP_database 复制完整模板，不要手动创建 |
| INPUT/OUTPUT 目录缺失 | 创建 RKMC 任务目录时一起创建 |
| ini.xyz 缺失 | 从 MSR 或 EKMC 任务目录复制 |
| 从 EKMC 取结构时 final_stru.xyz 缺失 | 先确认 EKMC 已成功完成 |
| Wine 缺失 | 提示安装指导 |
| RKMC 段错误 | Wine 版本不兼容，提示升级 |

## 11. 跨技能衔接

- **MSR → RKMC**：MSR 完成后产出 ini.xyz。本技能独立从 MOSP_database 取完整 RKMC 参数，不复用 MSR 的 input.json。
- **EKMC → RKMC**：EKMC 完成后产出 final_stru.xyz（演化后结构）。将 final_stru.xyz 复制为 ini.xyz 即可作为 RKMC 的初始结构。支持「先 EKMC 演化形貌，再 RKMC 分析反应活性」的链式工作流。
- **参数修改时**：用户改温度 → parameter-builder 必须重算气体熵。
- **长任务查询**：用户问"任务是否结束" → 执行 §9 检查脚本，必要时重绘图像。

## 12. 依赖

- **mosp-for-chatMOSP** — KMC 引擎（已克隆，含 main.exe）
- **chatmosp-parameter-builder** — 参数构建与气体熵计算
- **chatmosp-file-organizer** — 目录创建
- **chatmosp-input-coordinator** — 任务入口
- **chatmosp-ekmc-simulator** — EKMC（提供演化后的初始结构）
- **Wine** — 运行 Windows 版 main.exe（必需）

## 13. 文件结构

```
chatmosp-kmc-simulator/
├── SKILL.md       # 本文件（中文）
└── SKILL_en.md    # 英文版
```

## 14. 示例

```
用户: 对 Pt 纳米颗粒进行 CO 氧化 RKMC 模拟，850K，150Pa，2000 万步

系统: [识别为 RKMC → parameter-builder 查参数 → 展示 5 选项 →
      用户确认 → 检查 Wine 已装 → ⚠️ 2000 万步约 12 小时，警告 →
      用户再次确认 → 准备 input.json → 调 kmc_standalone.py →
      监控进度 → 检查输出 → 生成 4 张图像 → 逐张发送展示结果]

---

用户: 先跑 EKMC 演化团簇形貌，再跑 RKMC 分析反应活性

系统: [识别为 EKMC → RKMC 链式工作流 → 先调 ekmc-simulator 执行 EKMC →
      EKMC 完成产出 final_stru.xyz → 复制为 ini.xyz →
      调本技能执行 RKMC（反应活性） → 展示 TOF/覆盖度结果]
```
