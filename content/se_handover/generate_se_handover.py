import os
from dotenv import load_dotenv
from fetch_responses import latest
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_se_handover():
    if not latest:
        print("❌ No form responses found.")
        return

    title = latest.get("Feature title", "[Missing Title]")
    description = latest.get("Feature description", "Data not provided in google form, please fill in manually if applicable.")
    use_case = latest.get("Real-world use case", "Data not provided in google form, please fill in manually if applicable.")
    benefits = latest.get("Key benefits", "Data not provided in google form, please fill in manually if applicable.")
    enablement = latest.get("How to enable", "Data not provided in google form, please fill in manually if applicable.")
    limitations = latest.get("Known limitations or gotchas", "")
    extras = latest.get("Additional features", "")
    demo_video = latest.get("Demo video", "")

    # Generate real-life comparison
    try:
        prompt = f"""Write a short, real-life scenario analogy for the following feature so that a software engineer can easily relate to it. Feature: {title} — Description: {description}"""
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a technical writer skilled in relatable analogies."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )
        comparison = response.choices[0].message.content.strip()
    except Exception as e:
        comparison = "Data not provided in google form, please fill in manually if applicable."

    # Start building the output
    lines = [
        f"# SE {title} Handover",
        "",
        "## Feature Description",
        description,
        "",
        "## Real-world Use Case",
        use_case,
        "",
        "## Real-life Scenario Comparison",
        comparison,
        "",
        "## Key Benefits",
        benefits,
        "",
        "## How to Enable the Feature",
        f"{title} is currently behind the `{enablement}` feature flag.\nTo enable it, add a request in the `#slack-channel` to activate it on your account.",
        "",
        "## Known Limitations or Gotchas",
        limitations if limitations else "Data not provided in google form, please fill in manually if applicable.",
        "",
        "## Additional Features",
        extras if extras else "Data not provided in google form, please fill in manually if applicable.",
        "",
        "## Demos",
        demo_video if demo_video else "Data not provided in google form, please fill in manually if applicable.",
        "",
        "## Additional Resources",
        "- Blog: (link TBD)\n- Docs: (link TBD)"
    ]

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../output/se_handover.md"))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print("✅ SE handover written to output/se_handover.md")

if __name__ == "__main__":
    generate_se_handover()
