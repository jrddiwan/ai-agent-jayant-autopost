"""
Daily Automated Carousel Poster for @ai.agent_jayant
Pipeline:
1. Gemini API generates a viral AI workflow/tip carousel topic & content.
2. Playwright renders the 3D claymorphic HTML slides at 1080x1350 PNG.
3. Images are uploaded via high-speed direct image host (FreeImage / iili.io) to obtain public URLs.
4. Buffer GraphQL API schedules the carousel to @ai.agent_jayant.
"""

import os
import sys
import json
import time
import base64
import urllib.request
import urllib.parse
from pathlib import Path

# ==========================================
# CONFIGURATION & CREDENTIALS
# ==========================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or "AQ.Ab8RN6JR1YuN17YDmBFjTXHXz5xTwY9ZSR65Z3fshG09mLMLSQ"
BUFFER_API_TOKEN = os.environ.get("BUFFER_API_TOKEN") or "yQto5YnVBWqNBlJsJnkOi5ETOiwc6t-fl3YMxIpOIjz"
BUFFER_CHANNEL_ID = os.environ.get("BUFFER_CHANNEL_ID") or "6a8cc31bccaf649a670cfa58"  # @ai.agent_jayant

# Optional Cloudflare R2
R2_ACCOUNT_ID = os.environ.get("R2_ACCOUNT_ID", "")
R2_ACCESS_KEY_ID = os.environ.get("R2_ACCESS_KEY_ID", "")
R2_SECRET_ACCESS_KEY = os.environ.get("R2_SECRET_ACCESS_KEY", "")
R2_BUCKET_NAME = os.environ.get("R2_BUCKET_NAME", "instagram-carousels")
R2_PUBLIC_DOMAIN = os.environ.get("R2_PUBLIC_DOMAIN", "")

# Directories
BASE_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
HTML_PATH = BASE_DIR / "index.html"


