from transformers import pipeline

print("Loading FinBERT model (this may take a minute the first time)...")
# Initialize the FinBERT pipeline
# We use the ProsusAI/finbert model which categorizes into: positive, negative, neutral
sentiment_analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def analyze_post_sentiment(text):
    """
    Analyzes text using FinBERT and returns the sentiment label and confidence score.
    """
    # Clean up the text a bit (remove newlines)
    clean_text = text.replace('\n', ' ').strip()
    
    # BERT models have a hard limit of 512 "tokens" (roughly 400 words).
    # To prevent errors, we will truncate the text to the first 1500 characters.
    # Usually, the main "thesis" of a stock pitch is in the beginning anyway.
    if len(clean_text) > 1500:
        clean_text = clean_text[:1500]
        
    # If the post is completely empty (e.g., just a title with an image), handle it
    if not clean_text:
        return "neutral", 0.0

    try:
        # Run the text through the model
        result = sentiment_analyzer(clean_text)[0]
        
        # Extract label and score
        label = result['label']  # Will be 'positive', 'negative', or 'neutral'
        score = result['score']  # Confidence score between 0.0 and 1.0
        
        return label, round(score, 3)
        
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return "neutral", 0.0

# --- Let's test it with some dummy Reddit data ---
if __name__ == "__main__":
    # Example 1: Clear Bullish Sentiment
    post_1 = "Huge news for $ASTS today. They just secured funding and the tech is proven. I'm loading up on calls, this is going to the moon!"
    
    # Example 2: Clear Bearish Sentiment
    post_2 = "Honestly $MULN is a massive scam. CEO keeps diluting shares, earnings were terrible, and cash burn is out of control. Avoid at all costs."
    
    # Example 3: Unrelated/Neutral Analysis
    post_3 = "Can someone explain how options decay works? I have some $AAPL shares but I don't understand the Greeks at all."
    
    for idx, post in enumerate([post_1, post_2, post_3], 1):
        label, confidence = analyze_post_sentiment(post)
        print(f"Post {idx} Sentiment: {label.upper()} (Confidence: {confidence})")
        print(f"Text: '{post}'\n")