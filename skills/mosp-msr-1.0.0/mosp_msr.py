#!/usr/bin/env python3
"""
MOSP MSR Skill Implementation (简化版本)
团簇结构生成技能
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import argparse

class MOSPMSRSkill:
    """MOSP MSR技能（简化版本）"""
    
    def __init__(self, mosp_root: Optional[str] = None):
        """初始化MSR技能
        
        Args:
            mosp_root: MOSP软件根目录，默认从环境变量MOSP_HOME获取
        """
        # 优先使用环境变量MOSP_HOME，其次使用传入参数，最后使用默认值
        if mosp_root is None:
            mosp_root = os.environ.get("MOSP_HOME", "/root/.openclaw/workspace/MOSP")
        
        self.mosp_root = Path(mosp_root)
        self.output_dir = self.mosp_root / "OUTPUT"
        self.utils_dir = self.mosp_root / "utils"
        
        # 确保目录存在
        self.output_dir.mkdir(exist_ok=True)
        
        # 验证MOSP软件是否存在
        self._validate_mosp_installation()
    
    def _validate_mosp_installation(self):
        """验证MOSP软件是否安装正确"""
        required_files = [
            self.utils_dir / "msr.py",
            self.utils_dir / "paint.py",
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
    
    def run_msr_calculation(self, input_json: Path, output_base: Optional[Path] = None) -> Dict[str, Any]:
        """
        运行MSR计算
        
        Args:
            input_json: 输入JSON参数文件路径
            output_base: 输出基础目录
            
        Returns:
            计算结果
        """
        # 加载参数
        params = self._load_parameters(input_json)
        if not params:
            return {"success": False, "error": "无法加载参数文件"}
        
        # 创建输出目录
        output_dir = self._create_msr_directory(params, output_base)
        
        # 准备文件
        self._prepare_msr_files(input_json, output_dir)
        
        # 运行MSR计算
        msr_success = self._run_msr_command(output_dir)
        
        if not msr_success:
            return {"success": False, "error": "MSR计算失败", "output_dir": str(output_dir)}
        
        # 生成可视化
        vis_success = self._generate_visualizations(output_dir)
        
        # 生成分析报告
        report_path = self._generate_analysis_report(output_dir, params)
        
        return {
            "success": True,
            "output_dir": str(output_dir),
            "xyz_file": self._find_xyz_file(output_dir),
            "images": self._find_images(output_dir),
            "log_file": str(output_dir / "msr_run.log"),
            "report_file": str(report_path),
            "visualization_success": vis_success,
        }
    
    def _load_parameters(self, json_path: Path) -> Dict[str, Any]:
        """加载参数文件"""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"错误：无法加载参数文件 {json_path}: {e}")
            return {}
    
    def _create_msr_directory(self, params: Dict, output_base: Optional[Path]) -> Path:
        """创建MSR任务目录"""
        # 提取必要参数
        element = params.get("Element", "Unknown")
        temperature = params.get("Temperature", 700)
        pressure = params.get("Pressure", 6000)
        radius = params.get("Radius", 40)
        
        # 提取气体信息
        gas1_name = params.get("Gas1_name", "CO")
        gas1_pp = params.get("Gas1_pp", 9)
        gas2_name = params.get("Gas2_name", "O2")
        gas2_pp = params.get("Gas2_pp", 90)
        
        # 生成目录名
        dir_name = f"{element}_{temperature}K_{pressure}Pa_{gas1_name}{gas1_pp}_{gas2_name}{gas2_pp}_R{radius}A"
        
        # 创建目录
        if output_base:
            output_dir = output_base / dir_name
        else:
            output_dir = self.output_dir / dir_name
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        return output_dir
    
    def _prepare_msr_files(self, input_json: Path, output_dir: Path):
        """准备MSR计算文件"""
        # 复制并重命名JSON文件
        target_json = output_dir / "input.json"
        shutil.copy2(input_json, target_json)
        
        # 复制可视化工具
        paint_py = self.utils_dir / "paint.py"
        if paint_py.exists():
            shutil.copy2(paint_py, output_dir / "paint.py")
        else:
            print(f"警告：未找到可视化工具 {paint_py}")
    
    def _run_msr_command(self, output_dir: Path) -> bool:
        """运行MSR命令"""
        msr_script = self.utils_dir / "msr.py"
        if not msr_script.exists():
            print(f"错误：未找到MSR脚本 {msr_script}")
            return False
        
        # 构建命令
        cmd = [
            "python3",
            str(msr_script),
            "--json", str(output_dir / "input.json"),
            "--output", str(output_dir),
        ]
        
        # 检查大团簇警告
        params = self._load_parameters(output_dir / "input.json")
        radius = params.get("Radius", 0)
        if radius > 40:
            print(f"⚠️ 检测到大团簇（半径 > 40 Å），MSR计算可能较慢，请耐心等待...")
        
        # 执行计算
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.mosp_root),
                timeout=3600,  # 1小时超时
            )
            
            # 保存日志
            log_file = output_dir / "msr_run.log"
            log_file.write_text(result.stdout + "\n" + result.stderr)
            
            if result.returncode != 0:
                print(f"MSR计算失败，返回码: {result.returncode}")
                print(f"错误输出: {result.stderr[:500]}...")
                return False
            
            return True
            
        except subprocess.TimeoutExpired:
            print("MSR计算超时（1小时）")
            return False
        except Exception as e:
            print(f"MSR计算异常: {e}")
            return False
    
    def _generate_visualizations(self, output_dir: Path) -> bool:
        """生成可视化图像"""
        # 查找XYZ文件
        xyz_files = list(output_dir.glob("*_FCC_T_*_P_*_cluster.xyz"))
        if not xyz_files:
            print(f"错误：未找到MSR生成的XYZ文件")
            return False
        
        xyz_file = xyz_files[0]
        paint_py = output_dir / "paint.py"
        
        if not paint_py.exists():
            print(f"错误：未找到可视化工具 {paint_py}")
            return False
        
        original_cwd = os.getcwd()
        os.chdir(output_dir)
        
        try:
            # 生成旋转动画
            gif_cmd = ["python3", "paint.py", str(xyz_file.name), 
                      "--gif", "rotation.gif", "--color-by", "site_type"]
            gif_result = subprocess.run(gif_cmd, capture_output=True, text=True)
            
            if gif_result.returncode != 0:
                print(f"生成GIF失败: {gif_result.stderr[:200]}")
            
            # 生成静态结构图
            png_cmd = ["python3", "paint.py", str(xyz_file.name),
                      "--output", "structure.png", "--color-by", "site_type"]
            png_result = subprocess.run(png_cmd, capture_output=True, text=True)
            
            if png_result.returncode != 0:
                print(f"生成PNG失败: {png_result.stderr[:200]}")
            
            return gif_result.returncode == 0 or png_result.returncode == 0
            
        finally:
            os.chdir(original_cwd)
    
    def _generate_analysis_report(self, output_dir: Path, params: Dict) -> Path:
        """生成分析报告"""
        report_path = output_dir / "parameter_analysis.md"
        
        report_content = f"""# MSR计算参数分析报告

