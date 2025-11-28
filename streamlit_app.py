import streamlit as st
import pandas as pd
import ast

st.title("🔍 Text Classification with Custom Dictionaries")

# ---------------------------
# Default dictionaries
# ---------------------------
default_dictionaries = {
    'urgency_marketing': {
        'limited', 'limited time', 'limited run', 'limited edition', 'order now',
        'last chance', 'hurry', 'while supplies last', 'before they\'re gone',
        'selling out', 'selling fast', 'act now', 'don\'t wait', 'today only',
        'expires soon', 'final hours', 'almost gone'
    },

    'exclusive_marketing': {
        'exclusive', 'exclusively', 'exclusive offer', 'exclusive deal',
        'members only', 'vip', 'special access', 'invitation only',
        'premium', 'privileged', 'limited access', 'select customers',
        'insider', 'private sale', 'early access'
    }
}


# ---------------------------
# Helper Function
# ---------------------------
def classify_text(text, dictionaries):
    text_lower = text.lower()
    labels = []

    for label, terms in dictionaries.items():
        if any(term in text_lower for term in terms):
            labels.append(label)

    return ", ".join(labels) if labels else "none"


# ---------------------------
# Upload Section
# ---------------------------
st.header("📁 Upload Dataset")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# ---------------------------
# Dictionary Editing Section
# ---------------------------
st.header("🛠 Edit Dictionaries")

dict_text = st.text_area(
    "Modify the classification dictionaries below. Use Python dictionary syntax.",
    value=str(default_dictionaries),
    height=300
)

try:
    user_dictionaries = ast.literal_eval(dict_text)
    if not isinstance(user_dictionaries, dict):
        st.error("The dictionary must be a Python dict object.")
        user_dictionaries = default_dictionaries
except Exception:
    st.error("Invalid dictionary format. Reverting to default.")
    user_dictionaries = default_dictionaries


# ---------------------------
# Classification Section
# ---------------------------
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Preview of Uploaded Data", df.head())

    text_column = st.selectbox(
        "Select the column containing text to classify:",
        df.columns
    )

    if st.button("Run Classification"):
        df["dictionary_label"] = df[text_column].astype(str).apply(
            lambda x: classify_text(x, user_dictionaries)
        )

        st.success("Classification complete!")
        st.write(df.head())

        # Download button
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Classified CSV",
            csv,
            "classified_output.csv",
            "text/csv"
        )
