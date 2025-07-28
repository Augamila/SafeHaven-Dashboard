import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Load credentials
cred = credentials.Certificate("firebase-service-account.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load campaign data
def get_campaigns():
    docs = db.collection('artifacts/safehaven-app/public/data/campaigns').stream()
    return [doc.to_dict() for doc in docs]

st.set_page_config(page_title="SafeHaven Dashboard", layout="centered")
st.title("📊 SafeHaven Admin Dashboard")

campaigns = get_campaigns()
if not campaigns:
    st.warning("No campaigns found.")
else:
    for c in campaigns:
        st.subheader(c.get('title', 'Untitled'))
        st.write(f"Goal: ${c.get('goalAmount', 0)} | Raised: ${c.get('currentAmount', 0)}")
        progress = c.get('currentAmount', 0) / c.get('goalAmount', 1)
        st.progress(min(progress, 1.0))
