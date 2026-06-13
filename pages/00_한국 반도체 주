import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta


st.set_page_config(
    page_title="한국 반도체 주가 분석",
    page_icon="💻",
    layout="wide"
)


st.title("💻 한국 반도체 기업 주가 분석")
st.write(
    "yfinance 데이터를 활용해 국내 주요 반도체 기업의 최근 1년 주가 변동을 분석합니다."
)


# 한국 반도체 종목
stocks = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "한미반도체": "042700.KS",
    "리노공업": "058470.KQ",
    "DB하이텍": "000990.KS"
}


end = datetime.now()
start = end - timedelta(days=365)



@st.cache_data(ttl=3600)
def get_stock_data():

    result = {}

    for name, ticker in stocks.items():

        try:

            data = yf.download(
                ticker,
                start=start,
                end=end,
                progress=False,
                auto_adjust=False
            )


            if data.empty:
                continue


            # yfinance 최신 버전 대응
            if isinstance(data.columns, pd.MultiIndex):
                close = data["Close"].iloc[:, 0]

            else:
                close = data["Close"]


            close = close.dropna()


            if len(close) > 0:
                result[name] = close


        except Exception as e:
            st.warning(
                f"{name} 데이터 오류 : {e}"
            )


    return pd.DataFrame(result)



df = get_stock_data()


if df.empty:
    st.error("데이터를 불러올 수 없습니다.")
    st.stop()



# -------------------------
# 실제 주가 그래프
# -------------------------

st.subheader("📈 최근 1년 주가 변화")


fig = go.Figure()


for col in df.columns:

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[col],
            mode="lines",
            name=col
        )
    )


fig.update_layout(
    height=600,
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="주가"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# -------------------------
# 수익률 비교
# -------------------------

st.subheader("🚀 반도체 기업 수익률 비교")


return_df = (
    df / df.iloc[0] * 100
)


fig2 = go.Figure()


for col in return_df.columns:

    fig2.add_trace(
        go.Scatter(
            x=return_df.index,
            y=return_df[col],
            mode="lines",
            name=col
        )
    )


fig2.update_layout(
    height=550,
    hovermode="x unified",
    yaxis_title="초기 투자 대비 (%)"
)


st.plotly_chart(
    fig2,
    use_container_width=True
)



# -------------------------
# 분석 지표
# -------------------------

st.subheader("📊 투자 분석 지표")


analysis = pd.DataFrame(
    index=df.columns
)


analysis["현재 가격"] = df.iloc[-1]


analysis["1년 수익률(%)"] = (
    (df.iloc[-1] /
     df.iloc[0] - 1)
    * 100
)


analysis["변동성(%)"] = (
    df.pct_change()
    .std()
    * 100
)


analysis = analysis.round(2)



st.dataframe(
    analysis,
    use_container_width=True
)



# -------------------------
# 순위 그래프
# -------------------------

st.subheader("🏆 1년 수익률 순위")


rank = (
    analysis
    .sort_values(
        "1년 수익률(%)",
        ascending=False
    )
)


fig3 = px.bar(
    rank,
    x=rank.index,
    y="1년 수익률(%)",
    text="1년 수익률(%)"
)


fig3.update_layout(
    xaxis_title="기업",
    yaxis_title="수익률 (%)"
)


st.plotly_chart(
    fig3,
    use_container_width=True
)



best = rank.index[0]
lowest_vol = analysis["변동성(%)"].idxmin()


st.info(
    f"""
    📌 분석 결과

    - 1년 수익률 1위: **{best}**
    - 가장 안정적인 움직임(낮은 변동성): **{lowest_vol}**

    ※ 본 앱은 데이터 분석 목적이며 투자 추천이 아닙니다.
    """
)
