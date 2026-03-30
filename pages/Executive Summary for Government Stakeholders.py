import streamlit as st
from src.executive_summary import get_executive_summary
from utils.report_generator import generate_executive_pdf

# --- 0. Authentication Guard ---
#if not st.session_state.get('authentication_status'):
    #st.switch_page("app.py")

st.title("📄 Executive Summary for Government Stakeholders")

summary = get_executive_summary()

st.header(summary["title"])

st.subheader("🎯 Objective")
st.write(summary["objective"])

st.subheader("📊 Key Outcomes")
for item in summary["key_outcomes"]:
    st.markdown(f"- {item}")

st.subheader("🧠 Methodology")
for item in summary["methodology"]:
    st.markdown(f"- {item}")

st.subheader("📈 Key Insights")
for item in summary["key_insights"]:
    st.markdown(f"- {item}")

st.subheader("💼 Business Impact")
for item in summary["business_impact"]:
    st.markdown(f"- {item}")

st.subheader("🏛️ Policy Impact")
for item in summary["policy_impact"]:
    st.markdown(f"- {item}")

st.subheader(" Conclusion")
st.write(summary["conclusion"])

# --- PDF Download Logic ---
pdf_buffer = generate_executive_pdf(summary)

st.download_button(
    label="📥 Download Executive Summary (PDF)",
    data=pdf_buffer.getvalue(),
    file_name="Bank_Churn_Executive_Summary.pdf",
    mime="application/pdf"
)