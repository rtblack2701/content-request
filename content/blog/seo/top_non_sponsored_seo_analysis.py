import requests
from bs4 import BeautifulSoup

def analyze_webpage(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch: {url} [Status code: {response.status_code}]")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        headings = [
            {'tag': tag.name, 'text': tag.get_text(strip=True)}
            for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        ]

        word_count = len(soup.body.get_text(separator=' ', strip=True).split()) if soup.body else 0

        return {
            'title': soup.title.string if soup.title else "",
            'meta_description': soup.find('meta', attrs={'name': 'description'}).get('content', '') if soup.find('meta', attrs={'name': 'description'}) else "",
            'url_slug': url.split('/')[-1],
            'word_count': word_count,
            'heading_structure': headings
        }
    except Exception as e:
        print(f"Error analyzing {url}: {e}")
        return None