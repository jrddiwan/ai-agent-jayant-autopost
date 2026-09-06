"""
Daily Automated 3D Carousel Poster for @ai.agent_jayant
Pipeline:
1. Dynamic Topic Rotator + Gemini Flash generates a fresh, viral AI topic & architecture.
2. Playwright renders the tactile 3D claymorphic HTML slides at 1080x1350 portrait PNG.
3. Images are uploaded to FreeImage CDN for direct high-speed image delivery.
4. Buffer GraphQL API schedules the carousel to @ai.agent_jayant on Instagram.
"""

import os
import sys
import json
import time
import base64
import random
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
# 1. GENERATE DYNAMIC VIRAL AI CONTENT (Gemini)
# ==========================================
CATEGORIES = [
    "AUTONOMOUS AI AGENTS (CrewAI, LangGraph, AutoGen, Multi-agent swarms, Browser agents)",
    "AI NEWS & REVOLUTIONARY MODELS (Claude 3.7 Sonnet, DeepSeek V3 & R1, OpenAI Operator, Grok 3, Gemini 2.0)",
    "AI BUSINESS AUTOMATION & REVENUE (Building 24/7 client systems, AI lead machines, Agency automation)",
    "DEVELOPER & CODING WORKFLOWS (Cursor AI secrets, Claude Code CLI, Building fullstack apps in 10 minutes)",
    "NO-CODE AI PIPELINES (n8n automations, Make.com + AI agent routing, Webhook swarms)",
    "HIDDEN AI PRODUCTIVITY SECRETS (Deep research workflows, Advanced prompt engineering frameworks)"
]


