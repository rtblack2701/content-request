# ✨ Feature Content Generator

This project automates the generation of multiple types of product content from a single Google Form submission. Designed for teams shipping features regularly, it reduces the manual effort involved in creating internal documentation, marketing copy, and more — by using the OpenAI and Google APIs together.

## 💡 Why this exists

Shipping a feature doesn’t stop at writing code. Every release deserves:

- Clear documentation
- A concise internal handover
- A public announcement
- A compelling blog post
- A newsletter mention
- Accurate release notes

But coordinating these across docs, marketing, sales engineering, and product can be slow and inconsistent. This tool automates the content scaffolding so you can focus on refinement and coordination, not writing from scratch.

## 🧩 How it works

1. **Engineers submit a Google Form** describing the feature at the point it reaches UAT or QA.
2. The form data is written to a linked Google Sheet.
3. This CLI app fetches the latest response and uses OpenAI to generate various types of content:
   - A blog (SEO-optimized)
   - Internal + social-ready announcements
   - Sales engineering handover documentation
   - (Coming soon) Technical docs, Release notes, and Newsletter snippets

---

## 📙 Blog Post

Provides a narrative overview of the feature, its benefits, and real-world applications.  
💡 **SEO Sniping:**  
Before generating the blog, the app runs a live search on Google using the feature title. It:

- Scrapes the top-ranking non-sponsored article.
- Parses the heading structure and word count.
- Uses this structure to inform (but not dictate) the blog layout.

If the article has too few headings or is irrelevant (e.g. product docs, pricing pages), the blog generation is skipped automatically to avoid low-quality results.

---

## 📣 Internal + Social Media Announcement

Generates a short and exciting launch post suitable for both Slack and social media.

- Identifies tone based on keywords (e.g. `Now supported`, `New feature`, `Best practice spotlight`).
- Includes emojis, hashtags, and bullet point value props.
- Consistently under 100 words.

---

## 📄 SE Handover Document

Creates a markdown document to help Sales Engineering teams understand and explain the feature.

Sections include:

- Feature description
- Real-world use case
- Real-life scenario comparison (AI-generated)
- Key benefits
- Enablement instructions
- Known limitations
- Demos and additional resources (with placeholders if not provided)

---

## 📦 Coming Soon

- 📘 Technical documentation (like [Unleash Quickstart](https://docs.getunleash.io/quickstart))
- 📨 Newsletter snippet
- 📋 Release notes

---

## 🚀 Getting Started

Follow these steps to set up your environment, connect to the Google Form, and start generating content automatically.

### 1. ✅ Install dependencies

Create a virtual environment (recommended) and install the required packages:

```bash
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 2. 🧾 Connect your Google Form and Sheet

Use this sample form: [Feature Content Form](https://forms.gle/ngNvbon2XQPjmbUV8)  
Or create your own. Be sure to link the form to a Google Sheet.

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

---

### 3. 🔐 Set up your `.env` file

Create a `.env` file in the root directory of the project with the following contents:

```env
OPENAI_API_KEY=your-openai-api-key
GOOGLE_SHEET_ID=your-google-sheet-id
GOOGLE_CREDENTIALS_PATH=./path/to/credentials.json
```

- **OPENAI_API_KEY:** Your key from OpenAI
- **GOOGLE_SHEET_ID:** Found in the URL of your linked sheet: https://docs.google.com/spreadsheets/d/<THIS_ID>/edit#gid=0
- **GOOGLE_CREDENTIALS_PATH:** Path to your downloaded Google service account credentials file.

---

### 4. ✅ Run the CLI

Once everything is set up, you can use the CLI to generate different types of content from the most recent form response:

```bash
python main.py fetch           # See the latest form submission
python main.py blog            # Generate a technical blog
python main.py announcement    # Create an internal/social announcement
python main.py handover        # Generate an SE handover doc
python main.py release-notes   # Generate feature release notes
python main.py docs            # Generate technical documentation
python main.py all             # Run all generators
```
⸻

🧭 Strategic Content Cadence & GTM Alignment

This project isn’t just about content automation — it’s designed to accelerate collaboration across Product, Engineering, Marketing, and Docs.

🔍 Why this approach?

As a Developer Relations Engineer, I found myself chasing down details post-development, often having to produce documentation at the last minute. Coordination across content types was reactive and inconsistent, despite interest from Product Marketing and Comms in creating a broader narrative.

By introducing a simple, QA/UAT trigger point via a Google Form, I created a single source of feature truth early in the dev cycle — and used that to automatically scaffold multiple content types (docs, announcements, blogs, etc.).

This reduces bottlenecks, creates a consistent voice, and ensures content production begins before the release deadline hits.

⸻

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