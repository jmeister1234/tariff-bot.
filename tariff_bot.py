import time
import requests
from twilio.rest import Client

# ---------------------------
# CONFIGURATION
# ---------------------------
NEWSAPI_KEY = bbe0966b14f548d39a4084dedca602c3
TWILIO_SID = PNacd9f34014bde24045f7a7465d84c528
TWILIO_AUTH = f3091b1a8260bd9667480b9d52365535
TWILIO_PHONE = "+18774054480
MY_PHONE = "+5132762403

SEARCH_TERM = "US tariffs OR China tariffs OR trade tariffs"
CHECK_INTERVAL = 300  # seconds (5 minutes)

# ---------------------------
# SETUP TWILIO CLIENT
# ---------------------------
client = Client(TWILIO_SID, TWILIO_AUTH)

# ---------------------------
# TRACKING FOR NEW ARTICLES
# ---------------------------
seen_titles = set()

def get_latest_news():
    url = f"https://newsapi.org/v2/everything?q={SEARCH_TERM}&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWSAPI_KEY}"
    r = requests.get(url)
    data = r.json()
    return data.get("articles", [])

def send_sms(title, url):
    msg = f"📰 New Tariff News:\n{title}\n{url}"
    client.messages.create(
        body=msg,
        from_=TWILIO_PHONE,
        to=MY_PHONE
    )
    print(f"✅ Sent SMS: {title}")

print("✅ Tariff News Bot started... checking every 5 minutes.")

while True:
    try:
        articles = get_latest_news()
        for article in articles:
            title = article["title"]
            url = article["url"]
            if title not in seen_titles:
                seen_titles.add(title)
                send_sms(title, url)
        time.sleep(CHECK_INTERVAL)
    except Exception as e:
        print("⚠️ Error:", e)
        time.sleep(60)
