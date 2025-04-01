# main.py
import typer
from fetch_responses import latest
from content.blog.seo_sniper import generate_seo_data
from content.blog.generate_blog import generate_blog
from content.announcement.generate_announcement import generate_announcement

app = typer.Typer(help="Feature Content Generator CLI")

@app.command()
def fetch():
    "Displays the latest response from the form."
    if not latest:
        typer.echo("❌ No form responses found.")
    else:
        typer.echo("✅ Latest Form Response:")
        for key, value in latest.items():
            typer.echo(f"{key}: {value}")

@app.command()
def blog():
    "Generates a blog post using the feature title as the topic."
    if not latest:
        typer.echo("❌ No form responses found.")
        raise typer.Exit()

    typer.echo("✅ Latest Form Response:")
    for key, value in latest.items():
        typer.echo(f"{key}: {value}")

    typer.echo("\n--- Sniping SEO structure based on feature title ---")
    keyword = latest.get("Feature title")
    if not keyword:
        typer.echo("❌ Feature title not found in form response.")
        raise typer.Exit()

    from content.blog.seo_sniper import generate_seo_data
    success = generate_seo_data(keyword)
    if not success:
        typer.echo("❌ Blog generation skipped due to missing or invalid SEO structure.")
        raise typer.Exit()

    typer.echo("\n--- Generating blog ---")
    generate_blog()

@app.command()
def announcement():
    "Generates a product announcement for social and internal sharing."
    if not latest:
        typer.echo("❌ No form responses found.")
        raise typer.Exit()

    typer.echo("✅ Generating feature announcement...")
    generate_announcement()

@app.command()
def all():
    "Runs blog and announcement generation using form-derived data."
    blog()
    announcement()

if __name__ == "__main__":
    app()