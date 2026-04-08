# chatMOSP 依赖说明

## 📋 重要说明

chatMOSP**不包含**MOSP计算引擎，只包含对话控制接口。你需要同时安装MOSP软件才能进行计算。

## 🔗 所需组件

### 1. MOSP for chatMOSP软件（必需）
- **来源**：[mosp-for-chatMOSP](https://github.com/mosp-catalysis/mosp-for-chatMOSP) 仓库
- **功能**：核心计算引擎（MSR/KMC）
- **大小**：约1.5MB（压缩包）
- **关系**：chatMOSP的"大脑"，负责实际计算

### 2. chatMOSP（本仓库）
- **功能**：对话式控制接口
- **大小**：约74KB（压缩包）
- **依赖**：需要MOSP软件才能正常工作
- **关系**：MOSP的"嘴巴"和"耳朵"，负责与用户交流

## 🛠️ 安装顺序

**完整的chatMOSP体验需要两个部分**：

```
MOSP for chatMOSP（计算引擎）
        +
chatMOSP（对话接口）
        =
完整的对话式MOSP体验
```

**安装顺序**：
```
1. 安装MOSP for chatMOSP软件（计算能力）
2. 安装chatMOSP（对话能力）
3. 配置环境变量
4. 重启OpenClaw
```

## 📁 MOSP软件结构

安装MOSP软件后，您应该有以下目录结构：

```
mosp-software/
├── engine/           # 计算引擎（Windows可执行文件）
│   ├── main.exe     # KMC主程序
│   └── *.dll        # 依赖库
├── examples/         # 示例输入文件
├── utils/           # Python工具脚本
├── kmc_standalone.py # 主入口脚本
├── requirements.txt  # Python依赖
└── install.sh       # 安装脚本
```

## 🔧 技能如何调用MOSP

### 调用流程
```
用户命令 → OpenClaw技能 → 解析参数 → 调用MOSP软件 → 返回结果
```

### 具体实现
1. **语音命令**：通过`mosp-speech2text`技能转换
2. **参数解析**：通过`mosp-inputhandler`技能处理
3. **文件管理**：通过`mosp-inputfilemanager`技能管理
4. **计算执行**：
   - MSR计算：调用`utils/msr.py`
   - KMC计算：调用`kmc_standalone.py`
5. **结果处理**：通过技能解析和展示结果

## ⚠️ 常见问题

### Q1: 安装技能后无法运行MOSP计算
**可能原因**：未安装MOSP for chatMOSP软件
**解决方案**：
```bash
# 1. 下载MOSP for chatMOSP软件
git clone https://github.com/mosp-catalysis/mosp-for-chatMOSP.git

# 2. 安装MOSP软件
cd mosp-for-chatMOSP
bash install.sh

# 3. 设置环境变量
export MOSP_HOME=$(pwd)
export PATH=$PATH:$MOSP_HOME
```

### Q2: Linux/macOS上报错"无法运行main.exe"
**可能原因**：未安装Wine
**解决方案**：
```bash
# Ubuntu/Debian
sudo apt install wine

# macOS (Homebrew)
brew install wine
```

### Q3: Python依赖安装失败
**解决方案**：
```bash
# 使用pip3
pip3 install -r requirements.txt

# 或使用virtualenv
python3 -m venv mosp_venv
source mosp_venv/bin/activate
pip install -r requirements.txt
```

## 📄 许可证说明

### MOSP软件许可证
- 使用**学术非商业许可证**
- 允许学术研究使用
- 禁止商业用途
- 详细条款见MOSP软件仓库的LICENSE.txt

### OpenClaw技能许可证
- 使用**MIT许可证**
- 允许自由使用、修改、分发
- 详见本仓库的LICENSE文件

## 🔄 更新策略

### MOSP软件更新
- 需要从mosp-software仓库获取更新
- 可能涉及引擎版本升级
- 注意版本兼容性

### 技能更新
- 从本仓库获取更新
- 通常向后兼容
- 新功能可能需要MOSP软件支持

## 📞 技术支持

### 技能相关问题
- 在GitHub Issues中报告
- 提供OpenClaw日志
- 描述具体的错误信息

### MOSP软件问题
- 联系MOSP课题组
- 提供计算日志
- 描述系统环境和输入文件

## 🎯 最佳实践

### 安装验证
安装完成后，运行以下测试：
```bash
# 测试MOSP软件
cd mosp-software
python kmc_standalone.py --xyz examples/Au-CO.xyz --json examples/Au-COoxidation.json --out-dir test_run

# 测试OpenClaw技能
# 在OpenClaw中使用语音或文本命令
```

### 环境配置
建议将以下配置添加到`.bashrc`或`.zshrc`：
```bash
export MOSP_HOME=/path/to/mosp-software
export PATH=$PATH:$MOSP_HOME
alias mosp-run="python $MOSP_HOME/kmc_standalone.py"
```

### 数据管理
- 定期清理`OUTPUT/`目录
- 备份重要的输入文件
- 使用版本控制管理参数文件

---

**重要提示**：chatMOSP就像一个友好的助手，但需要MOSP软件这个"专家"来执行实际计算。两者配合才能提供完整的对话式MOSP体验。