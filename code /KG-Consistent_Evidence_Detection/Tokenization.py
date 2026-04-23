import nltk
import json
import yaml
import spacy
import string
from tqdm import tqdm
from nltk.corpus import stopwords
from collections import defaultdict
from transformers import BertTokenizer
from thefuzz import fuzz

# Load SpaCy's English tokenizer
#nlp = spacy.load("en_core_web_sm")

# Download NLTK stopwords
#nltk.download("stopwords")

# === Initialize BERT tokenizer ===
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

# === Load fake news JSON file ===
with open("filtered_LLAMA_FAKE_NEWS.json", "r") as f:
    fake_news_data = json.load(f)

# === Load KG triples YAML file ===
with open("triples_by_category.yaml", "r") as f:
    kg_data = yaml.safe_load(f)

# Function to clean token (remove subwords and special tokens)
def clean_token(token):
    return token.lstrip("##").strip().lower()

# Function to tokenize the entire text and return a list of clean tokens
def tokenize_text(text):
    if not isinstance(text, str):
        raise ValueError(f"Expected a string, but got {type(text)}: {text}")
    tokens = tokenizer.tokenize(text)
    return [clean_token(t) for t in tokens]

# Stopword removal function that also removes punctuation
def remove_stopwords_and_punctuation(tokens):
    stop_words = set(stopwords.words("english"))
    # Remove punctuation using string.punctuation
    #cleaned_tokens = [token for token in tokens if token not in stop_words and token not in string.punctuation]
    cleaned_tokens = [token for token in tokens if token not in string.punctuation]
    return cleaned_tokens

# Function to filter tokens while maintaining the original sequence
def filter_and_tokenize(fake_news_text):
    # Tokenize the fake news text
    fake_news_tokens = tokenize_text(fake_news_text)

    # Remove stopwords and punctuation from the tokens
    filtered_tokens = remove_stopwords_and_punctuation(fake_news_tokens)

    return fake_news_tokens, filtered_tokens

#====================================================================================
# Process the fake news data
#====================================================================================
# Prepare a dictionary to store the results
tokens_data = {} 
id=0

for entry in tqdm(fake_news_data, desc="Processing Fake News", unit="entry"): #for entry in fake_news_data[:1]:  # Process first entry (or all entries if needed)
    news_text = entry["fake_news"]
    id+=1
    
    # Get the tokens and filtered tokens after stopword removal
    fake_news_tokens, filtered_tokens = filter_and_tokenize(news_text)
    
    # print("Fake News:", news_text)
    # print("FakeNews_Tokens:", fake_news_tokens, "\n")
    # print("Filtered Tokens (after stopword removal):", filtered_tokens, "\n")
    # print("===============================================================================")
    
    # Store the tokens in the dictionary
    tokens_data[id] = {
        "fake_news": news_text,
        "tokens": fake_news_tokens,
        "filtered_tokens": filtered_tokens
    }

# Save the tokens data into a JSON file
with open("processed_fake_news_tokens.json", "w") as outfile:
    json.dump(tokens_data, outfile, indent=4)

print("Tokens have been processed and saved into 'processed_fake_news_tokens.json'.")
