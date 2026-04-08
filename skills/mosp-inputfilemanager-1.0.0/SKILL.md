---
name: mosp-inputfilemanager
description: MOSP输入文件管理器技能，负责example数据管理、参数查询、参数处理和交互式参数修改。
homepage: https://github.com/openclaw/openclaw
metadata: {"clawdbot":{"emoji":"📁🧪","requires":{"bins":["python3"]},"install":[{"id":"python","kind":"bin","bins":["python3"],"label":"需要Python 3.8+"}]}}
---

# MOSP InputFileManager Skill 📁🧪

## 概述

MOSP输入文件管理器技能，负责处理所有与输入参数相关的任务，包括：
1. **参数查询**：详细查询和展示MSR/KMC参数
2. **参数处理**：example数据管理与参数匹配
3. **参数修改**：交互式参数修改支持

## 核心功能

### 1. 参数查询功能
- **查询数据源**：
  - example参数：$MOSP_HOME/example/目录中的标准JSON文件
  - 历史任务参数：$MOSP_HOME/OUTPUT/目录中已完成任务的input.json
  - 推荐参数：基于相似体系的推荐值

- **查询内容详细展示**：
  - **MSR参数完整展示**（有效参数原则）
  - **KMC参数完整展示**（有效参数原则）
  - 数值单位明确标注
  - 参数来源明确标注（✅example/⚠️历史任务/🔧推荐值）

- **参数展示模式**：
  - **默认模式（完整展示）**：展示所有定义参数（有效参数）
  - **简要模式（`--brief`）**：只展示关键参数
  - **详细模式（`--expert`）**：完整参数 + 技术细节 + 参数分析

### 2. Example数据管理
- **重要原则**：example目录完全只读，不可修改
- **文件保护规则**：
  - ✅ 允许：读取、复制example文件
  - ❌ 禁止：修改、删除、在example内创建新文件
  - 🔧 自动：所有修改自动重定向到OUTPUT目录

- **支持的文件**：
  - `Au-COoxidation.json` - Au金一氧化碳氧化
  - `Pt-COoxidation.json` - Pt铂一氧化碳氧化  
  - `Cu-WGSr.json` - Cu铜水汽变换反应

### 3. 双模式参数处理

#### 情况A：需求体系与example完全匹配
- **匹配条件**：金属元素相同 **且** 气体组合相同
- **处理方式**：复制对应的example JSON文件到OUTPUT目录
- **用户告知**："✅ 检测到与现有example完全匹配：{金属}-{气体}系统，已复制到OUTPUT目录"

#### 情况B：需求体系与example不完全匹配
- **匹配条件**：金属元素不同 **或** 气体组合不同
- **处理方式**：提供推荐值和警告信息
- **用户告知**："⚠️ 未找到完全匹配的example，提供推荐参数（数据存疑）"

### 4. 交互式参数修改支持

#### 可修改参数范围：
1. **反应条件参数**：
   - 温度（Temperature）
   - 压力（Pressure）
   - 气体分压百分比（GasX_pp）

2. **几何参数**：
   - 团簇半径（Radius）
   - 晶面数量（nFaces）
   - 晶面选择

3. **标识参数**：
   - flag_MSR / flag_KMC

#### 交互流程：
1. 展示完整参数列表
2. 高亮可修改参数，说明不可修改原因
3. 文件位置说明："所有修改将在OUTPUT目录中进行，原始example文件保持不变"
4. 询问用户需要修改的参数

## 使用流程

### 1. 参数查询流程
```
用户查询 → 确定查询目标 → 读取参数文件 → 格式化展示 → 返回给用户
```

### 2. 参数处理流程
```
用户需求 → 匹配example → 完全匹配：复制文件 → 不完全匹配：生成推荐 → 交互修改 → 生成最终参数文件
```

### 3. 参数修改流程
```
展示参数 → 询问修改 → 收集修改 → 验证修改 → 生成新参数文件 → 保存到OUTPUT目录
```

