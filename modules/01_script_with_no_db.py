
import json
import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.reuters.com/sustainability/shareholder-activism/",
    "Origin": "https://www.reuters.com"
}

size = 100
offset = 0

url = f'https://www.reuters.com/pf/api/v3/content/fetch/articles-by-section-alias-or-id-v1?query=%7B%22arc-site%22%3A%22reuters%22%2C%22fetch_type%22%3A%22collection%22%2C%22offset%22%3A{offset}%2C%22requestId%22%3A2%2C%22section_id%22%3A%22%2Fsustainability%2Fshareholder-activism%2F%22%2C%22size%22%3A%22{size}%22%2C%22uri%22%3A%22%2Fsustainability%2Fshareholder-activism%2F%22%2C%22website%22%3A%22reuters%22%7D&d=318&mxId=00000000&_website=reuters'

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    articles = data['result']['articles']
    res = json.dumps(data,indent=4)
    print(res[:100])
    print('==='*20)
    print(len(articles))

    for article in articles[:5]:
        canonical_url = "https://www.reuters.com" + article['canonical_url']

        try:
            print(f"🔄 Loading: {article['web']}")

            response = requests.get(canonical_url, headers=headers)
            if response.status_code != 200:
                print(f"Error Loading: {canonical_url}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            paragraphs = soup.find('div', class_ ='article-body-module__content__bnXL1')
            full_text = paragraphs.get_text(strip=True)
            article['content'] = full_text

            print(article)


        except Exception as e:
            print(f"🚨 Error while processing {canonical_url}: {e}")



else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
