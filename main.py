import typer
from fetch_responses import latest
from content.blog.seo_sniper import generate_seo_data
from content.blog.generate_blog import generate_blog

app = typer.Typer(help="Feature Content Generator CLI")

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
        typer.echo("✅ Latest Form Response:")
        for key, value in latest.items():
            typer.echo(f"{key}: {value}")

@app.command()
def blog():
    "Generates a blog post using the form response title as the keyword."
    form_response = latest  # Cache the value of `latest` locally
    if not form_response:
        typer.echo("❌ No form responses found.")
        raise typer.Exit()

    typer.echo("✅ Latest Form Response:")
    for key, value in form_response.items():
        typer.echo(f"{key}: {value}")

    typer.echo("\n--- Sniping SEO structure based on feature title ---")
    keyword = form_response.get("Feature title")
    if not keyword:
        typer.echo("❌ Feature title not found in form response.")
        raise typer.Exit()

    success = generate_seo_data(keyword)
    if not success:
        typer.echo("❌ Blog generation skipped due to missing or invalid SEO structure.")
        raise typer.Exit()

    typer.echo("\n--- Generating blog ---")
    generate_blog()

@app.command()
def all():
    "Runs fetch, snipe, and blog generation using form-derived keyword."
    blog()

if __name__ == "__main__":
    app()