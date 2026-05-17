import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

from news_feed import get_finance_news
from expense_manager import add_expense, get_all_expenses, get_monthly_expenses, delete_expense
from budget_engine import analyze_budget
from ai_advisor import get_financial_advice, get_chat_response

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Finance Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }

    .main { background-color: #0f1117; }

    .metric-card {
        background: linear-gradient(135deg, #1e2130, #252a3a);
        border-radius: 16px;
        padding: 20px 24px;
        border: 1px solid #2e3350;
        margin-bottom: 12px;
    }

    .metric-label {
        color: #8b93b0;
        font-size: 13px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
    }

    .metric-sub {
        color: #5ce0a0;
        font-size: 13px;
        margin-top: 4px;
    }

    .alert-danger {
        background: linear-gradient(135deg, #3d1a1a, #4a1f1f);
        border-left: 4px solid #ff4f4f;
        border-radius: 8px;
        padding: 14px 18px;
        color: #ff9090;
        font-weight: 500;
    }

    .alert-warning {
        background: linear-gradient(135deg, #3d2e10, #4a3815);
        border-left: 4px solid #ffb74d;
        border-radius: 8px;
        padding: 14px 18px;
        color: #ffd580;
        font-weight: 500;
    }

    .alert-success {
        background: linear-gradient(135deg, #0d2e20, #0f3827);
        border-left: 4px solid #5ce0a0;
        border-radius: 8px;
        padding: 14px 18px;
        color: #5ce0a0;
        font-weight: 500;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 2px solid #2e3350;
    }

    .chat-user {
        background: #1e3a5f;
        border-radius: 12px 12px 2px 12px;
        padding: 10px 14px;
        margin: 6px 0;
        color: #cfe2ff;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
    }

    .chat-bot {
        background: #1e2130;
        border-radius: 12px 12px 12px 2px;
        padding: 10px 14px;
        margin: 6px 0;
        color: #e0e6f0;
        max-width: 85%;
        border-left: 3px solid #5ce0a0;
    }

    .news-item {
        padding: 8px 0;
        border-bottom: 1px solid #2e3350;
        color: #c0c8e0;
        font-size: 14px;
    }

    .news-item a {
        color: #7eb8ff;
        text-decoration: none;
    }

    .news-item a:hover {
        color: #5ce0a0;
    }

    div[data-testid="stSidebar"] {
        background: #090c14;
        border-right: 1px solid #1e2130;
    }

    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        font-family: 'Space Grotesk', sans-serif;
        padding: 8px 20px;
        transition: all 0.2s;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #60a5fa, #3b82f6);
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_income" not in st.session_state:
    st.session_state.last_income = 0
if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💰 Finance Manager")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["📊 Dashboard", "➕ Add Expense", "📋 Expense History", "🤖 AI Advisor Chat", "📰 Finance News"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("### 💼 Monthly Income")
    income = st.number_input("Set your monthly income (₹)", min_value=0, step=500, value=st.session_state.last_income)
    if income:
        st.session_state.last_income = income
    st.markdown("---")
    st.caption("Smart Finance Management System for Students")

# ── DASHBOARD ─────────────────────────────────────────────────────────────────
if page == "📊 Dashboard":
    st.markdown('<div class="section-title">📊 Dashboard</div>', unsafe_allow_html=True)

    total, percent, status, category_breakdown = analyze_budget(income)
    st.session_state.last_analysis = (total, percent, status, category_breakdown)

    # Metric cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Monthly Income</div>
            <div class="metric-value">₹{income:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Spent (This Month)</div>
            <div class="metric-value">₹{total:,.2f}</div>
            <div class="metric-sub">{percent:.1f}% of income</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        remaining = max(income - total, 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Remaining Balance</div>
            <div class="metric-value">₹{remaining:,.2f}</div>
        </div>""", unsafe_allow_html=True)

    # Status alert
    st.markdown("<br>", unsafe_allow_html=True)
    if "Overspending" in status:
        st.markdown(f'<div class="alert-danger">{status}</div>', unsafe_allow_html=True)
    elif "Warning" in status:
        st.markdown(f'<div class="alert-warning">{status}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-success">{status}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts
    if category_breakdown:
        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("**Spending by Category**")
            fig_pie = px.pie(
                names=list(category_breakdown.keys()),
                values=list(category_breakdown.values()),
                color_discrete_sequence=px.colors.sequential.Blues_r,
                hole=0.4
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#c0c8e0",
                legend=dict(font=dict(color="#c0c8e0")),
                margin=dict(t=20, b=20)
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_right:
            st.markdown("**Income vs Spending**")
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=["Income", "Spent", "Remaining"],
                y=[income, total, remaining],
                marker_color=["#3b82f6", "#f87171", "#5ce0a0"],
                text=[f"₹{v:,.0f}" for v in [income, total, remaining]],
                textposition="auto"
            ))
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#c0c8e0",
                showlegend=False,
                margin=dict(t=20, b=20),
                xaxis=dict(gridcolor="#2e3350"),
                yaxis=dict(gridcolor="#2e3350")
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        # Spending over time
        df_all = get_all_expenses()
        if not df_all.empty:
            st.markdown("**Spending Over Time**")
            df_all["date"] = pd.to_datetime(df_all["date"])
            daily = df_all.groupby("date")["amount"].sum().reset_index()
            fig_line = px.line(
                daily, x="date", y="amount",
                color_discrete_sequence=["#3b82f6"],
                markers=True
            )
            fig_line.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#c0c8e0",
                xaxis=dict(gridcolor="#2e3350"),
                yaxis=dict(gridcolor="#2e3350"),
                margin=dict(t=20, b=20)
            )
            st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("No expenses recorded this month. Add some expenses to see charts!")

# ── ADD EXPENSE ────────────────────────────────────────────────────────────────
elif page == "➕ Add Expense":
    st.markdown('<div class="section-title">➕ Add Expense</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox(
            "Category",
            ["🍔 Food", "🚌 Travel", "🏠 Rent", "📚 Education", "🎮 Entertainment", "🛒 Shopping", "💊 Health", "📦 Other"]
        )
    with col2:
        amount = st.number_input("Amount (₹)", min_value=1, step=10)

    note = st.text_input("Note (optional)", placeholder="e.g. Lunch at college canteen")

    if st.button("➕ Add Expense", use_container_width=True):
        try:
            add_expense(category, amount)
            st.success(f"✅ Added ₹{amount} for {category} successfully!")
            st.balloons()
        except ValueError as e:
            st.error(str(e))

# ── EXPENSE HISTORY ────────────────────────────────────────────────────────────
elif page == "📋 Expense History":
    st.markdown('<div class="section-title">📋 Expense History</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["This Month", "All Time"])

    with tab1:
        df_month = get_monthly_expenses()
        if df_month.empty:
            st.info("No expenses recorded this month.")
        else:
            df_display = df_month.rename(columns={"date": "Date", "category": "Category", "amount": "Amount (₹)"}).reset_index(drop=True)
            df_display["Amount (₹)"] = df_display["Amount (₹)"].apply(lambda x: f"₹{x:,.2f}")
            st.table(df_display)
            st.markdown(f"**Total this month: ₹{df_month['amount'].sum():,.2f}**")

    with tab2:
        df_all = get_all_expenses()
        if df_all.empty:
            st.info("No expenses recorded yet.")
        else:
            df_display = df_all.rename(columns={"date": "Date", "category": "Category", "amount": "Amount (₹)"}).reset_index(drop=True)
            df_display["Amount (₹)"] = df_display["Amount (₹)"].apply(lambda x: f"₹{x:,.2f}")
            st.table(df_display)
            st.markdown(f"**Total all time: ₹{df_all['amount'].sum():,.2f}**")

            st.markdown("---")
            st.markdown("**Delete an expense:**")
            del_index = st.number_input("Row number to delete (0-indexed)", min_value=0, max_value=max(len(df_all)-1, 0), step=1)
            if st.button("🗑️ Delete Selected Expense"):
                try:
                    delete_expense(del_index)
                    st.success("Expense deleted successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(str(e))

# ── AI ADVISOR CHAT ────────────────────────────────────────────────────────────
elif page == "🤖 AI Advisor Chat":
    st.markdown('<div class="section-title">🤖 AI Financial Advisor</div>', unsafe_allow_html=True)

    if income == 0:
        st.warning("Please set your monthly income in the sidebar first.")
    else:
        total, percent, status, category_breakdown = analyze_budget(income)

        col1, col2 = st.columns([2, 1])

        with col2:
            st.markdown("**Your Snapshot**")
            st.metric("Income", f"₹{income:,.0f}")
            st.metric("Spent", f"₹{total:,.2f}")
            st.metric("Status", "⚠️ Over" if percent > 100 else ("🔶 Alert" if percent > 80 else "✅ OK"))

            if st.button("🔄 Get Fresh Tips"):
                with st.spinner("Thinking..."):
                    advice = get_financial_advice(income, total, status, category_breakdown)
                st.info(advice)

        with col1:
            st.markdown("**Chat with your AI Advisor**")

            # Display chat history
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-user">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-bot">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

            user_input = st.text_input("Ask anything about your finances...", key="chat_input", placeholder="e.g. How can I save more on food?")

            col_send, col_clear = st.columns([3, 1])
            with col_send:
                if st.button("Send 💬", use_container_width=True):
                    if user_input.strip():
                        st.session_state.chat_history.append({"role": "user", "content": user_input})
                        with st.spinner("Advisor is thinking..."):
                            reply = get_chat_response(income, total, status, category_breakdown, st.session_state.chat_history, user_input)
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                        st.rerun()
            with col_clear:
                if st.button("Clear", use_container_width=True):
                    st.session_state.chat_history = []
                    st.rerun()

# ── FINANCE NEWS ───────────────────────────────────────────────────────────────
elif page == "📰 Finance News":
    st.markdown('<div class="section-title">📰 Latest Finance News</div>', unsafe_allow_html=True)

    with st.spinner("Loading latest news..."):
        news = get_finance_news()

    cols = st.columns(len(news))
    for col, (category, headlines) in zip(cols, news.items()):
        with col:
            st.markdown(f"**{category}**")
            for item in headlines:
                st.markdown(
                    f'<div class="news-item">• <a href="{item["link"]}" target="_blank">{item["title"]}</a></div>',
                    unsafe_allow_html=True
                )