## 技术实现

### 依赖
- Python 3.8+
- JSON文件处理
- 路径操作（os, pathlib）

### 核心处理逻辑

1. **参数文件解析**：
```python
def parse_msr_parameters(json_path: Path) -> Dict:
    """解析MSR参数文件，提取有效参数"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 提取有效参数（非空值）
    effective_params = {}
    for key, value in data.items():
        if value not in (None, "", [], {}):
            effective_params[key] = value
    
    return effective_params
```

2. **参数匹配算法**：
```python
def match_example(metal: str, gases: List[str]) -> Optional[Path]:
    """匹配最相似的example文件"""
    examples_dir = Path(os.environ.get("MOSP_HOME", ".")) / "example"
    
    best_match = None
    best_score = 0
    
    for example_file in examples_dir.glob("*.json"):
        example_params = parse_parameters(example_file)
        
        # 计算匹配分数
        score = calculate_match_score(metal, gases, example_params)
        
        if score > best_score:
            best_score = score
            best_match = example_file
    
    return best_match if best_score >= 0.8 else None
```

3. **参数展示格式化**：
```python
def format_parameters_for_display(params: Dict, mode: str = "full") -> str:
    """格式化参数用于展示"""
    if mode == "brief":
        return format_brief(params)
    elif mode == "expert":
        return format_expert(params)
    else:  # full
        return format_full(params)
```

## 使用示例

### 示例1：查询Pt-CO氧化参数
```
用户："查询Pt-CO氧化的MSR参数"

处理：
1. 读取$MOSP_HOME/example/Pt-COoxidation.json
2. 解析并格式化参数
3. 输出完整参数列表
4. 提示："如需简要查看核心参数，请使用 --brief 参数"
```

### 示例2：处理Au-CO氧化参数
```
用户："需要Au-CO氧化参数"

处理：
1. 匹配example：找到Au-COoxidation.json
2. 完全匹配：复制到OUTPUT目录
3. 告知："✅ 检测到与现有example完全匹配：Au-CO系统，已复制到OUTPUT目录"
```

### 示例3：处理新体系参数
```
用户："需要Fe-H2反应参数"

处理：
1. 匹配example：未找到完全匹配
2. 提供推荐参数：
   - 同金属不同气体：使用Fe体系的晶格常数
   - H2气体参数：提供典型范围
3. 告知："⚠️ 未找到完全匹配的example，提供推荐参数（数据存疑）"
```

### 示例4：参数修改交互
```
展示参数后：
系统："是否修改以下参数？[温度/压力/分压/半径/晶面]"

用户："修改温度为800K，压力为5000Pa"

处理：
1. 验证修改值有效性
2. 更新参数
3. 生成新参数文件
4. 保存到OUTPUT目录
```

## 配置选项

### 匹配阈值配置
```python
MATCH_THRESHOLDS = {
    "exact_match": 0.95,      # 完全匹配阈值
    "partial_match": 0.7,     # 部分匹配阈值
    "weak_match": 0.4,        # 弱匹配阈值
}
```

### 推荐参数配置
```python
RECOMMENDED_PARAMETERS = {
    # 金属晶格常数（Å）
    "lattice_constants": {
        "Pt": 3.92,
        "Au": 4.08,
        "Cu": 3.61,
        "Fe": 2.87,
        "Pd": 3.89,
        "Rh": 3.80,
        "Ru": 2.71,
    },
    
    # 气体典型参数范围
    "gas_parameters": {
        "CO": {"E_ads_range": [-0.5, -1.2], "S_ads_range": [-0.001, -0.002]},
        "O2": {"E_ads_range": [-0.3, -0.8], "S_ads_range": [-0.0015, -0.0025]},
        "H2O": {"E_ads_range": [-0.4, -0.9], "S_ads_range": [-0.002, -0.003]},
        "H2": {"E_ads_range": [-0.2, -0.5], "S_ads_range": [-0.001, -0.0015]},
    },
}
```

