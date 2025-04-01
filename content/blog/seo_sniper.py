import json
import os
from content.blog.seo.top_non_sponsored import get_top_non_sponsored_article

def generate_seo_data(keyword: str, feature_title: str) -> bool:
    print(f"🔍 Sniping SEO structure for: {keyword}")
    title, url, headings, word_count = get_top_non_sponsored_article(keyword, feature_title)

    if not title or not url or not headings or len(headings) < 3 or word_count < 250:
        print("❌ Skipped: No usable SEO structure found.")
        return False

    seo_data = {
        "keyword": keyword,
        "title": title,
        "source_url": url,
        "seo_headings": "\n".join([f"{h['tag'].upper()}: {h['text']}" for h in headings]),
        "word_count": word_count,
        "company_name": "Unleash",
        "trial_link": "https://www.getunleash.io/start",
        "docs_link": "https://docs.getunleash.io",
        "community_link": "https://github.com/Unleash"
    }

    log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../seo_sniping.log"))
    with open(log_path, "w") as log_file:
        log_file.write(json.dumps(seo_data, indent=2))

    seo_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../seo_data.json"))
    with open(seo_data_path, "w") as f:
        json.dump(seo_data, f, indent=2)

    print("✅ SEO data written to seo_data.json")
    return True