import subprocess
import sys

def install(package):
    p1 = subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("lxml")
install("fuzzywuzzy")