### 参数修改限制
```python
MODIFICATION_LIMITS = {
    "Temperature": {"min": 300, "max": 1000, "unit": "K"},
    "Pressure": {"min": 100, "max": 10000, "unit": "Pa"},
    "Radius": {"min": 10, "max": 100, "unit": "Å"},
    "GasX_pp": {"min": 0, "max": 100, "unit": "%"},
}
```

## 集成方式

### 与InputHandler集成
```python
# InputHandler调用InputFileManager
params = input_file_manager.process_parameters(
    metal="Pt",
    gases=["CO", "O2"],
    task_type="MSR"
)

# 返回参数文件路径和元数据
result = {
    "json_path": params["output_path"],
    "source": params["source"],
    "parameters": params["display_format"],
}
```

### 独立使用
```python
# 直接查询参数
query_result = input_file_manager.query_parameters(
    system="Pt-CO氧化",
    query_type="MSR",
    mode="full"
)

# 处理参数文件
process_result = input_file_manager.process_input_file(
    input_json="user_input.json",
    output_dir=os.path.join(os.environ.get("MOSP_HOME", "."), "OUTPUT", "task_001")
)
```

## 错误处理

### 文件访问错误
```
错误：无法读取example文件
处理：记录错误日志，提示用户检查文件权限
```

### 参数匹配失败
```
错误：未找到匹配的example
处理：提供推荐参数，明确标注数据不确定性
```

### 参数验证失败
```
错误：参数值超出合理范围
处理：提示有效范围，询问用户重新输入
```

## 性能优化

### 缓存机制
- 缓存example文件解析结果
- 缓存常用参数查询结果
- 减少文件IO操作

### 并行处理
- 支持多个参数文件并行解析
- 批量参数查询优化
- 异步文件操作

## 测试用例

### 单元测试
```python
def test_exact_match():
    """测试完全匹配功能"""
    result = match_example("Pt", ["CO", "O2"])
    assert result["matched"] == True
    assert result["file"] == "Pt-COoxidation.json"
    assert result["score"] >= 0.95

def test_parameter_parsing():
    """测试参数解析功能"""
    params = parse_msr_parameters("example/Pt-COoxidation.json")
    assert "Element" in params
    assert params["Element"] == "Pt"
    assert "Temperature" in params
    assert isinstance(params["Temperature"], (int, float))
```

### 集成测试
```python
def test_full_parameter_processing():
    """测试完整参数处理流程"""
    # 用户需求
    user_request = {
        "metal": "Au",
        "gases": ["CO", "O2"],
        "temperature": 700,
        "pressure": 6000,
    }
    
    # 处理参数
    result = input_file_manager.process_parameters(user_request)
    
    # 验证结果
    assert result["success"] == True
    assert os.path.exists(result["json_path"])
    assert result["source"] in ["example", "recommended"]
    
    # 验证参数内容
    with open(result["json_path"], 'r') as f:
        params = json.load(f)
        assert params["Element"] == "Au"
        assert params["Temperature"] == 700
        assert params["Pressure"] == 6000
```

## 更新日志

### v1.0.0 (2026-04-07)
- 初始版本发布
- 参数查询功能（完整/简要/详细模式）
- Example数据管理（只读保护）
- 双模式参数处理（完全匹配/不完全匹配）
- 交互式参数修改支持

## 后续开发计划

### 短期计划
- [ ] 添加更多example文件支持
- [ ] 改进参数匹配算法
- [ ] 添加参数验证规则

### 中期计划
- [ ] 支持自定义参数模板
- [ ] 添加参数版本控制
- [ ] 实现参数对比功能

### 长期计划
- [ ] 机器学习参数推荐
- [ ] 自动化参数优化
- [ ] 参数知识图谱构建

---

**使用提示**：InputFileManager是MOSP系统的参数处理核心，确保参数的正确性和一致性。所有对example文件的修改都会自动重定向到OUTPUT目录，保证原始数据的完整性。