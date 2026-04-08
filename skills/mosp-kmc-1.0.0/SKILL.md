---
name: mosp-kmc
description: MOSP动力学模拟技能，执行KMC（Kinetic Monte Carlo）计算，模拟表面反应动力学，生成TOF和覆盖度图。
homepage: https://github.com/openclaw/openclaw
metadata: {"clawdbot":{"emoji":"📈🧪","requires":{"bins":["python3","wine"]},"install":[{"id":"python","kind":"bin","bins":["python3"],"label":"需要Python 3.8+"},{"id":"wine","kind":"bin","bins":["wine"],"label":"需要Wine运行Windows KMC引擎"}]}}
---

# MOSP KMC Skill 📈🧪

## 概述

MOSP动力学模拟技能，负责执行KMC（Kinetic Monte Carlo）计算，模拟表面反应动力学，生成反应活性（TOF）和覆盖度随时间变化的图像。

## 核心功能

### 1. 文件夹创建与文件准备
- **输入**：
  - JSON参数文件（来自InputFileManager Skill）
  - XYZ结构文件（三选一来源）：
    a. **MSR新生成**：如果刚运行了MSR，使用其输出目录
    b. **example现有**：使用example目录中的Au/Pt/Cu团簇文件
    c. **用户指定**：用户提供自定义XYZ文件

- **智能目录创建规则**：
  - **检查目录存在性**：
    - 首先检查 `/{Element}_{Temperature}K_{Pressure}Pa_{Gas1}{PP1}_{Gas2}{PP2}_R{Radius}A/` 是否存在
    - 如果存在（已有MSR结构或之前创建的目录）：
      a. 检查KMC输出目录是否已存在
      b. 如果KMC目录存在且使用相同初始结构，直接使用
      c. 如果KMC目录存在但使用不同初始结构，创建带序号的文件夹

  - **新建目录流程**：
    - 创建参数目录（如果不存在）
    - 创建KMC输出目录：`KMC_{Temperature}K_{Pressure}Pa_{Gas1}{PP1}_{Gas2}{PP2}_{nLoop}steps/`

### 2. 文件准备规则
1. **创建KMC输出目录**：`KMC_{Temperature}K_{Pressure}Pa_{Gas1}{PP1}_{Gas2}{PP2}_{nLoop}steps/`
2. **手动创建子目录**：
   - 在KMC目录中新建INPUT文件夹
   - **注意**：根据最新修改，不再创建OUTPUT文件夹（输出到根目录）
3. **文件复制/移动规则**：
   - **JSON参数文件**：重命名为`kmc_input.json`
   - **XYZ结构文件**：重命名为`kmc_ini.xyz`
   - **重要**：文件放在KMC根目录，不在INPUT子目录中

### 3. 执行KMC计算
- **运行命令**：使用修改后的`kmc_standalone.py`（v3.3+版本）
  ```bash
  python3 $MOSP_HOME/kmc_standalone.py --json kmc_input.json --xyz kmc_ini.xyz --out-dir .
  ```
- **后台运行**：步数>10万步时使用nohup后台运行
  ```bash
  nohup python3 $MOSP_HOME/kmc_standalone.py --json kmc_input.json --xyz kmc_ini.xyz --out-dir . > run.log 2>&1 &
  ```
- **输出文件**（直接输出到KMC根目录）：
  - `rec_cov.data` - 覆盖度数据
  - `rec_event.data` - 事件数据
  - `rec_site_spc.data` - 位点数据
  - `coverage.csv` - 处理后的覆盖度CSV
  - `tof.csv` - TOF数据CSV
  - `site_tof.csv` - 位点TOF数据CSV
  - `coverage.png` - 覆盖度图像
  - `tof.png` - TOF图像
  - `run.log` - 运行日志

### 4. 结果处理与可视化
- **数据处理**：自动将原始数据转换为CSV格式
- **图像生成**：自动生成覆盖度和TOF图像
- **结果汇总**：生成计算结果摘要

## 文件管理规则

