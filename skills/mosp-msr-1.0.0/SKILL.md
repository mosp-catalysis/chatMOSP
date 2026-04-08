---
name: mosp-msr
description: MOSP团簇结构生成技能，执行MSR计算生成金属团簇结构，并生成旋转动画和静态结构图。
homepage: https://github.com/openclaw/openclaw
metadata: {"clawdbot":{"emoji":"🔬🧪","requires":{"bins":["python3"]},"install":[{"id":"python","kind":"bin","bins":["python3"],"label":"需要Python 3.8+"}]}}
---

# MOSP MSR Skill 🔬🧪

## 概述

MOSP团簇结构生成技能，负责执行MSR（Metal Surface Reaction）计算，生成金属团簇结构，并创建可视化图像。

## 核心功能

### 1. 文件夹创建与文件准备
- **输入**：来自InputFileManager Skill的最终JSON参数文件
- **文件夹命名格式**：
  ```
  {Element}_{Temperature}K_{Pressure}Pa_{Gas1}{PP1}_{Gas2}{PP2}_R{Radius}A/
  ```
- **文件准备**：
  - 移动并重命名JSON文件为`input.json`
  - 复制`utils/paint.py`到MSR文件夹
  - 创建完整文件夹结构

### 2. 执行MSR计算
- **运行命令**：使用固定的`utils/msr.py`脚本
  ```bash
  python3 utils/msr.py --json OUTPUT/{任务目录}/input.json --output OUTPUT/{任务目录}/
  ```
- **大团簇警告**：半径>40Å时提供警告提示
- **输出文件**：
  - `{Element}_FCC_T_{T}_P_{P}_cluster.xyz` - 带颜色标记的XYZ结构
  - `ini.xyz` - KMC初始结构（无颜色标记）
  - `faceinfo.txt` - 晶面统计信息
  - `msr_run.log` - 运行日志

### 3. 可视化生成（必选）
- **旋转动画**（GIF格式）：
  ```bash
  python3 paint.py {Element}_FCC_T_{T}_P_{P}_cluster.xyz --gif rotation.gif --color-by site_type
  ```
- **静态结构图**（PNG格式）：
  ```bash
  python3 paint.py {Element}_FCC_T_{T}_P_{P}_cluster.xyz --output structure.png --color-by site_type
  ```
- **路径验证**：确保在正确目录中运行paint.py

### 4. 参数分析报告生成
- 自动生成`parameter_analysis.md`文件
- 包含参数来源分析、计算条件说明、结果摘要

## 文件管理规则

### 严格规则（遵循核心实施原则一）
1. **路径白名单约束**：所有操作必须在`$MOSP_HOME/OUTPUT/{任务目录}/`内进行
2. **example目录保护**：example目录完全只读，所有修改重定向到OUTPUT目录
3. **测试沙箱机制**：所有测试在`$MOSP_HOME/OUTPUT/_test_sandbox/`中进行

### 禁止行为
- ❌ 禁止新建其他msr.py代码
- ❌ 禁止运行复制、移动、修改utils/msr.py脚本
- ❌ 禁止在workspace根目录创建任何MOSP相关文件
- ❌ 禁止在MOSP根目录创建临时文件
- ❌ 禁止修改example目录中的任何文件
- ❌ 禁止创建test_开头的测试脚本在非沙箱位置
- ❌ 禁止跳过可视化生成步骤
- ❌ 禁止不发送结果给用户
- ❌ 禁止在非任务目录中运行paint.py

## 错误处理

### 常见错误1：负表面能
```
Geometry construction failed: Nanoparticle broken
Negative surface energy
```

**原因分析**：
- 高氧分压（如O₂ 90%）导致强氧吸附
- 吸附能补偿过度，使有效表面能变为负值
- 相互作用能叠加效应加剧问题

**解决方案**：
1. **保守参数测试**：先使用弱吸附、高表面能参数
2. **逐步调整**：从简单到复杂，先无相互作用，后加w矩阵
3. **监控表面能**：确保有效表面能γ_eff始终为正
4. **高氧条件特殊处理**：
   - 降低氧吸附能绝对值
   - 增加表面能γ提供补偿空间
   - 减小或设零相互作用能

### 常见错误2：参数不收敛
**现象**：迭代求解覆盖度方程不收敛

