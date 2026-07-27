import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import kagglehub

st.set_page_config(layout="wide")
st.title('Global & Country-wise COVID-19 Cases Over Time')
st.write('Confirmed, Deaths, Recovered, and Active cases visualization.')

# --- Data Loading and Preprocessing ---
@st.cache_data
def load_data():
    try:
        # Kagglehub를 통해 데이터셋 다운로드
        # Streamlit Cloud 환경에서 실행될 경우, kagglehub는 설치되어 있어야 합니다.
        # 또는 데이터를 미리 `/data`와 같은 폴더에 업로드해야 합니다.
        path = kagglehub.dataset_download("imdevskp/corona-virus-report")
        csv_file_name = 'covid_19_clean_complete.csv'
        full_csv_path = os.path.join(path, csv_file_name)

        if not os.path.exists(full_csv_path):
            st.error(f"Error: {csv_file_name} not found at {path}")
            st.stop()

        df = pd.read_csv(full_csv_path)
        df['Date'] = pd.to_datetime(df['Date'])

        # Clean column names (remove leading/trailing spaces)
        df.columns = df.columns.str.strip()

        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

df = load_data()

if df is not None:
    # Get unique countries/regions
    countries = ['Global'] + sorted(df['Country/Region'].unique().tolist())

    # Country selection
    selected_country = st.selectbox('Select a Country/Region', countries)

    # Prepare data based on selection
    if selected_country == 'Global':
        daily_cases = df.groupby('Date')[['Confirmed', 'Deaths', 'Recovered', 'Active']].sum().reset_index()
        title = 'Global COVID-19 Cases Over Time'
    else:
        country_df = df[df['Country/Region'] == selected_country]
        daily_cases = country_df.groupby('Date')[['Confirmed', 'Deaths', 'Recovered', 'Active']].sum().reset_index()
        title = f'{selected_country} COVID-19 Cases Over Time'

    # Plotly time series graph
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=daily_cases['Date'], y=daily_cases['Confirmed'], mode='lines', name='Confirmed', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=daily_cases['Date'], y=daily_cases['Deaths'], mode='lines', name='Deaths', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=daily_cases['Date'], y=daily_cases['Recovered'], mode='lines', name='Recovered', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=daily_cases['Date'], y=daily_cases['Active'], mode='lines', name='Active', line=dict(color='orange')))

    fig.update_layout(
        title_text=title,
        xaxis_rangeslider_visible=True,
        xaxis_title='Date',
        yaxis_title='Number of Cases',
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("데이터 로드에 실패하여 앱을 표시할 수 없습니다.")

print("""
streamlit
pandas
plotly
kagglehub
""")

