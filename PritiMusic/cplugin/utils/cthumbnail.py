import os
import re
import random
import aiofiles
import aiohttp
import colorsys
from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps)
from py_yt import VideosSearch
from PritiMusic import app
from PritiMusic.utils.database import clonebotdb

# Helper: Glowing Circular Crop
def get_glowing_circle(image):
    """
    Crops the image into a circle and applies a multi-layered glow:
    Yellow -> White -> Pink -> White, with a solid white border.
    """
    img = image.convert("RGBA")
    size = min(img.size)
    
    # 1. Crop image into a perfect circle
    img = ImageOps.fit(img, (size, size), centering=(0.5, 0.5))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    circular_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    circular_img.paste(img, (0, 0), mask)

    # 2. Setup canvas for the glow effect
    offset = 50  # Padding for the glow
    glow_size = size + (offset * 2)
    glow = Image.new("RGBA", (glow_size, glow_size), (0, 0, 0, 0))
    draw_glow = ImageDraw.Draw(glow)

    # 3. Draw concentric circles for the glow effect
    draw_glow.ellipse((5, 5, glow_size-5, glow_size-5), fill=(255, 255, 0, 60))        # Outer Yellow
    draw_glow.ellipse((15, 15, glow_size-15, glow_size-15), fill=(255, 255, 255, 80))  # Outer White
    draw_glow.ellipse((25, 25, glow_size-25, glow_size-25), fill=(255, 105, 180, 150)) # Pink
    draw_glow.ellipse((35, 35, glow_size-35, glow_size-35), fill=(255, 255, 255, 200)) # Inner White
    
    # Apply Gaussian Blur to make the glow smooth
    glow = glow.filter(ImageFilter.GaussianBlur(15))
    
    # 4. Draw a solid white border directly around the image
    draw_border = ImageDraw.Draw(glow)
    draw_border.ellipse((offset - 4, offset - 4, size + offset + 4, size + offset + 4), outline="white", width=8)

    # 5. Paste the circular image on top of the glowing background
    glow.paste(circular_img, (offset, offset), circular_img)
    
    return glow, offset

def draw_text_with_glow(draw, position, text, font, fill, glow_fill):
    x, y = position
    for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3)]:
        draw.text((x + dx, y + dy), text, font=font, fill=glow_fill)
    draw.text((x, y), text, font=font, fill=fill)

# Helper: Text Truncator
def clear(text, max_length=25):
    text = text.strip()
    return text[:max_length].rstrip() + "..." if len(text) > max_length else text

# Helper: Download user profile
async def download_user_photo(user_id):
    try:
        async for photo in app.get_chat_photos(user_id, limit=1):
            return await app.download_media(photo.file_id, file_name=f"cache/{user_id}.jpg")
    except: return None
    return None