**解决方案**：
1. **检查参数合理性**：E_ads应在合理范围，w矩阵值不过大
2. **调整求解参数**：增加最大迭代次数，减小收敛阈值
3. **提供数值稳定化**：添加小阻尼项防止振荡

## 使用流程

```
InputHandler调用 → 准备文件夹 → 执行MSR计算 → 生成可视化 → 发送结果 → 生成分析报告
```

## 技术实现

### 依赖
- Python 3.8+
- $MOSP_HOME/utils/msr.py（固定脚本）
- $MOSP_HOME/utils/paint.py（可视化工具）

### 核心处理逻辑

1. **文件夹创建**：
```python
def create_msr_directory(params: Dict) -> Path:
    """创建MSR任务目录"""
    # 生成目录名
    dir_name = f"{params['Element']}_{params['Temperature']}K_{params['Pressure']}Pa_"
    dir_name += f"{params['Gas1_name']}{params['Gas1_pp']}_{params['Gas2_name']}{params['Gas2_pp']}_"
    dir_name += f"R{params['Radius']}A"
    
    # 创建目录
    output_dir = Path(os.environ.get("MOSP_HOME", ".")) / "OUTPUT" / dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return output_dir
```

2. **文件准备**：
```python
def prepare_msr_files(input_json: Path, output_dir: Path):
    """准备MSR计算文件"""
    # 移动并重命名JSON文件
    target_json = output_dir / "input.json"
    shutil.copy2(input_json, target_json)
    
    # 复制可视化工具
    paint_py = Path(os.environ.get("MOSP_HOME", ".")) / "utils" / "paint.py"
    if paint_py.exists():
        shutil.copy2(paint_py, output_dir / "paint.py")
```

3. **执行MSR计算**：
```python
def run_msr_calculation(output_dir: Path):
    """运行MSR计算"""
    input_json = output_dir / "input.json"
    
    # 构建命令
    cmd = [
        "python3", str(Path(os.environ.get("MOSP_HOME", ".")) / "utils" / "msr.py"),
        "--json", str(input_json),
        "--output", str(output_dir)
    ]
    
    # 大团簇警告
    params = load_parameters(input_json)
    if params.get("Radius", 0) > 40:
        print("⚠️ 检测到大团簇（半径 > 40 Å），MSR计算可能较慢，请耐心等待...")
    
    # 执行计算
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # 保存日志
    log_file = output_dir / "msr_run.log"
    log_file.write_text(result.stdout + "\n" + result.stderr)
    
    return result.returncode == 0
```

4. **可视化生成**：
```python
def generate_visualizations(output_dir: Path):
    """生成可视化图像"""
    # 进入任务目录
    original_cwd = os.getcwd()
    os.chdir(output_dir)
    
    try:
        # 查找XYZ文件
        xyz_files = list(output_dir.glob("*_FCC_T_*_P_*_cluster.xyz"))
        if not xyz_files:
            raise FileNotFoundError("未找到MSR生成的XYZ文件")
        
        xyz_file = xyz_files[0]
        
        # 生成旋转动画
        gif_cmd = ["python3", "paint.py", str(xyz_file), "--gif", "rotation.gif", "--color-by", "site_type"]
        subprocess.run(gif_cmd, check=True)
        
        # 生成静态结构图
        png_cmd = ["python3", "paint.py", str(xyz_file), "--output", "structure.png", "--color-by", "site_type"]
        subprocess.run(png_cmd, check=True)
        
    finally:
        os.chdir(original_cwd)
```

## 使用示例

### 示例1：标准MSR计算
```
输入参数：Pt, 700K, 6000Pa, CO 9%, O₂ 90%, 半径40Å

处理流程：
1. 创建目录：$MOSP_HOME/OUTPUT/Pt_700K_6000Pa_CO9_O290_R40A/
2. 准备文件：input.json, paint.py
3. 执行MSR：生成XYZ结构和晶面信息
4. 可视化：生成rotation.gif和structure.png
5. 发送结果：图像和文件位置给用户
```

### 示例2：大团簇计算
```
输入参数：Au, 600K, 5000Pa, CO 10%, O₂ 90%, 半径60Å

特殊处理：
1. 警告："⚠️ 检测到大团簇（半径 > 40 Å），MSR计算可能较慢，请耐心等待..."
2. 显示进度：计算过程中定期输出状态
3. 延长超时时间：给予更多计算时间
```

