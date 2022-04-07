import json
import boto3
import zipfile
import subprocess
import os
import asyncio
from pyppeteer import launch
import re

s3_bucket = boto3.resource("s3").Bucket(os.environ.get('BUCKET_NAME'))

S3_PATH = 'stable-headless-chromium-amazonlinux-2017-03.zip'
BROWSER = None

zip_file_path = "/tmp/chrome.zip"
if not os.path.exists(zip_file_path):
    s3_bucket.download_file(S3_PATH, zip_file_path)
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall("/tmp")
        subprocess.run(["chmod", "+x", "/tmp/headless-chromium"], check=True)


async def helper(url):
    browser = await launch(
        args=[
            "--no-sandbox",
            "--single-process",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--no-zygote",
        ],
        executablePath="/tmp/headless-chromium",
        userDataDir="/tmp",
    )
    # browser = await launch()

    page = await browser.newPage()

    await page.goto(url, {'waitUntil': 'domcontentloaded'})
    
    stats_div = await page.querySelector('div#slim_appbar')
    stats = await page.evaluate('(e) => e.textContent', stats_div) 

    results_divs = await page.querySelectorAll('div.g')
    titles = [await page.evaluate('(e) => e.querySelector("h3").textContent', div) for div in results_divs]
    hrefs = [await page.evaluate('(e) => e.querySelector("a").href', div) for div in results_divs]
    try:
        descriptions = [await page.evaluate('(e) => e.querySelector("div[style=\'-webkit-line-clamp:2\']").textContent', div) for div in results_divs]
    except:
        try:
            descriptions = [await page.evaluate('(e) => e.querySelector("div[data-content-feature=\\"1\\"]").textContent', div) for div in results_divs]
        except:
            div_text = [await page.evaluate('(e) => e.textContent', div) for div in results_divs]
            descriptions = []
            for text in div_text:
                chunks = text.split('...')
                if len(chunks[-1]) > 1:
                    desc = chunks[-1].strip()
                else:
                    desc = chunks[-2].strip() + ' ...'
                descriptions.append(desc)

    results = [{"title": title, "href": href, "desc": desc} for title, href, desc in zip(titles, hrefs, descriptions)]

    await browser.close()

    return stats, results


def lambda_handler(event, context):
    body = json.loads(event["body"])
    query = body.get("query")
    if query: query = query.replace('&', '%26')
    start = body.get("start")
    template_url = "https://www.google.com/search?q=site:reddit.com/"
    # Check if there is an r/ restriction which should be at the start of the query
    subreddit_matches = re.search(r'^(r/.*?)(\s|$)', query)
    if subreddit_matches:
        # Directly append query to end of template
        if start:
            query_url = f'{template_url}{query}&start={start}'
        else:
            query_url = f'{template_url}{query}'
    else:
        if start:
            query_url = f'{template_url} {query}&start={start}'
        else:
            query_url = f'{template_url} {query}'
    stats, results = asyncio.get_event_loop().run_until_complete(helper(query_url))
    return {
        'statusCode': 200,
        'body': json.dumps({
            "stats": stats,
            "results": results,
        })
    }
