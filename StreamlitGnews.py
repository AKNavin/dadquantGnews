import streamlit as st
import requests
from datetime import datetime, timedelta
from collections import Counter
import time

API_KEY = '213089457038ac5e5b2c5d0e59471ea4'

# Define sector keywords
sector_keywords = {
    'Banking': ['bank', 'psu bank', 'private bank', 'banking'],
    'Financial Services': ['nbfc', 'finance company', 'mutual fund', 'amc'],
    'IT': ['it company', 'tech stock', 'software company', 'infosys', 'tcs'],
    'Pharmaceuticals': ['pharma', 'drug maker', 'pharmaceutical', 'cipla', 'sun pharma'],
    'FMCG': ['fmcg', 'consumer goods', 'hindustan unilever', 'nestle'],
    'Automobile': ['automobile', 'auto stock', 'maruti', 'tata motors', 'hero moto'],
    'Energy': ['oil', 'gas', 'power', 'ongc', 'reliance energy'],
    'Metals': ['metal', 'steel', 'tata steel', 'hindalco'],
    'Real Estate': ['real estate', 'property'],
    'Telecom': ['telecom', 'airtel', 'vodafone', 'jio'],
    'Infrastructure': ['infra', 'infrastructure', 'l&t', 'adani ports'],
    'Capital Goods': ['capital goods', 'engineering', 'bharat forge'],
    'Cement': ['cement', 'ultratech', 'shree cement'],
    'Healthcare': ['healthcare', 'hospital', 'apollo'],
    'Consumer Durables': ['consumer durable', 'electronic appliances'],
    'Media': ['media', 'broadcast', 'news network'],
    'Chemicals': ['chemical', 'pidilite', 'alkyl amines'],
    'Textiles': ['textile', 'garments', 'vardhman']
}

# Sector query groups (to stay within GNews query char limits)
sector_groups = [
    'Banking OR Financial Services OR IT OR Pharmaceuticals',
    'FMCG OR Automobile OR Energy OR Metals OR Real Estate',
    'Telecom OR Infrastructure OR Capital Goods OR Cement',
    'Healthcare OR Consumer Durables OR Media OR Chemicals OR Textiles'
]

# Streamlit app UI
st.title("📈 India Market Sector News Dashboard")
st.write("🔍 Fetch and classify market sector news headlines for a selected date range.")

# Date picker for 'from' date
selected_date = st.date_input("Select Date (From)", datetime.today())
from_date = datetime.combine(selected_date, datetime.min.time())

# Calculate 'to' date (next day)
to_date = from_date + timedelta(days=1)

# Display selected date range
st.write(f"📅 Searching from **{selected_date.strftime('%Y-%m-%d')}** to **{to_date.strftime('%Y-%m-%d')}**")

if st.button("Fetch News"):
    sector_hits = Counter()
    seen_urls = set()
    article_index = 1

    st.info(f"🔎 Fetching sector-wise news from GNews from {selected_date.strftime('%Y-%m-%d')} to {to_date.strftime('%Y-%m-%d')}...")

    for group in sector_groups:
        params = {
            'q': group,
            'country': 'in',
            'lang': 'en',
            'from': from_date.strftime('%Y-%m-%dT00:00:00Z'),
            'to': to_date.strftime('%Y-%m-%dT00:00:00Z'),
            'sortby': 'publishedAt',
            'token': API_KEY,
            'max': 10
        }

        response = requests.get('https://gnews.io/api/v4/search', params=params)

        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])

            for article in articles:
                if article['url'] in seen_urls:
                    continue
                seen_urls.add(article['url'])

                text = f"{article['title']} {article.get('description', '')}".lower()
                matched_sectors = []
                for sector, keywords in sector_keywords.items():
                    if any(kw in text for kw in keywords):
                        matched_sectors.append(sector)
                        sector_hits[sector] += 1

                st.markdown(f"**{article_index}. {article['title']}**")
                st.write(f"📅 {article['publishedAt']}")
                st.write(f"🔗 [Read Article]({article['url']})")
                st.write(f"🏷️ Sectors: {', '.join(matched_sectors) if matched_sectors else 'Unclassified'}")
                st.write("---")
                article_index += 1

            time.sleep(1)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

    st.subheader("📊 Sector Mentions in Results:")
    for sector, count in sector_hits.most_common():
        st.write(f"**{sector}**: {count}")
