"""CampusCare demo.

Two tools in one small app:
1. Symptom helper (keyword rules, not a medical diagnosis)
2. Student mentor flag (attendance and marks rules)
"""

import streamlit as st

from risk_analyzer import load_students, summary
from symptom_checker import check_symptoms, load_rules

st.set_page_config(page_title="CampusCare", page_icon=":material/health_and_safety:")
st.title("CampusCare")
st.caption("A rule-based campus helper for a first-year hackathon profile. Not a medical device.")

tab_health, tab_risk, tab_how = st.tabs(["Symptom helper", "Mentor flag", "How it works"])

with tab_health:
    st.subheader("Describe what you feel")
    text = st.text_input("Symptom", placeholder="fever and headache")
    if st.button("Check", type="primary"):
        result = check_symptoms(text)
        st.write("**Matched words:**", ", ".join(result["matched"]) or "none")
        st.write("**Category:**", result["category"])
        st.write("**What you can do:**", result["advice"])
        st.warning(result["see_doctor_if"])
        st.info("This only matches words from a local JSON file. It does not diagnose.")

with tab_risk:
    st.subheader("Who may need a mentor")
    students = load_students()
    stats = summary(students)
    c1, c2, c3 = st.columns(3)
    c1.metric("Students", stats["total"])
    c2.metric("Need a check-in", stats["at_risk"])
    c3.metric("Class average", stats["class_average"])
    st.dataframe(students, use_container_width=True)
    st.write("Rule: attendance below 75, or subject average below 40.")

with tab_how:
    st.subheader("What a reviewer can ask")
    st.markdown(
        """
- Input is a sentence or a CSV row.
- Symptoms are matched with `if keyword in sentence`.
- Marks use a loop over rows and a simple average.
- Unknown symptoms are appended to `data/unknown_queries.txt`.
- No model is trained. The "intelligence" is the rule file.
- Next step: replace keyword matching with a small classifier.
        """
    )
    st.write("Rules currently loaded:", ", ".join(load_rules().keys()))
