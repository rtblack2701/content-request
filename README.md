# ✨ Feature Content Generator

Automate the creation of multiple product content types — from a single Google Form submission. Designed for fast-moving teams, this project reduces the manual effort of writing technical docs, release notes, announcements, and more using OpenAI and Google APIs.

---

## 💡 Why This Exists

Shipping a feature doesn’t stop at writing code. Every release deserves:

- Clear documentation.
- A concise internal handover.
- A public announcement.
- A compelling blog post.
- A newsletter mention.
- Accurate release notes.

But coordinating all this across Docs, Marketing, Sales Engineering, and Product can be slow and inconsistent.

This tool automates the **scaffolding** of each content type so you can focus on refinement and distribution — not writing from scratch.

---

## 🧩 How It Works

1. Engineers submit a **Google Form** when a feature reaches QA/UAT.
2. Form responses are saved to a **linked Google Sheet**.
3. This CLI app fetches the latest submission and uses **OpenAI** to generate:

   - 📙 SEO-optimized blog post
   - 📣 Internal + social-ready announcement
   - 📄 Sales Engineering (SE) handover doc
   - 📘 Technical documentation *(coming soon)*
   - 📨 Newsletter snippet *(coming soon)*
   - 🧾 Release notes *(coming soon)*

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.9+
- A Google Service Account
- An OpenAI API key
- A Google Form + linked Google Sheet

### 2. Clone & Install Dependencies

```bash
git clone https://github.com/your-org/feature-content-generator.git
cd feature-content-generator
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 3. Configure environment
At the project root, add the following:
- `.env` file (see `.env.example` for keys)
- `credentials.json` from your Google Cloud service account

#### Required .env keys

- `OPENAI_API_KEY`
- `SHEET_ID`
- `GOOGLE_CREDENTIALS_PATH`
- `COMPANY_NAME`
- `SITE_URL`

### 4. Form setup
1. Go to this [Google form URL](https://docs.google.com/forms/d/e/1FAIpQLSchyiIHgyJxDFFAsRGCeVt2QD11MKV0QF8dWnlypa6TXnQMUw/copy) and select **Make a Copy**
2. Go to the **Responses** tab and select **Link to Sheets**.
3. Under the **Create a new spreadsheet** option, rename you sheet and select **Create**
4. Copy the Google Sheet ID from the URL and add it to the .env file as the **SHEET_ID**
5. Download the Google Service Account credentials JSON file and add it to the root of the project as **credentials.json**
6. Add your OpenAI API key to the .env file as the **OPENAI_API_KEY**
7. Add your company name to the .env file as the **COMPANY_NAME**
8. Add your site URL to the .env file as the **SITE_URL**

#### Required fields in the form:

| Field name (as it appears in the sheet)     | Description                                           |
|---------------------------------------------|-------------------------------------------------------|
| Feature title                               | The main topic of the content                        |
| Feature description                         | Overview of the feature                              |
| Key benefits                                | Comma-separated list of advantages                   |
| How to enable                               | Internal instructions on feature activation          |
| Real-world use case                         | Practical example of the feature in action           |
| Known limitations or gotchas (optional)     | Any caveats or known issues                          |
| Demo video (optional)                       | Link to a demo video                                 |
| Competitor resources (optional)             | Link to a relevant comparison or competitor article  |


## Content Generation
### 📙 Blog Post

Narrative overview of the feature, its benefits, and applications.

**SEO Sniping:**
The app performs a live Google search using the feature title, then:
- Scrapes the top non-sponsored article.
- Parses its heading structure.
- Uses that layout to inform (not dictate) the blog format.

If the article lacks quality or is irrelevant (e.g. pricing page), blog generation is skipped.
---

### 📣 Internal + Social Media Announcement
Generates a short, punchy update ideal for Slack and LinkedIn.
- Auto-detects tone via keywords (e.g. Now supported, New feature).
- Includes emojis, hashtags, and value bullets.
- Stays under 100 words.
---

### 📄 SE Handover Document
Markdown handover doc designed for Sales Engineering teams.

**Sections include:**
- Feature description
- Real-world use case
- AI-generated scenario comparison
- Key benefits
- Enablement instructions
- Known limitations
- Demo links and placeholders
---

### 4. ✅ Run the CLI
Use the following commands to generate content from the most recent form submission:
```bash
python main.py fetch           # See the latest form submission
python main.py blog            # Generate a technical blog
python main.py announcement    # Create an internal/social announcement
python main.py handover        # Generate an SE handover doc
python main.py release-notes   # Generate feature release notes
python main.py docs            # Generate technical documentation
python main.py all             # Run all generators
```

## 🧭 Strategic Content Cadence & GTM Alignment

This project isn’t just about content automation — it’s designed to **accelerate collaboration** across Product, Engineering, Marketing, and Docs.

### 🔍 Why this approach?

Many content creators find themselves chasing down details post-development, often having to produce documentation at the last minute. Coordination across content types was reactive and inconsistent, despite interest from Product Marketing and Comms in creating a broader narrative.

By introducing a simple, **QA/UAT trigger point** via a Google Form, this created a single source of feature truth early in the dev cycle — and used that to automatically scaffold multiple content types (docs, announcements, blogs, etc.).

This reduces bottlenecks, creates a consistent voice, and ensures content production begins before the release deadline hits.

---

### 🪄 Prioritized Content Generation Flow

Not all content needs to be released at the same time. Here’s a suggested **release sequence** for each content type:

| Content Type         | Suggested Timing           | Purpose                                                   |
|----------------------|----------------------------|-----------------------------------------------------------|
| 📘 Technical Docs     | 1–2 weeks **before GA**     | Gives early adopters a path forward, adds SEO foundation. |
| 📄 SE Handover        | 1 week **before GA**        | Enables internal teams to prepare demos and responses.    |
| 📣 Internal Post      | On feature **enablement**   | Signals readiness and promotes usage internally.          |
| 🧾 Release Notes      | **Alongside GA**            | Canonical record of what shipped and why.                 |
| 📰 Newsletter Snippet | Monthly or **on milestone** | Keeps wider audience updated in a digestible format.      |
| 📝 Blog Post          | 1–2 weeks **after GA**      | Focused on storytelling and wider awareness.              |


This allows Marketing and Docs to **collaborate on refinement** rather than scramble to create from scratch.
---

## 🤝 Contributing
Feel free to open issues or submit PRs for new content generators, prompt improvements, or UI tooling.

## 📝 License
MIT