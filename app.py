import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="UPI Analytics Dashboard",
    page_icon="💳",
    layout="wide"
)
# -----------------------------------
# BACKGROUND IMAGE
# -----------------------------------

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpg;base64,{encoded});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local("upi5.jpg")
# -----------------------------------
# LOAD DATA
# -----------------------------------

df = pd.read_csv("upi_transactions.csv")

# -----------------------------------
# TITLE
# -----------------------------------

# st.title("💳 UPI Transaction Analytics Dashboard")
# st.markdown("### Customer Behavior, Revenue & Fraud Analysis")


# -----------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------

# page = st.sidebar.radio(
#     "🏠 Navigation",
#     [
#         "📊 Overview",
#         "📈 Business Analysis",
#         "🛡️ Fraud & Risk",
#         "📍 Geographic Analysis",
#         "📱 Device Analysis"
#     ]
# )

page = st.sidebar.radio(
    "🏠 Navigation",
    [
        "🏠 Home",
        "📄 Dataset Overview",
        "📊 Executive Summary",
        "📈 Business Analysis",
        "🛡️ Fraud & Risk",
        "📍 Geographic Analysis",
        "📱 Device Analysis",
        "💡 Insights",
        "🎯 Recommendations"
    ]
)
# -----------------------------------
# SIDEBAR FILTERS
# -----------------------------------

with st.sidebar.expander("🔍 Filters", expanded=True):

    transaction_filter = st.multiselect(
        "Transaction Type",
        df["transaction type"].unique(),
        default=df["transaction type"].unique()
    )

    state_filter = st.multiselect(
        "State",
        df["sender_state"].unique(),
        default=df["sender_state"].unique()
    )

    age_filter = st.multiselect(
        "Age Group",
        df["sender_age_group"].unique(),
        default=df["sender_age_group"].unique()
    )

    device_filter = st.multiselect(
        "Device Type",
        df["device_type"].dropna().unique(),
        default=df["device_type"].dropna().unique()
    )

# -----------------------------------
# FILTERED DATA
# -----------------------------------

filtered_df = df[
    (df["transaction type"].isin(transaction_filter)) &
    (df["sender_state"].isin(state_filter)) &
    (df["sender_age_group"].isin(age_filter)) &
    (df["device_type"].isin(device_filter))
]

# -----------------------------------
# HOME PAGE
# -----------------------------------

if page == "🏠 Home":

    st.header("💳 UPI Transaction Analytics Dashboard")

    st.markdown(
        "### Understanding Customer Behavior, Transaction Patterns and Fraud Risk"
    )

    # st.markdown("---")

    # KPI Cards

    # total_transactions = len(df)

    # total_revenue = df["amount (INR)"].sum()

    # avg_transaction = df["amount (INR)"].mean()

    # fraud_rate = (
    #     df["fraud_flag"]
    #     .value_counts(normalize=True)
    #     .get(1, 0) * 100
    # )

    # col1, col2, col3, col4 = st.columns(4)

    # col1.metric(
    #     "Total Transactions",
    #     f"{total_transactions:,}"
    # )

    # col2.metric(
    #     "Revenue",
    #     f"₹{total_revenue/1e6:.1f}M"
    # )

    # col3.metric(
    #     "Avg Transaction",
    #     f"₹{avg_transaction:.0f}"
    # )

    # col4.metric(
    #     "Fraud Rate",
    #     f"{fraud_rate:.3f}%"
    # )

    # st.markdown("---")

    st.subheader("📌 Problem Statement")

    st.write(
        """
        A digital payment company wants to understand how customers use its UPI platform. 
        The company needs insights into transaction behavior, revenue-generating categories,
        customer demographics, peak usage hours, and fraud patterns to improve business performance and customer experience.
        """
    )

    st.subheader("🎯 Objectives")

    st.markdown("""
    - Analyze transaction patterns across different transaction types.
    - Identify top revenue-generating merchant categories.
    - Understand customer spending behavior by age group.
    - Detect fraud patterns and risk factors.
    - Generate business insights and recommendations.
    """)

    st.subheader("👨‍💻 About Developer")

    st.markdown("""
### Developer Information

🎓 **B.Tech CSE (Data Science)**

📧 **Email:** jsravankumar06@gmail.com

💼 **LinkedIn:**https://www.linkedin.com/in/sravan-kumar-jangiti-ab53472a2?

💻 **GitHub:** https://github.com/your-username

📊 **Aspiring Data Analyst**

### Project

**UPI Transaction Analytics Dashboard**
""")
elif page == "📄 Dataset Overview":

    st.header("📄 Dataset Overview")

    rows, cols = df.shape

    st.subheader("Dataset Shape")

    col1, col2 = st.columns(2)

    col1.metric("Rows", f"{rows:,}")
    col2.metric("Columns", cols)

    st.markdown("---")

    st.subheader("Column Names")

    st.write(list(df.columns))

    st.markdown("---")

    st.subheader("Data Types")

    st.dataframe(
        pd.DataFrame(df.dtypes, columns=["Data Type"])
    )

    st.markdown("---")

    st.subheader("Dataset Preview")

    st.dataframe(df.head())

    st.markdown("---")

    missing_values = df.isnull().sum().sum()

    duplicate_rows = df.duplicated().sum()
    st.success(
        f""" 
### Observation
"""
    )
    st.success(
        f"""
        Dataset contains {rows:,} records.

        Missing Values: {missing_values}

        Duplicate Records: {duplicate_rows}
        """
    )

