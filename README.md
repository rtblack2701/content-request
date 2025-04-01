# Feature Content Generator

This repository automates the creation of several content deliverables from a single Google Form submission: [Feature Content Form](https://forms.gle/ngNvbon2XQPjmbUV8).

The goal is to reduce manual overhead and ensure consistent messaging across documentation, marketing, and internal teams by centralizing all relevant feature information in one place and using OpenAI to intelligently generate:

- Technical Docs
- Blog Posts
- Internal & Social Media Announcements
- Sales Engineering Handover Documents
- Release Notes
- Newsletter Highlights

---

## 📄 How It Works

1. **Feature Info Collection**
   - Engineers or PMs fill out the [Feature Content Form](https://forms.gle/ngNvbon2XQPjmbUV8).
   - The form collects:
     - Feature title & description
     - Key benefits
     - How to enable the feature
     - Release version
     - Real-world use case
     - Known limitations or gotchas
     - Demo video link (optional)
     - Competitor resources (optional)

2. **Data Parsing**
   - Responses are pulled from the Google Sheet via the Sheets API.
   - Latest response is cached and used for content generation.

3. **Prompt Definition**
   - Structured templates for each content type (stored in `/prompts`) are dynamically filled using the form data.
   - Each content type has a tailored prompt designed for the OpenAI Chat API.

4. **Content Generation**
   - Content is generated using the GPT-4 API.
   - SEO support for blog posts includes scraping the top non-sponsored Google result related to the feature title to inform structure.

5. **Output**
   - All outputs are written to the `/output` directory in markdown format.

---

## 📖 Generated Content Types

### ✍️ Technical Docs *(Coming Soon)*
Documentation-style content focused on how the feature works, how to enable/configure it, and what value it provides.

### 📙 Blog Post
The blog post offers a developer-focused narrative about the feature: what it is, why it matters, and how it’s used in real-world scenarios. The goal is to produce an insightful, educational blog that can stand on its own while supporting the broader content strategy.

What makes this blog special is its SEO-informed structure, which is automatically generated through a process we call SEO sniping:
- The app takes the feature title submitted through the Google Form and searches for the top non-sponsored result on Google.
- It uses Selenium to open a Chrome browser (or undetected_chromedriver in CAPTCHA-safe environments), searches for the keyword, and collects the first organic article result.
- The content of that article is scraped and passed through an internal analyzer that extracts:
- HTML headings and their structure (e.g., H1, H2, H3),
- Article word count,
- SEO-relevant terminology.
- These headings are not used to dictate the blog content but rather to guide the structure — ensuring the resulting blog is compatible with what people are already searching for.
- The actual blog topic is always rooted in the feature title, not the scraped article — this ensures consistency and relevance to the product.

This careful blend of SEO alignment and product relevance makes each blog more discoverable while remaining genuinely useful to developers and stakeholders.

### 💬 Internal / Social Announcement
A short, enthusiastic summary of the feature designed for internal Slack announcements or external social media posts.

### 👨‍💼 Sales Engineering Handover
Detailed, practical guide for SEs to understand and present the feature:
- Feature explanation
- Real-world example
- Analogy or relatable developer principle
- Benefits, limitations, enablement steps
- Video guides or screen recordings

### 🔄 Release Notes *(Coming Soon)*
Concise, clear notes describing what was released, why it matters, and how users can benefit.

### 🌐 Newsletter Highlight *(Coming Soon)*
A 2-3 sentence blurb highlighting the feature, ideal for embedding in product update emails.

---

## ⚙️ CLI Commands

Run any content type generator with:
```bash
python main.py blog
python main.py announcement
python main.py handover
```

Run everything:
```bash
python main.py all
```

---

## 🌐 SEO Sniping
Blog posts use a scraping script that finds the top non-sponsored Google result for the feature title and analyzes its heading structure for SEO-informed generation.

---

## 🚀 Roadmap
- [ ] Interactive CLI menu for prompt editing before generation.
- [ ] Support for scheduling generation from new form submissions.
- [ ] More content types: Docs, Release Notes, Newsletters.
- [ ] Built-in Confluence/GitHub/Slack publisher.

---

## 🚪 Contributing
Pull requests are welcome! This project is internal but aims to become reusable for other teams and content workflows.

---

## 👋 Made by DevRel, for everyone who hates duplicating content.