# ==========================================
# 1. GENERATE VIRAL CONTENT WITH GEMINI
# ==========================================
def generate_carousel_content():
    print("[1/4] Generating viral carousel topic with Gemini Flash...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GEMINI_API_KEY}"
    
    prompt = """
    You are the head content strategist for @ai.agent_jayant on Instagram.
    Your mission: help the account grow to 10,000 followers fast by delivering high-value, save-worthy AI workflows, automation hacks, and developer/money-making systems.

    Create content for an 8-slide educational carousel.
    The response MUST be ONLY valid JSON matching this schema (no markdown, no backticks):
    {
      "topic": "Short internal topic name",
      "caption": "High-converting Instagram caption with strong hook, 3 bullet points, CTA to comment a keyword, and 10 viral hashtags (#AIAgents #Automation #AIWorkflows #TechTrends ...)",
      "slides": [
        {
          "id": 1,
          "metaTopL": "BUILD\\nAUTOMATE\\nSCALE",
          "metaTopR": "IDEAS\\nLEADS\\nSALES",
          "num": "",
          "title": "I BUILT AN",
          "titleGreen": "AI AUTOMATION TEAM.",
          "subtitle": "7 AI AGENTS. 1 BUSINESS SYSTEM.",
          "metaBotL": "ONE TEAM.\\nREAL RESULTS.",
          "metaBotR": "AI TURNS\\nIDEAS INTO INCOME."
        },
        {
          "id": 2,
          "num": "02",
          "title": "IT FINDS",
          "titleGreen": "WHAT PEOPLE WANT.",
          "subtitle": "THE RESEARCH + PRODUCT AGENTS FIND REAL OPPORTUNITIES.",
          "metaBotL": "SAME WORK.\\nMORE OUTPUT.\\nBIGGER OPPORTUNITIES.",
          "metaBotR": "AI TURNS\\nIDEAS INTO INCOME."
        },
        {
          "id": 3,
          "num": "03",
          "title": "THEN IT FINDS",
          "titleGreen": "CUSTOMERS.",
          "subtitle": "THE LEAD AGENT FINDS AND QUALIFIES THE RIGHT PEOPLE.",
          "metaBotL": "SAME WORK.\\nMORE OUTPUT.\\nBIGGER OPPORTUNITIES.",
          "metaBotR": "AI TURNS\\nIDEAS INTO INCOME."
        },
        {
          "id": 4,
          "num": "04",
          "title": "THEN IT GETS",
          "titleGreen": "ATTENTION.",
          "subtitle": "CONTENT + ADS AGENTS CREATE POSTS, VIDEOS AND ADS TO BRING IN TRAFFIC.",
          "metaBotL": "SAME WORK.\\nMORE OUTPUT.\\nBIGGER OPPORTUNITIES.",
          "metaBotR": "AI TURNS\\nIDEAS INTO INCOME."
        },
        {
          "id": 5,
          "num": "05",
          "title": "THEN IT HELPS",
          "titleGreen": "MAKE THE SALE.",
          "subtitle": "THE SALES AGENT OUTREACHES, FOLLOWS UP, AND CONVERTS LEADS INTO CUSTOMERS.",
          "metaBotL": "SAME WORK.\\nMORE OUTPUT.\\nBIGGER OPPORTUNITIES.",
          "metaBotR": "AI TURNS\\nIDEAS INTO INCOME."
        },
        {
          "id": 6,
          "num": "06",
          "title": "ONE AI KEEPS",
          "titleGreen": "IT ALL RUNNING.",
          "subtitle": "THE OPERATIONS AGENT CONNECTS EVERY AGENT, MANAGES TASKS, AND KEEPS THINGS MOVING 24/7.",
          "metaBotL": "A SYSTEM THAT WORKS\\nTOGETHER.",
          "metaBotR": "AI TURNS\\nIDEAS INTO INCOME."
        },
        {
          "id": 7,
          "num": "07",
          "title": "THE FULL AI",
          "titleGreen": "MONEY-MAKING TEAM.",
          "subtitle": "7 AGENTS. 1 SYSTEM. REAL RESULTS.",
          "metaBotL": "SAME WORK.\\nMORE OUTPUT.\\nBIGGER OPPORTUNITIES.",
          "metaBotR": "AI TURNS\\nIDEAS INTO INCOME."
        },
        {
          "id": 8,
          "num": "08",
          "title": "I BUILT THE",
          "titleGreen": "FULL TEAM.",
          "subtitle": "SAME WORK. MORE OUTPUT. BIGGER OPPORTUNITIES.",
          "metaBotL": "REAL TOOLS.\\nREAL SYSTEMS.\\nREAL RESULTS.",
          "metaBotR": "AI TURNS\\nIDEAS INTO INCOME."
        }
      ]
    }
    """

    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                raw = res["candidates"][0]["content"]["parts"][0]["text"].strip()
                if raw.startswith("```json"):
                    raw = raw[7:]
                if raw.startswith("```"):
                    raw = raw[3:]
                if raw.endswith("```"):
                    raw = raw[:-3]
                data = json.loads(raw.strip())
                print(f"  -> Generated Topic: {data.get('topic')}")
                return data
        except Exception as e:
            print(f"  -> Attempt {attempt+1} failed: {e}. Retrying...")
            time.sleep(2)
    raise RuntimeError("Failed to generate carousel content from Gemini after 3 attempts.")


# ==========================================
# 2. RENDER SLIDES TO 1080x1350 PNG (Playwright)
# ==========================================
def render_slides(carousel_data):
    print("[2/4] Rendering slides with Playwright (1080x1350 portrait)...")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright is not installed. Installing...")
        os.system(f"{sys.executable} -m pip install playwright")
        os.system(f"{sys.executable} -m playwright install chromium")
        from playwright.sync_api import sync_playwright

    image_paths = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1080, "height": 1350},
            device_scale_factor=2
        )

        file_url = f"file:///{HTML_PATH.as_posix()}"
        page.goto(file_url)

        # Inject generated titles into the HTML template
        page.evaluate(f"""
            (newSlides) => {{
                for (let i = 0; i < newSlides.length; i++) {{
                    if (slidesData[i]) {{
                        slidesData[i].title = newSlides[i].title;
                        slidesData[i].titleGreen = newSlides[i].titleGreen;
                        slidesData[i].subtitle = newSlides[i].subtitle;
                    }}
                }}
            }}
        """, carousel_data["slides"])

        for i in range(len(carousel_data["slides"])):
            page.evaluate(f"goToSlide({i})")
            page.wait_for_timeout(350)

            out_file = OUTPUT_DIR / f"slide_{i+1}.png"
            slide_el = page.query_selector("#slideViewport")
            if slide_el:
                slide_el.screenshot(path=str(out_file))
            else:
                page.screenshot(path=str(out_file))
            
            image_paths.append(str(out_file))
            print(f"  -> Rendered {out_file.name}")

        browser.close()

    return image_paths


