---
name: chatmosp-file-organizer
description: |
  chatMOSP 系统的文件系统管理器。负责 MSR / RKMC / EKMC 任务的目录结构创建、智能命名（按
  金属_气体分压_温度K_压强Pa_R尺寸 格式）、安全文件操作（路径遍历防护、白名单限制）。
  触发场景：parameter-builder 完成参数构建并经用户确认后，创建任务目录；
  或下游任务需要在父目录下创建子目录时。
---

> **🌐 Language routing / 语言路由**
> Detect the user's language from their latest message.
> - **If the user writes in English** → read `SKILL_en.md` in this same skill
>   directory and follow it as the authoritative instructions; respond in English;
>   you do NOT need to read the rest of this Chinese document.
> - **若用户使用中文** → 继续使用本文件（`SKILL.md`）作为权威指令，并用中文回复。
> Always match the response language to the user's input language.

# chatmosp-file-organizer

## 1. 核心职责

1. **智能任务命名**：按 MSR / RKMC / EKMC 不同格式生成任务名
2. **标准目录创建**：MSR、RKMC 和 EKMC 的标准目录结构
3. **链式层级管理**：MSR → RKMC、MSR → EKMC、EKMC → RKMC 三种路由
4. **安全文件操作**：路径遍历防护 + 白名单限制

## 2. 安全第一原则

- ✅ 路径遍历防护：自动清理 `../`、`//`、`~` 等危险字符
- ✅ 白名单路径：所有操作限制在 `mosp-for-chatMOSP/OUTPUT/`
- ✅ TaskNameValidator：验证任务名合法性，支持新命名格式
- ✅ 权限检查：确保有适当读写权限

禁止模式：`..`、`//`、`~`、`/root`、`/etc`、`*.exe`、`*.sh`

允许字符：`a-zA-Z0-9_-.Å`

最大路径长度：512

## 3. 任务命名规则

### 3.1 MSR 任务

**格式**：`{金属}_{气体分压}_{温度}K_{压强}Pa_R{尺寸}`

**示例**：`Pd_CO9_O18_473K_101325Pa_R50`

| 字段 | 规则 | 默认值 |
|------|------|--------|
| 金属 | Pd、Pt、Au 等元素符号 | 必填 |
| 气体分压 | 多气体用 `_` 连接，分压跟在气体后（CO9 表示 CO 9%） | 必填 |
| 温度 | 数值 + K | 500 |
| 压强 | 数值 + Pa | 101325 |
| 尺寸 | R + 数值（Å） | 20 |

### 3.2 RKMC 任务

**⚠️ 重要**：RKMC 任务目录在父目录（MSR 或 EKMC）下创建子目录。

**格式**：`RKMC_{步数}steps`

**示例**：`RKMC_5000000steps`

> 温度/压强/气体等条件信息继承父目录，简洁不重复。仅当 RKMC 与父级条件不同时，追加参数标注：`RKMC_{T}K_{P}Pa_{pp}_{步数}steps`。

### 3.3 EKMC 任务

**⚠️ 重要**：EKMC 任务目录在 MSR 目录下创建子目录。

**格式**（同条件）：`EKMC_{步数}steps`

**示例**：`EKMC_1000000steps`

**格式**（异条件）：`EKMC_{T}K_{P}Pa_{pp}_{步数}steps`

**示例**：`EKMC_800K_1000Pa_CO100_2000000steps`

> 温度/压强/气体等条件信息继承 MSR 父目录。仅当条件与 MSR 不同时才在子目录名中标注。

## 4. 目录结构

### 4.1 MSR 任务目录

```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/
├── faceinfo.txt            # 晶面信息
├── ini.xyz                 # 真实团簇（RKMC/EKMC 输入）
├── {task_name}_cluster.xyz # 绘图用结构文件
├── rotation.gif            # 旋转动画
├── structure.png           # 结构图
├── input.json              # MSR 参数文件
└── metadata.json           # 任务元数据
```

### 4.2 RKMC 任务目录（MSR → RKMC 直连）

```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/
└── RKMC_{步数}steps/
    ├── input.json          # RKMC 参数（独立）
    ├── ini.xyz             # 从 MSR 复制
    ├── coverage.png        # 覆盖度 vs 时间
    ├── coverage_steps.png  # 覆盖度 vs 步数
    ├── tof.png             # TOF vs 时间
    ├── tof_time.png        # TOF vs 步数
    ├── INPUT/              # 引擎自动填充
    └── OUTPUT/             # 引擎自动输出
        ├── rec_cov.data
        ├── rec_event.data
        └── rec_site_spc.data
```

