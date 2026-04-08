---
name: mosp-inputhandler
description: MOSP系统总控技能，处理用户输入文本或语音转写后的内容，检测关键词并协调各个skill的调用。
homepage: https://github.com/openclaw/openclaw
metadata: {"clawdbot":{"emoji":"🎛️🧪","requires":{"bins":["python3"]},"install":[{"id":"python","kind":"bin","bins":["python3"],"label":"需要Python 3.8+"}]}}
---

# MOSP InputHandler Skill 🎛️🧪

## 概述

MOSP系统总控技能，负责处理用户输入（文本或语音转写结果），检测关键词，识别任务类型，并协调调用其他MOSP技能。

## 核心功能

### 1. 关键词检测与任务识别
- **系统相关**：`团簇`、`结构`、`构型`、`形貌`、`纳米粒子`、`金属`、`晶面`
- **反应相关**：`一氧化碳氧化`、`水汽变换`、`一氧化碳`、`CO氧化`、`WGSR`
- **金属相关**：`铂`、`金`、`铜`、`Pt`、`Au`、`Cu`、`铁`、`Fe`、`钯`、`Pd`
- **条件相关**：`环境`、`气氛`、`反应条件`、`温度`、`压强`、`压力`、`分压`
- **计算相关**：`MSR`、`KMC`、`MOSP`、`动力学`、`蒙特卡洛`、`表面反应`
- **结果相关**：`反应活性`、`TOF`、`覆盖度`、`活性`、`反应速率`、`转化频率`

### 2. 任务类型识别
- **MSR任务**：生成团簇结构
- **KMC任务**：模拟反应动力学
- **联合任务**：MSR→KMC工作流
- **查询参数任务**：查询系统参数
- **查询图像任务**：查看结果图像

### 3. 任务协调流程
1. 检测关键词并识别任务类型
2. 询问用户确认任务细节
3. 调用InputFileManager Skill进行参数处理
4. 协调MSR/KMC技能执行计算
5. 返回结果给用户

## 使用流程

```
用户输入（文本/语音） → InputHandler检测关键词 → 识别任务类型 → 用户确认 → 调用对应技能
```

## 安装要求

### 必需条件
在使用本技能之前，**必须**先安装MOSP软件：

#### 1. 安装MOSP for chatMOSP软件
```bash
# 下载MOSP计算引擎
git clone https://github.com/mosp-catalysis/mosp-for-chatMOSP.git
cd mosp-for-chatMOSP

# 安装依赖和配置
bash install.sh

# 设置环境变量（推荐）
export MOSP_HOME=$(pwd)
export PATH=$PATH:$MOSP_HOME
```

#### 2. 验证安装
```bash
# 检查MOSP软件是否安装成功
python -c "import sys; sys.path.insert(0, '$MOSP_HOME'); import kmc_standalone; print('MOSP软件安装成功')"
```

### 技术实现依赖
- Python 3.8+
- OpenClaw会话API
- MOSP for chatMOSP软件（必需）

### 核心处理逻辑

1. **关键词检测**：
```python
def detect_task_type(text: str) -> str:
    # 检测关键词组合
    msp_patterns = ["看.*结构", "生成.*团簇", "构造.*团簇", "MSR.*结构"]
    kmc_patterns = ["看.*活性", "计算.*TOF", "跑.*KMC", "KMC.*模拟"]
    query_param_patterns = ["查询.*参数", "查看.*参数", "参数.*是什么"]
    query_image_patterns = ["查看.*图像", "看.*图", "图像.*结果"]
```

2. **任务识别条件**：
```python
# MSR任务识别条件
# - "看{环境/气氛/反应条件下}的{结构/团簇/构型}"
# - "生成{金属}在{条件}下的{团簇/结构}"
# - 明确提到"MSR"或"MOSP"且涉及结构生成

# KMC任务识别条件  
# - "看{环境/气氛/反应条件下}的{反应活性/TOF/覆盖度/活性/反应}"
# - "计算{金属}在{条件}下的{反应速率/TOF}"
# - 明确提到"KMC"且涉及动力学模拟
```

3. **交互协调流程**：
```python
# 步骤1：初始询问与确认
def ask_confirmation(task_type: str, details: dict) -> str:
    if task_type == "MSR":
        return f"检测到您可能想进行MSR计算（生成团簇结构），是否继续？"
    elif task_type == "KMC":
        return f"检测到您可能想进行KMC计算（模拟反应动力学），是否继续？"
    # ...其他任务类型
```

## 使用示例

### 示例1：MSR任务
```
用户输入："我想看铂在CO氧化气氛下的团簇结构"

InputHandler检测：
- 关键词：看、铂、CO氧化、团簇、结构
- 任务类型：MSR任务
- 询问："检测到您可能想进行MSR计算（生成团簇结构），是否继续？"
```

