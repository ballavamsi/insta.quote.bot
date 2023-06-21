import os
from dotenv import load_dotenv
load_dotenv()

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

QUOTES_URL = os.getenv('QUOTES_URL')
COLORNAMES_URL = os.getenv('COLORNAMES_URL')
MAX_API_PAGENO = int(os.getenv('MAX_API_PAGENO'))
FONT_FAMILY_PATH = os.getenv('FONT_FAMILY_PATH')

IMAGE_SAVE_PATH = os.getenv('IMAGE_SAVE_PATH')
DOCKER_IMAGE_SAVE_PATH = os.getenv('DOCKER_IMAGE_SAVE_PATH')
IMAGE_WIDTH = int(os.getenv('IMAGE_WIDTH'))
IMAGE_HEIGHT = int(os.getenv('IMAGE_HEIGHT'))
CIRCLES = os.getenv('CIRCLES')
BLUR_PERCENT = int(os.getenv('BLUR_PERCENT'))
QUOTES_DB = os.getenv('QUOTES_DB')
TWO_COLOR_TONE = str2bool(os.getenv('TWO_COLOR_TONE'))
LINES_EQUAL_SPACES = str2bool(os.getenv('LINES_EQUAL_SPACES'))
FONT_SIZE = int(os.getenv('FONT_SIZE'))
FONT_FAMILY = os.getenv('FONT_FAMILY')
COLORS = os.getenv('COLORS').split(',')
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')
WAIT_TIME = int(os.getenv('WAIT_TIME'))
BROWSER_TYPE = os.getenv('BROWSER_TYPE')
SELENIUM_URL = os.getenv('SELENIUM_URL')
INSTAGRAM_POST = os.getenv('INSTAGRAM_POST')
