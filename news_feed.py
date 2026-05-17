import feedparser

def get_finance_news():
    feeds = {
        "📈 Fintech": "https://feeds.feedburner.com/ndtvprofit-latest",
        "🏦 Markets": "https://www.moneycontrol.com/rss/marketreports.xml",
        "🏢 Corporate": "https://www.moneycontrol.com/rss/latestnews.xml"
    }

    news_data = {}

    for category, url in feeds.items():
        try:
            feed = feedparser.parse(url)
            headlines = []
            for entry in feed.entries[:5]:
                title = entry.get("title", "").strip()
                link = entry.get("link", "#")
                if title:
                    headlines.append({"title": title, "link": link})
            news_data[category] = headlines if headlines else [{"title": "No news available right now.", "link": "#"}]
        except Exception:
            news_data[category] = [{"title": "Could not load news feed.", "link": "#"}]

    return news_data