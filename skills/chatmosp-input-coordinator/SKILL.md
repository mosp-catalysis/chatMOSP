---
name: chatmosp-input-coordinator
description: |
  chatMOSP 系统的入口技能。负责解析中英文自然语言输入，识别 MSR / RKMC / EKMC /
  参数查询 四种任务类型，提取金属/温度/气体/分压/步数/尺寸等参数，并调度
  parameter-builder、file-organizer、msr-generator、kmc-simulator、ekmc-simulator
  完成计算。
  触发场景：用户请求运行 MSR、RKMC、EKMC 计算、查询参数、调整参数、或描述金属催化
  反应体系（Pd、Pt、Au、CO 氧化、水汽变换等）。
---

> **🌐 Language routing / 语言路由**
> Detect the user's language from their latest message.
> - **If the user writes in English** → read `SKILL_en.md` in this same skill
>   directory and follow it as the authoritative instructions; respond in English;
>   you do NOT need to read the rest of this Chinese document.
> - **若用户使用中文** → 继续使用本文件（`SKILL.md`）作为权威指令，并用中文回复。
> Always match the response language to the user's input language.

# chatmosp-input-coordinator

## 1. 核心职责

1. 多语言意图理解：解析中英文自然语言输入
2. 任务识别：识别 MSR / RKMC / EKMC / 参数查询 四种任务类型
3. 参数提取：从输入中提取金属、温度、气体、分压、步数、尺寸等
4. 技能调度：按路由表串起 parameter-builder → file-organizer → 计算引擎
5. 对话管理：确认、澄清、错误处理

## 2. 任务类型识别

支持四种任务：

| 类型 | 含义 | 典型关键词 |
|------|------|------------|
| MSR | 金属团簇结构生成 | 团簇、结构、形貌、纳米颗粒、cluster、structure、morphology、MSR |
| RKMC | 反应动力学蒙特卡洛模拟 | 反应动力学、反应KMC、TOF、步数、kinetic、simulation、RKMC、Reaction KMC |
| EKMC | 环境动力学蒙特卡洛模拟（形貌演化） | 环境KMC、形貌演化、EKMC、environmental、morphology evolution |
| 参数查询 | 查看/调整参数 | 查询、参数、设置、调整、parameter documentation、show parameters |

> **术语说明**：KMC 现在细分为 RKMC（反应 KMC，关注反应活性/TOF）和 EKMC（环境 KMC，关注形貌演化/原子迁移）。用户只说"KMC"时，根据上下文判断意图；若模糊则询问用户是反应活性还是形貌演化。

置信度阈值 0.70。低于阈值时主动询问用户意图。

## 3. 参数提取

### 3.1 必提取参数

| 参数 | 识别规则 |
|------|----------|
| 金属元素 | Pd / Pt / Au / Cu / Ni 等中英文 |
| 温度 | 支持 °C 和 K，自动转 K |
| 压力 | Pa / kPa / MPa / atm |
| 气体种类 | CO / O₂ / H₂ / N₂ / CO₂ / NO 等 |

### 3.2 进阶参数

- 气体分压：CO9（CO 分压 9%）、O18（O₂ 分压 18%）；多气体用 `_` 连接：CO9_O18
- 团簇尺寸：R50（50 Å）、R20（默认 20 Å）
- 模拟步数：200000000steps、1e6 steps、一百万步

### 3.3 提取示例

| 用户输入 | 提取结果 |
|----------|----------|
| Pd 在 CO 氧化环境下 200 摄氏度结构 | metal=Pd, T=473K, gases=[CO, O₂] |
| Pt structure under CO oxidation at 400 Celsius | metal=Pt, T=673K, gases=[CO] |
| 运行 Pd 在 CO9_O18 分压下 473K 的 MSR，团簇尺寸 R50 | metal=Pd, T=473K, pp={CO:9,O₂:18}, R=50 |

## 4. 技能调度

### 4.1 路由表

```
MSR 任务   → parameter-builder → file-organizer → msr-generator
RKMC 任务  → parameter-builder → file-organizer → kmc-simulator
EKMC 任务  → parameter-builder → file-organizer → ekmc-simulator
参数查询   → parameter-builder
```

### 4.2 跨技能衔接（必须遵守）

- **MSR → RKMC**：MSR 完成后产出 ini.xyz。RKMC 由 kmc-simulator 独立从 MOSP_database 取完整 RKMC 参数（nspecies、s1/s2、p1、e1-e7、li 全套），不复用 MSR 的 input.json。详见 kmc-simulator。
- **MSR → EKMC**：MSR 完成后产出 ini.xyz。EKMC 由 ekmc-simulator 独立从 MOSP_database 取 EKMC 参数（EKMC section），不复用 MSR 的 input.json。详见 ekmc-simulator。
- **MSR → EKMC → RKMC**：EKMC 运行结束后产出 final_stru.xyz（演化后结构），可作为 RKMC 的初始结构。用户可要求先 EKMC 演化形貌，再 RKMC 分析反应活性。
- **参数修改时**：用户改温度 → parameter-builder 必须按 §8.5 重算气体熵。
- **参数缺失时**：关键参数（E_ads、w、gamma）缺 → parameter-builder 调用 literature-search 补全（开放获取期刊优先）。详见 literature-search。
- **可视化**：MSR 完成后由 msr-generator 调 utils/paint.py 生成 PNG + GIF。详见 msr-generator。
- **Wine 环境**：RKMC / EKMC 任务分别由 kmc-simulator 和 ekmc-simulator 负责检查和管理。详见各自技能。

### 4.3 错误处理

| 情况 | 处理 |
|------|------|
| 参数缺失 | 提示用户补充，给出合理默认 |
| 任务歧义 | 提供 2-3 个候选场景让用户选 |
| 技能失败 | 提示重试或降级 |
| 置信度低 | 主动澄清意图 |
| 目录已存在 | 询问是否覆盖 |

## 5. 交互机制

### 5.1 任务确认

识别任务后，必须向用户确认。展示模板见 parameter-builder 的「MSR / RKMC / EKMC 参数展示格式」章节。

### 5.2 澄清触发

- 模糊温度："高温" → 询问具体度数
- 气体配比不明：CO 氧化需 CO+O₂ → 询问分压比例
- 单位不明："压强" → 询问 Pa / kPa / atm
- 金属/气体未指定：列出当前任务可选项

## 6. 依赖

- **chatmosp-parameter-builder** — 参数补全 + 气体熵计算
- **chatmosp-file-organizer** — 目录结构创建
- **chatmosp-msr-generator** — MSR 计算
- **chatmosp-kmc-simulator** — RKMC（反应动力学）模拟
- **chatmosp-ekmc-simulator** — EKMC（环境形貌）模拟
- **chatmosp-literature-search** — 文献检索（参数缺失时）

## 7. 文件结构

```
chatmosp-input-coordinator/
├── SKILL.md       # 本文件（中文）
└── SKILL_en.md    # 英文版
```
