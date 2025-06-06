import streamlit as st
import pandas as pd
from ai_utils import analyze_tone, generate_response, send_email

st.title("📊 Tone Analyzer & Auto-Responder (Email Enabled)")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    if all(col in df.columns for col in ["Username", "Email", "Product", "Comment"]):
        st.write("### ✅ Uploaded Data")
        st.dataframe(df)

        results = []

        for _, row in df.iterrows():
            user = row["Username"]
            email = row["Email"]
            product = row["Product"]
            comment = row["Comment"]

            try:
                tone = analyze_tone(comment)
                reply = generate_response(comment, tone, user, product)

                # Send email
                subject = f"Response to your feedback on {product}"
                send_email(email, subject, reply)

            except Exception as e:
                tone = "Error"
                reply = f"Error: {e}"

            results.append({
                "Username": user,
                "Email": email,
                "Product": product,
                "Comment": comment,
                "Detected Tone": tone,
                "AI Response": reply
            })

        st.write("### 🧾 Results with Emails Sent")
        result_df = pd.DataFrame(results)
        st.dataframe(result_df)
    else:
        st.error("Excel must contain columns: Username, Email, Product, Comment")