### 示例3：错误处理
```
错误："Geometry construction failed: Negative surface energy"

处理：
1. 分析原因：高氧分压导致负表面能
2. 建议调整：降低氧吸附能，增加表面能
3. 提供修改建议：具体参数调整值
4. 记录错误：保存到错误日志
```

## 配置选项

### 计算参数
```python
MSR_CONFIG = {
    "max_radius_warning": 40,  # 大团簇警告阈值（Å）
    "timeout_seconds": 3600,   # 计算超时时间（秒）
    "progress_update_interval": 30,  # 进度更新间隔（秒）
}
```

### 可视化参数
```python
VISUALIZATION_CONFIG = {
    "gif_duration": 5,         # GIF动画时长（秒）
    "image_size": (800, 600),  # 图像尺寸
    "color_scheme": "site_type",  # 着色方案
}
```

### 错误处理参数
```python
ERROR_HANDLING_CONFIG = {
    "max_retries": 3,          # 最大重试次数
    "retry_delay": 5,          # 重试延迟（秒）
    "fallback_parameters": {   # 备用参数
        "Radius": 30,
        "Temperature": 600,
        "Pressure": 1000,
    },
}
```

## 集成方式

### 与InputHandler集成
```python
# InputHandler调用MSR Skill
msr_result = msr_skill.run_calculation(
    input_json=params["json_path"],
    output_base_dir=os.path.join(os.environ.get("MOSP_HOME", "."), "OUTPUT")
)

# 返回结果
result = {
    "success": msr_result["success"],
    "output_dir": msr_result["output_dir"],
    "xyz_file": msr_result["xyz_path"],
    "images": msr_result["images"],
    "log_file": msr_result["log_path"],
}
```

### 独立使用
```python
# 直接运行MSR计算
msr = MSRSkill()
result = msr.run(
    parameters={...},  # 参数字典
    output_dir="custom_output/"
)

# 只生成可视化
visualization = msr.generate_visualization(
    xyz_file="structure.xyz",
    output_dir="visualizations/"
)
```

## 性能优化

### 计算优化
- 预检查参数有效性
- 缓存中间计算结果
- 并行处理多个小任务

### 内存优化
- 流式处理大文件
- 及时释放不再需要的数据
- 限制同时运行的任务数

### 存储优化
- 压缩历史数据
- 定期清理临时文件
- 智能存储管理

## 测试用例

### 单元测试
```python
def test_directory_creation():
    """测试目录创建功能"""
    params = {
        "Element": "Pt",
        "Temperature": 700,
        "Pressure": 6000,
        "Gas1_name": "CO",
        "Gas1_pp": 9,
        "Gas2_name": "O2",
        "Gas2_pp": 90,
        "Radius": 40,
    }
    
    dir_path = create_msr_directory(params)
    assert dir_path.name == "Pt_700K_6000Pa_CO9_O290_R40A"
    assert dir_path.exists()

def test_file_preparation():
    """测试文件准备功能"""
    test_json = Path("test_input.json")
    output_dir = Path("test_output")
    
    prepare_msr_files(test_json, output_dir)
    assert (output_dir / "input.json").exists()
    assert (output_dir / "paint.py").exists()
```

### 集成测试
```python
def test_full_msr_workflow():
    """测试完整MSR工作流程"""
    # 准备测试参数
    test_params = {...}
    
    # 运行MSR计算
    result = msr_skill.run_full_workflow(test_params)
    
    # 验证结果
    assert result["success"] == True
    assert os.path.exists(result["output_dir"])
    assert os.path.exists(result["xyz_file"])
    assert os.path.exists(result["gif_file"])
    assert os.path.exists(result["png_file"])
    assert os.path.exists(result["log_file"])
```

## 更新日志

### v1.0.0 (2026-04-07)
- 初始版本发布
- 文件夹创建与文件准备
- MSR计算执行
- 可视化图像生成
- 参数分析报告
- 错误处理机制

## 后续开发计划

### 短期计划
- [ ] 添加更多可视化选项
- [ ] 改进错误处理机制
- [ ] 添加性能监控

### 中期计划
- [ ] 支持批量计算
- [ ] 添加结果对比功能
- [ ] 实现自动化参数优化

### 长期计划
- [ ] 集成机器学习预测
- [ ] 支持自定义晶面
- [ ] 实现实时可视化

---

**使用提示**：MSR Skill是MOSP系统的核心计算组件，确保严格遵循文件管理规则和安全约束。所有生成的文件都集中在任务目录中，便于管理和复现。