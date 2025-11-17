from __future__ import annotations
from datetime import datetime
from pathlib import Path
import sqlite3, pandas as pd
def ensure_schema(db_path: Path, schema_path: Path)->None:
    con = sqlite3.connect(db_path); 
    try: con.executescript(schema_path.read_text(encoding='utf-8'))
    finally: con.close()
def read_df(db_path: Path, query: str)->pd.DataFrame:
    con = sqlite3.connect(db_path); 
    try: return pd.read_sql_query(query, con, parse_dates=[])
    finally: con.close()
def execute(db_path: Path, sql: str, params: tuple|None=None)->None:
    con = sqlite3.connect(db_path); 
    try: cur=con.cursor(); cur.execute(sql, params or ()); con.commit()
    finally: con.close()
def insert_session(db_path: Path, row: dict)->None:
    fmt='%H:%M'; 
    duration=int((datetime.strptime(row['end_time'],fmt)-datetime.strptime(row['start_time'],fmt)).total_seconds()/60)
    if duration<0: raise ValueError('end_time must be after start_time')
    row=dict(row); row['duration_min']=duration
    cols=['date','start_time','end_time','duration_min','subject','technique','distractions','mood','caffeine_mg','productivity']
    placeholders=','.join(['?']*len(cols))
    sql=f"INSERT INTO study_sessions ({','.join(cols)}) VALUES ({placeholders})"
    execute(db_path, sql, tuple(row[c] for c in cols))