### 最新目录结构（2026-04-07修改后）
```
$MOSP_HOME/OUTPUT/
├── {Element}_{Temperature}K_{Pressure}Pa_{Gas1}{PP1}_{Gas2}{PP2}_R{Radius}A/  # 参数目录
│   ├── KMC_{Temperature}K_{Pressure}Pa_{Gas1}{PP1}_{Gas2}{PP2}_{nLoop}steps/  # KMC输出目录
│   │   ├── kmc_input.json      # 输入参数文件（根目录）
│   │   ├── kmc_ini.xyz         # 初始结构文件（根目录）
│   │   ├── INPUT/              # 输入子目录（由kmc_standalone.py创建）
│   │   ├── rec_cov.data        # KMC原始输出（根目录）
│   │   ├── rec_event.data      # KMC原始输出（根目录）
│   │   ├── rec_site_spc.data   # KMC原始输出（根目录）
│   │   ├── coverage.csv        # 处理后数据（根目录）
│   │   ├── tof.csv             # 处理后数据（根目录）
│   │   ├── site_tof.csv        # 处理后数据（根目录）
│   │   ├── coverage.png        # 图像（根目录）
│   │   ├── tof.png             # 图像（根目录）
│   │   └── run.log             # 日志文件（根目录）
│   │
│   └── [其他MSR相关文件...]
```

### 重要修改说明
1. **取消重复的OUTPUT子目录**：所有文件直接输出到KMC根目录
2. **INPUT目录自动创建**：由`kmc_standalone.py`自动创建
3. **简化目录结构**：避免嵌套过深，便于用户查找

## 错误处理

### 常见错误1：KMC引擎失败
```
错误：main.exe failed with exit code 1
原因：参数不匹配、结构文件问题、引擎兼容性问题
处理：检查输入文件格式，验证参数一致性，查看详细日志
```

### 常见错误2：Wine兼容性问题
```
错误：wine: cannot find '/path/to/main.exe'
原因：Wine配置问题或路径错误
处理：检查Wine安装，验证引擎文件存在性，设置正确环境变量
```

### 常见错误3：内存不足
```
错误：Memory allocation failed
原因：步数过多或系统过大
处理：减少nLoop步数，分批计算，增加系统内存
```

## 使用流程

### 情况A：MSR后接KMC（完整工作流）
```
MSR完成 → 获取XYZ结构 → 准备KMC参数 → 创建KMC目录 → 执行KMC计算 → 生成结果 → 发送图像
```

### 情况B：独立KMC计算
```
用户提供XYZ结构 → 准备KMC参数 → 创建参数目录和KMC目录 → 执行KMC计算 → 生成结果
```

### 情况C：使用example结构
```
选择example结构 → 准备KMC参数 → 创建目录 → 执行计算 → 生成结果
```

## 技术实现

### 依赖
- Python 3.8+
- Wine（运行Windows KMC引擎）
- $MOSP_HOME/kmc_standalone.py（修改后的v3.3+版本）

### 核心处理逻辑

1. **目录创建与检查**：
```python
def create_kmc_directory(base_params: Dict, kmc_params: Dict, xyz_source: str) -> Path:
    """创建KMC任务目录"""
    # 生成基础目录名
    base_dir_name = generate_base_directory_name(base_params)
    base_dir = Path(os.environ.get("MOSP_HOME", ".")) / "OUTPUT" / base_dir_name
    
    # 检查是否需要新建带序号目录
    if base_dir.exists() and xyz_source != "existing":
        # 查找最大序号
        max_suffix = 0
        for existing_dir in base_dir.parent.iterdir():
            if existing_dir.name.startswith(base_dir_name):
                # 提取序号
                match = re.search(r'_(\d+)$', existing_dir.name)
                if match:
                    suffix = int(match.group(1))
                    max_suffix = max(max_suffix, suffix)
        
        # 创建带序号目录
        if max_suffix > 0:
            base_dir = base_dir.parent / f"{base_dir_name}_{max_suffix + 1:02d}"
    
    # 创建基础目录
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建KMC目录
    kmc_dir_name = generate_kmc_directory_name(kmc_params)
    kmc_dir = base_dir / kmc_dir_name
    kmc_dir.mkdir(parents=True, exist_ok=True)
    
    return kmc_dir
```