### 示例2：KMC任务
```
用户输入："计算金一氧化碳氧化的反应活性"

InputHandler检测：
- 关键词：计算、金、一氧化碳氧化、反应活性
- 任务类型：KMC任务
- 询问："检测到您可能想进行KMC计算（模拟反应动力学），是否继续？"
```

### 示例3：查询参数任务
```
用户输入："查询Pt-CO氧化的MSR参数"

InputHandler检测：
- 关键词：查询、Pt-CO氧化、MSR、参数
- 任务类型：查询参数任务
- 询问："检测到您想查询参数，请确认：1. 查询什么体系？2. 查MSR还是KMC参数？3. 查特定任务还是example参数？"
```

## 配置选项

### 关键词权重配置
```python
# 关键词权重设置
KEYWORD_WEIGHTS = {
    # MSR相关
    "团簇": 1.5,
    "结构": 1.5,
    "MSR": 2.0,
    "MOSP": 2.0,
    
    # KMC相关
    "活性": 1.5,
    "TOF": 2.0,
    "KMC": 2.0,
    "动力学": 1.5,
    
    # 查询相关
    "查询": 1.5,
    "查看": 1.3,
    "参数": 1.5,
    "图像": 1.5,
}
```

### 置信度阈值
```python
CONFIDENCE_THRESHOLDS = {
    "high": 0.7,     # 高置信度，直接确认
    "medium": 0.4,   # 中置信度，询问用户
    "low": 0.2,      # 低置信度，需要详细信息
}
```

## 集成方式

### 与Speech2Text Skill集成
```python
# 接收Speech2Text的输出
speech_text = "看铂在CO氧化条件下的团簇结构"
task_info = input_handler.process_input(speech_text)
```

### 与InputFileManager Skill集成
```python
# 调用InputFileManager处理参数
param_result = input_file_manager.process_parameters(
    metal="Pt",
    gases=["CO", "O2"],
    task_type="MSR"
)
```

### 与MSR/KMC Skills集成
```python
# 调用MSR Skill
msr_result = msr_skill.run_calculation(
    input_json=param_result["json_path"],
    output_dir=param_result["output_dir"]
)

# 调用KMC Skill
kmc_result = kmc_skill.run_calculation(
    input_json=param_result["json_path"],
    xyz_file=msr_result["xyz_path"]
)
```

## 错误处理

### 任务识别失败
```
输入："今天天气怎么样"
检测：未检测到MOSP相关关键词
响应："未识别到MOSP计算任务，请提供更详细的需求描述"
```

### 参数不完整
```
输入："我想看团簇结构"
检测：缺少金属元素信息
响应："检测到团簇结构需求，但缺少金属元素信息，请指定金属（如铂、金、铜等）"
```

### 系统错误
```
错误："无法连接到InputFileManager Skill"
处理：记录错误日志，提示用户稍后重试
```

## 性能优化

### 关键词缓存
- 缓存常用关键词检测结果
- 预编译正则表达式模式
- 快速路径匹配优化

### 并发处理
- 支持多个任务并发检测
- 异步调用子技能
- 超时控制和重试机制

## 测试用例

### 单元测试
```python
def test_msr_task_detection():
    input_text = "我想看铂在CO氧化气氛下的团簇结构"
    result = detect_task_type(input_text)
    assert result["task_type"] == "MSR"
    assert "铂" in result["metals"]
    assert "CO" in result["gases"]

def test_kmc_task_detection():
    input_text = "计算金一氧化碳氧化的反应活性"
    result = detect_task_type(input_text)
    assert result["task_type"] == "KMC"
    assert "金" in result["metals"]
    assert "CO" in result["gases"]
```

### 集成测试
```python
def test_full_workflow():
    # 模拟用户输入
    user_input = "看铂在CO氧化条件下的团簇结构"
    
    # InputHandler处理
    task_info = input_handler.process_input(user_input)
    
    # 调用InputFileManager
    params = input_file_manager.process_parameters(task_info)
    
    # 调用MSR Skill
    msr_result = msr_skill.run_calculation(params)
    
    # 验证结果
    assert msr_result["success"] == True
    assert os.path.exists(msr_result["xyz_path"])
    assert os.path.exists(msr_result["image_path"])
```

## 更新日志

### v1.0.0 (2026-04-07)
- 初始版本发布
- 关键词检测与任务识别功能
- 任务协调与确认机制
- 与其他MOSP技能集成接口

## 后续开发计划

### 短期计划
- [ ] 添加更多关键词模式
- [ ] 改进置信度评估算法
- [ ] 添加任务历史记录

### 中期计划
- [ ] 支持多语言关键词检测
- [ ] 添加任务优先级管理
- [ ] 实现智能任务调度

### 长期计划
- [ ] 机器学习优化关键词检测
- [ ] 自适应学习用户偏好
- [ ] 跨技能知识共享

---

**使用提示**：InputHandler是MOSP系统的入口点，负责理解用户意图并协调整个计算流程。确保与其他技能的良好集成是实现流畅用户体验的关键。