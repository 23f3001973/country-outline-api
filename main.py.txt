from fastapi import FastAPI
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/outline")
async def get_country_outline(country: str):
    url = f"https://en.wikipedia.org/wiki/{country}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        outline = " ".join(p.text for p in paragraphs[:3])
        return {"country": country, "outline": outline}