2. **文件准备**：
```python
def prepare_kmc_files(json_path: Path, xyz_path: Path, kmc_dir: Path):
    """准备KMC计算文件"""
    # 复制并重命名JSON文件
    target_json = kmc_dir / "kmc_input.json"
    shutil.copy2(json_path, target_json)
    
    # 复制并重命名XYZ文件
    target_xyz = kmc_dir / "kmc_ini.xyz"
    shutil.copy2(xyz_path, target_xyz)
```

3. **执行KMC计算**：
```python
def run_kmc_calculation(kmc_dir: Path, use_background: bool = False):
    """运行KMC计算"""
    # 构建命令
    cmd = [
        "python3", str(Path(os.environ.get("MOSP_HOME", ".")) / "kmc_standalone.py"),
        "--json", str(kmc_dir / "kmc_input.json"),
        "--xyz", str(kmc_dir / "kmc_ini.xyz"),
        "--out-dir", str(kmc_dir),
    ]
    
    # 检查是否需要后台运行
    nloop = extract_nloop_from_json(kmc_dir / "kmc_input.json")
    
    if nloop > 100000 and use_background:
        # 后台运行
        cmd_str = " ".join(cmd)
        bg_cmd = f"nohup {cmd_str} > {kmc_dir/'run.log'} 2>&1 &"
        subprocess.run(bg_cmd, shell=True)
        
        # 获取进程ID
        pid = get_background_pid()
        return {"success": True, "background": True, "pid": pid, "log_file": kmc_dir/"run.log"}
    else:
        # 前台运行
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(kmc_dir))
        
        # 保存日志
        log_file = kmc_dir / "run.log"
        log_file.write_text(result.stdout + "\n" + result.stderr)
        
        return {"success": result.returncode == 0, "background": False, "log_file": log_file}
```

4. **结果验证**：
```python
def verify_kmc_results(kmc_dir: Path) -> Dict[str, bool]:
    """验证KMC计算结果"""
    required_files = [
        "rec_cov.data",
        "rec_event.data", 
        "rec_site_spc.data",
        "coverage.csv",
        "tof.csv",
        "coverage.png",
        "tof.png",
    ]
    
    results = {}
    for filename in required_files:
        file_path = kmc_dir / filename
        results[filename] = file_path.exists() and file_path.stat().st_size > 0
    
    return results
```

## 使用示例

### 示例1：MSR后接KMC
```
MSR生成：Pt_700K_6000Pa_CO9_O290_R40A/目录

KMC处理：
1. 使用MSR的ini.xyz作为初始结构
2. 创建KMC目录：KMC_700K_6000Pa_CO9_O290_1000000steps/
3. 执行KMC计算（后台运行）
4. 生成TOF和覆盖度图像
5. 发送结果给用户
```

### 示例2：独立KMC计算
```
用户提供：自定义Au团簇.xyz

KMC处理：
1. 创建基础目录：Au_600K_5000Pa_CO10_O290_R30A/
2. 创建KMC目录：KMC_600K_5000Pa_CO10_O290_500000steps/
3. 复制并重命名文件
4. 执行KMC计算
5. 生成结果
```

### 示例3：大计算量任务
```
参数：nLoop = 5000000 steps

处理：
1. 检测大计算量："步数>10万步，KMC将在后台运行"
2. 使用nohup后台运行
3. 提供进程ID和日志文件位置
4. 定期检查进度
5. 完成后通知用户
```

## 配置选项

### 计算参数
```python
KMC_CONFIG = {
    "background_threshold": 100000,  # 后台运行阈值（步数）
    "timeout_hours": 24,             # 计算超时时间（小时）
    "memory_warning_threshold": 10000000,  # 内存警告阈值（步数）
    "check_interval": 60,            # 进度检查间隔（秒）
}
```

