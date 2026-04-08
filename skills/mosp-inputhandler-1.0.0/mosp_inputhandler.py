#!/usr/bin/env python3
"""
MOSP InputHandler Skill Implementation
总控技能，处理用户输入，检测关键词，协调调用其他技能
"""

import os
import sys
import re
import json
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import argparse

class MOSPInputHandler:
    """MOSP系统总控技能"""
    
    def __init__(self):
        """初始化输入处理器"""
        # 关键词词典
        self.keywords = {
            # 系统相关
            "system": ["团簇", "结构", "构型", "形貌", "纳米粒子", "金属", "晶面"],
            
            # 反应相关
            "reaction": ["一氧化碳氧化", "水汽变换", "一氧化碳", "CO氧化", "WGSR", "CO", "O₂", "H₂O", "H₂"],
            
            # 金属相关
            "metal": ["铂", "金", "铜", "铁", "钯", "铑", "钌", "Pt", "Au", "Cu", "Fe", "Pd", "Rh", "Ru"],
            
            # 条件相关
            "condition": ["环境", "气氛", "反应条件", "温度", "压强", "压力", "分压", "K", "Pa", "atm"],
            
            # 计算相关
            "calculation": ["MSR", "KMC", "MOSP", "动力学", "蒙特卡洛", "表面反应", "计算", "模拟"],
            
            # 结果相关
            "result": ["反应活性", "TOF", "覆盖度", "活性", "反应速率", "转化频率", "覆盖率", "活性图"],
            
            # 查询相关
            "query": ["查询", "查看", "检查", "参数", "图像", "图", "结果", "历史"],
            
            # 动作相关
            "action": ["看", "生成", "构造", "计算", "运行", "执行", "做", "弄", "搞"],
        }
        
        # 关键词权重
        self.keyword_weights = {
            # 高权重关键词（明确指示任务类型）
            "MSR": 2.0,
            "KMC": 2.0,
            "MOSP": 2.0,
            "TOF": 2.0,
            "查询": 1.8,
            "查看": 1.5,
            
            # 中权重关键词（强烈暗示）
            "团簇": 1.5,
            "结构": 1.5,
            "活性": 1.5,
            "参数": 1.5,
            "图像": 1.5,
            
            # 低权重关键词（一般指示）
            "金属": 1.2,
            "反应": 1.2,
            "温度": 1.2,
            "计算": 1.2,
        }
        
        # 任务类型检测模式
        self.task_patterns = {
            # MSR任务模式
            "MSR": [
                r'看.*(结构|团簇|构型)',
                r'生成.*(团簇|结构)',
                r'构造.*团簇',
                r'MSR.*(结构|团簇)',
                r'MOSP.*(结构|团簇)',
                r'(铂|金|铜|Pt|Au|Cu).*团簇',
                r'团簇.*(铂|金|铜|Pt|Au|Cu)',
            ],
            
            # KMC任务模式
            "KMC": [
                r'看.*(活性|TOF|覆盖度|反应速率)',
                r'计算.*(活性|TOF|覆盖度|反应速率)',
                r'运行.*KMC',
                r'KMC.*模拟',
                r'蒙特卡洛.*模拟',
                r'动力学.*模拟',
                r'TOF.*计算',
                r'覆盖度.*计算',
            ],
            
            # 查询参数任务模式
            "QUERY_PARAM": [
                r'查询.*参数',
                r'查看.*参数',
                r'参数.*是什么',
                r'参数.*怎么样',
                r'参数.*设置',
                r'MSR.*参数',
                r'KMC.*参数',
                r'输入.*参数',
                r'JSON.*参数',
                r'相互作用.*矩阵',
                r'表面.*数据',
                r'晶面.*参数',
                r'物种.*参数',
            ],
            
            # 查询图像任务模式
            "QUERY_IMAGE": [
                r'查看.*图像',
                r'看.*图',
                r'图像.*结果',
                r'结构.*图',
                r'性能.*图',
                r'覆盖.*图',
                r'TOF.*图',
                r'结构.*动画',
                r'旋转.*动图',
                r'团簇.*图',
                r'可视化.*结果',
                r'哪个.*任务.*图',
                r'哪一次.*计算.*结果',
                r'查看.*历史.*结果',
            ],
            
            # 联合任务模式
            "COMBINED": [
                r'先生成.*然后.*看.*活性',
                r'先.*MSR.*后.*KMC',
                r'结构.*活性',
                r'团簇.*反应',
            ]
        }
        
        # 预编译正则表达式
        self.compiled_patterns = {}
        for task_type, patterns in self.task_patterns.items():
            self.compiled_patterns[task_type] = [
                re.compile(pattern, re.IGNORECASE | re.UNICODE) 
                for pattern in patterns
            ]
        
        # 置信度阈值
        self.confidence_thresholds = {
            "high": 0.7,     # 高置信度，直接确认
            "medium": 0.4,   # 中置信度，询问用户
            "low": 0.2,      # 低置信度，需要详细信息
        }
    
    def detect_keywords(self, text: str) -> Dict[str, List[str]]:
        """
        检测文本中的关键词
        
        Args:
            text: 输入文本
            
        Returns:
            检测到的关键词分类字典
        """
        detected = {category: [] for category in self.keywords}
        
        for category, words in self.keywords.items():
            for word in words:
                # 忽略大小写匹配
                if re.search(rf'\b{re.escape(word)}\b', text, re.IGNORECASE | re.UNICODE):
                    detected[category].append(word)
        
        return detected
    
    def calculate_confidence(self, detected_keywords: Dict[str, List[str]]) -> float:
        """
        计算任务识别置信度
        
        Args:
            detected_keywords: 检测到的关键词
            
        Returns:
            置信度分数 (0.0-1.0)
        """
        if not detected_keywords:
            return 0.0
        
        total_weight = 0.0
        weighted_sum = 0.0
        
        # 计算所有关键词的权重
        for category, words in detected_keywords.items():
            for word in words:
                weight = self.keyword_weights.get(word, 1.0)
                weighted_sum += weight
                total_weight += 1.0
        
        if total_weight == 0:
            return 0.0
        
        # 基础置信度
        base_confidence = weighted_sum / total_weight / 2.0  # 归一化到0-1
        
        # 增强因素
        enhancement = 0.0
        
        # 1. 关键词多样性
        category_count = sum(1 for words in detected_keywords.values() if words)
        if category_count >= 3:
            enhancement += 0.2
        
        # 2. 关键任务词存在
        task_keywords = ["MSR", "KMC", "MOSP", "TOF", "查询", "查看"]
        if any(keyword in text for keyword in task_keywords for words in detected_keywords.values() for word in words):
            enhancement += 0.2
        
        # 3. 金属元素存在
        metal_keywords = ["铂", "金", "铜", "Pt", "Au", "Cu", "铁", "Fe", "钯", "Pd", "铑", "Rh", "钌", "Ru"]
        if any(keyword in text for keyword in metal_keywords for words in detected_keywords.values() for word in words):
            enhancement += 0.1
        
        # 最终置信度
        confidence = min(1.0, base_confidence + enhancement)
        
        return confidence
    
    def detect_task_type(self, text: str) -> Dict[str, Any]:
        """
        检测任务类型
        
        Args:
            text: 输入文本
            
        Returns:
            任务类型信息字典
        """
        # 检测关键词
        detected_keywords = self.detect_keywords(text)
        
        # 计算置信度
        confidence = self.calculate_confidence(detected_keywords)
        
        # 匹配任务模式
        matched_tasks = []
        for task_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(text):
                    matched_tasks.append(task_type)
                    break
        
        # 提取关键信息
        extracted_info = self.extract_info(text, detected_keywords)
        
        # 确定主要任务类型
        primary_task = self.determine_primary_task(matched_tasks, confidence, extracted_info)
        
        return {
            "text": text,
            "detected_keywords": detected_keywords,
            "matched_tasks": matched_tasks,
            "primary_task": primary_task,
            "confidence": confidence,
            "extracted_info": extracted_info,
            "needs_confirmation": confidence < self.confidence_thresholds["high"],
            "suggested_response": self.generate_suggested_response(primary_task, confidence, extracted_info),
        }
    
    def extract_info(self, text: str, detected_keywords: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        从文本中提取关键信息
        
        Args:
            text: 输入文本
            detected_keywords: 检测到的关键词
            
        Returns:
            提取的信息字典
        """
        info = {
            "metals": [],
            "gases": [],
            "temperatures": [],
            "pressures": [],
            "task_specific": {},
        }
        
        # 提取金属元素
        metal_patterns = [
            r'(铂|金|铜|铁|钯|铑|钌)',  # 中文名称
            r'\b(Pt|Au|Cu|Fe|Pd|Rh|Ru)\b',  # 英文符号
        ]
        
        for pattern in metal_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            info["metals"].extend([m.upper() if len(m) <= 2 else m for m in matches])
        
        # 去重
        info["metals"] = list(set(info["metals"]))
        
        # 提取气体
        gas_patterns = [
            r'CO\s*氧化',
            r'一氧化碳',
            r'水汽变换',
            r'WGSR',
            r'\bCO\b',
            r'\bO₂?\b',
            r'\bH₂?O\b',
            r'\bH₂?\b',
            r'\bCO₂?\b',
        ]
        
        for pattern in gas_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            info["gases"].extend(matches)
        
        # 提取温度
        temp_patterns = [
            r'(\d+)\s*度',
            r'(\d+)\s*K',
            r'温度\s*(\d+)',
            r'T\s*=\s*(\d+)',
        ]
        
        for pattern in temp_patterns:
            matches = re.findall(pattern, text)
            info["temperatures"].extend([int(m) for m in matches])
        
        # 提取压力
        pressure_patterns = [
            r'(\d+)\s*Pa',
            r'(\d+)\s*atm',
            r'(\d+)\s*大气压',
            r'压力\s*(\d+)',
            r'压强\s*(\d+)',
            r'P\s*=\s*(\d+)',
        ]
        
        for pattern in pressure_patterns:
            matches = re.findall(pattern, text)
            info["pressures"].extend([int(m) for m in matches])
        
        # 提取其他任务特定信息
        # MSR相关
        if any(word in text for word in ["半径", "尺寸", "大小"]):
            radius_match = re.search(r'半径\s*(\d+)\s*Å?', text)
            if radius_match:
                info["task_specific"]["radius"] = int(radius_match.group(1))
        
        # KMC相关
        if any(word in text for word in ["步数", "循环", "迭代"]):
            steps_match = re.search(r'步数\s*(\d+)', text)
            if steps_match:
                info["task_specific"]["nloop"] = int(steps_match.group(1))
        
        return info
    
    def determine_primary_task(self, matched_tasks: List[str], confidence: float, 
                              extracted_info: Dict[str, Any]) -> str:
        """
        确定主要任务类型
        
        Args:
            matched_tasks: 匹配的任务类型列表
            confidence: 置信度
            extracted_info: 提取的信息
            
        Returns:
            主要任务类型
        """
        if not matched_tasks:
            return "UNKNOWN"
        
        # 如果只匹配到一个任务，直接返回
        if len(matched_tasks) == 1:
            return matched_tasks[0]
        
        # 优先级：联合任务 > 查询任务 > 计算任务
        task_priority = {
            "COMBINED": 4,
            "QUERY_PARAM": 3,
            "QUERY_IMAGE": 3,
            "KMC": 2,
            "MSR": 1,
            "UNKNOWN": 0,
        }
        
        # 按优先级排序
        sorted_tasks = sorted(matched_tasks, key=lambda t: task_priority.get(t, 0), reverse=True)
        
        # 返回最高优先级的任务
        return sorted_tasks[0]
    
    def generate_suggested_response(self, task_type: str, confidence: float, 
                                   extracted_info: Dict[str, Any]) -> str:
        """
        生成建议的响应消息
        
        Args:
            task_type: 任务类型
            confidence: 置信度
            extracted_info: 提取的信息
            
        Returns:
            建议的响应消息
        """
        if confidence < self.confidence_thresholds["low"]:
            return "未识别到MOSP计算任务，请提供更详细的需求描述。"
        
        responses = {
            "MSR": "检测到您可能想进行MSR计算（生成团簇结构），是否继续？",
            "KMC": "检测到您可能想进行KMC计算（模拟反应动力学），是否继续？",
            "COMBINED": "检测到完整工作流需求（MSR生成结构 → KMC模拟动力学），是否继续？",
            "QUERY_PARAM": "检测到您想查询参数，请确认：1. 查询什么体系？2. 查MSR还是KMC参数？3. 查特定任务还是example参数？",
            "QUERY_IMAGE": "检测到您想查看图像，请确认：1. 查看哪个任务的图像？2. 查看什么类型的图像？",
            "UNKNOWN": "检测到MOSP相关需求，但任务类型不明确，请详细说明您的需求。",
        }
        
        base_response = responses.get(task_type, responses["UNKNOWN"])
        
        # 添加提取的信息
        info_parts = []
        
        if extracted_info["metals"]:
            info_parts.append(f"金属：{', '.join(extracted_info['metals'])}")
        
        if extracted_info["gases"]:
            info_parts.append(f"气体：{', '.join(extracted_info['gases'])}")
        
        if extracted_info["temperatures"]:
            info_parts.append(f"温度：{', '.join(map(str, extracted_info['temperatures']))}K")
        
        if extracted_info["pressures"]:
            info_parts.append(f"压力：{', '.join(map(str, extracted_info['pressures']))}Pa")
        
        if info_parts:
            info_text = "；".join(info_parts)
            return f"{base_response}\n\n识别到的信息：{info_text}"
        
        return base_response
    
    def process_input(self, text: str, auto_confirm: bool = False) -> Dict[str, Any]:
        """
        处理用户输入
        
        Args:
            text: 输入文本
            auto_confirm: 是否自动确认（用于测试）
            
        Returns:
            处理结果
        """
        # 检测任务
        task_info = self.detect_task_type(text)
        
        # 如果需要确认且未启用自动确认
        if task_info["needs_confirmation"] and not auto_confirm:
            return {
                "action": "ask_confirmation",
                "task_info": task_info,
                "message": task_info["suggested_response"],
            }
        
        # 准备执行任务
        return {
            "action": "execute_task",
            "task_info": task_info,
            "message": f"确认执行{task_info['primary_task']}任务",
            "next_steps": self.generate_next_steps(task_info),
        }
    
    def generate_next_steps(self, task_info: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        生成下一步行动建议
        
        Args:
            task_info: 任务信息
            
        Returns:
            下一步行动列表
        """
        task_type = task_info["primary_task"]
        extracted_info = task_info["extracted_info"]
        
        steps = []
        
        if task_type == "MSR":
            steps = [
                {"action": "call_inputfilemanager", "description": "调用InputFileManager处理MSR参数"},
                {"action": "call_msr_skill", "description": "调用MSR Skill执行计算"},
                {"action": "send_results", "description": "发送结果给用户"},
            ]
        
        elif task_type == "KMC":
            steps = [
                {"action": "call_inputfilemanager", "description": "调用InputFileManager处理KMC参数"},
                {"action": "find_structure", "description": "查找或生成初始结构"},
                {"action": "call_kmc_skill", "description": "调用KMC Skill执行计算"},
                {"action": "send_results", "description": "发送结果给用户"},
            ]
        
        elif task_type == "COMBINED":
            steps = [
                {"action": "call_inputfilemanager", "description": "调用InputFileManager处理参数"},
                {"action": "call_msr_skill", "description": "调用MSR Skill生成结构"},
                {"action": "call_kmc_skill", "description": "调用KMC Skill模拟动力学"},
                {"action": "send_results", "description": "发送完整结果给用户"},
            ]
        
        elif task_type in ["QUERY_PARAM", "QUERY_IMAGE"]:
            steps = [
                {"action": "call_inputfilemanager", "description": "调用InputFileManager查询信息"},
                {"action": "format_results", "description": "格式化查询结果"},
                {"action": "send_results", "description": "发送查询结果给用户"},
            ]
        
        return steps


def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description='MOSP InputHandler 总控技能')
    parser.add_argument('input', help='用户输入文本')
    parser.add_argument('--auto-confirm', action='store_true', help='自动确认任务')
    parser.add_argument('--output', choices=['text', 'json', 'full'], default='text', help='输出格式')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    
    args = parser.parse_args()
    
    # 创建处理器
    handler = MOSPInputHandler()
    
    # 处理输入
    result = handler.process_input(args.input, args.auto_confirm)
    
    # 输出结果
    if args.output == 'text':
        print(result["message"])
    
    elif args.output == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.output == 'full':
        print("=" * 60)
        print("MOSP InputHandler 处理结果")
        print("=" * 60)
        
        task_info = result["task_info"]
        
        print(f"输入文本: {task_info['text']}")
        print(f"主要任务: {task_info['primary_task']}")
        print(f"置信度: {task_info['confidence']:.2f}")
        print(f"需要确认: {task_info['needs_confirmation']}")
        
        print("\n检测到的关键词:")
        for category, words in task_info['detected_keywords'].items():
            if words:
                print(f"  {category}: {', '.join(words)}")
        
        print("\n提取的信息:")
        info = task_info['extracted_info']
        if info['metals']:
            print(f"  金属: {', '.join(info['metals'])}")
        if info['gases']:
            print(f"  气体: {', '.join(info['gases'])}")
        if info['temperatures']:
            print(f"  温度: {', '.join(map(str, info['temperatures']))}K")
        if info['pressures']:
            print(f"  压力: {', '.join(map(str, info['pressures']))}Pa")
        
        print(f"\n建议响应: {task_info['suggested_response']}")
        print(f"\n处理动作: {result['action']}")
        
        if 'next_steps' in result:
            print("\n下一步行动:")
            for i, step in enumerate(result['next_steps'], 1):
                print(f"  {i}. [{step['action']}] {step['description']}")
        
        print("=" * 60)
    
    # 设置退出码
    sys.exit(0 if task_info['confidence'] > 0.2 else 1)


if __name__ == "__main__":
    main()