import streamlit as st
import pandas as pd
from ai_utils import analyze_tone, generate_response  # assume this is implemented

st.title("Excel-based Tone Analyzer & Responder")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    if all(col in df.columns for col in ["Username", "Product", "Comment"]):
        st.write("### Uploaded Data")
        st.dataframe(df)

        results = []

        for _, row in df.iterrows():
            user = row["Username"]
            product = row["Product"]
            comment = row["Comment"]

            try:
                tone = analyze_tone(comment)
                reply = generate_response(comment, tone, user, product)
            except Exception as e:
                tone = "Error"
                reply = str(e)

            results.append({
                "Username": user,
                "Product": product,
                "Comment": comment,
                "Detected Tone": tone,
                "AI Response": reply
            })

        st.write("### Results")
        result_df = pd.DataFrame(results)
        st.dataframe(result_df)
    else:
        st.error("Excel must contain columns: Username, Product, Comment")

