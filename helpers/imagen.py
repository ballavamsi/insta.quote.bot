import random
import textwrap
from .constants import *
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import time
import datetime
from better_profanity import profanity
from .logging import logger


def generate_abstract_image(sentiment=''):
    colors = get_colors_based_on_sentiment(sentiment)
    # trail
    image = create_gradient_image0(colors, (IMAGE_WIDTH, IMAGE_HEIGHT))
    return image
    # Get a drawing context
    draw = ImageDraw.Draw(image)

    circles = generate_circles(colors=colors)
    for x, y, radius, color in circles:
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)

    return image


def get_colors_based_on_sentiment(sentiment=''):

    return [x.upper() for x in COLORS]

    # Make a request to the Color API to get a list of colors based on the sentiment
    url = f'{COLORNAMES_URL}{sentiment}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the background color of the .freshButton elements
    buttons = soup.select('.freshButton')
    colors = [button['style'].split(':')[1].upper() for button in buttons]
    return colors


def generate_circles(colors=[]):
    # Generate random circles and colors
    circles = []
    for i in range(CIRCLES):
        color = random.choice(colors)
        radius = random.randint(50, IMAGE_HEIGHT/2)
        x, y = random.randint(0, IMAGE_WIDTH), random.randint(0, IMAGE_HEIGHT)

        overlap = False
        for j in range(i):
            dx = x - circles[j][0]
            dy = y - circles[j][1]
            distance = (dx**2 + dy**2)**0.5
            if distance < (radius + circles[j][2]) * 0.7:
                overlap = True
                break

        # If the circle overlaps more than 30% of the circles below it, adjust its location
        if overlap:
            x, y = random.randint(
                0, IMAGE_WIDTH), random.randint(0, IMAGE_HEIGHT)

        circles.append((x, y, radius, color))
    return circles


def generate_image(quote, sentiment):
    # Create a blank image
    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color="white")

    # Create a blank image for the circles
    circles_image = generate_abstract_image(sentiment)

    # Create a drawing context for the text
    image.paste(circles_image, (0, 0))
    image = image.filter(ImageFilter.BoxBlur(radius=BLUR_PERCENT))

    text_color = get_best_font_color(image)
    image = add_text(image, quote, text_color)

    now = datetime.datetime.now()
    just_filename = f"image_{now.year}_{now.month}_{now.day}.jpg"

    localtesting = True
    if localtesting == True:
        filename = os.path.join(IMAGE_SAVE_PATH, just_filename)
        image.save(filename)
        filename = os.path.join(DOCKER_IMAGE_SAVE_PATH, just_filename)
    else:
        filename = os.path.join(DOCKER_IMAGE_SAVE_PATH, just_filename)
        image.save(filename)
    return filename


def create_gradient_image0(colors, size):
    """Create a gradient image with the specified colors and size."""
    # Pick two random colors from the list
    color1 = random.choice(colors)
    colors.remove(color1)

    colors_are_complementary = False

    logger.debug(f"Color1: {color1}")
    r1, g1, b1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
    if TWO_COLOR_TONE:
        if len(colors) == 0:
            colors.append("#0c0c0c")
            colors.append("#ffffff")
        color2 = random.choice(colors)
        logger.debug(f"Checking Color2: {color2}")

        # Convert the hexcode colors to RGB
        r2, g2, b2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))

        colors_are_complementary = are_colors_complementary(
            (r1, g1, b1), (r2, g2, b2), int(os.getenv("COMPLEMENTARY_THRESHOLD", 75)))
        while not colors_are_complementary and len(colors) > 0:
            colors.remove(color2)
            color2 = random.choice(colors)
            logger.debug(f"Checking Color2: {color2}")
            r2, g2, b2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
            colors_are_complementary = are_colors_complementary(
                (r1, g1, b1), (r2, g2, b2), int(os.getenv("COMPLEMENTARY_THRESHOLD", 75)))

    if not colors_are_complementary or not TWO_COLOR_TONE:
        logger.info("Colors are not complementary so using a single color")
        r2, g2, b2 = r1, g1, b1

    # Create a gradient image with the two colors
    # Make output image
    gradient = np.zeros((size[1], size[0], 3), np.uint8)

    # Fill R, G and B channels with linear gradient between two end colours
    gradient[:, :, 0] = np.linspace(r1, r2, size[0], dtype=np.uint8)
    gradient[:, :, 1] = np.linspace(g1, g2, size[0], dtype=np.uint8)
    gradient[:, :, 2] = np.linspace(b1, b2, size[0], dtype=np.uint8)

    # Save result
    return Image.fromarray(gradient)