# ==========================================
# 3. UPLOAD IMAGES TO GET PUBLIC URLS
# ==========================================
def upload_images(image_paths):
    print("[3/4] Uploading images to cloud storage for Buffer...")
    public_urls = []

    # Priority 1: Cloudflare R2 (if configured)
    if R2_ACCOUNT_ID and R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY:
        import boto3
        s3 = boto3.client(
            "s3",
            endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
            aws_access_key_id=R2_ACCESS_KEY_ID,
            aws_secret_access_key=R2_SECRET_ACCESS_KEY,
            region_name="auto"
        )
        timestamp = int(time.time())
        for path_str in image_paths:
            filename = f"carousel_{timestamp}_{Path(path_str).name}"
            s3.upload_file(path_str, R2_BUCKET_NAME, filename, ExtraArgs={"ContentType": "image/png"})
            url = f"{R2_PUBLIC_DOMAIN.rstrip('/')}/{filename}"
            public_urls.append(url)
            print(f"  -> Uploaded to R2: {url}")
        return public_urls

    # Priority 2: Direct High-Speed Image Host (FreeImage CDN / iili.io)
    print("  -> Uploading to high-speed public CDN (FreeImage / iili.io)...")
    for path_str in image_paths:
        filepath = Path(path_str)
        with open(filepath, "rb") as f:
            b64_img = base64.b64encode(f.read()).decode("utf-8")

        params = {
            "key": "6d207e02198a847aa98d0a2a901485a5",
            "action": "upload",
            "source": b64_img,
            "format": "json"
        }
        data = urllib.parse.urlencode(params).encode("utf-8")
        req = urllib.request.Request(
            "https://freeimage.host/api/1/upload",
            data=data,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            img_url = res["image"]["url"]
            public_urls.append(img_url)
            print(f"  -> Uploaded: {img_url}")

    return public_urls


# ==========================================
# 4. PUBLISH / SCHEDULE VIA BUFFER GRAPHQL API
# ==========================================
def schedule_to_buffer(caption, image_urls):
    print(f"[4/4] Scheduling carousel to Buffer for channel {BUFFER_CHANNEL_ID} (@ai.agent_jayant)...")
    
    graphql_url = "https://api.buffer.com"
    assets_input = [{"image": {"url": u}} for u in image_urls]

    mutation = """
    mutation CreatePost($input: CreatePostInput!) {
      createPost(input: $input) {
        ... on PostActionSuccess {
          post {
            id
            status
            dueAt
          }
        }
        ... on MutationError {
          message
        }
      }
    }
    """

    variables = {
        "input": {
            "channelId": BUFFER_CHANNEL_ID,
            "text": caption,
            "assets": assets_input,
            "schedulingType": "automatic",
            "mode": "addToQueue",
            "metadata": {
                "instagram": {
                    "type": "post",
                    "shouldShareToFeed": True
                }
            }
        }
    }

    body = json.dumps({"query": mutation, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(
        graphql_url,
        data=body,
        headers={
            "Authorization": f"Bearer {BUFFER_API_TOKEN}",
            "Content-Type": "application/json"
        }
    )

    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        print("Buffer API Response:")
        print(json.dumps(res, indent=2))

        # Check for errors
        if "errors" in res:
            raise RuntimeError(f"Buffer GraphQL Error: {json.dumps(res['errors'])}")
        create_post_data = res.get("data", {}).get("createPost", {})
        if "message" in create_post_data:
            raise RuntimeError(f"Buffer Mutation Error: {create_post_data['message']}")
        post_obj = create_post_data.get("post")
        if not post_obj or not post_obj.get("id"):
            raise RuntimeError(f"Buffer did not return a valid post: {res}")
        print(f"Successfully scheduled post ID: {post_obj.get('id')} for {post_obj.get('dueAt')}")
        return res


# ==========================================
# MAIN EXECUTION
# ==========================================
def run_daily_job():
    print("==================================================")
    print("Starting Daily Carousel Pipeline for @ai.agent_jayant")
    print("==================================================")
    content = generate_carousel_content()
    images = render_slides(content)
    public_urls = upload_images(images)
    result = schedule_to_buffer(content["caption"], public_urls)
    print("==================================================")
    print("Daily Carousel successfully scheduled to Buffer!")
    print("==================================================")


if __name__ == "__main__":
    run_daily_job()
