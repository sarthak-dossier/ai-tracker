import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# Page config
st.set_page_config(page_title="📚 Study Tracker", layout="wide")

# 💡 Centered custom title
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>📘 MADE BY SARTHAK</h1>
""", unsafe_allow_html=True)

st.markdown("## 📈 Study Time & Productivity Tracker")
# Load data
try:
    df = pd.read_csv("data.csv")
except:
    df = pd.DataFrame(columns=["Date", "Hours_Studied", "Tasks_Completed", "Mood"])

# 🎯 Input Section
st.markdown("---")
st.markdown("### 📆 Log Today's Study")
col1, col2, col3 = st.columns(3)

with col1:
    today = st.date_input("📅 Select Date", value=date.today())
with col2:
    hours = st.slider("⏱️ Hours Studied", 0, 16, 2)
with col3:
    tasks = st.number_input("✅ Tasks Completed", min_value=0, max_value=20, step=1)

mood = st.selectbox("🧠 Mood Today", ["😄 Happy", "😐 Neutral", "😞 Tired", "🔥 Motivated"])

# 💾 Save entry
if st.button("💾 Save Entry"):
    new_row = {"Date": today, "Hours_Studied": hours, "Tasks_Completed": tasks, "Mood": mood}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("data.csv", index=False)
    st.success("✅ Your entry has been saved successfully!")

# 📊 Show Log
st.markdown("---")
st.markdown("### 📋 Your Productivity Log")
st.dataframe(df, use_container_width=True)

# 📈 Charts & Analytics
st.markdown("---")
st.markdown("### 📊 Study Analytics")

df["Date"] = pd.to_datetime(df["Date"])
df_sorted = df.sort_values("Date")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(df_sorted, x="Date", y="Hours_Studied", title="📈 Hours Studied Over Time", markers=True)
    fig1.update_layout(title_font=dict(size=20), plot_bgcolor="white")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(df_sorted, x="Date", y="Tasks_Completed", title="📊 Tasks Completed Over Time", color="Tasks_Completed")
    fig2.update_layout(title_font=dict(size=20), plot_bgcolor="white")
    st.plotly_chart(fig2, use_container_width=True)

# 🧁 Mood Pie Chart
fig3 = px.pie(values=df["Mood"].value_counts().values,
              names=df["Mood"].value_counts().index,
              title="🧁 Mood Distribution")
fig3.update_traces(textinfo='percent+label')
st.plotly_chart(fig3, use_container_width=True)