# -----------------------------------
# EXECUTIVE SUMMARY
# -----------------------------------

elif page == "📊 Executive Summary":

    st.header("📊 Executive Summary")

    total_transactions = len(filtered_df)

    total_revenue = filtered_df["amount (INR)"].sum()

    avg_transaction = filtered_df["amount (INR)"].mean()

    success_rate = (
        filtered_df["transaction_status"]
        .value_counts(normalize=True)
        .get("SUCCESS", 0) * 100
    )

    fraud_rate = (
        filtered_df["fraud_flag"]
        .value_counts(normalize=True)
        .get(1, 0) * 100
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Transactions",
        f"{total_transactions:,}"
    )

    col2.metric(
        "Revenue",
        f"₹{total_revenue/1e6:.1f}M"
    )

    col3.metric(
        "Avg Amount",
        f"₹{avg_transaction:.0f}"
    )

    col4.metric(
        "Success Rate",
        f"{success_rate:.2f}%"
    )

    col5.metric(
        "Fraud Rate",
        f"{fraud_rate:.3f}%"
    )

    st.markdown("---")

    st.subheader("📌 Key Findings")

    st.info("""
### Customer Behavior

• Age group 26–35 contributes the highest transaction value.

• Android users account for the majority of transactions.

• Peak transaction activity occurs during evening hours.
""")

    st.success("""
### Revenue Insights

• Shopping is the highest revenue-generating category.

• Maharashtra generates the highest transaction value.

• Education has the highest average transaction amount.
""")

    st.warning("""
### Risk Insights

• Overall fraud rate remains below 0.2%.

• Recharge transactions show the highest fraud exposure.

• Transaction success rate exceeds 95%.
""")    
    # -----------------------------------
# BUSINESS ANALYSIS PAGE
# -----------------------------------

