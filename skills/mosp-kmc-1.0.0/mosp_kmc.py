#!/usr/bin/env python3
"""
MOSP KMC Skill Implementation
动力学模拟技能，执行KMC（Kinetic Monte Carlo）计算
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import argparse

class MOSPKMCSkill:
    """MOSP KMC技能"""
    
    def __init__(self, mosp_root: Optional[str] = None):
        """初始化KMC技能
        
        Args:
            mosp_root: MOSP软件根目录，默认从环境变量MOSP_HOME获取
        """
        # 优先使用环境变量MOSP_HOME，其次使用传入参数，最后使用默认值
        if mosp_root is None:
            mosp_root = os.environ.get("MOSP_HOME", "/root/.openclaw/workspace/MOSP")
        
        self.mosp_root = Path(mosp_root)
        self.output_dir = self.mosp_root / "OUTPUT"
        
        # 确保目录存在
        self.output_dir.mkdir(exist_ok=True)
        
        # 验证MOSP软件是否存在
        self._validate_mosp_installation()
    
    def _validate_mosp_installation(self):
        """验证MOSP软件是否安装正确"""
        required_files = [
            self.mosp_root / "kmc_standalone.py",
            self.mosp_root / "engine" / "main.exe",
        ]
        
        missing_files = []
        for file_path in required_files:
            if not file_path.exists():
                missing_files.append(str(file_path))
        
        if missing_files:
            print(f"警告：缺少必需的MOSP文件: {', '.join(missing_files)}")
            print(f"请确保MOSP软件正确安装在: {self.mosp_root}")
            print("安装方法: git clone https://github.com/mosp-catalysis/mosp-for-chatMOSP.git")
            print("然后设置环境变量: export MOSP_HOME=/path/to/mosp-for-chatMOSP")
    
    def run_kmc_calculation(self, json_file: Path, xyz_file: Path, 
                           output_base: Optional[Path] = None) -> Dict[str, Any]:
        """
        运行KMC计算
        
        Args:
            json_file: 输入JSON参数文件
            xyz_file: 输入XYZ结构文件
            output_base: 输出基础目录
            
        Returns:
            计算结果
        """
        # 验证输入文件
        if not json_file.exists():
            return {"success": False, "error": f"JSON文件不存在: {json_file}"}
        
        if not xyz_file.exists():
            return {"success": False, "error": f"XYZ文件不存在: {xyz_file}"}
        
        # 加载参数
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                params = json.load(f)
        except Exception as e:
            return {"success": False, "error": f"无法加载JSON参数: {str(e)}"}
        
        # 创建输出目录
        output_dir = self._create_kmc_directory(params, output_base)
        
        # 准备文件
        kmc_input_json = output_dir / "kmc_input.json"
        kmc_ini_xyz = output_dir / "kmc_ini.xyz"
        
        try:
            shutil.copy(json_file, kmc_input_json)
            shutil.copy(xyz_file, kmc_ini_xyz)
        except Exception as e:
            return {"success": False, "error": f"文件复制失败: {str(e)}"}
        
        # 运行KMC计算
        result = self._execute_kmc_calculation(kmc_input_json, kmc_ini_xyz, output_dir)
        
        # 处理结果
        if result["success"]:
            result["output_dir"] = str(output_dir)
            result["kmc_input"] = str(kmc_input_json)
            result["kmc_structure"] = str(kmc_ini_xyz)
        
        return result
    
    def _create_kmc_directory(self, params: Dict, output_base: Optional[Path]) -> Path:
        """创建KMC输出目录"""
        # 从参数中提取信息用于目录命名
        element = params.get("Element", "Unknown")
        temperature = params.get("Temperature", "300K")
        pressure = params.get("Pressure", "101325Pa")
        
        # 提取气体信息
        kmc_params = params.get("KMC", {})
        species = kmc_params.get("Species", [])
        
        # 构建目录名
        gas_info = []
        for specie in species:
            if isinstance(specie, dict):
                name = specie.get("Name", "")
                partial_pressure = specie.get("Partial pressure", "")
                if name and partial_pressure:
                    gas_info.append(f"{name}{partial_pressure}")
        
        # 从KMC参数获取步数
        events = kmc_params.get("Events", [])
        total_steps = 0
        for event in events:
            if isinstance(event, dict):
                steps = event.get("nSteps", 0)
                if isinstance(steps, (int, float)):
                    total_steps += steps
        
        # 创建目录名
        dir_name = f"KMC_{temperature}_{pressure}"
        if gas_info:
            dir_name += "_" + "_".join(gas_info)
        if total_steps > 0:
            dir_name += f"_{total_steps}steps"
        
        # 确定输出目录
        if output_base:
            output_dir = output_base / dir_name
        else:
            output_dir = self.output_dir / dir_name
        
        # 处理目录重名
        counter = 1
        original_dir = output_dir
        while output_dir.exists():
            output_dir = original_dir.parent / f"{original_dir.name}_{counter}"
            counter += 1
        
        # 创建目录
        output_dir.mkdir(parents=True, exist_ok=True)
        
        return output_dir
    
    def _execute_kmc_calculation(self, json_file: Path, xyz_file: Path, 
                               output_dir: Path) -> Dict[str, Any]:
        """执行KMC计算"""
        # 构建命令
        kmc_script = self.mosp_root / "kmc_standalone.py"
        
        cmd = [
            "python3", str(kmc_script),
            "--json", str(json_file),
            "--xyz", str(xyz_file),
            "--out-dir", str(output_dir),
        ]
        
        # 执行计算
        try:
            print(f"执行KMC计算: {' '.join(cmd)}")
            
            # 检查是否需要后台运行（基于步数）
            nloop = self._extract_nloop_from_json(json_file)
            
            if nloop > 100000:
                # 后台运行
                log_file = output_dir / "kmc_run.log"
                full_cmd = cmd + ["2>&1"]
                with open(log_file, 'w') as log:
                    process = subprocess.Popen(
                        " ".join(full_cmd),
                        shell=True,
                        stdout=log,
                        stderr=subprocess.STDOUT,
                        cwd=output_dir
                    )
                
                return {
                    "success": True,
                    "pid": process.pid,
                    "log_file": str(log_file),
                    "message": f"KMC计算已后台启动 (PID: {process.pid})",
                    "status": "running"
                }
            else:
                # 前台运行
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd=output_dir
                )
                
                if result.returncode == 0:
                    return {
                        "success": True,
                        "output": result.stdout,
                        "message": "KMC计算完成",
                        "status": "completed"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"KMC计算失败 (退出码: {result.returncode})",
                        "stderr": result.stderr,
                        "stdout": result.stdout
                    }
                    
        except Exception as e:
            return {
                "success": False,
                "error": f"执行KMC计算时出错: {str(e)}"
            }
    
    def _extract_nloop_from_json(self, json_file: Path) -> int:
        """从JSON文件中提取总步数"""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            kmc_params = data.get("KMC", {})
            events = kmc_params.get("Events", [])
            
            total_steps = 0
            for event in events:
                if isinstance(event, dict):
                    steps = event.get("nSteps", 0)
                    if isinstance(steps, (int, float)):
                        total_steps += steps
            
            return total_steps
        except:
            return 0
    
    def process_kmc_results(self, output_dir: Path) -> Dict[str, Any]:
        """处理KMC计算结果"""
        if not output_dir.exists():
            return {"success": False, "error": f"输出目录不存在: {output_dir}"}
        
        result_files = []
        data_files = []
        image_files = []
        
        # 查找结果文件
        for file_path in output_dir.iterdir():
            if file_path.is_file():
                file_name = file_path.name
                
                if file_name.endswith('.data'):
                    data_files.append(str(file_name))
                elif file_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    image_files.append(str(file_name))
                elif file_name.endswith('.log'):
                    result_files.append(str(file_name))
        
        return {
            "success": True,
            "output_dir": str(output_dir),
            "data_files": data_files,
            "image_files": image_files,
            "log_files": result_files,
            "message": f"找到 {len(data_files)} 个数据文件, {len(image_files)} 个图像文件"
        }


def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description='MOSP KMC Skill 动力学模拟')
    parser.add_argument('--json', required=True, help='输入JSON参数文件')
    parser.add_argument('--xyz', required=True, help='输入XYZ结构文件')
    parser.add_argument('--output', help='输出目录（可选）')
    parser.add_argument('--process', action='store_true', help='只处理已有结果')
    parser.add_argument('--dir', help='要处理的KMC结果目录')
    
    args = parser.parse_args()
    
    # 创建KMC技能
    kmc = MOSPKMCSkill()
    
    if args.process:
        # 处理已有结果
        if not args.dir:
            print("错误：处理模式需要 --dir 参数")
            sys.exit(1)
        
        result = kmc.process_kmc_results(Path(args.dir))
        if result["success"]:
            print(f"KMC结果处理完成: {result['message']}")
            print(f"数据文件: {', '.join(result['data_files'])}")
            print(f"图像文件: {', '.join(result['image_files'])}")
        else:
            print(f"错误: {result['error']}")
            sys.exit(1)
    else:
        # 运行KMC计算
        json_file = Path(args.json)
        xyz_file = Path(args.xyz)
        
        if not json_file.exists():
            print(f"错误：JSON文件不存在 {args.json}")
            sys.exit(1)
        
        if not xyz_file.exists():
            print(f"错误：XYZ文件不存在 {args.xyz}")
            sys.exit(1)
        
        output_base = Path(args.output) if args.output else None
        result = kmc.run_kmc_calculation(json_file, xyz_file, output_base)
        
        if result["success"]:
            print(f"KMC计算成功: {result['message']}")
            if "output_dir" in result:
                print(f"输出目录: {result['output_dir']}")
            if "pid" in result:
                print(f"后台进程ID: {result['pid']}")
                print(f"日志文件: {result['log_file']}")
        else:
            print(f"KMC计算失败: {result['error']}")
            if "stderr" in result:
                print(f"错误输出: {result['stderr'][:500]}")
            sys.exit(1)


if __name__ == "__main__":
    main()