async def get_thumb(videoid, user_id, client):
    # 1. Fetch Bot & Owner
    me = await client.get_me()
    bot_name = me.first_name.upper()
    bot_id = me.id
    owner_name = "OWNER"
    try:
        bot_data = await clonebotdb.find_one({"bot_id": bot_id})
        if bot_data:
            owner = await client.get_users(bot_data.get("user_id"))
            owner_name = owner.first_name.upper()
    except: owner_name = "ADMIN"

    # 2. Setup Files
    os.makedirs("cache", exist_ok=True)
    filename = f"cache/{videoid}_{bot_id}.png"
    if os.path.isfile(filename): return filename

    # 3. Download YT Data
    results = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
    data = await results.next()
    result = data["result"][0]
    title = re.sub(r"\W+", " ", result["title"]).title()
    duration = result.get("duration", "00:00")
    views = result.get("viewCount", {}).get("short", "Unknown")
    channel = result.get("channel", {}).get("name", "Unknown Artist")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(result["thumbnails"][0]["url"].split("?")[0]) as resp:
            f = await aiofiles.open(f"cache/temp_{videoid}.jpg", mode="wb")
            await f.write(await resp.read())
            await f.close()

    # 4. Drawing Logic
    bg = Image.open(f"cache/temp_{videoid}.jpg").convert("RGBA").resize((1920, 1080))
    background = bg.filter(ImageFilter.GaussianBlur(25)).point(lambda p: p * 0.4)
    
    # --- SOLID BLACK CARD ---
    black_card = Image.new("RGBA", background.size, (0, 0, 0, 0))
    draw_card = ImageDraw.Draw(black_card)
    # Fill is now solid black (0, 0, 0, 255) instead of transparent
    draw_card.rounded_rectangle((40, 40, 1880, 940), radius=60, fill=(0, 0, 0, 255), outline=(132, 224, 240, 200), width=6)
    
    # Paste black card onto blurred background
    background = Image.alpha_composite(background, black_card)
    draw = ImageDraw.Draw(background)

    # --- RAIN EFFECT ---
    for _ in range(300):
        rx = random.randint(50, 1870)
        ry = random.randint(50, 930)
        length = random.randint(10, 30)
        draw.line([(rx, ry), (rx + 5, ry + length)], fill=(255, 255, 255, 50), width=1)
    
    try:
        f1 = ImageFont.truetype("PritiMusic/assets/font.ttf", 65)
        f2 = ImageFont.truetype("PritiMusic/assets/font2.ttf", 45)
        br = ImageFont.truetype("PritiMusic/assets/font2.ttf", 50)
    except:
        f1 = f2 = br = ImageFont.load_default()

    # --- GLOWING IMAGES ---
    # YouTube Thumbnail
    yt_img_glowing, yt_offset = get_glowing_circle(bg.resize((500, 500)))
    background.paste(yt_img_glowing, (80 - yt_offset, 250 - yt_offset), yt_img_glowing)
    
    # User Profile Image
    u_photo = await download_user_photo(user_id)
    if u_photo:
        u_img_glowing, u_offset = get_glowing_circle(Image.open(u_photo).resize((450, 450)))
        background.paste(u_img_glowing, (1350 - u_offset, 250 - u_offset), u_img_glowing)

    # Fetch User Name
    try:
        user_info = await client.get_users(user_id)
        user_name = user_info.first_name
    except: user_name = "User"

    # Text Placement
    draw.text((650, 300), clear(title, 25), fill="white", font=f1)
    draw.text((650, 400), f"Artist: {channel}", fill=(200, 200, 200), font=f2)
    draw.text((650, 470), f"Views: {views}", fill=(150, 150, 150), font=f2)
    draw.text((650, 530), f"Duration: {duration}", fill=(150, 150, 150), font=f2)
    
    # Branding & Request
    draw.text((100, 100), f"BOT: {bot_name}", fill="yellow", font=br)
    draw.text((1400, 100), f"OWNER: {owner_name}", fill="cyan", font=br)
    draw.text((1350, 880), f"Requested by: {user_name[:15]}", fill="white", font=f2)

    # --- NEON AUDIO WAVE (Red to Yellow, Thinner lines) ---
    center_y = 750
    num_bars = 75
    bar_width = 3    # Thinner bars
    spacing = 15
    start_x = 650
    
    # Specific bar indexes for placing musical notes
    top_note_indices = [10, 30, 50]
    bottom_note_indices = [20, 40, 60]
    notes = ['♪', '♫', '♬']
    note_colors = [(255, 80, 80), (255, 255, 80), (255, 150, 0)] # Red & yellow variations
    
    for i in range(num_bars):
        h = random.randint(40, 80) if i % 5 == 0 else random.randint(10, 45)
        x1 = start_x + (i * spacing)
        x2 = x1 + bar_width
        if x2 > 1800: break
            
        # Gradient from Red (0.0) to Yellow (0.16)
        hue = 0.0 + (i / num_bars) * 0.16
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
        
        # Draw thinner, sharper glowing bars
        draw.rounded_rectangle((x1 - 6, center_y - h - 6, x2 + 6, center_y + h + 6), radius=6, fill=(r, g, b, 15))
        draw.rounded_rectangle((x1 - 3, center_y - h - 3, x2 + 3, center_y + h + 3), radius=4, fill=(r, g, b, 45))
        draw.rounded_rectangle((x1 - 1, center_y - h - 1, x2 + 1, center_y + h + 1), radius=2, fill=(r, g, b, 120))
        draw.rounded_rectangle((x1, center_y - h, x2, center_y + h), radius=1, fill=(255, 255, 255, 255))

        # Add glowing musical notes on specific top positions
        if i in top_note_indices:
            nc = random.choice(note_colors)
            draw_text_with_glow(draw, (x1 - 10, center_y - h - 50), random.choice(notes), f2, nc, (nc[0], nc[1], nc[2], 120))
        
        # Add glowing musical notes on specific bottom positions
        if i in bottom_note_indices:
            nc = random.choice(note_colors)
            draw_text_with_glow(draw, (x1 - 10, center_y + h + 10), random.choice(notes), f2, nc, (nc[0], nc[1], nc[2], 120))

    # --- BUTTON CONTROLS (Backward, Play/Pause, Forward) ---
    btn_y = 880
    
    # 1. Backward Button (Left)
    draw.ellipse((700, btn_y-20, 740, btn_y+20), outline="white", width=3)
    draw.polygon([(725, btn_y-12), (725, btn_y+12), (710, btn_y)], fill="white")
    draw.rectangle((705, btn_y-12, 708, btn_y+12), fill="white")
    
    # 2. Play/Pause Button icon (Center)
    draw.ellipse((770, btn_y-30, 830, btn_y+30), outline="white", width=4)
    draw.rectangle((790, btn_y-15, 800, btn_y+15), fill="white")
    draw.rectangle((805, btn_y-15, 815, btn_y+15), fill="white")

    # 3. Forward Button (Right)
    draw.ellipse((860, btn_y-20, 900, btn_y+20), outline="white", width=3)
    draw.polygon([(875, btn_y-12), (875, btn_y+12), (890, btn_y)], fill="white")
    draw.rectangle((892, btn_y-12, 895, btn_y+12), fill="white")

    background.convert("RGB").save(filename)
    if os.path.exists(f"cache/temp_{videoid}.jpg"):
        os.remove(f"cache/temp_{videoid}.jpg")
    if u_photo and os.path.exists(u_photo): 
        os.remove(u_photo)
    return filename
