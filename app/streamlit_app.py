from __future__ import annotations
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))
import sqlite3, joblib, pandas as pd, streamlit as st, plotly.express as px
from utils import ensure_schema, insert_session
import time

# Paths
DB_PATH = Path(__file__).resolve().parents[1]/'data'/'study.db'
SCHEMA_PATH = Path(__file__).resolve().parents[1]/'sql'/'schema.sql'
MODEL_PATH = Path(__file__).resolve().parents[1]/'models'/'pipeline.joblib'

# Page config
st.set_page_config(page_title='AI Study Tracker', page_icon='📚', layout='wide')
st.title('📚 ScholarSync Personal Study Tracker')

# Custom CSS
st.markdown("""
<style>
body {
    background-color: #f0f8ff;
    font-family: 'Arial', sans-serif;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Plotly config
CFG = {'displayModeBar': True, 'responsive': True}

# Load data
@st.cache_data(show_spinner=False)
def load_df() -> pd.DataFrame:
    if not DB_PATH.exists(): return pd.DataFrame()
    con = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query('SELECT * FROM study_sessions', con)
    finally:
        con.close()
    return df

# Load ML model
def load_model():
    if MODEL_PATH.exists(): return joblib.load(MODEL_PATH)
    return None

# Ensure DB schema
ensure_schema(DB_PATH, SCHEMA_PATH)

# Sidebar: Add Session
with st.sidebar:
    st.header('Add Session 📝')
    with st.form('new_session'):
        date_v = st.date_input('Date')
        start_v = st.time_input('Start time')
        end_v = st.time_input('End time')
        subject_v = st.selectbox('Subject', ['Math','Physics','CS','Biology','History'])
        technique_v = st.selectbox('Technique', ['Pomodoro','Active Recall','Note-taking','Practice Problems','Spaced Repetition'])
        distractions_v = st.number_input('Distractions', min_value=0, step=1, value=1)
        mood_v = st.slider('Mood (1-5)',1,5,4)
        caffeine_v = st.number_input('Caffeine (mg)', min_value=0, step=10, value=120)
        productivity_v = st.slider('Productivity (1-5)',1,5,4)
        submitted = st.form_submit_button('Save ✅')
    if submitted:
        try:
            insert_session(DB_PATH, {
                'date': date_v.isoformat(),
                'start_time': start_v.strftime('%H:%M'),
                'end_time': end_v.strftime('%H:%M'),
                'subject': subject_v,
                'technique': technique_v,
                'distractions': int(distractions_v),
                'mood': int(mood_v),
                'caffeine_mg': int(caffeine_v),
                'productivity': int(productivity_v)
            })
            st.success('Session saved ✅')
            st.cache_data.clear()
        except Exception as e:
            st.error(f'Failed to save session: {e}')

# Load data for dashboard
df = load_df()

if df.empty:
    st.info('No data yet. Generate sample data or add sessions using the sidebar.', icon='ℹ️')
else:
    # KPI Tiles
    col1, col2, col3, col4 = st.columns(4)
    total_min = int(df['duration_min'].sum())
    avg_prod = df['productivity'].mean()
    sessions = len(df)
    avg_mood = df['mood'].mean()
    col1.metric('📖 Total Minutes', f'{total_min:,}')
    col2.metric('🗂 Sessions', f'{sessions:,}')
    col3.metric('⚡ Avg Productivity', f'{avg_prod:.2f}')
    col4.metric('🙂 Avg Mood', f'{avg_mood:.2f}')

    st.divider()
    
    # Charts
    left, right = st.columns(2)
    
    with left:
        by_date = df.groupby('date', as_index=False).agg(minutes=('duration_min','sum'))
        fig = px.line(by_date, x='date', y='minutes', markers=True,
                      title='Study Minutes Over Time',
                      color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, config=CFG, use_container_width=True)
        
    with right:
        by_subj = df.groupby('subject', as_index=False).agg(avg_prod=('productivity','mean'))
        fig2 = px.bar(by_subj, x='subject', y='avg_prod',
                      title='Average Productivity by Subject',
                      color='subject', color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig2, config=CFG, use_container_width=True)
    
    # All Sessions
    st.subheader('All Sessions 📊')
    st.dataframe(df.sort_values(['date','start_time']), hide_index=True)
    
# Progress Bar Example
st.divider()
st.subheader("📈 Weekly Progress")
progress = st.progress(0)
for i in range(100):
    time.sleep(0.005)
    progress.progress(i + 1)

# Productivity Estimator
pipe = load_model()
st.subheader('🔮 Productivity Estimator')
if pipe is None:
    st.warning('Model not trained yet. Run: `python src/train_model.py` after ingesting data.', icon='⚠️')
else:
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: sub = st.selectbox('Subject',['Math','Physics','CS','Biology','History'], key='pred_sub')
    with c2: tech = st.selectbox('Technique',['Pomodoro','Active Recall','Note-taking','Practice Problems','Spaced Repetition'], key='pred_tech')
    with c3: dur = st.number_input('Duration (min)', min_value=10, step=5, value=60, key='pred_dur')
    with c4: dis = st.number_input('Distractions', min_value=0, step=1, value=2, key='pred_dis')
    with c5: mood = st.slider('Mood',1,5,4, key='pred_mood')
    with c6: caf = st.number_input('Caffeine (mg)', min_value=0, step=10, value=100, key='pred_caf')
    
    df_in = pd.DataFrame([{
        'duration_min': dur,
        'subject': sub,
        'technique': tech,
        'distractions': dis,
        'mood': mood,
        'caffeine_mg': caf
    }])
    pred = float(pipe.predict(df_in)[0])
    st.metric('Estimated Productivity (1..5)', f'{pred:.2f}')
