import subprocess
import sys

def install_packages(packages):
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# 需要安装的包列表
packages_to_install = ["pandas", "tushare"]

# 调用函数安装包
install_packages(packages_to_install)
