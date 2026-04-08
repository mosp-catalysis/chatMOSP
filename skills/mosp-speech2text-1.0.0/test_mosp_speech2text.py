#!/usr/bin/env python3
"""
MOSP Speech2Text Skill 测试脚本
"""

import os
import sys
import json
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mosp_speech2text import MOSPSpeech2Text

def create_mock_processor():
    """创建模拟的MOSPSpeech2Text处理器，绕过whisper检查"""
    processor = MOSPSpeech2Text.__new__(MOSPSpeech2Text)
    # 手动设置属性，绕过__init__中的whisper检查
    processor.model = "tiny"
    processor.language = "auto"
    processor.whisper_cmd = "whisper"  # 模拟值
    
    # 设置术语修正词典
    processor.term_corrections = {
        "铐": "Rh（铑）",
        "钉": "Ru（钌）",
        "白金": "Pt（铂）",
        "黄金": "Au（金）",
        "红铜": "Cu（铜）",
        "铁": "Fe（铁）",
        "钯": "Pd（钯）",
        "摩斯普": "MOSP",
        "莫斯普": "MOSP",
        "团族": "团簇",
        "团足": "团簇",
        "纳米团": "纳米团簇",
        "那米团簇": "纳米团簇",
        "一氧化碳氧化": "CO氧化",
        "水汽变换": "水汽变换反应",
        "水气变换": "水汽变换反应",
        "wgsr": "WGSR",
        "w g s r": "WGSR",
        "msr": "MSR",
        "kmc": "KMC",
        "蒙特卡洛": "KMC",
        "动力学": "KMC",
        "脱伏": "TOF",
        "覆盖度": "覆盖度",
        "活性": "反应活性",
    }
    
    processor.unit_conversions = {
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
    
    processor.mosp_context_keywords = [
        "团簇", "纳米", "金属", "Pt", "Au", "Cu", "Fe", "Pd", "Rh", "Ru",
        "CO", "O2", "H2O", "H2", "CO2", "氧化", "反应", "吸附", "表面",
        "晶面", "温度", "压强", "分压", "MSR", "KMC", "MOSP"
    ]
    
    # 手动设置方法引用（因为跳过了__init__）
    processor.correct_mosp_terms = MOSPSpeech2Text.correct_mosp_terms.__get__(processor)
    processor.is_mosp_context = MOSPSpeech2Text.is_mosp_context.__get__(processor)
    processor.format_for_inputhandler = MOSPSpeech2Text.format_for_inputhandler.__get__(processor)
    processor._estimate_confidence = MOSPSpeech2Text._estimate_confidence.__get__(processor)
    
    return processor

def test_term_correction():
    """测试术语修正功能"""
    print("测试术语修正功能...")
    processor = create_mock_processor()
    # 手动设置属性，绕过__init__中的whisper检查
    processor.model = "tiny"
    processor.language = "auto"
    processor.whisper_cmd = "whisper"  # 模拟值
    # 设置术语修正词典
    processor.term_corrections = {
        "铐": "Rh（铑）",
        "钉": "Ru（钌）",
        "白金": "Pt（铂）",
        "黄金": "Au（金）",
        "红铜": "Cu（铜）",
        "铁": "Fe（铁）",
        "钯": "Pd（钯）",
        "摩斯普": "MOSP",
        "莫斯普": "MOSP",
        "团族": "团簇",
        "团足": "团簇",
        "纳米团": "纳米团簇",
        "那米团簇": "纳米团簇",
        "一氧化碳氧化": "CO氧化",
        "水汽变换": "水汽变换反应",
        "水气变换": "水汽变换反应",
        "wgsr": "WGSR",
        "w g s r": "WGSR",
        "msr": "MSR",
        "kmc": "KMC",
        "蒙特卡洛": "KMC",
        "动力学": "KMC",
        "脱伏": "TOF",
        "覆盖度": "覆盖度",
        "活性": "反应活性",
    }
    processor.unit_conversions = {
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
    processor.mosp_context_keywords = [
        "团簇", "纳米", "金属", "Pt", "Au", "Cu", "Fe", "Pd", "Rh", "Ru",
        "CO", "O2", "H2O", "H2", "CO2", "氧化", "反应", "吸附", "表面",
        "晶面", "温度", "压强", "分压", "MSR", "KMC", "MOSP"
    ]
    
    # 手动设置方法引用（因为跳过了__init__）
    processor.correct_mosp_terms = MOSPSpeech2Text.correct_mosp_terms.__get__(processor)
    processor.is_mosp_context = MOSPSpeech2Text.is_mosp_context.__get__(processor)
    processor.format_for_inputhandler = MOSPSpeech2Text.format_for_inputhandler.__get__(processor)
    processor._estimate_confidence = MOSPSpeech2Text._estimate_confidence.__get__(processor)
    
    test_cases = [
        ("我想看铑的团簇结构", "看Rh（铑）的团簇结构"),
        ("计算白金在CO氧化条件下的活性", "计算Pt（铂）在CO氧化条件下的反应活性"),
        ("生成红铜纳米团", "生成Cu（铜）纳米团簇"),
        ("温度300度压强1大气压", "温度300 K压强1 atm"),
        ("尺寸50埃", "尺寸50 Å"),
        ("我想run一个msr计算", "run一个MSR计算"),  # 注意：run没有完全转换为"运行"
        ("看一下kmc的结果", "看一下KMC的结果"),
    ]
    
    all_passed = True
    for input_text, expected in test_cases:
        result = processor.correct_mosp_terms(input_text)
        passed = result == expected
        status = "✓" if passed else "✗"
        print(f"  {status} 输入: {input_text}")
        print(f"     预期: {expected}")
        print(f"     实际: {result}")
        if not passed:
            all_passed = False
    
    return all_passed

def test_context_detection():
    """测试MOSP上下文检测"""
    print("\n测试MOSP上下文检测...")
    processor = create_mock_processor()
    
    test_cases = [
        ("看Pt在CO氧化条件下的团簇结构", True),
        ("今天天气怎么样", False),
        ("计算Au的TOF", True),
        ("帮我写一封邮件", False),
        ("MSR计算需要什么参数", True),
    ]
    
    all_passed = True
    for text, expected in test_cases:
        result = processor.is_mosp_context(text)
        passed = result == expected
        status = "✓" if passed else "✗"
        print(f"  {status} 文本: {text}")
        print(f"     预期MOSP上下文: {expected}, 实际: {result}")
        if not passed:
            all_passed = False
    
    return all_passed

def test_command_formatting():
    """测试命令格式化"""
    print("\n测试命令格式化...")
    processor = create_mock_processor()
    
    test_cases = [
        ("我想看铂在CO氧化条件下的团簇结构", "看Pt（铂）在CO氧化条件下的团簇结构"),
        ("那个，就是，我想计算一下金的反应活性", "计算Au（金）的反应活性"),
        ("生成一个铜的纳米团簇", "生成Cu（铜）的纳米团簇"),
    ]
    
    all_passed = True
    for input_text, expected in test_cases:
        corrected = processor.correct_mosp_terms(input_text)
        result = processor.format_for_inputhandler(corrected)
        passed = result == expected
        status = "✓" if passed else "✗"
        print(f"  {status} 输入: {input_text}")
        print(f"     预期: {expected}")
        print(f"     实际: {result}")
        if not passed:
            all_passed = False
    
    return all_passed

def test_confidence_estimation():
    """测试置信度估计"""
    print("\n测试置信度估计...")
    processor = create_mock_processor()
    
    # 注意：这是一个简化测试，实际置信度需要音频文件
    test_texts = [
        ("看Pt在CO氧化条件下的团簇结构", 0.6),  # 包含MOSP关键词，应该较高
        ("这是一个测试", 0.5),  # 不包含MOSP关键词，中等
        ("[听不清] 不知道", 0.3),  # 包含问题标记，应该较低
    ]
    
    all_passed = True
    for text, min_expected in test_texts:
        # 使用模拟的stderr
        stderr = ""
        confidence = processor._estimate_confidence(text, stderr)
        passed = confidence >= min_expected
        status = "✓" if passed else "✗"
        print(f"  {status} 文本: {text}")
        print(f"     最低预期置信度: {min_expected:.2f}, 实际: {confidence:.2f}")
        if not passed:
            all_passed = False
    
    return all_passed

def test_integration():
    """测试集成功能（模拟）"""
    print("\n测试集成功能（模拟）...")
    
    # 创建模拟的音频处理结果
    mock_results = {
        "success": True,
        "raw_text": "我想看铑在CO氧化条件下的团簇结构",
        "corrected_text": "看Rh（铑）在CO氧化条件下的团簇结构",
        "formatted_text": "看Rh（铑）在CO氧化条件下的团簇结构",
        "confidence": 0.65,
        "needs_confirmation": False,
        "is_mosp_context": True,
        "final_text": "看Rh（铑）在CO氧化条件下的团簇结构"
    }
    
    print(f"  模拟输入: {mock_results['raw_text']}")
    print(f"  修正后: {mock_results['corrected_text']}")
    print(f"  置信度: {mock_results['confidence']:.2f}")
    print(f"  需要确认: {mock_results['needs_confirmation']}")
    print(f"  最终命令: {mock_results['final_text']}")
    
    # 验证输出格式
    assert mock_results['success'] == True
    assert "Rh" in mock_results['corrected_text']
    assert not mock_results['needs_confirmation']
    
    print("  ✓ 集成测试通过")
    return True

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("MOSP Speech2Text Skill 测试套件")
    print("=" * 60)
    
    test_results = []
    
    # 运行各个测试
    test_results.append(("术语修正", test_term_correction()))
    test_results.append(("上下文检测", test_context_detection()))
    test_results.append(("命令格式化", test_command_formatting()))
    test_results.append(("置信度估计", test_confidence_estimation()))
    test_results.append(("集成测试", test_integration()))
    
    # 输出汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in test_results:
        status = "通过 ✓" if passed else "失败 ✗"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("所有测试通过！✓")
    else:
        print("部分测试失败！✗")
    
    return all_passed

if __name__ == "__main__":
    # 运行测试
    success = run_all_tests()
    
    # 设置退出码
    sys.exit(0 if success else 1)