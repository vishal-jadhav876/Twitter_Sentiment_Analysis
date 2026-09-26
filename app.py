import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit Page Configuration
st.set_page_config(page_title="Twitter Sentiment Analysis", layout="wide")

st.title("📊 Real-Time Sentiment Analysis Dashboard")
st.write("Analyze and visualize public sentiment on Twitter data in real-time.")

# 1. Text Cleaning Function (NLP Technique)
def clean_tweet(text):
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)  # Remove Mentions
    text = re.sub(r'#[A-Za-z0-9_]+', '', text)  # Remove Hashtags
    text = re.sub(r'RT[\s]+', '', text)  # Remove Retweets
    text = re.sub(r'[^\w\s]', '', text)  # Remove Punctuations
    text = text.lower().strip()  # Convert to lowercase
    return text

# 2. Sentiment Analysis Function (Using TextBlob)
def get_sentiment(text):
    analysis = TextBlob(text)
    # Polarity ranges from -1 (Negative) to +1 (Positive)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity == 0:
        return "Neutral"
    else:
        return "Negative"

def get_polarity(text):
    return TextBlob(text).sentiment.polarity

# Sidebar Options
st.sidebar.header("User Options")
data_option = st.sidebar.radio("Select Data Source:", ("Sample Live Dataset", "Enter Custom Tweet"))

if data_option == "Sample Live Dataset":
    st.subheader("📁 Analyzing Sample Twitter Dataset")

    # Mock Data (Twitter Data Format)
    mock_tweets = [
        "I love the new updates to the software! Extremely helpful and fast. #tech",
        "The service was terrible. Very disappointed with the customer support.",
        "It's an okay product. Nothing extraordinary, works fine.",
        "Great experience! Highly recommended for everyone. 👍",
        "Worst experience ever. Totally waste of money and time.",
        "The package arrived on time, but the quality is average.",
        "Fantastic application! Easy to use and super intuitive UI."
    ]

    df = pd.DataFrame(mock_tweets, columns=["Raw_Tweet"])
    
    # Cleaning & Sentiment Computation
    df["Cleaned_Tweet"] = df["Raw_Tweet"].apply(clean_tweet)
    df["Sentiment"] = df["Cleaned_Tweet"].apply(get_sentiment)
    df["Polarity"] = df["Cleaned_Tweet"].apply(get_polarity)

    # Key Metrics Display
    total_tweets = len(df)
    pos_count = (df["Sentiment"] == "Positive").sum()
    neu_count = (df["Sentiment"] == "Neutral").sum()
    neg_count = (df["Sentiment"] == "Negative").sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tweets", total_tweets)
    col2.metric("Positive", pos_count)
    col3.metric("Neutral", neu_count)
    col4.metric("Negative", neg_count)

    st.markdown("---")

    # Data & Visualizations
    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        st.subheader("Data Preview")
        st.dataframe(df[["Raw_Tweet", "Sentiment", "Polarity"]], use_container_width=True)

    with right_col:
        st.subheader("Sentiment Distribution")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(x="Sentiment", data=df, palette={"Positive": "#2ecc71", "Neutral": "#f1c40f", "Negative": "#e74c3c"}, ax=ax)
        plt.xlabel("Sentiment Category")
        plt.ylabel("Tweet Count")
        st.pyplot(fig)

elif data_option == "Enter Custom Tweet":
    st.subheader("📝 Analyze Individual Tweet / Text")
    
    user_input = st.text_area("Enter Tweet or Text here:", "This product is amazing and easy to use!")
    
    if st.button("Analyze Sentiment"):
        cleaned = clean_tweet(user_input)
        sentiment = get_sentiment(cleaned)
        polarity = get_polarity(cleaned)

        st.markdown(f"**Cleaned Text:** `{cleaned}`")
        
        if sentiment == "Positive":
            st.success(f"Result: **Positive** (Polarity Score: {polarity:.2f})")
        elif sentiment == "Neutral":
            st.info(f"Result: **Neutral** (Polarity Score: {polarity:.2f})")
        else:
            st.error(f"Result: **Negative** (Polarity Score: {polarity:.2f})")