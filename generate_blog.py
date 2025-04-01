import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from dotenv import load_dotenv
from fetch_responses import latest  # reuses the parsed response
import json

load_dotenv()

# You can fetch this from your SEO sniping script as needed
seo_data = {
    "keyword": "feature flags in CI/CD",
    "seo_headings": """
# Introduction
## What are Feature Flags?
## Why They Matter in CI/CD
## Common Pitfalls
## A Real-World Example
## How to Implement Safely
## Key Takeaways
""",
    "company_name": "Unleash",
    "trial_link": "https://www.getunleash.io/start",
    "docs_link": "https://docs.getunleash.io",
    "community_link": "https://github.com/Unleash",
}

# Load and fill prompt template
with open("prompts/blog.prompt") as f:
    template = f.read()

prompt = template.format(
    keyword=seo_data["keyword"],
    seo_headings=seo_data["seo_headings"],
    title=latest["Feature Title"],
    description=latest["Feature Description"],
    benefits=latest["Key Benefits"],
    enablement=latest["How to Enable"],
    use_case=latest["Real-world Use Case"],
    competitor_link=latest.get("Competitor Docs (if any)", "N/A"),
    company_name=seo_data["company_name"],
    trial_link=seo_data["trial_link"],
    docs_link=seo_data["docs_link"],
    community_link=seo_data["community_link"],
)

# Generate with OpenAI
response = client.chat.completions.create(model="gpt-4",
messages=[
    {"role": "system", "content": "You are a developer content writer."},
    {"role": "user", "content": prompt}
],
temperature=0.7)

blog_text = response.choices[0].message.content

# Save to file
os.makedirs("output", exist_ok=True)
with open("output/blog.md", "w") as f:
    f.write(blog_text)

print("✅ Blog written to output/blog.md")