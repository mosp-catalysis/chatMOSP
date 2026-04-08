---
name: mosp-speech2text
description: MOSP专用语音识别技能，使用OpenAI Whisper tiny模型，包含MOSP术语修正，将语音转换为适合InputHandler处理的文本命令。
homepage: https://github.com/openclaw/openclaw
metadata: {"clawdbot":{"emoji":"🎙️🧪","requires":{"bins":["whisper"]},"install":[{"id":"whisper","kind":"bin","bins":["whisper"],"label":"需要OpenAI Whisper CLI"}]}}
---

# MOSP Speech2Text Skill 🎙️🧪

## 概述

MOSP专用语音识别技能，专门处理科研计算领域的语音输入，特别是MOSP（金属团簇表面反应）相关术语。

## 核心功能

### 1. 语音识别
- 使用OpenAI Whisper tiny模型进行快速语音识别
- 支持中文、英文及中英文混合语音
- 自动检测语言，无需手动指定

### 2. MOSP术语修正
- **金属元素谐音修正**：
  - "铐" → "Rh（铑）"
  - "钉" → "Ru（钌）"
  - "白金" → "Pt（铂）"
  - "黄金" → "Au（金）"
  - "红铜" → "Cu（铜）"

- **化学术语修正**：
  - "吸附" vs "吸收"（根据上下文判断）
  - "温度300度" → "300 K"（MOSP默认温标）
  - "50埃" → "50 Å"

- **专业术语标准化**：
  - "MOSP" / "摩斯普" / "莫斯普" → "MOSP"
  - "团簇" / "团族" → "团簇"
  - "纳米团簇" / "nano cluster" → "纳米团簇"

### 3. 命令转换
- 将语音识别结果转换为自然语言文本命令
- 格式适合InputHandler Skill直接处理
- 不转换为代码命令格式

### 4. 错误处理
- 识别置信度低时询问用户确认
- 提供修正建议
- 支持重新录音

## 使用流程

```
用户语音输入
    ↓
OpenAI Whisper识别（tiny模型）
    ↓
MOSP术语修正层
    ↓
命令转换（自然语言格式）
    ↓
[可选] 低置信度 → 用户确认
    ↓
传递给InputHandler Skill
```

## 技术实现

### 依赖
- OpenAI Whisper CLI（已安装）
- Python 3.8+

### 核心处理逻辑

1. **语音文件处理**：
   - 支持常见音频格式（mp3, wav, m4a, flac等）
   - 自动格式转换（如需要）

2. **Whisper参数**：
   ```bash
   whisper audio_file.mp3 \
     --model tiny \
     --language auto \
     --output_format txt \
     --fp16 False  # 确保兼容性
   ```

3. **术语修正词典**：
   ```python
   MOSP_TERM_CORRECTIONS = {
       # 金属元素
       "铐": "Rh（铑）",
       "钉": "Ru（钌）",
       "白金": "Pt（铂）",
       "黄金": "Au（金）",
       "红铜": "Cu（铜）",
       
       # 单位转换
       "度": "K",
       "埃": "Å",
       "大气压": "atm",
       
       # 专业术语
       "摩斯普": "MOSP",
       "莫斯普": "MOSP",
       "团族": "团簇",
   }
   ```

4. **上下文感知修正**：
   - 在化学上下文中，"铐"一定是"Rh"而非刑具
   - 在化学上下文中，"钉"一定是"Ru"而非钉子
   - "吸附"与"吸收"根据反应类型判断

## 使用示例

### 示例1：MSR任务语音输入
```
用户语音："我想看铂在CO氧化气氛下的团簇结构"

识别结果："我想看Pt在CO氧化气氛下的团簇结构"

修正后："看Pt在CO氧化条件下的团簇结构" → InputHandler
```

### 示例2：KMC任务语音输入
```
用户语音："计算金一氧化碳氧化的反应活性"

识别结果："计算Au-CO氧化的反应活性"

修正后："计算Au在CO氧化条件下的反应活性" → InputHandler
```

### 示例3：混合语言输入
```
用户语音："我想run一个Pt CO oxidation的KMC simulation"

识别结果："我想run一个Pt CO oxidation的KMC simulation"

修正后："运行Pt-CO氧化反应的KMC模拟" → InputHandler
```

## 错误处理场景

### 场景1：低置信度识别
```
识别结果："我想看[不清楚]在CO氧化条件下的结构"
置信度：0.45

系统响应："识别结果置信度较低，您说的是'铂'还是'金'？"
用户确认："铂"
最终结果："看Pt在CO氧化条件下的团簇结构"
```

