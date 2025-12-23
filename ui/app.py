import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from main import PromptInjectionSystem

st.set_page_config(page_title="Prompt Injection Detection", layout="centered")

st.title("Prompt Injection Detection System")
st.write("Analyze user prompts for potential prompt injection attacks.")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(base_dir, "data", "prompts.csv")

system = PromptInjectionSystem(data_path=data_path)
def clear_prompt():
    st.session_state.prompt_input = ""

prompt = st.text_area(
    "Enter a prompt to analyze",
    height=120,
    key="prompt_input"
)

btn_left, btn_right = st.columns([6, 1])

with btn_left:
    analyze_clicked = st.button("Analyze")

with btn_right:
    st.button("Clear", on_click=clear_prompt)

if analyze_clicked:
    if prompt.strip() == "":
        st.warning("Please enter a prompt")
    else:
        result = system.analyze_prompt(prompt)     

        if result["is_malicious"]:
            st.error("❌ Potential Prompt Injection Detected")
        else:
            st.success("✅ Prompt Appears Safe")
        st.caption("Decision rule: prompts are flagged only when risk is HIGH (confidence ≥ 0.7)")
        st.subheader("Detection Details")
        st.write("Method:", result["method"])
        st.write("Attack Type:", result.get("attack_type", "N/A"))
        risk = result.get("risk_level", "N/A")

        if risk == "HIGH":
            st.markdown("**Risk Level:** 🔴 HIGH")
        elif risk == "MEDIUM":
            st.markdown("**Risk Level:** 🟠 MEDIUM")
        else:
            st.markdown("**Risk Level:** 🟢 LOW")
        confidence = float(result["confidence"])

        if confidence >= 0.7:
            st.write("Model Assessment: High uncertainty (potentially malicious)")
        elif confidence >= 0.4:
            st.write("Model Assessment: Medium uncertainty")
        else:
            st.write("Model Assessment: Low uncertainty (safe)")

        with st.expander("Show technical details"):
            st.write("Model Uncertainty Score:", confidence)
            st.progress(confidence)
            st.caption("Lower values indicate lower likelihood of malicious intent")

        st.subheader("Explanation")
        st.write(result["reason"])

import os
import pandas as pd
import streamlit as st

show_logs = st.checkbox("Show recent activity")

if show_logs:
    log_file = os.path.join(base_dir, "logs", "prompt_logs.csv")

    if os.path.exists(log_file):
        logs = pd.read_csv(log_file)

        if not logs.empty:
            count = st.number_input(
                "Show last records",
                min_value=1,
                max_value=len(logs),
                value=min(5, len(logs)),
                step=1
            )

            safe_count = min(count, len(logs))
            recent_logs = logs.tail(safe_count).reset_index(drop=True)
            recent_logs.index = recent_logs.index + 1
            st.dataframe(recent_logs)

        else:
            st.write("No logs available yet.")
    else:
        st.write("Log file not found.")

