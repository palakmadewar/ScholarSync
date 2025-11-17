from __future__ import annotations
import argparse, pandas as pd
from pathlib import Path
from utils import ensure_schema, insert_session
def main():
    ap=argparse.ArgumentParser(description='Ingest CSV into SQLite')
    ap.add_argument('--csv',default='data/sessions.csv'); ap.add_argument('--db',default='data/study.db'); ap.add_argument('--schema',default='sql/schema.sql')
    args=ap.parse_args()
    db=Path(args.db); schema=Path(args.schema); db.parent.mkdir(parents=True, exist_ok=True); ensure_schema(db, schema)
    df=pd.read_csv(args.csv)
    for _,r in df.iterrows():
        insert_session(db, {'date':r['date'],'start_time':r['start_time'],'end_time':r['end_time'],'subject':r['subject'],'technique':r['technique'],'distractions':int(r['distractions']),'mood':int(r['mood']),'caffeine_mg':int(r['caffeine_mg']),'productivity':int(r['productivity'])})
    print(f'Ingested {len(df)} rows -> {db}')
if __name__=='__main__': main()
