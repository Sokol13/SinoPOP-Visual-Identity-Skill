"""读取 UTF-8 staff.csv，逐人生成独立的内卡正反面文件。"""
import sys, csv, argparse, re
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from build_card_final import insert
from production import export_art

def main():
    p=argparse.ArgumentParser();p.add_argument('--csv',default=str(Path(__file__).with_name('staff.csv')));p.add_argument('--out',default=str(Path(__file__).with_name('batch-output')));args=p.parse_args()
    with open(args.csv,encoding='utf-8-sig',newline='') as fh:
        reader=csv.DictReader(fh);required=['name_cn','name_en','title','phone','wechat','email']
        if reader.fieldnames!=required:raise ValueError('CSV columns must be: '+','.join(required))
        rows=list(reader)
        if not rows:raise ValueError('CSV must contain at least one staff row')
        jobs=[]
        for i,row in enumerate(rows,1):
            if not all(row.get(k,'').strip() for k in required):raise ValueError(f'Row {i}: all fields are required')
            safe=re.sub(r'[^A-Za-z0-9_-]+','-',row['name_en']).strip('-') or 'staff'
            # 先校验整份名单与所有字段的排版宽度，再写任何文件。
            jobs.append((insert(row),Path(args.out)/f'{i:03}-{safe}'))
        for arts,folder in jobs:export_art(arts,folder,'insert',bleed_mm=3.175)
    print('Staff insert exports complete')

if __name__=='__main__':main()
