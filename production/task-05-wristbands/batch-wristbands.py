"""按票档数量和独立编号段生成带出血的 A3 手环拼版。"""
from pathlib import Path
import sys, argparse, csv
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from build_credentials import batch_wristbands, TIERS

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--csv',type=Path,help='CSV 列：tier,quantity,start_serial')
p.add_argument('--ga',type=int,default=0)
p.add_argument('--vip',type=int,default=0)
p.add_argument('--svip',type=int,default=0)
p.add_argument('--ga-start',type=int,default=1)
p.add_argument('--vip-start',type=int,default=100001)
p.add_argument('--svip-start',type=int,default=200001)
p.add_argument('--output',type=Path,required=True)
args=p.parse_args()
counts=dict(GA=args.ga,VIP=args.vip,SVIP=args.svip)
starts=dict(GA=args.ga_start,VIP=args.vip_start,SVIP=args.svip_start)
if args.csv:
    with args.csv.open(encoding='utf-8-sig',newline='') as f:
        rows=csv.DictReader(f)
        if rows.fieldnames!=['tier','quantity','start_serial']:raise SystemExit('CSV 列应为 tier,quantity,start_serial')
        counts={};starts={}
        for row in rows:
            tier=row['tier'].strip().upper()
            if tier not in TIERS or tier in counts:raise SystemExit('票档无效或重复')
            counts[tier]=int(row['quantity']);starts[tier]=int(row['start_serial'])
if not any(counts.values()):raise SystemExit('请指定至少一档数量')
if any(n<0 for n in counts.values()):raise SystemExit('数量不可为负')
batch_wristbands(counts,starts,args.output)
print(args.output.resolve())
