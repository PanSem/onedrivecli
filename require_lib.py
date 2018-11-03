import pip
import subprocess
import sys

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

if __name__ == '__main__':
    ns = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
    ins_pkg = [r.decode().split('==')[0] for r in ns.split()]

    if not "selenium" in ins_pkg:
        install("selenium")

    if not "colorama" in ins_pkg:
        install("colorama")
