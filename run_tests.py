#!/usr/bin/env python3
"""
测试运行脚本
"""
import subprocess
import sys
from pathlib import Path


def run_tests():
    """运行测试套件"""
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    print("=" * 60)
    print("App 全自动生产工作流 - 测试套件")
    print("=" * 60)
    
    # 检查是否安装了 pytest
    try:
        import pytest
    except ImportError:
        print("错误: pytest 未安装")
        print("请运行: pip install pytest pytest-cov pytest-mock")
        return 1
    
    # 运行测试
    print("\n[1/3] 运行单元测试...")
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "tests/unit/",
        "-v",
        "--tb=short"
    ], cwd=project_root)
    
    if result.returncode != 0:
        print("\n❌ 单元测试失败")
        return result.returncode
    
    print("\n✅ 单元测试通过")
    
    # 运行测试覆盖率
    print("\n[2/3] 检查测试覆盖率...")
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "tests/unit/",
        "--cov=src",
        "--cov-report=term-missing",
        "--cov-fail-under=50"
    ], cwd=project_root)
    
    # 集成测试（可选）
    print("\n[3/3] 集成测试（跳过，需要真实 API Key）")
    print("   提示: 配置 .env 文件后可运行: pytest tests/integration/")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(run_tests())