def are_colors_complementary(color1, color2, threshold=50):
    # Extract the red, green, and blue values of each color
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    # Calculate the differences between the red, green, and blue values
    diff_r = abs(r1 - r2)
    diff_g = abs(g1 - g2)
    diff_b = abs(b1 - b2)

    # Check if the differences are all within the threshold
    if diff_r < threshold and diff_g < threshold and diff_b < threshold:
        return True
    else:
        return False


def get_best_font_color(image):
    """Determine the best font color for the given image."""
    width, height = image.size
    pixels = image.load()
    r_total = g_total = b_total = 0
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            r_total += r
            g_total += g
            b_total += b
    r_avg = r_total / (width * height)
    g_avg = g_total / (width * height)
    b_avg = b_total / (width * height)

    avg_color = int((r_avg + g_avg + b_avg) / 3)
    logger.info(f"avg_color = {avg_color}")

    # Determine the best font color based on the average pixel value
    if avg_color > 150:
        logger.info("should be black color")
        return "black"
    else:
        logger.info("should be white color")
        return "white"


def add_text(image, text, color):
    """Add text to the image with the specified font, font size, position, and color."""
    # Create a drawing context for the image
    draw = ImageDraw.Draw(image)

    wrapper = textwrap.TextWrapper(width=image.width)
    font = ImageFont.truetype(os.path.join(
        FONT_FAMILY_PATH, FONT_FAMILY), FONT_SIZE)
    lines = wrap_text(text, image.width - 200, font)

    x, y = 50, 100

    if LINES_EQUAL_SPACES:
        text_height = int((IMAGE_WIDTH - x - y)/len(lines))
    else:
        text_height = FONT_SIZE + 20

    logger.info(text_height)
    for line in lines:
        try:
            logger.info(f"x: {x} y: {y} line: {line}")
            draw.text((x, y), line, font=font, fill=color)
            y += text_height
        except:
            logger.info("error")

    return image


def wrap_text(text, width, font):
    author = ""
    if '―' in text:
        author = " - " + text.split('―')[1]
        text = text.split('―')[0]

    text = clean_text(text)
    author = clean_text(author)
    logger.info(text)

    text_lines = return_text_lines_by_font(text, font, width)
    author_text_lines = return_text_lines_by_font(author, font, width)
    text_lines += author_text_lines

    # remove badwords
    text_lines = [profanity.censor(x) for x in text_lines]
    return text_lines


def clean_text(text):
    while "  " in text:
        text = text.replace("\n", " ").replace("\t", " ").replace("  ", " ")

    while "  " in text:
        text = text.replace("  ", " ")

    return text


def return_text_lines_by_font(text, font, width):
    words = text.split()
    font_size = font.getsize(text)
    text_lines = []
    text_line = []
    for word in words:
        if word == '[br]':
            text_lines.append(' '.join(text_line))
            text_line = []
            continue
        text_line.append(word)
        w, h = font.getsize(' '.join(text_line))
        if w > width:
            text_line.pop()
            text_lines.append(' '.join(text_line))
            text_line = [word]

    if len(text_line) > 0:
        final_text = ' '.join(text_line)
        text_lines.append(final_text)
    text_lines = [x for x in text_lines if len(x.strip()) > 0]
    return text_lines
