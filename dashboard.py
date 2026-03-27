import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIG
st.set_page_config(
    page_title="PhonePe Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.metric-card {
    background: linear-gradient(135deg, #1f1c2c, #928dab);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}
.metric-title {
    font-size: 14px;
    color: #ccc;
}
.metric-value {
    font-size: 28px;
    font-weight: bold;
}
.section-title {
    font-size: 22px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
# 📊 PhonePe Analytics Dashboard  
### 🚀 Digital Payments Intelligence Panel
""")

# LOAD
@st.cache_data
def load():
    df_trans = pd.read_csv("aggregated_transaction.csv")
    df_user = pd.read_csv("aggregated_user.csv")
    df_map_user = pd.read_csv("map_user.csv")
    df_ins = pd.read_csv("aggregated_insurance.csv")
    return df_trans, df_user, df_map_user, df_ins

df_trans, df_user, df_map_user, df_ins = load()


# SIDEBAR
st.sidebar.markdown("## 🎯 Filters")

year = st.sidebar.selectbox("Year", sorted(df_trans["year"].unique()))
quarter = st.sidebar.selectbox("Quarter", sorted(df_trans["quarter"].unique()))

df_trans_f = df_trans[(df_trans["year"] == year) & (df_trans["quarter"] == quarter)]
df_map_user_f = df_map_user[(df_map_user["year"] == year) & (df_map_user["quarter"] == quarter)]
df_ins_f = df_ins[(df_ins["year"] == year) & (df_ins["quarter"] == quarter)]

# KPI
st.markdown('<div class="section-title">📌 Key Metrics</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

total_amount = df_trans_f["transaction_amount"].sum()
total_txn = df_trans_f["transaction_count"].sum()
total_users = df_user["user_count"].sum()

col1.markdown(f"""
<div class="metric-card">
<div class="metric-title">Transaction Amount</div>
<div class="metric-value">₹ {total_amount:,.0f}</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="metric-card">
<div class="metric-title">Transactions</div>
<div class="metric-value">{total_txn:,.0f}</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="metric-card">
<div class="metric-title">Users</div>
<div class="metric-value">{total_users:,.0f}</div>
</div>
""", unsafe_allow_html=True)

# TABS
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Transactions",
    "🌍 Geography",
    "📱 Devices & Engagement",
    "🛡️ Insurance"
])

# TAB 1
with tab1:

    # Trend
    trend = df_trans.groupby(["year","quarter"])["transaction_amount"].sum().reset_index()
    trend["time"] = trend["year"].astype(str) + "-Q" + trend["quarter"].astype(str)

    fig_trend = px.line(trend, x="time", y="transaction_amount", title="Transaction Growth")
    st.plotly_chart(fig_trend, use_container_width=True)

    # Type Distribution
    df_type = df_trans.groupby("transaction_type")["transaction_amount"].sum().reset_index()
    fig_type = px.pie(df_type, values="transaction_amount", names="transaction_type")
    st.plotly_chart(fig_type, use_container_width=True)

# TAB 2
with tab2:

    # State
    df_state = df_trans_f.groupby("state")["transaction_amount"].sum().reset_index()
    df_state = df_state[df_state["state"] != "India"]

    fig_state = px.bar(df_state.sort_values(by="transaction_amount", ascending=False).head(10),
                       x="state", y="transaction_amount")
    st.plotly_chart(fig_state, use_container_width=True)

# TAB 3
with tab3:

    # Device
    df_device = df_user.groupby("brand")["user_count"].sum().reset_index()
    fig_device = px.pie(df_device.head(10), values="user_count", names="brand")
    st.plotly_chart(fig_device, use_container_width=True)

    # Engagement FIXED
    df_eng = df_map_user.groupby("state").agg({
        "registered_users": "sum",
        "app_opens": "sum"
    }).reset_index()

    df_eng["engagement"] = df_eng.apply(
        lambda x: x["app_opens"] / x["registered_users"] if x["registered_users"] > 0 else 0,
        axis=1
    )

    df_eng = df_eng[df_eng["engagement"] > 0]

    fig_eng = px.bar(df_eng.sort_values(by="engagement", ascending=False).head(10),
                     x="state", y="engagement")

    st.plotly_chart(fig_eng, use_container_width=True)

# TAB 4
with tab4:

    # Insurance Trend
    ins_trend = df_ins.groupby(["year","quarter"])["transaction_amount"].sum().reset_index()
    ins_trend["time"] = ins_trend["year"].astype(str) + "-Q" + ins_trend["quarter"].astype(str)

    fig_ins_trend = px.line(ins_trend, x="time", y="transaction_amount")
    st.plotly_chart(fig_ins_trend, use_container_width=True)

    # Insurance State
    if df_ins_f.empty:
        df_ins_state = df_ins.groupby("state")["transaction_amount"].sum().reset_index()
    else:
        df_ins_state = df_ins_f.groupby("state")["transaction_amount"].sum().reset_index()

    df_ins_state = df_ins_state[df_ins_state["state"] != "India"]

    fig_ins_state = px.bar(df_ins_state.sort_values(by="transaction_amount", ascending=False).head(10),
                          x="state", y="transaction_amount")

    st.plotly_chart(fig_ins_state, use_container_width=True)