### 4.3 EKMC 任务目录（MSR → EKMC）

```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/
└── EKMC_{步数}steps/                    ← EKMC 任务目录
    ├── input.json                        ← EKMC 参数（独立）
    ├── ini.xyz                           ← 从 MSR 复制
    ├── coverage.png
    ├── events.png
    ├── migration.png
    ├── structure_cov.png/.gif + structure_cov_legend.png
    ├── structure_cn.png/.gif  + structure_cn_colorbar.png
    ├── structure_gcn.png/.gif + structure_gcn_colorbar.png
    ├── EKMC-INPUT/                       ← 引擎工作目录
    └── EKMC-OUTPUT/                      ← 引擎原始输出
        ├── rec_cov.data
        ├── rec_event.data
        ├── final_stru.xyz                ← 演化后结构（可供 RKMC）
        └── migration_infos.data
```

### 4.4 EKMC → RKMC 链式目录（嵌套）

```
mosp-for-chatMOSP/OUTPUT/{msr_task_name}/
└── EKMC_{步数}steps/
    ├── ... (EKMC 文件，同上)
    └── RKMC_{步数}steps/                 ← RKMC 嵌套在 EKMC 下
        ├── input.json                    ← RKMC 参数（独立）
        ├── ini.xyz                       ← 从 EKMC-OUTPUT/final_stru.xyz 复制
        ├── coverage.png / coverage_steps.png
        ├── tof.png / tof_time.png
        ├── INPUT/
        └── OUTPUT/
```

> ⚠️ **设计原则**：RKMC 嵌套在 EKMC 下 = RKMC 使用 EKMC 的演化结构。平级 = 平行实验（不依赖）。

## 5. 路径逻辑（三种路由）

```
ROUTE 1: MSR → RKMC（反应活性）
  OUTPUT/{msr}/RKMC_{steps}/
  ini.xyz 来源：MSR 的 ini.xyz

ROUTE 2: MSR → EKMC（形貌演化）
  OUTPUT/{msr}/EKMC_{steps}/
  ini.xyz 来源：MSR 的 ini.xyz

ROUTE 3: MSR → EKMC → RKMC（演后反析）
  OUTPUT/{msr}/EKMC_{steps}/RKMC_{steps}/
  ini.xyz 来源：EKMC 的 EKMC-OUTPUT/final_stru.xyz
```

### 5.1 MSR 任务路径

- 位置：`mosp-for-chatMOSP/OUTPUT/{msr_task_name}/`
- MSR 生成 `ini.xyz` 和 `{task_name}_cluster.xyz`
- **不要**为 MSR 准备 `ini.xyz`（MSR 自己生成）

### 5.2 条件继承规则

子目录（RKMC / EKMC）的命名遵循**条件继承**原则：
- 温度/压强/气体分压与父级相同时 → 简名（`RKMC_{steps}steps` / `EKMC_{steps}steps`）
- 条件不同时 → 在子目录名中标注差异参数
- 路径中缺少的上下文通过向上追溯父目录名获取

## 6. 可视化（引用 msr-generator）

MSR 结构图和旋转动画由 `chatmosp-msr-generator` 的 §5 步骤 3 负责生成。
详见 msr-generator §5。

## 7. 接口示例

### 创建 MSR 目录

**输入**：

```json
{
  "action": "create_msr_directory",
  "parameters": {
    "metal": "Pd",
    "temperature": "473",
    "gases": ["CO", "O2"],
    "partial_pressures": {"CO": 9, "O2": 18},
    "pressure": "101325",
    "radius": "50"
  }
}
```

**输出**：

```json
{
  "success": true,
  "task_type": "MSR",
  "task_name": "Pd_CO9_O18_473K_101325Pa_R50",
  "directory_path": "mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_101325Pa_R50",
  "standard_files": [
    "faceinfo.txt", "ini.xyz", "{task_name}_cluster.xyz",
    "rotation.gif", "structure.png", "input.json", "metadata.json"
  ]
}
```

### 创建 RKMC 目录

**输入**：

