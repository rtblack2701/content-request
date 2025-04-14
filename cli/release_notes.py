import os
from dotenv import load_dotenv
from openai import OpenAI
from core.fetch_responses import latest

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
COMPANY_NAME = os.getenv('COMPANY_NAME')
SITE_URL = os.getenv('SITE_URL')

def generate_release_notes():
    if not latest:
        print("❌ No form responses found.")
        return

    prompt_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../templates/release_notes.prompt")
    )
    with open(prompt_path) as f:
        template = f.read()

    title = latest.get("Feature title", "(Untitled Feature)")
    version = latest.get("Release version", "(Unversioned)")
    description = latest.get("Feature description", "No description provided.")
    use_case = latest.get("Real-world use case", "Use case not provided.")
    gotchas = latest.get("Known limitations or gotchas", "None specified.")

    prompt = template.format(
        company_name=COMPANY_NAME,
        site_url=SITE_URL,
        title=title,
        version=version,
        description=description,
        use_case=use_case,
        gotchas=gotchas
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional technical writer generating developer-facing release notes.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        release_note = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error calling OpenAI: {e}")
        return

    # 📝 Save the Release Notes
    output_dir = os.getenv("OUTPUT_DIR", os.path.expanduser("~/Desktop/contentgen_output"))
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "release_notes.md")
    with open(output_path, "w") as f:
        f.write(release_note)

    print(f"✅ Release notes written to {output_path}")

if __name__ == "__main__":
    generate_release_notes()