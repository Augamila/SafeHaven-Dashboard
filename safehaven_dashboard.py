import streamlit as st
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase credentials securely from Streamlit Secrets
firebase_creds = json.loads(st.secrets["firebase"])
cred = credentials.Certificate(firebase_creds)
firebase_admin.initialize_app(cred)

db = firestore.client()

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
        progress = c.get('currentAmount', 0) / max(c.get('goalAmount', 1), 1)
        st.progress(min(progress, 1.0))
