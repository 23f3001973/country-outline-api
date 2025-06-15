from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/generate")
def generate_outline(country: str = Query(...)):
    # Format country name for URL
    country_name = country.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{country_name}"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return {"status": "error", "detail": "Wikipedia page not found"}

    soup = BeautifulSoup(response.text, "html.parser")
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    markdown_lines = []
    for tag in headings:
        level = int(tag.name[1])  # h2 -> 2
        text = tag.get_text(strip=True)
        markdown_lines.append(f"{'#' * level} {text}")

    markdown = "\n".join(markdown_lines)
    return {"status": "success", "outline": markdown}