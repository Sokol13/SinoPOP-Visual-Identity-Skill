from pathlib import Path
import sys
# 从交付根目录复用字体、标志与印刷引擎。
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from build_rollups import main
if __name__=='__main__':main()
