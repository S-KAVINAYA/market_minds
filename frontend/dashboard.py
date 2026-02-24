import pandas as pd
import streamlit as st
from api_client import (
    fetch_clients_cached,
    fetch_customer_comparison_trend,
    build_risk_dashboard_metrics,
    group_clients_by_ticker,
    generate_ticker_drop_alerts,
    fetch_risk_level_asset_timeseries,
    ai_explain_risk_asset_timeseries,
    ai_stock_recommendation,
)
from components.client_table import display_client_table
from components.client_profile import display_client_profile
from components.charts import customer_comparison_chart, asset_time_series_chart


def dashboard_page():
    st.title("Portfolio Intelligence Dashboard")

    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    risk_filter = st.sidebar.multiselect(
        "Filter by Risk",
        ["Low", "Moderate", "High"],
        default=["Low", "Moderate", "High"],
    )

    clients = fetch_clients_cached(st.session_state.manager_id)
    if risk_filter:
        clients = [c for c in clients if c["risk_level"] in risk_filter]

    metrics = build_risk_dashboard_metrics(clients)
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total Portfolio Value", f"₹{metrics['total_portfolio_value']:,.0f}")
    k2.metric("Overall Risk Score", metrics["overall_risk_score"])
    k3.metric("Sharpe Score", metrics["sharpe_score"])
    k4.metric("Sector Penalty", metrics["sector_penalty"])
    k5.metric("Allocation Penalty", metrics["allocation_penalty"])

    st.markdown("### Risk Classification Grouped by Ticker")
    grouped = group_clients_by_ticker(clients)
    if grouped:
        st.dataframe(pd.DataFrame(grouped), use_container_width=True)

    alerts = generate_ticker_drop_alerts(clients)
    if alerts:
        st.markdown("### Ticker Drop Alerts")
        for alert in alerts:
            st.warning(f"{alert['ticker']} dropped {alert['drop_pct']}%. Notify: {', '.join(alert['affected_clients'])}")

    st.markdown("### Asset Time Series by Risk Level")
    risk_asset_df = fetch_risk_level_asset_timeseries(clients)
    for risk_level in ["Low", "Moderate", "High"]:
        subset = risk_asset_df[risk_asset_df["Risk"] == risk_level]
        if subset.empty:
            continue
        with st.expander(f"{risk_level} Risk - Asset Trends", expanded=(risk_level == "Moderate")):
            asset_time_series_chart(subset, f"{risk_level} Risk: Asset Time Series")
            st.info(ai_explain_risk_asset_timeseries(risk_asset_df, risk_level))
            rec = ai_stock_recommendation(risk_level)
            st.success(
                f"AI Future Prediction ({risk_level}): invest consideration in {rec['symbol']} near {rec['best_time']} "
                f"(expected ~{rec['expected_return_pct']}%)."
            )

    selected_client_from_click = display_client_table(clients)

    if not clients:
        st.warning("No clients match the selected risk level(s).")
        return

    default_client = clients[0]["client_id"]
    selected_client_id = selected_client_from_click or st.selectbox(
        "Select Client to View Details",
        [c["client_id"] for c in clients],
        index=[c["client_id"] for c in clients].index(default_client)
    )

    selected_client = next(c for c in clients if c["client_id"] == selected_client_id)
    display_client_profile(selected_client)

    st.markdown("### Customer-to-Customer Time Series Comparison")
    compare_ids = st.multiselect(
        "Select customers to compare",
        [c["client_id"] for c in clients],
        default=[c["client_id"] for c in clients[:3]],
    )

    comparison_df = fetch_customer_comparison_trend(compare_ids)
    if not comparison_df.empty:
        customer_comparison_chart(comparison_df)
