import os
from dotenv import load_dotenv
from openai import OpenAI
from fetch_responses import latest

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_docs():
    if not latest:
        print("\u274c No form responses found.")
        return

    prompt_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../prompts/docs.prompt")
    )
    with open(prompt_path) as f:
        template = f.read()

    prompt = template.format(
        title=latest.get("Feature title", "(Untitled Feature)"),
        description=latest.get("Feature description", "No description provided."),
        use_case=latest.get("Real-world use case", ""),
        benefits=latest.get("Key benefits", ""),
        enablement=latest.get("How to enable", ""),
        known_limitations=latest.get("Known limitations or gotchas", "None listed."),
        version=latest.get("Release version", "(Unreleased)"),
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior technical writer creating user documentation for software engineers.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )
        docs_md = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"\u274c Error calling OpenAI: {e}")
        return

    # Write to docs output file
    output_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../output/docs.md")
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write(docs_md)

    print("\u2705 Docs written to output/docs.md")

if __name__ == "__main__":
    generate_docs()