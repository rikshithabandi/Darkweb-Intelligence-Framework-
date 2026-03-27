import re
import spacy
from nltk.sentiment import SentimentIntensityAnalyzer
from django.core.mail import send_mail

nlp = spacy.load("en_core_web_sm")
sia = SentimentIntensityAnalyzer()

SUSPICIOUS_WORDS = [
    "hack", "ransomware", "bitcoin", "exploit", "weapon", 
    "drug", "credit card", "leak", "passport", "sell data", "botnet"
]

def compute_threat_score(text):
    text = text.lower()
    word_hits = sum(1 for w in SUSPICIOUS_WORDS if w in text)
    
    # named entities count
    doc = nlp(text)
    entity_count = len([ent for ent in doc.ents if ent.label_ in ["PERSON", "ORG", "MONEY", "GPE"]])
    
    # tone score
    sentiment = sia.polarity_scores(text)
    neg_score = sentiment["neg"] * 100
    
    # overall weighted score
    threat_score = min(100, (word_hits * 8) + (entity_count * 4) + neg_score)
    return round(threat_score, 2)

def send_threat_alert(url, score):
    subject = f"⚠️ High Threat Alert: {url}"
    message = f"Threat score: {score}\nImmediate review required!"
    send_mail(subject, message, "ayushtiwari.creatorslab@gmail.com", ["reethu120824@gmail.com"])
