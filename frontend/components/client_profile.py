import pandas as pd
import streamlit as st
from components.charts import (
    allocation_chart,
    trend_chart,
    stock_time_series_chart,
    client_value_comparison_chart,
    ticker_exposure_chart,
    forecast_chart,
    asset_time_series_chart,
)
from api_client import (
    fetch_client_trend,
    fetch_stock_universe,
    fetch_stock_trend,
    ai_risk_explainability,
    ai_stock_recommendation,
    forecast_stock_prices,
    fetch_client_asset_timeseries,
    recommendation_timestamp,
)


def display_client_profile(client):
    st.header(f"Client Dashboard · {client['client_id']}")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Risk Level", client["risk_level"])
    m2.metric("Risk Asset", client["risk_asset"])
    m3.metric("Invested Value", f"₹{client['invested_value']:,.0f}")
    m4.metric("Current Value", f"₹{client['current_value']:,.0f}")

    tab1, tab2, tab3 = st.tabs(["Overview", "Time-Series", "AI Insights & Prediction"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            client_value_comparison_chart(client)
            holdings_df = pd.DataFrame(client.get("holdings", []))
            if not holdings_df.empty:
                ticker_exposure_chart(holdings_df)
        with c2:
            allocation_chart(client["portfolio"])

    with tab2:
        st.markdown("#### Portfolio Value Trend")
        trend_chart(fetch_client_trend(client["client_id"]))

        st.markdown("#### All Assets Time Series (Single Graph)")
        asset_time_series_chart(
            fetch_client_asset_timeseries(client),
            f"{client['client_id']} Asset-Level Time Series"
        )

    with tab3:
        st.info(ai_risk_explainability(client))

        stocks = fetch_stock_universe(client["risk_level"])
        options = [f"{s['symbol']} - {s['name']}" for s in stocks]
        if options:
            selected_stock = st.selectbox(
                "Risk-aligned stock",
                options,
                key=f"stock_selector_{client['client_id']}"
            )
            selected_symbol = selected_stock.split(" - ")[0]
            stock_time_series_chart(fetch_stock_trend(selected_symbol), selected_symbol)

        rec = ai_stock_recommendation(client["risk_level"])
        st.success(
            f"AI Future Prediction: Consider **{rec['symbol']}** with expected return ~{rec['expected_return_pct']}%. "
            f"Suggested entry window: **{rec['best_time']}**."
        )
        st.caption(rec["explanation"])
        st.caption(f"Recommendation timestamp: {recommendation_timestamp()}")
        forecast_chart(forecast_stock_prices(rec["symbol"]), rec["symbol"])
