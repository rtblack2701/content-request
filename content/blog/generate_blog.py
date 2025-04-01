# content/blog/generate_blog.py (updated)
import os
import openai
import json
from dotenv import load_dotenv
from fetch_responses import latest

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_blog():
    if not latest:
        print("\u274c No form responses found.")
        return

    seo_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../seo_data.json"))
    if not os.path.exists(seo_data_path) or os.stat(seo_data_path).st_size == 0:
        print("\u274c seo_data.json is empty or missing.")
        return

    with open(seo_data_path) as f:
        seo_data = json.load(f)

    prompt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../prompts/blog.prompt"))
    with open(prompt_path) as f:
        template = f.read()

    prompt = template.format(
        keyword=seo_data["keyword"],
        seo_headings=seo_data["seo_headings"],
        title=latest["Feature title"],
        description=latest["Feature description"],
        benefits=latest["Key benefits"],
        enablement=latest["How to enable"],
        use_case=latest["Real-world use case"],
        competitor_link=latest.get("Competitor resources", "N/A"),
        company_name=seo_data["company_name"],
        trial_link=seo_data["trial_link"],
        docs_link=seo_data["docs_link"],
        community_link=seo_data["community_link"]
    )

    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a developer content writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        blog_text = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"\u274c Error calling OpenAI: {e}")
        return

    if not blog_text:
        print("\u274c OpenAI returned an empty response.")
        return

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../output/blog.md"))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(blog_text)

    print("\u2705 Blog written to output/blog.md")