def generate_carousel_content():
    print("[1/4] Brainstorming viral AI topic with Gemini Flash...")
    
    # Pick today's category
    chosen_category = random.choice(CATEGORIES)
    print(f"  -> Category Theme: {chosen_category}")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""
    You are the elite Instagram content strategist for @ai.agent_jayant.
    Your target audience: developers, founders, tech professionals, and builders who want to master AI, autonomous agents, and automation to grow their income and save 20+ hours a week.

    TODAY'S THEME: {chosen_category}

    Create an original, highly save-worthy 8-slide Instagram carousel breakdown on a specific, trending topic within this theme.
    DO NOT use generic advice. Be specific, tactical, and mention real tools (like DeepSeek, Claude 3.7, Cursor, n8n, OpenAI, etc.).

    Return ONLY a valid JSON object matching this structure (no markdown fences, no backticks, just raw JSON):
    {{
      "topic": "Specific viral topic name",
      "categoryTag": "Short category pill (e.g. AI AGENTS, AI NEWS, DEV TOOLS, AUTOMATION)",
      "ctaKeyword": "A single uppercase trigger keyword to comment (e.g. AGENT, PROMPT, FLOW, CLAUDE, SYSTEM, REVENUE)",
      "ctaSub": "I'll DM you the full setup + copy-paste prompts.",
      "caption": "Viral Instagram caption with hook, bullet points, CTA to comment the keyword, follow reminder for @ai.agent_jayant, and 15 hashtags.",
      "plinthTitle": "2-3 word engraved title for 3D rack (e.g. CLAUDE 3.7, AGENT SWARM, DEEPSEEK)",
      "plinthTag": "Short badge tag (e.g. 2026, V3, PRO, 24/7)",
      "items": [
        {{"name": "TOOL 1", "icon": "zap"}},
        {{"name": "TOOL 2", "icon": "cpu"}},
        {{"name": "TOOL 3", "icon": "bot"}},
        {{"name": "TOOL 4", "icon": "chart"}},
        {{"name": "TOOL 5", "icon": "gear"}}
      ],
      "slides": [
        {{
          "id": 1,
          "num": "",
          "title": "PUNCHY HOOK LINE 1",
          "titleGreen": "BOLD NEON PUNCHLINE.",
          "subtitle": "THE 1-SENTENCE HOOK EXPLAINING THE SYSTEM.",
          "metaBotL": "PRINCIPLE OR PROMISE",
          "metaBotR": "VALUE PROPOSITION"
        }},
        {{
          "id": 2,
          "num": "02",
          "title": "THE BREAKTHROUGH OR",
          "titleGreen": "WHY IT MATTERS.",
          "subtitle": "EXPLAINING THE CORE PROBLEM OR REVOLUTIONARY CAPABILITY.",
          "metaBotL": "OLD WAY VS NEW WAY",
          "metaBotR": "EXPONENTIAL LEVERAGE"
        }},
        {{
          "id": 3,
          "num": "03",
          "title": "STEP 1:",
          "titleGreen": "THE INGESTION / SETUP.",
          "subtitle": "HOW THE DATA OR AGENT INITIALIZATION WORKS.",
          "metaBotL": "STEP 1 BREAKDOWN",
          "metaBotR": "AUTONOMOUS SYSTEM"
        }},
        {{
          "id": 4,
          "num": "04",
          "title": "STEP 2:",
          "titleGreen": "THE EXECUTION ENGINE.",
          "subtitle": "HOW THE AI PROCESSES, REASONS, OR CREATES.",
          "metaBotL": "STEP 2 BREAKDOWN",
          "metaBotR": "HIGH SPEED OUTPUT"
        }},
        {{
          "id": 5,
          "num": "05",
          "title": "STEP 3:",
          "titleGreen": "THE DELIVERABLE.",
          "subtitle": "HOW RESULTS ARE DELIVERED OR MONETIZED.",
          "metaBotL": "STEP 3 BREAKDOWN",
          "metaBotR": "MEASURABLE RESULTS"
        }},
        {{
          "id": 6,
          "num": "06",
          "title": "THE COMPLETE",
          "titleGreen": "CONNECTED WORKFLOW.",
          "subtitle": "HOW ALL TOOLS/STEPS INTERACT 24/7 SEAMLESSLY.",
          "metaBotL": "NETWORK MAP",
          "metaBotR": "ZERO MANUAL WORK"
        }},
        {{
          "id": 7,
          "num": "07",
          "title": "THE IMPACT &",
          "titleGreen": "COMPOUNDING RESULTS.",
          "subtitle": "WHAT HAPPENS WHEN THIS RUNS FOR 30 DAYS STRAIGHT.",
          "metaBotL": "COMPOUND VALUE",
          "metaBotR": "WORK LESS SCALE MORE"
        }},
        {{
          "id": 8,
          "num": "08",
          "title": "STEAL THIS",
          "titleGreen": "FULL SYSTEM.",
          "subtitle": "COMMENT BELOW AND I WILL SEND YOU THE COMPLETE SETUP + PROMPT PACK.",
          "metaBotL": "SAVE FOR LATER",
          "metaBotR": "REAL RESULTS"
        }}
      ]
    }}
    """

    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                raw = res["candidates"][0]["content"]["parts"][0]["text"].strip()
                if raw.startswith("```json"): raw = raw[7:]
                if raw.startswith("```"): raw = raw[3:]
                if raw.endswith("```"): raw = raw[:-3]
                data = json.loads(raw.strip())
                print(f"  -> Generated Topic: {data.get('topic')}")
                print(f"  -> CTA Keyword: {data.get('ctaKeyword')}")
                return data
        except Exception as e:
            print(f"  -> Attempt {attempt+1} failed: {e}. Retrying...")
            time.sleep(3)
            
    raise RuntimeError("Failed to generate carousel content from Gemini after 4 attempts.")


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

        # Inject generated content, tiles, branding & CTA into the HTML studio
        page.evaluate("""
            (carousel) => {
                for (let i = 0; i < carousel.slides.length; i++) {
                    const s = carousel.slides[i];
                    const idx = s.id - 1;
                    if (slidesData[idx]) {
                        slidesData[idx].title = s.title;
                        slidesData[idx].titleGreen = s.titleGreen;
                        slidesData[idx].subtitle = s.subtitle;
                        slidesData[idx].metaTopR = carousel.categoryTag || "AI SYSTEMS";
                        if (s.metaBotL) slidesData[idx].metaBotL = s.metaBotL;
                    }
                }
                if (slidesData[0]) {
                    if (carousel.plinthTitle) slidesData[0].plinthTitle = carousel.plinthTitle;
                    if (carousel.plinthTag) slidesData[0].plinthTag = carousel.plinthTag;
                    if (carousel.items && carousel.items.length > 0) {
                        slidesData[0].items = carousel.items;
                    }
                }
                if (slidesData[7]) {
                    slidesData[7].ctaKeyword = carousel.ctaKeyword || "SYSTEM";
                    slidesData[7].ctaSub = carousel.ctaSub || "I'll DM you the full setup + prompts.";
                    if (carousel.plinthTitle) slidesData[7].plinthTitle = carousel.plinthTitle;
                    if (carousel.plinthTag) slidesData[7].plinthTag = carousel.plinthTag;
                    if (carousel.items && carousel.items.length > 0) {
                        slidesData[7].items = carousel.items;
                    }
                }
            }
        """, carousel_data)

        for i in range(len(carousel_data["slides"])):
            page.evaluate(f"goToSlide({i})")
            page.wait_for_timeout(400)

            out_file = OUTPUT_DIR / f"slide_{i+1}.png"
            slide_el = page.query_selector("#slideViewport")
            if slide_el:
                slide_el.screenshot(path=str(out_file))
            else:
                page.screenshot(path=str(out_file))
            
            image_paths.append(str(out_file))
            print(f"  -> Rendered Slide {i+1}/8")

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
        with urllib.request.urlopen(req, timeout=30) as resp:
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

    with urllib.request.urlopen(req, timeout=30) as resp:
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
