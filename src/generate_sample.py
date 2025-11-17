from __future__ import annotations
import argparse, random, csv
from datetime import datetime, timedelta, date
from pathlib import Path
SUBJECTS=['Math','Physics','CS','Biology','History']
TECHNIQUES=['Pomodoro','Active Recall','Note-taking','Practice Problems','Spaced Repetition']
def sample_row(day: date)->dict:
    start_hour=random.choice([6,7,8,9,10,14,15,16,19,20,21])
    start_min=random.choice([0,15,30,45])
    duration=random.choice([25,30,45,60,75,90,120])
    end_dt=datetime.combine(day, datetime.min.time()).replace(hour=start_hour, minute=start_min)+timedelta(minutes=duration)
    end_time=end_dt.strftime('%H:%M'); start_time=f'{start_hour:02d}:{start_min:02d}'
    subject=random.choice(SUBJECTS); technique=random.choice(TECHNIQUES)
    distractions=max(0,int(random.gauss(2,1))); mood=min(5,max(1,int(random.gauss(4,1))))
    caffeine=max(0,int(random.gauss(120,60)))
    base=3+(mood-3)*0.5-distractions*0.2+(1 if 9<=start_hour<=11 else 0)+(1 if technique in ['Active Recall','Spaced Repetition'] else 0)
    prod=int(min(5,max(1,round(base+random.uniform(-0.7,0.7)))))
    return {'date':day.isoformat(),'start_time':start_time,'end_time':end_time,'subject':subject,'technique':technique,'distractions':distractions,'mood':mood,'caffeine_mg':caffeine,'productivity':prod}
def main():
    ap=argparse.ArgumentParser(description='Generate synthetic study sessions CSV')
    ap.add_argument('--days',type=int,default=28); ap.add_argument('--sessions_per_day',type=int,default=2)
    ap.add_argument('--out',default='data/sessions.csv'); args=ap.parse_args()
    start=date.today()-timedelta(days=args.days); rows=[]
    for d in range(args.days):
        day=start+timedelta(days=d)
        for _ in range(args.sessions_per_day): rows.append(sample_row(day))
    out=Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=['date','start_time','end_time','subject','technique','distractions','mood','caffeine_mg','productivity'])
        w.writeheader(); w.writerows(rows)
    print(f'Wrote {len(rows)} rows -> {out}')
if __name__=='__main__': main()
