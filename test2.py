import shutil
import os

base = "./bots/base/"
target = "./bots/4"

os.makedirs(os.path.dirname(target), exist_ok=True)
shutil.copytree(base, target)