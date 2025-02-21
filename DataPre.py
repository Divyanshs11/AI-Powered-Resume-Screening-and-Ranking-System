import re
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))
def clean_text(text):
    """Cleans text by removing numbers, special characters, and stopwords"""
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    words = text.lower().split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)
