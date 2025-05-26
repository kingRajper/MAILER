import streamlit as st
from pipeline import build_email_graph

graph = build_email_graph()

st.title("📬 MAILER - Email Assistant")

with st.form("email_form"):
    sender = st.text_input("Sender Email", "test@example.com")
    subject = st.text_input("Subject", "Sample Subject")
    body = st.text_area("Email Body", "Dear Sir/Madam, ...")
    submitted = st.form_submit_button("Process Email")

if submitted:
    email = {
        "sender": sender,
        "subject": subject,
        "body": body
    }
    result = graph.invoke({
        "email": email,
        "is_spam": None,
        "spam_reason": None,
        "email_category": None,
        "email_draft": None,
        "messages": []
    })

    if result.get("is_spam"):
        st.warning("🚫 This email was classified as SPAM.")
        st.write(f"**Reason**: {result.get('spam_reason')}")
    else:
        st.success("✅ Legitimate email.")
        st.write(f"**Category**: {result.get('email_category')}")
        st.markdown("### ✉ Drafted Response")
        st.code(result.get("email_draft"), language="markdown")
