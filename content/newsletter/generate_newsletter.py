import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from fetch_responses import records

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
COMPANY_NAME = os.getenv('COMPANY_NAME')

def generate_newsletter():
    entries = records
    if not entries:
        print("❌ No form responses found.")
        return

    prompt_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../prompts/newsletter.prompt")
    )
    with open(prompt_path) as f:
        template = f.read()

    # Build a summarized list of recent features
    feature_summaries = []
    for entry in entries:
        title = entry.get("Feature title", "(No title)")
        description = entry.get("Feature description", "(No description)")
        version = entry.get("Release version", "(No version)")
        blog_url = entry.get("Blog URL", "(link TBD)")
        feature_summary = f"\n🚀 {title} (v{version})\n{description}\n→ Read the blog: {blog_url}\n"
        feature_summaries.append(feature_summary)

    combined_summary = "\n".join(feature_summaries)

    prompt = template.format(
        feature_updates=combined_summary,
        company_name=COMPANY_NAME
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a friendly and professional product marketing writer generating monthly newsletters.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        newsletter = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error calling OpenAI: {e}")
        return

    # 📝 Save the newletter
    output_dir = os.getenv("OUTPUT_DIR", os.path.expanduser("~/Desktop/contentgen_output"))
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "newsletter.md")
    with open(output_path, "w") as f:
        f.write(newsletter)

    print(f"✅ Blog written to {output_path}")


if __name__ == "__main__":
    generate_newsletter()
