from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import subprocess
import aiohttp
import asyncio

app = FastAPI()

class URLRequest(BaseModel):
    url: str

class ScrapeRequest(BaseModel):
    url: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Web Scraper API!"}

@app.post("/start-scraping")
async def start_scraping(request: URLRequest):
    # Placeholder for starting the scraping process with the provided URL
    url = request.url
    return {"message": f"Scraping started for {url}!"}

@app.get("/data")
async def get_data():
    # Return scraped data
    return JSONResponse(content={"data": data})

@app.get("/download")
async def download_data():
    # Placeholder for downloading data as CSV or JSON
    return {"message": "Download endpoint (to be implemented)"}

@app.post("/download")
async def download_url(request: URLRequest):
    url = request.url
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    # Process content if needed
                    return JSONResponse(content={"status": "success", "url": url})
                else:
                    raise HTTPException(status_code=response.status, detail=f"Failed to download {url}")
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"HTTP error: {str(e)}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}") from e

@app.post("/download-multiple")
async def download_multiple_urls(urls: list[URLRequest]):
    async def fetch_url(url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url.url) as response:
                    if response.status == 200:
                        return {"url": url.url, "status": "success"}
                    else:
                        return {"url": url.url, "status": "failed", "reason": response.status}
        except aiohttp.ClientError as e:
            return {"url": url.url, "status": "error", "reason": str(e)}
        except Exception as e:
            return {"url": url.url, "status": "error", "reason": str(e)}

    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

@app.post("/scrape")
async def scrape_url(request: ScrapeRequest):
    url = request.url
    try:
        process = subprocess.run(
            ["scrapy", "crawl", "book_spider", "-a", f"start_url={url}"],
            capture_output=True,
            text=True,
            check=True
        )

        if process.returncode == 0:
            return {"status": "success", "url": url}
        else:
            raise HTTPException(status_code=500, detail=process.stderr)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Scrapy process error: {e.stderr}") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}") from e