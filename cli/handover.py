import os
from dotenv import load_dotenv
from core.fetch_responses import latest
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_se_handover():
    if not latest:
        print("❌ No form responses found.")
        return

    # Load the SE handover template
    prompt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../templates/se_handover.prompt"))
    with open(prompt_path) as f:
        template = f.read()

    def get_field(key, label):
        value = latest.get(key, "").strip()
        return value if value else f"{label} not provided in google form, please fill in manually if applicable."

    title = latest.get("Feature title", "(Unknown Feature Title)")
    description = get_field("Feature description", "Feature description")
    use_case = get_field("Real-world use case", "Real-world use case")
    benefits = get_field("Key benefits", "Key benefits")
    enablement = get_field("Feature flag", "Enablement instructions")
    known_limitations = get_field("Known limitations or gotchas", "Known limitations or gotchas")
    additional_features = get_field("Additional features", "Additional features")
    competitors = get_field("Competitor resources", "Competitor resources")
    demo_video = get_field("Demo video", "Demo video")

    # Ask OpenAI to generate the scenario using the prompt
    try:
        prompt_scenario = template.format(
            title=title,
            description=description,
            use_case=use_case,
            scenario="<FILL_IN_SCENARIO>",
            benefits=benefits,
            enablement=enablement,
            known_limitations=known_limitations,
            additional_features=additional_features,
            competitors=competitors,
            demo_video=demo_video,
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You generate internal SE handover documents using provided structure."},
                {"role": "user", "content": prompt_scenario.replace("<FILL_IN_SCENARIO>", "(insert analogy for real-life comparison of the feature)")}
            ],
            temperature=0.7
        )
        full_text = response.choices[0].message.content.strip()
    except Exception as e:
        full_text = "Scenario not generated. Please add manually if needed."
        print(f"⚠️ OpenAI error: {e}")

    # 📝 Save the SE Handover
    output_dir = os.getenv("OUTPUT_DIR", os.path.expanduser("~/Desktop/contentgen_output"))
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "se_handover.md")
    with open(output_path, "w") as f:
        f.write(full_text)

    print(f"✅ SE Handover written to {output_path}")

# Optional run
if __name__ == "__main__":
    generate_se_handover()