### 文件管理
```python
FILE_MANAGEMENT = {
    "max_directory_depth": 3,        # 最大目录深度
    "cleanup_temp_files": True,      # 清理临时文件
    "compress_old_results": False,   # 压缩旧结果
    "retention_days": 30,            # 结果保留天数
}
```

### 错误处理
```python
ERROR_CONFIG = {
    "max_retries": 3,                # 最大重试次数
    "retry_delay": 10,               # 重试延迟（秒）
    "fallback_nloop": 100000,        # 备用步数
    "notify_on_error": True,         # 错误时通知
}
```

## 集成方式

### 与InputHandler集成
```python
# InputHandler调用KMC Skill
kmc_result = kmc_skill.run_calculation(
    input_json=params["json_path"],
    xyz_file=structure_path,
    background=should_run_in_background(params)
)

# 返回结果
result = {
    "success": kmc_result["success"],
    "kmc_dir": kmc_result["kmc_dir"],
    "output_files": kmc_result["output_files"],
    "images": kmc_result["images"],
    "log_file": kmc_result["log_file"],
    "background": kmc_result.get("background", False),
    "pid": kmc_result.get("pid"),
}
```

### 独立使用
```python
# 直接运行KMC计算
kmc = KMCSkill()
result = kmc.run(
    json_file="kmc_params.json",
    xyz_file="structure.xyz",
    output_base_dir=os.path.join(os.environ.get("MOSP_HOME", "."), "OUTPUT")
)

# 只处理结果
processed = kmc.process_results(
    kmc_dir=os.path.join(os.environ.get("MOSP_HOME", "."), "OUTPUT", "task_001", "KMC_...")
)
```

## 性能优化

### 计算优化
- 智能步数选择（根据系统大小自适应）
- 并行处理多个小系统
- 缓存中间计算结果

### 内存优化
- 流式处理大数据文件
- 及时释放不用的数据
- 限制同时运行的KMC任务数

### 存储优化
- 按需生成图像
- 压缩历史数据
- 智能清理临时文件

## 测试用例

### 单元测试
```python
def test_directory_creation():
    """测试KMC目录创建"""
    base_params = {...}
    kmc_params = {...}
    
    kmc_dir = create_kmc_directory(base_params, kmc_params, "example")
    assert kmc_dir.name.startswith("KMC_")
    assert kmc_dir.exists()

def test_file_preparation():
    """测试文件准备"""
    test_json = Path("test.json")
    test_xyz = Path("test.xyz")
    kmc_dir = Path("test_kmc")
    
    prepare_kmc_files(test_json, test_xyz, kmc_dir)
    assert (kmc_dir / "kmc_input.json").exists()
    assert (kmc_dir / "kmc_ini.xyz").exists()
```

### 集成测试
```python
def test_full_kmc_workflow():
    """测试完整KMC工作流程"""
    # 准备测试文件
    test_params = {...}
    test_structure = "example/Au-CO.xyz"
    
    # 运行KMC计算
    result = kmc_skill.run_full_workflow(test_params, test_structure)
    
    # 验证结果
    assert result["success"] == True
    assert os.path.exists(result["kmc_dir"])
    assert os.path.exists(result["coverage_png"])
    assert os.path.exists(result["tof_png"])
    assert os.path.exists(result["log_file"])
```

## 更新日志

### v1.0.0 (2026-04-07)
- 初始版本发布
- 智能目录创建与管理
- KMC计算执行（支持后台运行）
- 结果处理与可视化
- 错误处理机制
- 集成最新kmc_standalone.py修改（v3.3+）

## 后续开发计划

### 短期计划
- [ ] 添加计算进度监控
- [ ] 改进错误恢复机制
- [ ] 添加结果对比功能

### 中期计划
- [ ] 支持批量KMC计算
- [ ] 添加敏感性分析
- [ ] 实现参数扫描

### 长期计划
- [ ] 集成机器学习加速
- [ ] 支持分布式计算
- [ ] 实时可视化监控

---

**使用提示**：KMC Skill是MOSP系统的动力学模拟核心，支持从MSR无缝衔接或独立运行。对于大计算量任务会自动转为后台运行，确保不会阻塞用户交互。