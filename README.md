# chatMOSP

chatMOSP - 通过自然语言对话控制MOSP计算的OpenClaw技能集合。让催化反应计算像聊天一样简单！

## 🧪 功能概述

chatMOSP让MOSP计算像聊天一样简单：

1. **语音聊天** (`mosp-speech2text`)
   - 语音转文本，自动修正MOSP专业术语
   - "说"出你的计算需求

2. **对话理解** (`mosp-inputhandler`)
   - 理解自然语言命令
   - 智能路由到相应计算模块

3. **参数聊天** (`mosp-inputfilemanager`)
   - 通过对话管理参数
   - "温度调到400K"这样的自然指令

4. **结构聊天** (`mosp-msr`)
   - "生成一个Pt55团簇"
   - 对话式团簇结构生成

5. **模拟聊天** (`mosp-kmc`)
   - "模拟CO氧化反应"
   - 对话控制动力学模拟

## 🚀 安装方法

### 前提条件
**需要先安装MOSP软件**，然后才能使用这些技能控制MOSP。

### 步骤1：安装MOSP for chatMOSP软件
从[mosp-for-chatMOSP](https://github.com/mosp-catalysis/mosp-for-chatMOSP)仓库下载并安装MOSP软件：
```bash
# 下载MOSP for chatMOSP软件
git clone https://github.com/mosp-catalysis/mosp-for-chatMOSP.git
cd mosp-for-chatMOSP

# 安装依赖和配置
bash install.sh
```

### 步骤2：安装OpenClaw技能
#### 方法1：手动安装
1. 下载本仓库
2. 将skills文件夹中的内容复制到OpenClaw的workspace/skills目录：
   ```
   cp -r skills/* ~/.openclaw/workspace/skills/
   ```

#### 方法2：使用压缩包
下载最新版本的压缩包，解压到OpenClaw workspace目录。

### 步骤3：配置环境变量（可选）
确保MOSP软件路径在系统PATH中，或设置环境变量：
```bash
export MOSP_HOME=/path/to/mosp-for-chatMOSP
export PATH=$PATH:$MOSP_HOME
```

## 💬 使用示例

### 聊天式工作流程
你说 → chatMOSP理解 → 执行计算 → 返回结果

### 示例对话
```
你: "帮我生成一个Pt55团簇"
chatMOSP: "正在生成Pt55团簇结构..."
你: "温度调到400K"
chatMOSP: "已将温度参数更新为400K"
你: "运行CO氧化模拟"
chatMOSP: "开始CO氧化动力学模拟..."
```

### 自然语言命令
- "看看Au的CO氧化反应"
- "把铜团簇大小改成100"
- "显示当前的温度设置"
- "运行水汽变换反应模拟"

## 🛠️ 技能配置

每个技能都有独立的配置文件（如果适用）：
- `SKILL.md` - 技能使用说明
- `*.py` - Python实现代码
- `requirements.txt` - Python依赖

## 📁 目录结构

```
mosp-skills/
├── README.md                 # 本文件
├── skills/                   # 技能目录
│   ├── mosp-speech2text-1.0.0/
│   ├── mosp-inputhandler-1.0.0/
│   ├── mosp-inputfilemanager-1.0.0/
│   ├── mosp-msr-1.0.0/
│   └── mosp-kmc-1.0.0/
├── examples/                 # 使用示例
│   ├── basic-usage.md
│   └── advanced-scenarios.md
└── docs/                     # 详细文档
    ├── api-reference.md
    └── troubleshooting.md
```

## 🔧 系统要求

### 必需条件
- OpenClaw v0.10.0+
- MOSP软件（从mosp-software仓库安装）
- Python 3.8+

### MOSP for chatMOSP软件要求
- **Windows**：可以直接运行
- **Linux/macOS**：需要安装Wine来运行Windows可执行文件
- Python包：numpy, pandas, matplotlib, scipy

### 推荐配置
- 4GB+ 内存
- 10GB+ 可用磁盘空间（用于计算结果）
- 支持的科学计算环境

## 🤝 贡献指南

欢迎贡献代码、文档或报告问题！

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启Pull Request

## 📄 许可证

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件。

## 🙏 致谢

感谢所有为催化反应计算和自动化研究做出贡献的研究人员。

## 📞 支持

如有问题或建议，请：
1. 在GitHub Issues中提交问题
2. 查看详细文档
3. 联系维护者

---

**chatMOSP** - 让催化反应计算像聊天一样简单！ 💬🧪✨