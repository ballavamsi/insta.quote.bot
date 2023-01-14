import random
from bs4 import BeautifulSoup
import requests
from better_profanity import profanity
from textblob import TextBlob
import sqlite3
import langdetect

from .constants import *
from .logging import logger


def get_quote():
    return get_random_tag_quote()
    page = random.randint(1, MAX_API_PAGENO)
    # Make a request to the website to get the quotes for the current page
    response = requests.get(QUOTES_URL, params={"page": page})
    return get_quote_from_page(response.text)


def get_quote_from_page(html):
    quotes = []
    # Parse the HTML using Beautiful Soup
    soup = BeautifulSoup(html, "html.parser")

    # Extract the quotes from the HTML
    quote_elements = soup.select(".quoteText")
    for quote_element in quote_elements:
        quote_text = quote_element.get_text().strip()
        quotes.append(profanity.censor(quote_text))
    if len(quotes) == 0:
        return get_quote()
    return random.choice(quotes)


def get_random_tag_quote():
    # Make a request to the website to get the quotes for the current page

    response = requests.get(QUOTES_URL)
    html = response.text

    # Parse the HTML using Beautiful Soup
    soup = BeautifulSoup(html, "html.parser")

    # Extract the quotes from the HTML
    all_tags = soup.select(".greyText a")
    random_href = random.choice(all_tags).attrs["href"]
    tag_url = QUOTES_URL + random_href.replace("/quotes", "")

    # Make a request to the website to get the quotes for the current page
    page = random.randint(1, 100)
    response = requests.get(tag_url, params={"page": page})
    return get_quote_from_page(response.text)


def analyze_sentiment(quote):
    # Analyze the sentiment of the quote using TextBlob
    quote_blob = TextBlob(quote)

    # Get the sentiment of the quote
    sentiment = quote_blob.sentiment.polarity

    # Classify the quote based on its sentiment
    if sentiment > 0.5:
        return "happy"
    elif sentiment > 0:
        return "motivational"
    elif sentiment == 0:
        return "neutral"
    elif sentiment > -0.5:
        return "sad"
    else:
        return "mental health"


def has_quote_been_posted(quote):
    # Connect to the database
    conn = sqlite3.connect(QUOTES_DB)
    cursor = conn.cursor()

    # Check if the quote has already been posted
    cursor.execute(
        "SELECT * FROM quotes WHERE quote=?", (quote,)
    )
    return cursor.fetchone() is not None


def insert_quote_to_db(quote):
    # Connect to the database
    conn = sqlite3.connect(QUOTES_DB)
    cursor = conn.cursor()

    # Insert the quote into the database
    cursor.execute("INSERT INTO quotes VALUES (?)",
                   (quote,))
    conn.commit()
    logger.info("Inserted quote to db")


def is_quote_in_en(quote):
    # Analyze the sentiment of the quote using TextBlob
    lang_of_quote = langdetect.detect(quote)
    if lang_of_quote == 'en':
        logger.info("Quote is in English")
        return True
    else:
        logger.info("Quote is not in English")
        return False
