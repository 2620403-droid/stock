import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta


st.set_page_config(
    page_title="주가 분석",
    page_icon="📈",
    layout="wide"
)


st.title("📈 최근 1년 주가 변동 분석")


stocks = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "Google": "GOOGL",
    "Microsoft": "MSFT",
    "Apple": "AAPL"
}


end_date = datetime.now()
start_date = end_date - timedelta(days=365)



@st.cache_data(ttl=3600)
def load_data():

    result = {}

    for name, ticker in stocks.items():

        try:
            df = yf.download(
                ticker,
                start=start_date,
                end=end_date,
                progress=False,
                auto_adjust=False
            )

            if df.empty:
                continue


            # yfinance 최신 버전 MultiIndex 대응
            if isinstance(df.columns, pd.MultiIndex):
                close = df["Close"].iloc[:, 0]
            else:
                close = df["Close"]


            close = close.dropna()

            if len(close) > 0:
                result[name] = close


        except Exception as e:
            st.warning(f"{name} 데이터 불러오기 실패: {e}")


    if len(result) == 0:
        return pd.DataFrame()


    return pd.DataFrame(result)



price_df = load_data()



if price_df.empty:
    st.error("주가 데이터를 가져오지 못했습니다.")
    st.stop()



st.subheader("📊 실제 주가 변화")


fig = go.Figure()


for col in price_df.columns:
    fig.add_trace(
        go.Scatter(
            x=price_df.index,
            y=price_df[col],
            name=col,
            mode="lines"
        )
    )


fig.update_layout(
    height=600,
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="가격"
)


st.plotly_chart(fig, use_container_width=True)



st.subheader("📈 동일 기준 수익률 비교")


normalized = price_df / price_df.iloc[0] * 100


fig2 = go.Figure()


for col in normalized.columns:
    fig2.add_trace(
        go.Scatter(
            x=normalized.index,
            y=normalized[col],
            name=col,
            mode="lines"
        )
    )


fig2.update_layout(
    height=600,
    hovermode="x unified",
    yaxis_title="초기 투자 대비 (%)"
)


st.plotly_chart(fig2, use_container_width=True)



st.subheader("📌 투자 성과 요약")


summary = pd.DataFrame(index=price_df.columns)


summary["현재 가격"] = price_df.iloc[-1]

summary["1년 수익률(%)"] = (
    (price_df.iloc[-1] /
     price_df.iloc[0] - 1) * 100
)


summary["변동성(%)"] = (
    price_df.pct_change()
    .std() * 100
)


summary = summary.round(2)


st.dataframe(
    summary,
    use_container_width=True
)



st.subheader("🏆 1년 수익률 비교")


fig3 = px.bar(
    summary,
    x=summary.index,
    y="1년 수익률(%)",
    text="1년 수익률(%)"
)


fig3.update_layout(
    xaxis_title="기업",
    yaxis_title="수익률 (%)"
)


st.plotly_chart(fig3, use_container_width=True)
