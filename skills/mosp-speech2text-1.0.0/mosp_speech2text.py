#!/usr/bin/env python3
"""
MOSP Speech2Text Skill Implementation
语音识别技能，专门处理MOSP科研计算的语音输入
"""

import os
import sys
import json
import tempfile
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse

class MOSPSpeech2Text:
    """MOSP专用语音识别处理器"""
    
    def __init__(self, model: str = "tiny", language: str = "auto"):
        """
        初始化语音识别器
        
        Args:
            model: Whisper模型大小 (tiny, base, small, medium, large)
            language: 语言代码 (auto, zh, en, etc.)
        """
        self.model = model
        self.language = language
        self.whisper_cmd = self._find_whisper()
        
        # MOSP术语修正词典
        self.term_corrections = {
            # 金属元素谐音修正
            "铐": "Rh（铑）",
            "钉": "Ru（钌）",
            "白金": "Pt（铂）",
            "黄金": "Au（金）",
            "红铜": "Cu（铜）",
            "铁": "Fe（铁）",
            "钯": "Pd（钯）",
            "铑": "Rh（铑）",      # 直接映射
            "铂": "Pt（铂）",      # 直接映射
            "金": "Au（金）",      # 直接映射
            "铜": "Cu（铜）",      # 直接映射
            
            # 专业术语标准化
            "摩斯普": "MOSP",
            "莫斯普": "MOSP",
            "团族": "团簇",
            "团足": "团簇",
            "纳米团": "纳米团簇",
            "那米团簇": "纳米团簇",
            
            # 反应类型
            "一氧化碳氧化": "CO氧化",
            "水汽变换": "水汽变换反应",
            "水气变换": "水汽变换反应",
            "wgsr": "WGSR",
            "w g s r": "WGSR",
            
            # 计算类型
            "msr": "MSR",
            "kmc": "KMC",
            "蒙特卡洛": "KMC",
            "动力学": "KMC",
            
            # 结果类型
            "脱伏": "TOF",
            "覆盖度": "覆盖度",
            "活性": "反应活性",
        }
        
        # 单位转换
        self.unit_conversions = {
            "度": "K",
            "摄氏度": "K",
            "开尔文": "K",
            "埃": "Å",
            "angstrom": "Å",
            "大气压": "atm",
            "巴": "bar",
            "托": "Torr",
            "千帕": "kPa",
            "兆帕": "MPa",
        }
        
        # 上下文关键词（用于判断是否在MOSP上下文中）
        self.mosp_context_keywords = [
            "团簇", "纳米", "金属", "Pt", "Au", "Cu", "Fe", "Pd", "Rh", "Ru",
            "CO", "O2", "H2O", "H2", "CO2", "氧化", "反应", "吸附", "表面",
            "晶面", "温度", "压强", "分压", "MSR", "KMC", "MOSP"
        ]
    
    def _find_whisper(self) -> str:
        """查找whisper命令路径"""
        # 检查是否安装whisper
        try:
            subprocess.run(["whisper", "--version"], 
                         capture_output=True, check=False)
            return "whisper"
        except FileNotFoundError:
            # 尝试其他可能的路径
            possible_paths = [
                "/usr/local/bin/whisper",
                "/opt/homebrew/bin/whisper",
                os.path.expanduser("~/.local/bin/whisper"),
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return path
            
            raise RuntimeError(
                "未找到OpenAI Whisper CLI。请安装：\n"
                "  brew install openai-whisper\n"
                "  或 pip install openai-whisper"
            )
    
    def transcribe_audio(self, audio_path: str) -> Dict[str, any]:
        """
        使用Whisper转录音频
        
        Args:
            audio_path: 音频文件路径
            
        Returns:
            Dict包含转录文本和置信度信息
        """
        # 创建临时文件保存输出
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
            output_file = tmp.name
        
        try:
            # 构建whisper命令
            cmd = [
                self.whisper_cmd,
                audio_path,
                "--model", self.model,
                "--output_format", "txt",
                "--output_dir", os.path.dirname(output_file),
                "--fp16", "False",  # 确保兼容性
            ]
            
            if self.language != "auto":
                cmd.extend(["--language", self.language])
            
            # 运行whisper
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            # 读取转录结果
            transcript_file = output_file.replace('.txt', '.txt')
            if os.path.exists(transcript_file):
                with open(transcript_file, 'r', encoding='utf-8') as f:
                    transcript = f.read().strip()
            else:
                # 如果没有生成文件，使用标准输出
                transcript = result.stdout
            
            # 清理临时文件
            for ext in ['.txt', '.vtt', '.srt', '.tsv', '.json']:
                temp_file = output_file.replace('.txt', ext)
                if os.path.exists(temp_file):
                    try:
                        os.unlink(temp_file)
                    except:
                        pass
            
            # 提取置信度信息（简化版本）
            confidence = self._estimate_confidence(transcript, result.stderr)
            
            return {
                "text": transcript,
                "confidence": confidence,
                "raw_output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
                "success": result.returncode == 0
            }
            
        except Exception as e:
            return {
                "text": "",
                "confidence": 0.0,
                "error": str(e),
                "success": False
            }
        finally:
            # 清理临时文件
            if os.path.exists(output_file):
                try:
                    os.unlink(output_file)
                except:
                    pass
    
    def _estimate_confidence(self, transcript: str, stderr: str) -> float:
        """估计转录置信度（简化版本）"""
        if not transcript:
            return 0.0
        
        # 基于转录长度和内容的质量启发式评估
        confidence = 0.5  # 基础置信度
        
        # 1. 转录长度
        if len(transcript) > 10:
            confidence += 0.1
        
        # 2. 是否包含MOSP关键词
        mosp_keywords_found = 0
        for keyword in self.mosp_context_keywords:
            if keyword in transcript:
                mosp_keywords_found += 1
        
        if mosp_keywords_found > 0:
            confidence += min(0.3, mosp_keywords_found * 0.1)
        
        # 3. 检查是否有明显的识别问题标记
        problem_indicators = ["[", "]", "(不明)", "(听不清)", "***"]
        for indicator in problem_indicators:
            if indicator in transcript:
                confidence -= 0.2
        
        # 限制在0.0-1.0之间
        return max(0.0, min(1.0, confidence))
    
    def correct_mosp_terms(self, text: str) -> str:
        """
        对转录文本进行MOSP术语修正
        
        Args:
            text: 原始转录文本
            
        Returns:
            修正后的文本
        """
        if not text:
            return text
        
        corrected = text
        
        # 1. 术语替换
        for wrong, correct in self.term_corrections.items():
            corrected = corrected.replace(wrong, correct)
        
        # 2. 单位转换
        # 处理"300度" -> "300 K"
        corrected = re.sub(r'(\d+)\s*度', r'\1 K', corrected)
        
        # 处理"50埃" -> "50 Å"
        corrected = re.sub(r'(\d+)\s*埃', r'\1 Å', corrected)
        
        # 处理"1大气压" -> "1 atm"
        corrected = re.sub(r'(\d+)\s*大气压', r'\1 atm', corrected)
        
        # 处理其他单位
        for unit_from, unit_to in self.unit_conversions.items():
            if unit_from in ["度", "埃", "大气压"]:  # 已单独处理
                continue
            corrected = corrected.replace(unit_from, unit_to)
        
        # 3. 金属符号大写
        corrected = re.sub(r'\b(pt|au|cu|fe|pd|rh|ru)\b', lambda m: m.group(1).upper(), corrected, flags=re.IGNORECASE)
        
        # 4. 标准化命令格式
        # "我想看" -> "看"
        corrected = re.sub(r'^我想看', '看', corrected)
        corrected = re.sub(r'^我想计算', '计算', corrected)
        corrected = re.sub(r'^我想生成', '生成', corrected)
        corrected = re.sub(r'^我想', '', corrected)  # 通用处理
        
        # "run" -> "运行"
        corrected = re.sub(r'\brun\b', '运行', corrected, flags=re.IGNORECASE)
        
        # 5. 移除不必要的填充词
        filler_words = ["那个", "这个", "然后", "就是", "的话", "一下", "一个"]
        for word in filler_words:
            corrected = re.sub(r'\s+' + re.escape(word) + r'\s+', ' ', corrected)
            corrected = re.sub(r'^' + re.escape(word) + r'\s+', '', corrected)
            corrected = re.sub(r'\s+' + re.escape(word) + r'$', '', corrected)
        
        # 6. 移除重复的"簇"字
        corrected = re.sub(r'簇簇', '簇', corrected)
        
        return corrected.strip()
    
    def is_mosp_context(self, text: str) -> bool:
        """判断文本是否在MOSP上下文中"""
        if not text:
            return False
        
        text_lower = text.lower()
        for keyword in self.mosp_context_keywords:
            if keyword.lower() in text_lower:
                return True
        
        return False
    
    def format_for_inputhandler(self, text: str) -> str:
        """
        将文本格式化为适合InputHandler处理的命令
        
        Args:
            text: 修正后的文本
            
        Returns:
            格式化后的命令文本
        """
        if not text:
            return text
        
        # 确保以适当的动词开头
        commands = text
        
        # 如果是MOSP上下文，进一步优化格式
        if self.is_mosp_context(commands):
            # 确保命令清晰
            commands = re.sub(r'\s+', ' ', commands)  # 移除多余空格
            commands = commands.strip()
        
        return commands
    
    def process_audio(self, audio_path: str, min_confidence: float = 0.4) -> Dict[str, any]:
        """
        完整处理音频文件
        
        Args:
            audio_path: 音频文件路径
            min_confidence: 最小置信度阈值
            
        Returns:
            处理结果字典
        """
        # 1. 转录音频
        transcript_result = self.transcribe_audio(audio_path)
        
        if not transcript_result["success"]:
            return {
                "success": False,
                "error": transcript_result.get("error", "转录失败"),
                "needs_confirmation": False,
                "final_text": ""
            }
        
        raw_text = transcript_result["text"]
        confidence = transcript_result["confidence"]
        
        # 2. MOSP术语修正
        corrected_text = self.correct_mosp_terms(raw_text)
        
        # 3. 格式化命令
        formatted_text = self.format_for_inputhandler(corrected_text)
        
        # 4. 判断是否需要用户确认
        needs_confirmation = confidence < min_confidence
        
        return {
            "success": True,
            "raw_text": raw_text,
            "corrected_text": corrected_text,
            "formatted_text": formatted_text,
            "confidence": confidence,
            "needs_confirmation": needs_confirmation,
            "is_mosp_context": self.is_mosp_context(corrected_text),
            "final_text": formatted_text if confidence >= min_confidence else corrected_text
        }


def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description='MOSP Speech2Text 语音识别')
    parser.add_argument('audio_file', help='音频文件路径')
    parser.add_argument('--model', default='tiny', 
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper模型大小 (默认: tiny)')
    parser.add_argument('--language', default='auto', 
                       help='语言代码 (默认: auto)')
    parser.add_argument('--min-confidence', type=float, default=0.4,
                       help='最小置信度阈值 (默认: 0.4)')
    parser.add_argument('--output', choices=['text', 'json', 'full'], 
                       default='text', help='输出格式')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not os.path.exists(args.audio_file):
        print(f"错误：文件不存在 {args.audio_file}")
        sys.exit(1)
    
    # 创建处理器
    try:
        processor = MOSPSpeech2Text(model=args.model, language=args.language)
    except RuntimeError as e:
        print(f"初始化错误: {e}")
        sys.exit(1)
    
    # 处理音频
    result = processor.process_audio(args.audio_file, args.min_confidence)
    
    # 输出结果
    if args.output == 'text':
        if result['success']:
            if result['needs_confirmation']:
                print(f"# 识别结果（置信度较低，需要确认）")
                print(f"原始识别: {result['raw_text']}")
                print(f"建议修正: {result['corrected_text']}")
                print(f"最终命令: {result['final_text']}")
            else:
                print(result['final_text'])
        else:
            print(f"错误: {result.get('error', '未知错误')}")
    
    elif args.output == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.output == 'full':
        print("=" * 60)
        print("MOSP Speech2Text 处理结果")
        print("=" * 60)
        
        if result['success']:
            print(f"原始识别: {result['raw_text']}")
            print(f"修正后文本: {result['corrected_text']}")
            print(f"格式化命令: {result['formatted_text']}")
            print(f"置信度: {result['confidence']:.2f}")
            print(f"需要确认: {'是' if result['needs_confirmation'] else '否'}")
            print(f"MOSP上下文: {'是' if result['is_mosp_context'] else '否'}")
            print("-" * 60)
            print(f"最终输出: {result['final_text']}")
        else:
            print(f"处理失败: {result.get('error', '未知错误')}")
        
        print("=" * 60)
    
    # 设置退出码
    sys.exit(0 if result['success'] else 1)


if __name__ == "__main__":
    main()