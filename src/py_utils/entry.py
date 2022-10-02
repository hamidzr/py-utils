import typer

app = typer.Typer()


@app.command()
def test():
    """
    For testing purposes.
    """
    print("Hello World!")


if __name__ == "__main__":
    app()
