"""读取 name,role,zones，为每位人员生成双面工牌。"""
from pathlib import Path
import argparse,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from build_credentials import batch_passes
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('csv',type=Path)
p.add_argument('--output',type=Path,required=True)
args=p.parse_args()
batch_passes(args.csv,args.output)
print(args.output.resolve())