### 场景2：术语歧义
```
识别结果："我想看铑的团簇结构"
上下文：未明确是Rh还是其他金属

系统响应："检测到'铑'，确认是指Rh（铑）元素吗？"
用户确认："是"
最终结果："看Rh的团簇结构"
```

### 场景3：识别失败
```
识别结果："[噪音] 无法识别"
系统响应："语音识别失败，请重新录音或改用文字输入"
```

## 集成方式

### 作为独立技能
```bash
# 直接调用语音识别
mosp-speech2text --audio recording.wav

# 输出转换后的文本命令
# 输出：看Pt在CO氧化条件下的团簇结构
```

### 与InputHandler集成
```python
# InputHandler调用Speech2Text
speech_result = call_speech2text(audio_file)
if speech_result["confidence"] > 0.7:
    command = speech_result["text"]
    process_with_inputhandler(command)
else:
    ask_user_confirmation(speech_result)
```

### 实时语音处理
- 支持麦克风实时输入
- 流式识别（需要额外配置）
- 实时术语修正

## 配置选项

### 模型选择
```yaml
# 配置文件示例
speech2text:
  model: "tiny"           # tiny, base, small, medium, large
  language: "auto"        # auto, zh, en, etc.
  temperature: 0.0        # 随机性控制
  beam_size: 5            # 束搜索大小
  best_of: 5              # 候选结果数
```

### 术语修正配置
```yaml
term_correction:
  enable: true
  metals:
    - from: "铐"
      to: "Rh（铑）"
    - from: "钉"
      to: "Ru（钌）"
  units:
    - from: "度"
      to: "K"
      context: "temperature"
```

### 置信度阈值
```yaml
confidence:
  high_threshold: 0.7     # 高于此值直接使用
  medium_threshold: 0.4   # 低于此值询问用户
  low_threshold: 0.2      # 低于此值重新识别
```

## 性能优化

### 速度优化
1. **使用tiny模型**：最快，适合实时应用
2. **FP16禁用**：确保兼容性，避免CUDA问题
3. **批处理**：多个音频文件批量处理

### 准确性优化
1. **上下文增强**：利用MOSP任务上下文提高识别
2. **后处理修正**：基于规则的术语修正
3. **用户反馈学习**：记录修正历史，优化词典

### 内存优化
- tiny模型仅需~75MB内存
- 无需GPU即可运行
- 支持低资源环境

## 测试用例

### 单元测试
```python
def test_metal_correction():
    assert correct_term("铐") == "Rh（铑）"
    assert correct_term("钉") == "Ru（钌）"
    assert correct_term("白金") == "Pt（铂）"

def test_unit_conversion():
    assert convert_units("300度") == "300 K"
    assert convert_units("50埃") == "50 Å"
```

### 集成测试
```python
def test_full_pipeline():
    audio = "test_audio.wav"
    result = speech_to_text(audio)
    assert result["confidence"] > 0.6
    assert "MOSP" in result["text"] or "团簇" in result["text"]
```

## 故障排除

### 常见问题
1. **Whisper未安装**：
   ```
   错误：找不到whisper命令
   解决：brew install openai-whisper 或 pip install openai-whisper
   ```

2. **模型下载失败**：
   ```
   错误：无法下载tiny模型
   解决：手动下载并放入~/.cache/whisper/
   ```

3. **音频格式不支持**：
   ```
   错误：不支持的音频格式
   解决：使用ffmpeg转换格式：ffmpeg -i input.m4a output.wav
   ```

4. **内存不足**：
   ```
   错误：CUDA out of memory
   解决：使用tiny模型，禁用GPU：whisper --model tiny --device cpu
   ```

### 调试模式
```bash
# 启用详细日志
mosp-speech2text --audio test.wav --debug

# 输出中间结果
mosp-speech2text --audio test.wav --verbose
```

## 更新日志

### v1.0.0 (2026-04-07)
- 初始版本发布
- 基于OpenAI Whisper tiny模型
- 包含MOSP术语修正
- 支持中英文混合识别
- 低置信度用户确认机制

## 后续开发计划

### 短期计划
- [ ] 实时麦克风输入支持
- [ ] 更多MOSP术语扩充
- [ ] 用户自定义修正词典

### 中期计划
- [ ] 多语言混合识别优化
- [ ] 上下文感知增强
- [ ] 语音命令快捷方式

### 长期计划
- [ ] 自定义语音模型训练
- [ ] 声纹识别（用户识别）
- [ ] 情感分析（用户意图识别）

---

**使用提示**：对于科研计算场景，建议在安静环境下录音，清晰发音专业术语，可获得最佳识别效果。