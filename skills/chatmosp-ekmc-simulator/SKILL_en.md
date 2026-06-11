<!--
本文件 (SKILL_cn.md) 是 chatmosp-ekmc-simulator (EKMC) 的中文输出参考。

加载机制说明:
- OpenClaw 只识别 SKILL.md 作为主加载文档(本技能的主文档是英文版,见 SKILL.md)
- 本文件不会被自动注入到 Agent 系统提示词
- 当 input-coordinator §5 检测到 user_lang = zh 时,Agent 会显式 read 本文件

使用规则:
- 当 user_lang = zh 时,Agent 应参考本文件的术语、章节标题、表达方式
- 当 user_lang = en 时,Agent 直接使用 SKILL.md 的英文内容
- 本文件结构与 SKILL.md 一一对应(§0/§1/.../§14)
-->

---
name: chatmosp-ekmc-simulator
description: |
  [中文输出参考 - 不被 OpenClaw 加载,仅供按需 read]
  chatMOSP 系统的 EKMC(环境动力学蒙特卡洛)模拟引擎,模拟团簇在反应气氛中的【动态形貌】。
  调用 generate_ekmc_input.py 一键式流程(读 JSON → 生成输入 → Wine 运行 EKMC-main.exe
  → 绘图),产出覆盖度/事件/迁移分析图,以及大尺寸不透明原子结构图与旋转动图(连续着色另配
  独立 colorbar)。EKMC 需要初始结构(如 MSR 生成的团簇)。
---

# chatmosp-ekmc-simulator (EKMC, 中文输出参考)