## 计算基本信息
- **计算时间**: {self._get_current_time()}
- **输出目录**: {output_dir.name}
- **计算状态**: 完成

## 参数设置
- **金属元素**: {params.get('Element', 'Unknown')}
- **温度**: {params.get('Temperature', 'N/A')} K
- **压力**: {params.get('Pressure', 'N/A')} Pa
- **团簇半径**: {params.get('Radius', 'N/A')} Å

## 气体参数
- **气体1**: {params.get('Gas1_name', 'N/A')} ({params.get('Gas1_pp', 'N/A')}%)
- **气体2**: {params.get('Gas2_name', 'N/A')} ({params.get('Gas2_pp', 'N/A')}%)

## 生成文件
1. XYZ结构文件: {self._find_xyz_file(output_dir) or '未找到'}
2. 旋转动画: {'rotation.gif (存在)' if (output_dir / 'rotation.gif').exists() else '未生成'}
3. 静态结构图: {'structure.png (存在)' if (output_dir / 'structure.png').exists() else '未生成'}

## 注意事项
- 所有文件已保存在当前目录
- 原始参数文件: input.json
- 计算日志: msr_run.log

---
报告生成时间: {self._get_current_time()}
"""
        
        report_path.write_text(report_content, encoding='utf-8')
        return report_path
    
    def _find_xyz_file(self, output_dir: Path) -> Optional[str]:
        """查找XYZ文件"""
        xyz_files = list(output_dir.glob("*_FCC_T_*_P_*_cluster.xyz"))
        if xyz_files:
            return str(xyz_files[0].name)
        return None
    
    def _find_images(self, output_dir: Path) -> List[str]:
        """查找图像文件"""
        images = []
        for ext in ['.gif', '.png', '.jpg', '.jpeg']:
            for img_file in output_dir.glob(f"*{ext}"):
                images.append(str(img_file.name))
        return images
    
    def _get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description='MOSP MSR Skill 团簇结构生成')
    parser.add_argument('--json', required=True, help='输入JSON参数文件')
    parser.add_argument('--output', help='输出目录（可选）')
    parser.add_argument('--test', action='store_true', help='测试模式')
    
    args = parser.parse_args()
    
    input_json = Path(args.json)
    if not input_json.exists():
        print(f"错误：输入文件不存在 {args.json}")
        sys.exit(1)
    
    # 创建MSR技能
    msr = MOSPMSRSkill()
    
    # 运行计算
    output_base = Path(args.output) if args.output else None
    result = msr.run_msr_calculation(input_json, output_base)
    
    # 输出结果
    if result["success"]:
        print("✅ MSR计算成功完成")
        print(f"输出目录: {result['output_dir']}")
        
        if result.get("xyz_file"):
            print(f"XYZ结构文件: {result['xyz_file']}")
        
        if result.get("images"):
            print(f"生成图像: {', '.join(result['images'])}")
        
        if result.get("report_file"):
            print(f"分析报告: {result['report_file']}")
        
        if not result.get("visualization_success", True):
            print("⚠️ 可视化生成部分失败，但计算已完成")
    else:
        print(f"❌ MSR计算失败: {result.get('error', '未知错误')}")
        if "output_dir" in result:
            print(f"查看日志: {result['output_dir']}/msr_run.log")
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()