```json
{
  "action": "create_rkmc_directory",
  "parameters": {
    "steps": "5000000",
    "parent_task": "Pd_CO9_O18_473K_101325Pa_R50",
    "parent_type": "MSR"
  }
}
```

**输出**：

```json
{
  "success": true,
  "task_type": "RKMC",
  "task_name": "RKMC_5000000steps",
  "directory_path": "mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_101325Pa_R50/RKMC_5000000steps",
  "required_files": ["input.json", "ini.xyz"],
  "empty_directories": ["INPUT", "OUTPUT"],
  "output_files": ["coverage.png", "coverage_steps.png", "tof.png", "tof_time.png"]
}
```

### 创建 EKMC 目录

**输入**：

```json
{
  "action": "create_ekmc_directory",
  "parameters": {
    "steps": "1000000",
    "parent_task": "Pd_CO9_O18_473K_101325Pa_R50",
    "temperature_override": null,
    "pressure_override": null
  }
}
```

> `temperature_override` / `pressure_override` 非空时子目录名追加条件标注。

**输出**：

```json
{
  "success": true,
  "task_type": "EKMC",
  "task_name": "EKMC_1000000steps",
  "directory_path": "mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_101325Pa_R50/EKMC_1000000steps",
  "required_files": ["input.json", "ini.xyz"],
  "empty_directories": ["EKMC-INPUT", "EKMC-OUTPUT"],
  "output_files": ["coverage.png", "events.png", "migration.png", "structure_cov.png", "structure_cn.png", "structure_gcn.png"]
}
```

### 创建 EKMC → RKMC 链式目录

**输入**：

```json
{
  "action": "create_rkmc_directory",
  "parameters": {
    "steps": "2000000",
    "parent_task": "Pd_CO9_O18_473K_101325Pa_R50/EKMC_1000000steps",
    "parent_type": "EKMC"
  }
}
```

**输出**：

```json
{
  "success": true,
  "task_type": "RKMC",
  "parent_type": "EKMC",
  "task_name": "RKMC_2000000steps",
  "directory_path": "mosp-for-chatMOSP/OUTPUT/Pd_CO9_O18_473K_101325Pa_R50/EKMC_1000000steps/RKMC_2000000steps",
  "ini_source": "EKMC-OUTPUT/final_stru.xyz"
}
```

## 8. 路由总结

| 路由 | 目录路径 | ini.xyz 来源 |
|------|----------|-------------|
| MSR → RKMC | `{msr}/RKMC_{steps}/` | MSR `ini.xyz` |
| MSR → EKMC | `{msr}/EKMC_{steps}/` | MSR `ini.xyz` |
| MSR → EKMC → RKMC | `{msr}/EKMC_{steps}/RKMC_{steps}/` | EKMC `final_stru.xyz` |

## 9. 错误处理

| 错误 | 处理 |
|------|------|
| 路径遍历攻击（../） | 拒绝操作，返回错误 |
| 任务名非法字符 | TaskNameValidator 拒绝 |
| 目录已存在 | 询问是否覆盖 |
| 权限不足 | 提示用户检查权限 |
| 路径超出白名单 | 拒绝操作 |
| 父目录不存在 | 提示先创建父任务目录 |
| 链式嵌套过深 | 限制最大嵌套 2 层（MSR → EKMC → RKMC） |

## 10. 跨技能衔接

- **parameter-builder → 本技能**：参数确认后调用创建目录
- **本技能 → msr-generator**：MSR 目录创建后调用计算
- **本技能 → kmc-simulator**：RKMC 目录创建后调用模拟
- **本技能 → ekmc-simulator**：EKMC 目录创建后调用模拟
- **ekmc-simulator → 本技能**：EKMC 完成后如用户需要 RKMC，本技能在 EKMC 下创建嵌套 RKMC 子目录

## 11. 依赖

- **chatmosp-parameter-builder** — 获取任务参数
- **chatmosp-input-coordinator** — 获取任务类型和路由
- **chatmosp-msr-generator** — MSR 计算接收方
- **chatmosp-kmc-simulator** — RKMC 模拟接收方
- **chatmosp-ekmc-simulator** — EKMC 模拟接收方

## 12. 文件结构

```
chatmosp-file-organizer/
├── SKILL.md       # 本文件（中文）
└── SKILL_en.md    # 英文版
```
