import pandas as pd

# Load your data
df = pd.read_csv("sample_data.csv")

# Provided dictionaries
dictionaries = {
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

# Function to label each row
def classify_text(text, dictionaries):
    text_lower = text.lower()
    labels = []

    for label, terms in dictionaries.items():
        if any(term in text_lower for term in terms):
            labels.append(label)

    return ", ".join(labels) if labels else "none"

# Apply classification
df["dictionary_label"] = df["Statement"].astype(str).apply(lambda x: classify_text(x, dictionaries))

# Save or display
df.to_csv("classified_output.csv", index=False)
df.head()
