import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta


# 페이지 설정
st.set_page_config(
    page_title="글로벌 주가 분석",
    page_icon="📈",
    layout="wide"
)


st.title("📈 최근 1년 글로벌 기업 주가 변동 분석")
st.write(
    "yfinance를 활용하여 삼성전자, SK하이닉스, Google, Microsoft, Apple의 "
    "최근 1년 주가 흐름을 비교합니다."
)


# 종목 설정
stocks = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "Google": "GOOGL",
    "Microsoft": "MSFT",
    "Apple": "AAPL"
}


# 기간 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)


@st.cache_data
def load_data():

    data = {}

    for name, ticker in stocks.items():
        stock = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            progress=False
        )

        if not stock.empty:
            data[name] = stock["Close"]

    df = pd.DataFrame(data)

    return df



price_df = load_data()


if price_df.empty:
    st.error("주가 데이터를 불러오지 못했습니다.")
    st.stop()



# 멀티인덱스 처리
if isinstance(price_df.columns, pd.MultiIndex):
    price_df.columns = price_df.columns.get_level_values(0)



st.subheader("📊 최근 1년 주가 변화")


fig = go.Figure()


for col in price_df.columns:
    fig.add_trace(
        go.Scatter(
            x=price_df.index,
            y=price_df[col],
            mode="lines",
            name=col
        )
    )


fig.update_layout(
    height=600,
    xaxis_title="날짜",
    yaxis_title="주가",
    hovermode="x unified"
)


st.plotly_chart(fig, use_container_width=True)



# 정규화 비교
st.subheader("📈 수익률 기준 비교")


normalized = price_df / price_df.iloc[0] * 100


fig2 = go.Figure()


for col in normalized.columns:

    fig2.add_trace(
        go.Scatter(
            x=normalized.index,
            y=normalized[col],
            mode="lines",
            name=col
        )
    )


fig2.update_layout(
    height=550,
    yaxis_title="초기 투자 대비 (%)",
    hovermode="x unified"
)


st.plotly_chart(fig2, use_container_width=True)



# 분석 지표

st.subheader("📌 투자 성과 분석")


result = pd.DataFrame()


result["최종 가격"] = price_df.iloc[-1]
result["1년 수익률(%)"] = (
    (price_df.iloc[-1] / price_df.iloc[0] - 1) * 100
)

result["변동성(%)"] = (
    price_df.pct_change().std() * 100
)


result = result.round(2)



st.dataframe(
    result,
    use_container_width=True
)



# 수익률 막대 그래프

st.subheader("🏆 1년 수익률 비교")


fig3 = px.bar(
    result,
    x=result.index,
    y="1년 수익률(%)",
    text="1년 수익률(%)"
)


fig3.update_layout(
    xaxis_title="기업",
    yaxis_title="수익률 (%)"
)


st.plotly_chart(fig3, use_container_width=True)



# 변동성 설명

st.subheader("📚 분석 해석")

best = result["1년 수익률(%)"].idxmax()
stable = result["변동성(%)"].idxmin()


st.write(
    f"""
    - 가장 높은 1년 수익률을 기록한 종목: **{best}**
    - 가장 낮은 변동성을 보인 종목: **{stable}**
    
    수익률이 높다고 항상 안정적인 것은 아니며,
    변동성과 함께 고려해야 합니다.
    """
)