> Skill created by Sanyang Ye (https://github.com/sanyangye)

> **术语**: 本技能即 **EKMC**(Environmental KMC,环境动力学蒙特卡洛)。模拟团簇在反应气氛中的
> **动态形貌**(原子迁移/形貌演化)。相关概念:
> - **MSR** — 模拟团簇在反应气氛中的**平衡形貌**(静态,无需初始结构)。
> - **RKMC** — 模拟团簇在反应气氛中的**反应活性**(见 `chatmosp-kmc-simulator`,需初始结构)。
> - **EKMC** — 模拟团簇在反应气氛中的**动态形貌**(本技能,需初始结构,如 MSR 团簇)。

## 0. ⚠️ 强制规则:输出语言绑定

**所有**输出内容必须与用户最近一条消息的语言保持一致。

**检测规则**:用户最后一条消息含 CJK 字符 → `user_lang = zh`,否则 → `en`。

**输出前读取 `OUTPUT/{task_name}/context.json` 的 `user_lang`**。若为 `zh`,再 read 本文件。

> 完整规则见 `input-coordinator` §0。

## 1. 核心职责

1. 检查并管理 Wine 环境(EKMC 引擎依赖)
2. 检查 Python 依赖(numpy、pandas、matplotlib、scipy、imageio)
3. 通过一键脚本准备 EKMC 输入(从 MOSP_database 复制模板 + 用户指定温度/压强/分压/步数)
4. 运行 EKMC 引擎(Wine 跑 `EKMC-main.exe`)并监控进度
5. 步数预警
6. 生成覆盖度/事件/迁移分析图,以及大尺寸不透明原子结构图/旋转动图(连续着色另配独立 colorbar)
7. 结果不满意时按需重绘图像

## 2. 前置条件

- ✅ 已具备初始结构(EKMC 必需,如 MSR 生成的 `ini.xyz`)
- ✅ `parameter-builder` 已构建 EKMC 参数(JSON 的 `EKMC` 段)
- ✅ 用户已通过 5 选项确认
- ✅ Wine 已安装(首次运行时检查)— 见 §3
- ✅ Python 依赖已安装(numpy、pandas、matplotlib、scipy、imageio)— 见 §3.4
- ✅ `user_lang` 已写入 `context.json`
- ❌ 禁止绕过 `parameter-builder`
- ❌ 禁止复用 MSR/RKMC 的 `input.json`——EKMC 使用自己的 `EKMC` 段

## 3. 环境检查(Wine + Python)

> 执行任何 EKMC 之前必须同时运行 §3.1(Wine)和 §3.4(Python)。本节 prompt 遵循 `user_lang`。

### 3.1 检查 Wine

```bash
which wine64 || which wine
```

### 3.2 安装 Wine(Ubuntu/Debian)

```bash
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install wine64 wine32
```

### 3.3 自动 Wine 检查

- ✅ 已安装 → 正常执行
- ⚠️ 未安装 → 提示安装(用 `user_lang`)
- ❌ 不兼容 → 提示升级

### 3.4 Python 依赖检查(强制,给绘图用)

> **为什么**:EKMC 跑完后,`utils/postprocess_ekmc.py` 读取 EKMC 输出生成覆盖度/事件/迁移图以及结构图与旋转动图。结构动图需要 `imageio`;结构 CN/GCN 计算与 KDTree 近邻逻辑依赖 `scipy`。缺包会导致模拟跑完但绘图崩溃。

```bash
python3 -c "import numpy, pandas, matplotlib, scipy, imageio; print('OK')" 2>/dev/null
RC=$?

if [ $RC -ne 0 ]; then
  echo "❌ postprocess_ekmc.py 缺少 Python 依赖"
  echo "诊断:当前用的是哪个 python3?"
  which python3
  echo "修复(PEP 668 系统,例如 Ubuntu 23.04+、Debian 12+):"
  echo "  cd mosp-for-chatMOSP"
  echo "  python3 -m venv .venv && source .venv/bin/activate"
  echo "  pip install -r requirements.txt"
  echo "修复(旧系统):"
  echo "  cd mosp-for-chatMOSP && pip install -r requirements.txt"
  exit 1
fi
```

**检查失败必须停止,不要继续 §7**。用 `user_lang` 输出诊断。

必装包:`numpy`、`pandas`、`matplotlib`、`scipy`、`imageio`(全在 `mosp-for-chatMOSP/requirements.txt`)。

## 4. 步数警告

EKMC 步数(`nLoop`)较大时,执行前提醒用户(耗时随步数和网格尺寸增长)。用 `user_lang`。

```
⚠️ 计算时间提醒:
当前 EKMC 步数(nLoop)为 {N} 步,网格 {dim_x}×{dim_y}×{dim_z}。
步数/网格越大耗时越长。是否继续?
```

## 5. 输入契约(EKMC JSON 必含字段)

> 参考模板:`mosp-for-chatMOSP/MOSP_database/*-EKMC*.json`(如 `Pt-CO-EKMC-test.json`)。

### 顶层字段

| 字段 | 类型 | 说明 |
|------|------|------|
| Element | string | 金属元素 |
| Lattice constant | string | 晶格常数(Å) |
| Crystal structure | string | FCC / BCC / HCP |
| Temperature | string | 温度(K) |
| Pressure | string | 压力(Pa) |
| EKMC | object | EKMC 参数对象 |

### EKMC 对象内必含字段

| 字段 | 类型 | 说明 |
|------|------|------|
| dim_x / dim_y / dim_z | string | 晶格网格维度(团簇尺寸表征) |
| nLoop | string | 模拟步数 |
| record_int | string | 记录间隔 |
| E_bond | string | 键能 |
| Ecoh_U0 | string | 内聚能基准项 |
| Ecoh_A1 / Ecoh_t1 | string | 内聚能指数项 1 |
| Ecoh_A2 / Ecoh_t2 | string | 内聚能指数项 2 |
| nspecies | number | 物种数量 |
| nevents | number | 事件数量 |
| nevents_mob | number | 移动事件数量 |
| s1 ... sN | string | 物种定义(JSON 字符串;含 name/mass/PP_ratio/S_gas/S_ads/sticking/E_ads_para/Ea_diff/is_twosite) |
| e1 ... eM | string | 事件定义(JSON 字符串;type ∈ Adsorption/Desorption/Diffusion,cov_before/cov_after,is_twosite) |
| li | array | 晶格相互作用矩阵 |

> **与 RKMC 的区别**:RKMC 用 `KMC` 段(含产物的反应事件 → 反应活性);EKMC 用 `EKMC` 段(吸附/脱附/扩散 → 形貌演化)。EKMC 无 `products`,但有内聚能项与逐物种扩散势垒。

## 6. 目录结构

EKMC 任务目录命名参照 `file-organizer`,含金属/气体分压/温度/压强/团簇尺寸/步数,并加 `-EKMC` 后缀:

**格式**:`{metal}_{gas-pp}_{T}K_{P}Pa_R{size}_{steps}steps-EKMC`

**示例**:`Pt_CO100_800K_1000Pa_R50_10000steps-EKMC`

EKMC 任务目录应在 MSR 目录下(若从 MSR 团簇起步):

```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/
└── {metal}_{gas-pp}_{T}K_{P}Pa_R{size}_{steps}steps-EKMC/   ← EKMC 任务目录
    ├── input.json                ← EKMC 参数(EKMC 段)
    ├── ini.xyz                   ← 初始结构(必需,如来自 MSR)
    ├── run.log                   ← 引擎日志
    ├── coverage.png              ← 覆盖度随时间
    ├── events.png                ← 事件统计
    ├── migration.png             ← 迁移分析(Ea/dE/CN/GCN)
    ├── structure_cov.png/.gif   + structure_cov_legend.png
    ├── structure_cn.png/.gif    + structure_cn_colorbar.png
    ├── structure_gcn.png/.gif   + structure_gcn_colorbar.png
    ├── EKMC-INPUT/               ← 引擎工作目录(input.txt、LI.txt、species.txt、events.txt、ini.xyz)
    └── EKMC-OUTPUT/              ← 引擎原始输出(rec_cov.data、rec_event.data、final_stru.xyz、migration_infos.data)
```

> ⚠️ **重要**:
> - `EKMC-main.exe` 以相对路径读 `EKMC-INPUT`、写 `EKMC-OUTPUT`。一键脚本把引擎 cwd 设为 `--out-dir` 并在其下创建这些子目录。
> - 结构图/动图**不**内嵌 colorbar;连续着色(cov/cn/gcn)单独生成 `*_colorbar.png`,便于一张 colorbar 配多张结构图统一展示。
> - 所有 EKMC 图像标题都包含金属/温度/压强/分压/团簇网格尺寸/EKMC 步数。
> - `ini.xyz` 和 `input.json` 同时放置在任务根目录（参照 KMC 惯例，便于用户查看）。

## 7. 执行步骤(一键脚本)

### 7.1 步骤 1:创建 EKMC 任务目录

```bash
mkdir -p OUTPUT/Pt_CO9_O18_473K_101325Pa_R50/Pt_CO100_800K_1000Pa_R50_10000steps-EKMC
```

### 7.2 步骤 2:提供初始结构(必需)

```bash
cp OUTPUT/{msr_task_name}/ini.xyz \
   OUTPUT/{msr_task_name}/Pt_CO100_800K_1000Pa_R50_10000steps-EKMC/ini.xyz
```

### 7.3 步骤 3:准备 input.json

```bash
# 从 MOSP_database 复制 EKMC 模板(不要手动创建)
cp mosp-for-chatMOSP/MOSP_database/{metal}-{reaction}-EKMC*.json \
   OUTPUT/{msr_task_name}/{ekmc_task_name}/input.json
# 调整:Temperature、Pressure、EKMC.nLoop、EKMC.record_int、
#       逐物种 PP_ratio / S_gas、网格维度 dim_x/dim_y/dim_z
```

### 7.4 步骤 4:展示参数给用户确认

使用 `parameter-builder` EKMC 参数展示格式(5 选项)。

### 7.5 步骤 5:检查 Wine + 步数警告(§3.1、§4)

### 7.6 步骤 6:运行一键 EKMC 流程

`generate_ekmc_input.py` 完成:读 JSON → 生成输入 → Wine 跑 `EKMC-main.exe` → 绘图。`--out-dir` 是运行目录,脚本在其下创建 `EKMC-INPUT`、`EKMC-OUTPUT` 并把引擎 cwd 设为该目录。图像输出到任务根目录。

```bash
python3 mosp-for-chatMOSP/generate_ekmc_input.py \
  --json   OUTPUT/{msr_task_name}/{ekmc_task_name}/input.json \
  --out-dir OUTPUT/{msr_task_name}/{ekmc_task_name} \
  --xyz    OUTPUT/{msr_task_name}/{ekmc_task_name}/ini.xyz
```

> 图像标题由 JSON 自动拼出(金属/温度/压强/分压/网格尺寸/步数-EKMC)。

## 8. 输出文件

| 文件 | 位置 | 说明 |
|------|------|------|
| coverage.png | 任务目录 | 表面覆盖度随时间 |
| events.png | 任务目录 | 事件计数与最终统计 |
| migration.png | 任务目录 | 迁移势垒/能量/CN/GCN 分析 |
| structure_cov.png / .gif (+ _legend.png) | 任务目录 | 按覆盖度着色（灰=未覆盖，红=覆盖）+ 独立图例 |
| structure_cn.png / .gif (+ _colorbar.png) | 任务目录 | 按 CN 着色 + 独立 colorbar |
| structure_gcn.png / .gif (+ _colorbar.png) | 任务目录 | 按 GCN 着色 + 独立 colorbar |
| rec_cov.data / rec_event.data | EKMC-OUTPUT/ | 引擎原始记录 |
| final_stru.xyz | EKMC-OUTPUT/ | 演化后的最终结构(ele/x/y/z/cov/cn/gcn) |
| migration_infos.data | EKMC-OUTPUT/ | 逐次迁移记录 |
| run.log | 任务目录 | 引擎日志 |

> EKMC 的输出描述**形貌演化**(最终结构、迁移)。反应活性(TOF)请用 RKMC(`chatmosp-kmc-simulator`)。

## 9. 输出检查与重绘

EKMC 完成后(尤其用户问"任务是否结束"时),检查数据文件,缺失或不满意则重绘:

```bash
EKMC_OUTPUT="{ekmc_task_dir}/EKMC-OUTPUT"

if [ ! -f "$EKMC_OUTPUT/rec_cov.data" ] || \
   [ ! -f "$EKMC_OUTPUT/rec_event.data" ] || \
   [ ! -f "$EKMC_OUTPUT/final_stru.xyz" ]; then
  echo "❌ EKMC 输出文件缺失,模拟可能未完成"
  exit 1
fi

# 仅重绘(不重跑)。传入相同标题信息以保持图像标题一致。
python3 mosp-for-chatMOSP/utils/postprocess_ekmc.py "$EKMC_OUTPUT" \
  --title "Pt CO100% 800K 1000Pa grid50x50x50 10000steps-EKMC"
```

> 重绘模块 `utils/postprocess_ekmc.py` 仅负责绘图;可通过 `--img-dir` 指定图像输出位置。完整流程是 `generate_ekmc_input.py`。

## 10. 错误处理

> 本节 prompt 遵循 `context.json` 的 `user_lang`。

| 错误 | 处理 |
|------|------|
| Wine 缺失 | 提示安装(见 §3) |
| 运行时找不到 `wine` | 引擎无法运行;安装 Wine |
| Python `ImportError`(numpy/pandas/matplotlib/scipy/imageio) | 见 §3.4,修复前不要继续 |
| JSON 缺少 `EKMC` 段 | 从 MOSP_database 复制完整 EKMC 模板 |
| ini.xyz 缺失 | EKMC 必需初始结构;从 MSR 复制 |
| `EKMC-main.exe` 非零退出 | 检查 `run.log`;核对输入文件与 Wine 版本 |
| 运行后输出文件缺失 | 引擎未完成;查看 `run.log` |
| 结构动图被跳过 | 未安装 `imageio`(见 §3.4) |
| final_stru.xyz 中出现垃圾原子 | EKMC 引擎 Fortran 未初始化内存 bug；基本不影响结果 | postprocess_ekmc 自动过滤；使用网格维度 ≥ 3× 团簇半径可避免 |

## 11. 跨技能衔接

- **MSR → EKMC**:MSR 产出 `ini.xyz`(初始结构),EKMC 用其做形貌演化。
- **EKMC → RKMC**:EKMC 在 `EKMC-OUTPUT/` 中产出 `final_stru.xyz`(演化后结构)。将其复制为 `ini.xyz` 即可作为 RKMC 的初始结构。支持「先 EKMC 演化形貌,再 RKMC 分析反应活性」的链式工作流。
- **EKMC vs RKMC**:两者都需要 MSR 初始结构。EKMC → 形貌(结构图/动图/迁移);RKMC → 反应活性(TOF/覆盖度)。由 `input-coordinator` 按用户意图路由。
- **参数构建**:`parameter-builder` 构建 `EKMC` 段;温度改变时与 MSR/RKMC 一致地重算气体熵。
- **目录命名**:`file-organizer` 创建 `...-EKMC` 任务目录。
- **`user_lang` 来自 `context.json`**:所有面向用户的消息都遵循(见 §0)。

## 12. 依赖

- **mosp-for-chatMOSP** — EKMC 引擎(`engine/EKMC-main.exe`)+ `generate_ekmc_input.py` + `utils/postprocess_ekmc.py`
- **chatmosp-parameter-builder** — EKMC 参数构建
- **chatmosp-file-organizer** — `...-EKMC` 目录创建
- **chatmosp-input-coordinator** — 任务入口与 `user_lang`
- **chatmosp-kmc-simulator** — 同级技能,负责反应活性(RKMC)
- **Wine** — 运行 `EKMC-main.exe`
- **Python 包** — `numpy`、`pandas`、`matplotlib`、`scipy`、`imageio`

## 13. 文件结构

```
chatmosp-ekmc-simulator/
├── SKILL.md       # 主文档(英文,被 OpenClaw 加载)
└── SKILL_cn.md    # 中文输出参考(按需 read,见 §0)
```

## 14. 示例

> 输出语言遵循 `user_lang`。英文示例见 SKILL.md §14。

```
用户: 对 Pt 团簇在 CO 气氛 800K、1000Pa 下做 EKMC,1 万步

系统: [识别为 EKMC(形貌演化)→ parameter-builder 构建 EKMC 段 →
      展示 5 选项 → 用户确认 →
      环境检查:Wine OK(§3.1)+ Python OK(§3.4)→
      创建 ...-EKMC 任务目录 → 复制 MSR 的 ini.xyz(初始结构)→ 准备 input.json →
      运行 generate_ekmc_input.py(--json/--out-dir/--xyz)→
      Wine 跑引擎 → 生成图像(coverage/events/migration +
      structure_cov/cn/gcn 的 .png/.gif 及独立 colorbar,
      标题含金属/温度/压强/分压/网格/步数-EKMC)→ 展示结果(用 user_lang)]

---

用户: 先跑 EKMC 演化团簇形貌,再跑 RKMC 分析反应活性

系统: [识别为 EKMC → RKMC 链式工作流 →
      先调 ekmc-simulator 执行 EKMC 形貌演化 →
      EKMC 在 EKMC-OUTPUT/ 中产出 final_stru.xyz →
      将 final_stru.xyz 复制为 ini.xyz 给 RKMC 用 →
      切换到 kmc-simulator 分析反应活性 → 展示 TOF/覆盖度结果]
```
