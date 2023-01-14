import sqlite3
import os
from apscheduler.schedulers.blocking import BlockingScheduler

import os
import datetime

from helpers.constants import *
from helpers.instagram import *
from helpers.imagen import *
from helpers.quote import *
from helpers.logging import logger

if not os.path.exists(IMAGE_SAVE_PATH):
    os.makedirs(IMAGE_SAVE_PATH)


def scheduled_job():

    logger.info("starting the process")
    # Connect to the database
    conn = sqlite3.connect(QUOTES_DB)
    cursor = conn.cursor()

    # Create the quotes table if it doesn't exist

    logger.info("creating the quotes table if it doesn't exist")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS quotes (quote text)"
    )

    # Generate a quote and create the image

    logger.info("generating a quote")
    quote = get_quote()

    # Check if the quote has already been posted
    if has_quote_been_posted(quote) or len(quote) > 300 or not is_quote_in_en(quote):
        # If the quote has already been posted, try again
        scheduled_job()
        return

    logger.info("Todays Quote: " + quote)
    logger.info("analyze sentiment")
    sentiment = analyze_sentiment(quote)
    logger.info("generating image")
    filename = generate_image(quote, sentiment)
    logger.info("posting to instagram")
    post_to_instagram(quote, filename)
    logger.info("inserting quote to db")
    insert_quote_to_db(quote)
    logger.info("completed the process")


if __name__ == "__main__":
    if os.getenv("RUN_ONCE") == "1":
        scheduled_job()
    scheduler = BlockingScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(scheduled_job, 'interval', hours=int(os.getenv("POST_FREQUENCY_HOURS")),
                      start_date='2023-01-01 00:00:00',
                      misfire_grace_time=60*60*2)
    scheduler.start()
