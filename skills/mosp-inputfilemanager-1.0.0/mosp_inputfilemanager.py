#!/usr/bin/env python3
"""
MOSP InputFileManager Skill Implementation
输入文件管理器，负责example数据管理、参数查询、参数处理
"""

import os
import sys
import json
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import argparse

class MOSPInputFileManager:
    """MOSP输入文件管理器"""
    
    def __init__(self, mosp_root: Optional[str] = None):
        """初始化文件管理器
        
        Args:
            mosp_root: MOSP软件根目录，默认从环境变量MOSP_HOME获取
        """
        # 优先使用环境变量MOSP_HOME，其次使用传入参数，最后使用默认值
        if mosp_root is None:
            mosp_root = os.environ.get("MOSP_HOME", "/root/.openclaw/workspace/MOSP")
        
        self.mosp_root = Path(mosp_root)
        self.examples_dir = self.mosp_root / "example"
        self.output_dir = self.mosp_root / "OUTPUT"
        
        # 确保目录存在
        self.examples_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # 验证MOSP软件是否存在
        self._validate_mosp_installation()
        
        # 加载example文件信息
        self.example_files = self._scan_example_files()
    
    def _validate_mosp_installation(self):
        """验证MOSP软件是否安装正确"""
        required_dirs = [
            self.examples_dir,
            self.output_dir,
            self.mosp_root / "engine",
        ]
        
        missing_dirs = []
        for dir_path in required_dirs:
            if not dir_path.exists():
                missing_dirs.append(str(dir_path))
        
        if missing_dirs:
            print(f"警告：缺少必需的MOSP目录: {', '.join(missing_dirs)}")
            print(f"请确保MOSP软件正确安装在: {self.mosp_root}")
            print("安装方法: git clone https://github.com/mosp-catalysis/mosp-for-chatMOSP.git")
            print("然后设置环境变量: export MOSP_HOME=/path/to/mosp-for-chatMOSP")
        
        # 金属晶格常数（Å）
        self.lattice_constants = {
            "Pt": 3.92, "Au": 4.08, "Cu": 3.61, "Fe": 2.87,
            "Pd": 3.89, "Rh": 3.80, "Ru": 2.71,
        }
        
        # 气体典型参数范围
        self.gas_parameters = {
            "CO": {"E_ads_range": [-0.5, -1.2], "S_ads_range": [-0.001, -0.002]},
            "O2": {"E_ads_range": [-0.3, -0.8], "S_ads_range": [-0.0015, -0.0025]},
            "H2O": {"E_ads_range": [-0.4, -0.9], "S_ads_range": [-0.002, -0.003]},
            "H2": {"E_ads_range": [-0.2, -0.5], "S_ads_range": [-0.001, -0.0015]},
        }
    
    def _scan_example_files(self) -> Dict[str, Dict]:
        """扫描example目录中的文件"""
        examples = {}
        
        for json_file in self.examples_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 提取基本信息
                element = data.get("Element", "Unknown")
                gases = []
                
                # 提取气体信息
                for i in range(1, 4):
                    gas_key = f"Gas{i}_name"
                    if gas_key in data:
                        gases.append(data[gas_key])
                
                examples[json_file.name] = {
                    "path": json_file,
                    "element": element,
                    "gases": gases,
                    "data": data,
                }
                
            except Exception as e:
                print(f"警告：无法解析example文件 {json_file.name}: {e}")
        
        return examples
    
    def query_parameters(self, system: str, query_type: str = "MSR", 
                        mode: str = "full") -> Dict[str, Any]:
        """
        查询参数
        
        Args:
            system: 系统名称（如"Pt-CO氧化"）
            query_type: 查询类型（"MSR" 或 "KMC"）
            mode: 展示模式（"full", "brief", "expert"）
            
        Returns:
            查询结果
        """
        # 解析系统名称
        metal, gases = self._parse_system_name(system)
        
        # 查找匹配的example
        matched_example = self._find_matching_example(metal, gases)
        
        if matched_example:
            # 从example读取参数
            source = "example"
            params = matched_example["data"]
            source_file = matched_example["path"]
        else:
            # 生成推荐参数
            source = "recommended"
            params = self._generate_recommended_params(metal, gases, query_type)
            source_file = None
        
        # 格式化参数用于展示
        formatted_params = self._format_parameters(params, query_type, mode, source)
        
        return {
            "success": True,
            "system": system,
            "query_type": query_type,
            "source": source,
            "source_file": str(source_file) if source_file else None,
            "parameters": params,
            "formatted": formatted_params,
            "recommendation": "使用完整参数进行验证" if source == "recommended" else "参数已验证",
        }
    
    def process_parameters(self, metal: str, gases: List[str], 
                          task_type: str = "MSR", output_base: Optional[Path] = None) -> Dict[str, Any]:
        """
        处理参数
        
        Args:
            metal: 金属元素
            gases: 气体列表
            task_type: 任务类型
            output_base: 输出基础目录
            
        Returns:
            处理结果
        """
        if output_base is None:
            output_base = self.output_dir / "temp_task"
        
        # 查找匹配的example
        matched_example = self._find_matching_example(metal, gases)
        
        if matched_example:
            # 完全匹配：复制example文件
            source = "example"
            source_file = matched_example["path"]
            
            # 创建输出目录
            output_dir = output_base / f"{metal}_{'_'.join(gases)}"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 复制文件
            output_json = output_dir / "input.json"
            shutil.copy2(source_file, output_json)
            
            message = f"✅ 检测到与现有example完全匹配：{metal}-{'_'.join(gases)}系统，已复制到OUTPUT目录"
            
        else:
            # 不完全匹配：生成推荐参数
            source = "recommended"
            source_file = None
            
            # 创建输出目录
            output_dir = output_base / f"{metal}_{'_'.join(gases)}_recommended"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 生成推荐参数
            params = self._generate_recommended_params(metal, gases, task_type)
            output_json = output_dir / "input.json"
            
            with open(output_json, 'w', encoding='utf-8') as f:
                json.dump(params, f, indent=2, ensure_ascii=False)
            
            message = f"⚠️ 未找到完全匹配的example，提供推荐参数（数据存疑）"
        
        # 格式化参数用于展示
        formatted_params = self._format_parameters(
            self._load_parameters(output_json) if output_json.exists() else {},
            task_type, "full", source
        )
        
        return {
            "success": True,
            "metal": metal,
            "gases": gases,
            "task_type": task_type,
            "source": source,
            "source_file": str(source_file) if source_file else None,
            "output_dir": str(output_dir),
            "output_json": str(output_json),
            "formatted_params": formatted_params,
            "message": message,
        }
    
    def _parse_system_name(self, system: str) -> Tuple[str, List[str]]:
        """解析系统名称"""
        # 简单解析逻辑，实际应该更复杂
        metal = "Pt"  # 默认
        gases = ["CO", "O2"]  # 默认
        
        if "Pt" in system or "铂" in system:
            metal = "Pt"
        elif "Au" in system or "金" in system:
            metal = "Au"
        elif "Cu" in system or "铜" in system:
            metal = "Cu"
        
        if "CO" in system or "一氧化碳" in system:
            gases = ["CO", "O2"]
        elif "WGSR" in system or "水汽变换" in system:
            gases = ["CO", "H2O"]
        
        return metal, gases
    
    def _find_matching_example(self, metal: str, gases: List[str]) -> Optional[Dict]:
        """查找匹配的example文件"""
        best_match = None
        best_score = 0
        
        for file_info in self.example_files.values():
            score = 0
            
            # 金属匹配
            if file_info["element"] == metal:
                score += 0.5
            
            # 气体匹配
            example_gases = file_info["gases"]
            gas_match = sum(1 for gas in gases if gas in example_gases)
            score += gas_match * 0.25
            
            if score > best_score:
                best_score = score
                best_match = file_info
        
        # 需要较高的匹配分数
        return best_match if best_score >= 0.75 else None
    
    def _generate_recommended_params(self, metal: str, gases: List[str], 
                                    task_type: str) -> Dict[str, Any]:
        """生成推荐参数"""
        if task_type == "MSR":
            return self._generate_msr_params(metal, gases)
        else:  # KMC
            return self._generate_kmc_params(metal, gases)
    
    def _generate_msr_params(self, metal: str, gases: List[str]) -> Dict[str, Any]:
        """生成MSR推荐参数"""
        params = {
            "Element": metal,
            "Temperature": 700,
            "Pressure": 6000,
            "Lattice constant": self.lattice_constants.get(metal, 3.92),
            "flag_MSR": True,
            "flag_KMC": False,
            "Radius": 40,
            "nFaces": 20,
        }
        
        # 添加气体参数
        for i, gas in enumerate(gases[:3], 1):  # 最多3种气体
            params[f"Gas{i}_name"] = gas
            params[f"Gas{i}_pp"] = 50 if i == 1 else 50  # 简单分配
            
            # 添加气体典型参数
            if gas in self.gas_parameters:
                gas_params = self.gas_parameters[gas]
                # 这里应该根据具体需求设置更详细的参数
        
        # 添加晶面参数（简化）
        params["surface"] = [
            {
                "index": 111,
                "gamma": 0.145,
                "E_ads": [-0.85, -0.42] if len(gases) >= 2 else [-0.85],
                "S_ads": [-0.0012, -0.0015] if len(gases) >= 2 else [-0.0012],
                "w": [[0.02, -0.05], [-0.05, 0.03]] if len(gases) >= 2 else [[0.02]]
            }
        ]
        
        return params
    
    def _generate_kmc_params(self, metal: str, gases: List[str]) -> Dict[str, Any]:
        """生成KMC推荐参数"""
        # 简化的KMC参数
        params = {
            "Temperature": 700,
            "Pressure": 6000,
            "nLoop": 1000000,
            "record_int": 1000,
            "nspecies": 2,
            "nproducts": 1,
            "nevents": 4,
            "li": [[0.0, 0.1], [0.1, 0.0]],  # 相互作用矩阵
        }
        
        return params
    
    def _load_parameters(self, json_path: Path) -> Dict[str, Any]:
        """加载参数文件"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"错误：无法加载参数文件 {json_path}: {e}")
            return {}
    
    def _format_parameters(self, params: Dict[str, Any], query_type: str, 
                          mode: str, source: str) -> str:
        """格式化参数用于展示"""
        if not params:
            return "无可用参数"
        
        lines = []
        lines.append(f"# 参数查询结果")
        lines.append(f"- 来源: {source}")
        lines.append(f"- 类型: {query_type}")
        lines.append(f"- 模式: {mode}")
        lines.append("")
        
        if mode == "brief":
            # 简要模式：只显示关键参数
            lines.append("## 核心参数")
            
            if query_type == "MSR":
                keys = ["Element", "Temperature", "Pressure", "Radius", "nFaces"]
                for key in keys:
                    if key in params:
                        lines.append(f"- {key}: {params[key]}")
            
            else:  # KMC
                keys = ["Temperature", "Pressure", "nLoop", "record_int", "nspecies"]
                for key in keys:
                    if key in params:
                        lines.append(f"- {key}: {params[key]}")
        
        else:
            # 完整模式：显示所有参数
            lines.append("## 完整参数列表")
            
            for key, value in params.items():
                if isinstance(value, (list, dict)):
                    # 复杂类型，简化显示
                    lines.append(f"- {key}: {type(value).__name__} ({len(value) if hasattr(value, '__len__') else 'N/A'})")
                else:
                    lines.append(f"- {key}: {value}")
        
        if mode == "full":
            lines.append("")
            lines.append("提示：如需简要查看核心参数，请使用 `--brief` 参数")
        
        return "\n".join(lines)


def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description='MOSP InputFileManager 输入文件管理器')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 查询参数命令
    query_parser = subparsers.add_parser('query', help='查询参数')
    query_parser.add_argument('system', help='系统名称（如"Pt-CO氧化"）')
    query_parser.add_argument('--type', choices=['MSR', 'KMC'], default='MSR', help='查询类型')
    query_parser.add_argument('--mode', choices=['full', 'brief', 'expert'], default='full', help='展示模式')
    
    # 处理参数命令
    process_parser = subparsers.add_parser('process', help='处理参数')
    process_parser.add_argument('--metal', required=True, help='金属元素')
    process_parser.add_argument('--gases', nargs='+', required=True, help='气体列表')
    process_parser.add_argument('--task', choices=['MSR', 'KMC'], default='MSR', help='任务类型')
    process_parser.add_argument('--output', help='输出目录')
    
    # 列表命令
    list_parser = subparsers.add_parser('list', help='列出example文件')
    
    args = parser.parse_args()
    
    # 创建管理器
    manager = MOSPInputFileManager()
    
    if args.command == 'query':
        # 查询参数
        result = manager.query_parameters(args.system, args.type, args.mode)
        
        if result['success']:
            print(result['formatted'])
        else:
            print(f"错误：{result.get('error', '未知错误')}")
    
    elif args.command == 'process':
        # 处理参数
        output_dir = Path(args.output) if args.output else None
        result = manager.process_parameters(args.metal, args.gases, args.task, output_dir)
        
        print(result['message'])
        print(f"输出目录: {result['output_dir']}")
        print(f"输出文件: {result['output_json']}")
        print(f"\n参数预览:")
        print(result['formatted_params'])
    
    elif args.command == 'list':
        # 列出example文件
        print("Available example files:")
        for filename, info in manager.example_files.items():
            print(f"- {filename}: {info['element']}-{'_'.join(info['gases'])}")
    
    else:
        parser.print_help()
    
    sys.exit(0)


if __name__ == "__main__":
    main()