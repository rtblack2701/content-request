import os
import typer
import datetime
from core.fetch_responses import latest
from core.seo_sniper import generate_seo_data
from cli.blog import generate_blog
from cli.announcement import generate_announcement
from cli.handover import generate_se_handover
from cli.newsletter import generate_newsletter
from cli.docs import generate_docs
from cli.release_notes import generate_release_notes

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
        typer.echo(f"✅ Form response logged to: {path}")

@app.command()
def blog():
    "Generates a blog post using the form response title as the keyword."
    if not latest:
        typer.echo("❌ No form responses found.")
        raise typer.Exit()

    path = log_form_response()
    typer.echo(f"✅ Form response logged to: {path}")
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
    typer.echo(f"✅ Form response logged to: {path}")
    typer.echo("✅ Generating feature announcement...")
    generate_announcement()

@app.command()
def handover():
    "Generates an SE handover markdown doc from the form response."
    if not latest:
        typer.echo("❌ No form responses found.")
        raise typer.Exit()

    path = log_form_response()
    typer.echo(f"✅ Form response logged to: {path}")
    typer.echo("✅ Generating SE Handover doc...")
    generate_se_handover()

@app.command()
def newsletter():
    "Generates a newsletter with all Google Form submissions not yet used."
    typer.echo("✅ Generating newsletter...")
    generate_newsletter()

@app.command()
def docs():
    "Generates technical documentation from the latest Google Form entry."
    typer.echo("✅ Generating technical documentation...")
    generate_docs()

@app.command()
def release_notes():
    "Generates release notes from the latest Google Form entry."
    typer.echo("✅ Generating release notes...")
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