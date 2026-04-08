# MOSP Speech2Text Skill

MOSP专用语音识别技能，用于处理科研计算领域的语音输入。

## 快速开始

### 安装依赖
```bash
# 安装OpenAI Whisper CLI
brew install openai-whisper
# 或
pip install openai-whisper
```

### 基本使用
```bash
# 转录音频文件
python mosp_speech2text.py audio.wav

# 使用不同模型
python mosp_speech2text.py audio.wav --model small

# 输出JSON格式
python mosp_speech2text.py audio.wav --output json

# 详细输出
python mosp_speech2text.py audio.wav --output full
```

### 在OpenClaw中使用
```python
from mosp_speech2text import MOSPSpeech2Text

# 创建处理器
processor = MOSPSpeech2Text(model="tiny")

# 处理音频
result = processor.process_audio("recording.wav")

if result["success"]:
    if result["needs_confirmation"]:
        print(f"需要确认: {result['corrected_text']}")
    else:
        print(f"识别结果: {result['final_text']}")
        # 传递给InputHandler Skill
        # input_handler.process(result['final_text'])
else:
    print(f"错误: {result['error']}")
```

## 功能特性

### 1. 语音识别
- 使用OpenAI Whisper tiny模型（快速、轻量）
- 支持中英文混合语音
- 自动语言检测

### 2. MOSP术语修正
- 金属元素谐音修正（"铐"→"Rh"，"钉"→"Ru"）
- 专业术语标准化
- 单位自动转换（"度"→"K"，"埃"→"Å"）

### 3. 智能处理
- 置信度评估
- 低置信度时询问用户确认
- 自动格式化命令

### 4. 与InputHandler集成
- 输出自然语言命令格式
- 直接传递给InputHandler Skill处理
- 保持MOSP任务上下文

## 使用示例

### 示例1：MSR任务
```bash
# 用户说："我想看铂在CO氧化气氛下的团簇结构"
python mosp_speech2text.py msp_task.wav

# 输出：
# 看Pt在CO氧化条件下的团簇结构
```

### 示例2：KMC任务
```bash
# 用户说："计算金一氧化碳氧化的反应活性"
python mosp_speech2text.py kmc_task.wav

# 输出：
# 计算Au在CO氧化条件下的反应活性
```

### 示例3：混合语言
```bash
# 用户说："我想run一个Pt CO oxidation的KMC simulation"
python mosp_speech2text.py mixed_task.wav

# 输出：
# 运行Pt-CO氧化反应的KMC模拟
```

## 配置选项

### 命令行参数
```bash
# 基本参数
--model tiny|base|small|medium|large    # 模型大小
--language auto|zh|en|...               # 语言代码
--min-confidence 0.4                    # 置信度阈值
--output text|json|full                 # 输出格式

# 示例
python mosp_speech2text.py audio.wav --model small --language zh --output json
```

### 程序化配置
```python
processor = MOSPSpeech2Text(
    model="tiny",        # 模型大小
    language="auto"      # 语言检测
)

result = processor.process_audio(
    "audio.wav",
    min_confidence=0.4   # 置信度阈值
)
```

## 测试

运行单元测试：
```bash
python test_mosp_speech2text.py
```

## 故障排除

### 常见问题

1. **Whisper未安装**
   ```
   错误：未找到OpenAI Whisper CLI
   解决：brew install openai-whisper 或 pip install openai-whisper
   ```

2. **音频格式不支持**
   ```
   错误：不支持的音频格式
   解决：使用ffmpeg转换：ffmpeg -i input.m4a output.wav
   ```

3. **内存不足**
   ```
   错误：CUDA out of memory
   解决：使用tiny模型：--model tiny
   ```

4. **识别准确率低**
   ```
   解决：
   - 在安静环境下录音
   - 清晰发音专业术语
   - 使用更大的模型：--model small 或 --model medium
   ```

### 调试模式
```bash
# 启用详细输出
python mosp_speech2text.py audio.wav --output full

# 检查中间结果
python mosp_speech2text.py audio.wav --debug
```

## 与MOSP系统集成

### 在技能链中使用
```
用户语音 → Speech2Text → 术语修正 → InputHandler → MSR/KMC计算
```

### 实时处理
```python
# 实时语音处理示例（概念）
import pyaudio
import wave
from mosp_speech2text import MOSPSpeech2Text

def record_and_process():
    processor = MOSPSpeech2Text()
    
    # 录制音频
    audio_data = record_audio(duration=5)
    
    # 保存到临时文件
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        save_audio(f.name, audio_data)
        result = processor.process_audio(f.name)
    
    return result
```

## 开发指南

### 扩展术语词典
```python
# 在代码中添加自定义术语
processor.term_corrections.update({
    "新术语": "正确术语",
    "另一个术语": "标准术语",
})

# 添加单位转换
processor.unit_conversions.update({
    "新单位": "标准单位",
})
```

### 添加新语言支持
```python
# 修改语言相关配置
processor = MOSPSpeech2Text(language="zh")  # 中文
# 或
processor = MOSPSpeech2Text(language="en")  # 英文
```

### 自定义置信度评估
```python
class CustomMOSPSpeech2Text(MOSPSpeech2Text):
    def _estimate_confidence(self, transcript: str, stderr: str) -> float:
        # 自定义置信度评估逻辑
        confidence = super()._estimate_confidence(transcript, stderr)
        # 添加自定义逻辑
        if "特定关键词" in transcript:
            confidence += 0.1
        return confidence
```

## 性能优化

### 速度优化
- 使用tiny模型（最快）
- 禁用GPU：`--fp16 False`
- 批量处理多个文件

### 准确性优化
- 使用medium或large模型
- 添加更多术语到修正词典
- 利用上下文信息

### 内存优化
- tiny模型仅需~75MB内存
- 可在CPU上运行
- 支持低资源环境

## 更新日志

### v1.0.0 (2026-04-07)
- 初始版本发布
- 基于OpenAI Whisper tiny模型
- 包含MOSP术语修正
- 支持中英文混合识别
- 低置信度用户确认机制

## 许可证

MIT License