import os
import typer
import datetime
from fetch_responses import latest
from content.blog.seo_sniper import generate_seo_data
from content.blog.generate_blog import generate_blog
from content.announcement.generate_announcement import generate_announcement
from content.se_handover.generate_se_handover import generate_se_handover
from content.newsletter.generate_newsletter import generate_newsletter
from content.docs.generate_docs import generate_docs
from content.release_notes.generate_release_notes import generate_release_notes

app = typer.Typer(help="Feature Content Generator CLI")

def log_form_response():
    if not latest:
        return None
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "latest_form_response.log")

    with open(log_path, "w") as f:
        f.write(f"✅ Latest Form Response - Logged at {datetime.datetime.now()}\n\n")
        for key, value in latest.items():
            f.write(f"{key}: {value}\n")

    return log_path

@app.command()
def snipe(keyword: str):
    "Snipes the SEO structure for a given keyword."
    generate_seo_data(keyword)

@app.command()
def fetch():
    "Displays the latest response from the form."
    if not latest:
        typer.echo("❌ No form responses found.")
    else:
        path = log_form_response()

@app.command()
def blog():
    "Generates a blog post using the form response title as the keyword."
    if not latest:
        typer.echo("❌ No form responses found.")
        raise typer.Exit()

    path = log_form_response()
    typer.echo("\n--- Sniping SEO structure based on feature title ---")

    keyword = latest.get("Feature title")
    if not keyword:
        typer.echo("❌ Feature title not found in form response.")
        raise typer.Exit()

    success = generate_seo_data(keyword, latest["Feature title"])
    if not success:
        typer.echo("❌ Blog generation skipped due to missing or invalid SEO structure.")
        raise typer.Exit()

    typer.echo("\n--- Generating blog ---")
    generate_blog()

@app.command()
def announcement():
    "Generates a short internal and social-ready announcement post."
    if not latest:
        typer.echo("❌ No form responses found.")
        raise typer.Exit()

    path = log_form_response()
    typer.echo("\n--- Generating feature announcement ---")
    generate_announcement()

@app.command()
def handover():
    "Generates an SE handover markdown doc from the form response."
    if not latest:
        typer.echo("❌ No form responses found.")
        raise typer.Exit()

    path = log_form_response()
    typer.echo("\n--- Generating SE handover ---")
    generate_se_handover()

@app.command()
def newsletter():
    "Generates a newsletter with all Google Form submissions not yet used."
    typer.echo("\n--- Generating newsletter ---")
    generate_newsletter()

@app.command()
def docs():
    "Generates technical documentation from the latest Google Form entry."
    typer.echo("\n--- Generating technical documentation ---")
    generate_docs()

@app.command()
def release_notes():
    "Generates release notes from the latest Google Form entry."
    typer.echo("\n--- Generating release ntoes ---")
    generate_release_notes()

@app.command()
def all():
    "Runs fetch, SEO snipe, blog, announcement, and handover generation."
    blog()
    announcement()
    handover()
    newsletter()
    docs()
    release_notes() #type automatically swaps _ with -, so run with python miain.py release-notes

if __name__ == "__main__":
    app()