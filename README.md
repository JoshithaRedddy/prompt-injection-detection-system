# Prompt Injection Detection System

This project is a simple but practical attempt to understand and detect **prompt injection attacks** in applications that use Large Language Models (LLMs).

The idea behind this project is to act as a **security layer** that checks user prompts *before* they are sent to an AI model, and flags inputs that look suspicious or risky.


## Motivation

Prompt injection is becoming a real problem in AI systems.  
Users can sometimes manipulate prompts to:

- Ignore system instructions  
- Bypass safety rules  
- Extract hidden or restricted information  

While many AI applications focus on generating responses, this project focuses on **analyzing the input itself** and deciding whether it is safe to proceed.


## What this system does

The system checks a user’s prompt and answers questions like:

- Does this prompt look like a prompt injection attempt?
- How risky is it if we allow this prompt?
- Why was it classified this way?

Instead of just saying *safe* or *unsafe*, the system explains its decision in a way that is easy to understand.


## How detection works (in simple terms)

The system uses **two approaches**:

### 1. Rule-based detection  
Known prompt injection patterns (for example, instruction overrides or role manipulation) are checked first.  
If a prompt matches one of these patterns, it is immediately flagged.

### 2. Machine learning detection  
If no rule matches, a machine learning model analyzes the prompt based on similarity to previously seen safe and malicious examples.  
This helps detect subtle or unseen attacks.

The final output includes:
- Detection method used  
- Attack type (if identifiable)  
- Risk level (LOW / MEDIUM / HIGH)  
- Explanation  
- Model uncertainty (for transparency)


## User Interface

The project includes a Streamlit-based interface where:

- Users can enter prompts manually  
- Results are shown clearly with risk level and explanation  
- Confidence values are explained to avoid confusion  
- Previous activity can be viewed for review  

The UI is intentionally kept simple and clean.


## Tech Stack

- Python  
- Streamlit  
- Scikit-learn  
- Pandas  

No external APIs are required.


## How to run the project

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run ui/app.py
