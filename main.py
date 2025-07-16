import feedparser
import requests
from bs4 import BeautifulSoup
import json
import time
import os
from PIL import Image
from io import BytesIO
import base64

# 🔑 ImageKit credentials
IMAGEKIT_PUBLIC_KEY = "public_DoXYDWBqB/du3xdZsTK7iRxIiZY="
IMAGEKIT_PRIVATE_KEY = "private_gOdixB3YlB9UlPGQz/cLyUS0wo4="
IMAGEKIT_UPLOAD_URL = "https://upload.imagekit.io/api/v1/files/upload"

# 📰 Jagran Naidunia Indore RSS feed URL
rss_url = "https://rss.jagran.com/naidunia/madhya-pradesh/indore.xml"
feed = feedparser.parse(rss_url)
print(f"🔄 Processing {len(feed.entries)} articles...\n")

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

output_file = "jagran-naidunia-indore-news.json"
articles = []

# ✅ Load existing articles
existing_links = set()
if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as f:
        try:
            existing_articles = json.load(f)
            articles = existing_articles
            existing_links = {a["link"] for a in existing_articles}
        except:
            print("⚠️ Starting with a fresh file.")
            articles = []

# 🖼️ Image upload function
def upload_to_imagekit(image_url, filename, folder="/jagran-news"):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content)).convert("RGB")
        buffer = BytesIO()
        img.save(buffer, format="WEBP", quality=80)
        encoded = base64.b64encode(buffer.getvalue()).decode()

        headers = {
            "Authorization": "Basic " + base64.b64encode(f"{IMAGEKIT_PRIVATE_KEY}:".encode()).decode()
        }

        payload = {
            "file": encoded,
            "fileName": filename + ".webp",
            "folder": folder,
            "useUniqueFileName": "true"
        }

        r = requests.post(IMAGEKIT_UPLOAD_URL, headers=headers, data=payload)
        r.raise_for_status()
        return r.json().get("url")
    except Exception as e:
        print(f"⚠️ Image upload failed: {e}")
        return image_url  # fallback

# 🔄 Process new articles
new_count = 0
for i, entry in enumerate(feed.entries):
    title = entry.title
    link = entry.link
    published = entry.get("published", "")

    if link in existing_links:
        print(f"⏩ Skipped (already exists): {link}")
        continue

    print(f"🔗 [{i+1}] Fetching: {title[:60]}...")

    try:
        page = requests.get(link, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")

        content = ""
        author = ""
        summary = ""
        tags = []
        image_url = ""

        # ✅ Find the article container
        content_div = soup.find("div", class_="articleSide")

        if content_div:
            paragraphs = []

            # Headline
            h1 = content_div.find("h1")
            if h1:
                paragraphs.append(h1.get_text(strip=True))

            # Subheadline / summary
            h2 = content_div.find("h2", class_="headArt")
            if h2:
                summary = h2.get_text(strip=True)
                paragraphs.append(summary)

            # All <p> tags
            for p in content_div.find_all("p"):
                text = p.get_text(strip=True)
                if text:
                    paragraphs.append(text)

            # Combine content
            content = "\n".join(paragraphs)

            # Author
            name_divs = content_div.find_all("div", class_="name")
            for div in name_divs:
                strong = div.find("strong")
                if strong:
                    possible_author = strong.get_text(strip=True)
                    if possible_author and "Edit" not in possible_author:
                        author = possible_author
                        break
        else:
            # Fallback to RSS description
            print("⚠️ Content not found on page. Using RSS summary.")
            content = BeautifulSoup(entry.description, "html.parser").get_text(strip=True)
            summary = content

        # Image extraction
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            image_url = og_image["content"]
            image_url = upload_to_imagekit(image_url, f"jagran_{hash(image_url)}")

        # Save article
        articles.append({
            "title": title,
            "link": link,
            "published": published,
            "author": author,
            "summary": summary,
            "tags": tags,
            "image": image_url,
            "content": content
        })

        existing_links.add(link)
        new_count += 1
        print(f"✅ Added: {title[:60]}...")
        time.sleep(1)

    except Exception as e:
        print(f"❌ Error: {e}")
        continue

# 💾 Save JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"\n✅ Completed. {new_count} new articles added.")
print(f"📁 Total articles saved: {len(articles)}")