elif page == "📈 Business Analysis":

    st.header("📈 Business Analysis")

    # Transaction Type Distribution
    transaction_counts = (
        filtered_df["transaction type"]
        .value_counts()
        .reset_index()
    )

    transaction_counts.columns = [
        "Transaction Type",
        "Count"
    ]

    fig_transaction = px.pie(
        transaction_counts,
        names="Transaction Type",
        values="Count",
        hole=0.5,
        title="Transaction Type Distribution"
    )

    # Merchant Revenue
    merchant_revenue = (
        filtered_df
        .groupby("merchant_category")["amount (INR)"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig_merchant = px.bar(
        merchant_revenue,
        x="merchant_category",
        y="amount (INR)",
        text_auto=True,
        title="Revenue by Merchant Category"
    )

    # First Row
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            fig_transaction,
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            fig_merchant,
            use_container_width=True
        )

    # Age Group Revenue
    age_revenue = (
        filtered_df
        .groupby("sender_age_group")["amount (INR)"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig_age = px.bar(
        age_revenue,
        x="sender_age_group",
        y="amount (INR)",
        text_auto=True,
        title="Revenue by Age Group"
    )

    # Transactions by Hour
    hourly_transactions = (
        filtered_df
        .groupby("hour_of_day")
        .size()
        .reset_index(name="Transactions")
    )

    fig_hour = px.line(
        hourly_transactions,
        x="hour_of_day",
        y="Transactions",
        markers=True,
        title="Transactions by Hour"
    )

    # Second Row
    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(
            fig_age,
            use_container_width=True
        )

    with col4:
        st.plotly_chart(
            fig_hour,
            use_container_width=True
        )

    # Insights
    

    top_category = merchant_revenue.iloc[0]["merchant_category"]

    top_age_group = age_revenue.iloc[0]["sender_age_group"]

    peak_hour = hourly_transactions.loc[
        hourly_transactions["Transactions"].idxmax(),
        "hour_of_day"
    ]

    st.subheader("📝 Observations")
    st.info("""
• P2P transactions dominate the platform, accounting for approximately 45% of all transactions.

• Shopping is the highest revenue-generating category, contributing approximately ₹76.86M.

• Users aged 26–35 generate the highest revenue, making them the platform's most valuable customer segment.

• Transaction activity peaks between 6 PM and 8 PM, indicating maximum customer engagement during evening hours.

• Healthcare, Entertainment, and Transport contribute the least revenue, presenting opportunities for targeted growth initiatives.
""") 
    
      
    st.subheader(" 📋 Business Insights")
    st.success(
        f"""
🏆 Highest Revenue Category: {top_category}

👥 Highest Spending Age Group: {top_age_group}

⏰ Peak Transaction Hour: {int(peak_hour)}:00
        """
    )

    # -----------------------------------
# FRAUD & RISK PAGE
# -----------------------------------

elif page == "🛡️ Fraud & Risk":

    st.header("🛡️ Fraud & Risk Analysis")

    # Fraud KPI

    fraud_rate = (
        filtered_df["fraud_flag"]
        .value_counts(normalize=True)
        .get(1, 0) * 100
    )

    total_fraud = (
        filtered_df["fraud_flag"]
        .sum()
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Fraud Transactions",
        f"{int(total_fraud):,}"
    )

    col2.metric(
        "Fraud Rate",
        f"{fraud_rate:.3f}%"
    )

    # Fraud Distribution

    fraud_distribution = (
        filtered_df["fraud_flag"]
        .value_counts()
        .reset_index()
    )

    fraud_distribution.columns = [
        "Fraud Flag",
        "Count"
    ]

    fraud_distribution["Fraud Flag"] = (
        fraud_distribution["Fraud Flag"]
        .map({
            0: "Legitimate",
            1: "Fraudulent"
        })
    )

    fig_fraud = px.pie(
        fraud_distribution,
        names="Fraud Flag",
        values="Count",
        hole=0.5,
        title="Fraud vs Legitimate Transactions"
    )

    # Fraud Rate By Transaction Type

    fraud_by_type = (
        pd.crosstab(
            filtered_df["transaction type"],
            filtered_df["fraud_flag"],
            normalize="index"
        ) * 100
    )

    fraud_by_type = (
        fraud_by_type[1]
        .reset_index()
    )

    fraud_by_type.columns = [
        "Transaction Type",
        "Fraud Rate (%)"
    ]

    fig_fraud_type = px.bar(
        fraud_by_type,
        x="Transaction Type",
        y="Fraud Rate (%)",
        text_auto=".3f",
        title="Fraud Rate by Transaction Type"
    )

    # Charts

    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(
            fig_fraud,
            use_container_width=True
        )

    with col4:
        st.plotly_chart(
            fig_fraud_type,
            use_container_width=True
        )

    # Insights

    highest_risk_type = fraud_by_type.loc[
        fraud_by_type["Fraud Rate (%)"].idxmax(),
        "Transaction Type"
    ]
    st.subheader("📝 Observations")

    st.warning("""
• The platform maintains a very low fraud rate of only 0.192%.

• More than 99.8% of all transactions are legitimate.

• Recharge transactions exhibit the highest fraud rate (0.239%).

• P2P transactions show the lowest fraud occurrence (0.183%).

• Fraud incidents are concentrated in a few transaction categories, highlighting the need for focused risk monitoring.
""")
    st.subheader("📋 Risk Insights")

    st.warning(
        f"""
⚠️ Highest Risk Transaction Type: {highest_risk_type}

🛡️ Overall Fraud Rate: {fraud_rate:.3f}%

📊 Fraud transactions remain a very small percentage of total transactions.
        """
    )
# -----------------------------------
# GEOGRAPHIC ANALYSIS PAGE
# -----------------------------------

elif page == "📍 Geographic Analysis":

    st.header("📍 Geographic Analysis")

    # Revenue by State

    state_revenue = (
        filtered_df
        .groupby("sender_state")["amount (INR)"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    # Top 10 States

    top_10_states = state_revenue.head(10)

    fig_state = px.bar(
        top_10_states,
        x="amount (INR)",
        y="sender_state",
        orientation="h",
        text_auto=True,
        title="Top 10 Revenue Generating States"
    )

    st.plotly_chart(
        fig_state,
        use_container_width=True
    )

    # State Ranking Table

    st.subheader("🏆 State Revenue Ranking")

    ranking_df = state_revenue.copy()

    ranking_df.columns = [
        "State",
        "Revenue"
    ]

    st.dataframe(
        ranking_df,
        use_container_width=True
    )
    st.subheader("📝 Observations")

    st.info("""
• Maharashtra leads all states in revenue generation, contributing approximately ₹49.04M.

• Uttar Pradesh and Karnataka follow closely with strong transaction volumes.

• The top three states contribute a significant share of total platform revenue.

• Southern states demonstrate strong digital payment adoption.

• Revenue is well distributed across multiple regions, reducing dependence on any single state.
""")
    # Geographic Insights

    top_state = top_10_states.iloc[0]["sender_state"]

    top_revenue = top_10_states.iloc[0]["amount (INR)"]

    st.subheader("📋 Geographic Insights")

    st.info(
        f"""
📍 Highest Revenue State: {top_state}

💰 Revenue Generated: ₹{top_revenue:,.0f}

📊 Revenue is concentrated among a few leading states, indicating stronger digital payment adoption in these regions.
        """
    )    
    # -----------------------------------
# DEVICE ANALYSIS PAGE
# -----------------------------------

elif page == "📱 Device Analysis":

    st.header("📱 Device Analysis")

    # Device Distribution

    device_distribution = (
        filtered_df["device_type"]
        .value_counts()
        .reset_index()
    )

    device_distribution.columns = [
        "Device Type",
        "Count"
    ]

    fig_device = px.pie(
        device_distribution,
        names="Device Type",
        values="Count",
        hole=0.5,
        title="Device Usage Distribution"
    )

    # Revenue by Device

    device_revenue = (
        filtered_df
        .groupby("device_type")["amount (INR)"]
        .sum()
        .reset_index()
    )

    fig_revenue = px.bar(
        device_revenue,
        x="device_type",
        y="amount (INR)",
        text_auto=True,
        title="Revenue by Device Type"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            fig_device,
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            fig_revenue,
            use_container_width=True
        )

    # Average Transaction Value

    avg_device_amount = (
        filtered_df
        .groupby("device_type")["amount (INR)"]
        .mean()
        .reset_index()
    )

    fig_avg = px.bar(
        avg_device_amount,
        x="device_type",
        y="amount (INR)",
        text_auto=".0f",
        title="Average Transaction Value by Device"
    )

    st.plotly_chart(
        fig_avg,
        use_container_width=True
    )
    st.subheader("📝 Observations")

    st.success("""
• Android dominates the platform, accounting for approximately 75% of all users.

• Android users contribute the highest platform revenue.

• iOS users represent nearly 20% of users while generating substantial revenue.

• Web usage remains limited, indicating a strong preference for mobile transactions.

• Average transaction values are similar across Android, iOS, and Web devices.
""")
    # Insights

    top_device = device_distribution.iloc[0]["Device Type"]

    st.subheader("📋 Device Insights")

    st.success(
        f"""
📱 Most Used Device: {top_device}

💳 Mobile devices dominate digital payment transactions.

📊 Device preferences can help optimize user experience and marketing strategies.
        """
    )


# -----------------------------------
# INSIGHTS PAGE
# -----------------------------------

elif page == "💡 Insights":

    st.header("💡 Key Business Insights")

    st.success("""
### 1️⃣ Transaction Type Insights

• P2P transactions account for the largest share of transactions.

• Recharge transactions have the highest fraud rate among transaction types.

• Bill Payments and P2M transactions show strong transaction success rates.
""")

    st.info("""
### 2️⃣ Merchant Category Insights

• Shopping generates the highest revenue.

• Education has the highest average transaction value.

• Grocery contributes the largest transaction volume.
""")

    st.warning("""
### 3️⃣ Customer Insights

• Customers aged 26–35 generate the highest revenue.

• Digital payment adoption is strongest among young and middle-aged users.

• Older age groups contribute a smaller share of transaction value.
""")

    st.success("""
### 4️⃣ Geographic Insights

• Maharashtra is the top revenue-generating state.

• Uttar Pradesh and Karnataka are major contributors.

• Revenue is concentrated in a few highly active states.
""")

    st.info("""
### 5️⃣ Device Insights

• Android dominates transaction volume.

• Mobile devices drive the majority of digital payments.

• Average transaction values are similar across devices.
""")

    st.error("""
### 6️⃣ Fraud Insights

• Overall fraud rate is extremely low.

• Fraudulent transactions tend to have slightly higher transaction amounts.

• Recharge transactions show relatively higher fraud exposure.
""")
    
# -----------------------------------
# RECOMMENDATIONS PAGE
# -----------------------------------

elif page == "🎯 Recommendations":

    st.header("🎯 Business Recommendations")

    st.subheader("1. Fraud Prevention")

    st.write("""
    • Apply additional fraud monitoring on Recharge transactions.

    • Introduce real-time anomaly detection for suspicious transactions.

    • Strengthen authentication for high-value payments.
    """)

    st.subheader("2. Customer Growth")

    st.write("""
    • Target users aged 26–35 with loyalty programs.

    • Encourage higher adoption among older age groups.

    • Launch cashback campaigns for low-engagement users.
    """)

    st.subheader("3. Revenue Optimization")

    st.write("""
    • Focus promotional campaigns on Shopping and Education categories.

    • Partner with merchants in top-performing categories.

    • Create category-specific offers to increase transaction frequency.
    """)

    st.subheader("4. Geographic Expansion")

    st.write("""
    • Increase marketing in lower-performing states.

    • Replicate successful strategies from Maharashtra and Karnataka.

    • Develop regional merchant partnerships.
    """)

    st.subheader("5. Mobile Experience")

    st.write("""
    • Continue optimizing Android user experience.

    • Improve mobile payment speed and reliability.

    • Promote mobile-first features and offers.
    """)

    st.success("""
### Final Recommendation

Focus on high-value customer segments (26–35 age group), strengthen fraud monitoring for Recharge transactions, and expand successful revenue strategies from top-performing states to increase overall UPI transaction growth.
""")    


#     st.markdown("---")

# st.caption(
#     "UPI Transaction Analytics Dashboard | Built with Streamlit, Plotly & Python"
# )
