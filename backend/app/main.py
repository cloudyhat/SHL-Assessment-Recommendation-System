import sys
import torch
# to avoid pytorch errors when importing streamlit.
sys.modules["torch.classes"] = None

import streamlit as st
from query import recommend_assessments

st.title("SHL Assessment Recommendation System")

user_input = st.text_area("Enter job description or query:")

if st.button("Recommend"):
    if user_input:
        recommendations = recommend_assessments(user_input, top_k=10)
        for idx, rec in enumerate(recommendations, 1):
            content = rec.page_content
            if "URL:" in content:
                parts = content.split("URL:")
                st.markdown(f"**{idx}.** {parts[0].strip()} [Link]({parts[1].strip()})")
            else:
                st.write(f"{idx}. {content}")
    else:
        st.warning("Please enter a query.")