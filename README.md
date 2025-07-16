# 📰 Jagran Naidunia Indore News Scraper

This repository contains an automated news scraper that extracts the latest headlines and article content from the **Jagran Naidunia Indore** RSS feed and saves them in a structured JSON format (`jagran-naidunia-indore-news.json`). It is powered by a Python script and runs every 15 minutes using **GitHub Actions**.

---

## 🌐 Live JSON Feed

You can access the live JSON output at:

```
[https://mrsakshamji.github.io/jagran-news-scraper/jagran-naidunia-indore-news.json](https://mrsakshamji.github.io/indore-news-scrapper/jagran-naidunia-indore-news.json)
```

---

## 📁 Output Format

Each news item in the JSON file contains:

```json
[
  {
    "title": "News headline",
    "link": "https://example.com/article",
    "published": "Mon, 14 Jul 2025 23:12:32 +0530",
    "author": "Author Name",
    "summary": "Short description",
    "tags": [],
    "image": "https://ik.imagekit.io/your-image.webp",
    "content": "Full article text here..."
  },
  ...
]
```

---

## 🛠️ Technologies Used

- **Python 3.11+**
- **feedparser** for reading RSS feeds
- **Requests + BeautifulSoup** for full article scraping
- **Pillow (PIL)** for image processing
- **ImageKit.io** for image CDN hosting
- **GitHub Actions** for automation (runs every 15 minutes)
- **GitHub Pages** for publicly hosting the JSON output

---

## ⚙️ How It Works

1. The Python script (`main.py`) reads the Jagran Indore RSS feed.
2. It visits each article and extracts full content, author, image, and other metadata.
3. The main article image is converted to `.webp` and uploaded to **ImageKit**.
4. The structured result is saved as `jagran-naidunia-indore-news.json`.
5. A GitHub Actions workflow runs every 15 minutes:
   - Fetches new articles
   - Updates the JSON file
   - Commits and pushes changes
6. **GitHub Pages** serves the updated JSON file publicly.

---

## 📦 Setup Locally

### Requirements

- Python 3.11 or higher
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Run Locally

```bash
python main.py
```

The JSON file will be saved as `jagran-naidunia-indore-news.json`.

---

## 🤖 GitHub Actions Setup

See `.github/workflows/scrape.yml`:

- Runs automatically every 15 minutes via cron.
- Checks and commits new content only if updates are detected.
- Pushes JSON file to `main` branch.
- JSON is served by **GitHub Pages**.

---

## 🔐 API Integration (Optional)

If you're using this in a backend:

```bash
GET https://your-api.vercel.app/api/jagran-news
Headers: x-api-key: YOUR_SECRET_KEY
```

---

## 📄 License

MIT License – free for personal and commercial use.

---

## 🙋‍♂️ Author

Built with ❤️ by [@mrsakshamji](https://github.com/mrsakshamji)
