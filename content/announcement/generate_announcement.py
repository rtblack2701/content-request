import os
import json
from dotenv import load_dotenv
from fetch_responses import latest
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
COMPANY_NAME = os.getenv("COMPANY_NAME")

def generate_announcement():
    if not latest:
        print("❌ No form responses found.")
        return

    prompt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../prompts/announcement.prompt"))
    with open(prompt_path) as f:
        template = f.read()

    # 🔍 Add tone logic
    title_lower = latest["Feature title"].lower()
    description = latest["Feature description"].lower()

    if any(word in title_lower for word in ["support", "integration", "compatible", "connect"]):
        tone_type = "integration"
    elif "enable" in description or "flag" in description:
        tone_type = "feature_flag"
    elif any(kw in title_lower for kw in ["deployment", "release", "rollout", "control"]):
        tone_type = "new_capability"
    else:
        tone_type = "best_practice"

    # 🧩 Optional version fallback
    version = latest.get("Release version", "")
    version_line = f" in version {version}" if version else ""

    template = template.replace("{COMPANY_NAME}", COMPANY_NAME or "YourCompany")

    # 🧠 Prepare the prompt
    prompt = template.format(
        title=latest["Feature title"],
        benefits=latest["Key benefits"],
        tone_type=tone_type,
        version_line=version_line
    )

    # 🤖 Call OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a developer marketer writing social and internal feature announcements."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        announcement_text = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error calling OpenAI: {e}")
        return

    # 📝 Save the announcement
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../output/announcement.md"))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(announcement_text)

    print("✅ Announcement written to output/announcement.md")

# Optional local run
if __name__ == "__main__":
    generate_announcement()