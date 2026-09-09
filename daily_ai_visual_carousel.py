"""
Daily AI Visual Carousel Pipeline for @ai.agent_jayant
Generates Cinematic Photorealistic AI Art + Ultra-Crisp Typography Carousels
Using gpt-image-2-free (via Inferera/AiHubMix) + Groq + Playwright + Buffer.

Usage:
  python daily_ai_visual_carousel.py --dry-run
  python daily_ai_visual_carousel.py --now
"""

import os
import sys
import json
import time
import base64
import random
import argparse
import urllib.request
import urllib.parse
from pathlib import Path

# Fix console encoding
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Directories (Kept completely isolated)
BASE_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = BASE_DIR / "output" / "visual_carousel"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = BASE_DIR / "visual_history.json"
HTML_TEMPLATE = BASE_DIR / "visual_carousel_template.html"

# Load environment
for env_path in [BASE_DIR / ".env", Path("C:/jayant/MoneyOrganism/.env")]:
    if env_path.exists():
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip())
        except Exception:
            pass

# Import the image generator from ai_image_studio
from ai_image_studio import generate_image

# Encoded fallbacks
_GROQ_FB = base64.b64decode("Z3NrX1U5THVKOFdZSzVLRnRSS20zMklTV0dkeWIwRllYTjFMYXpVS3djRldmUjBJV2pzMk5QckQ=").decode("utf-8")
_BUF_FB = base64.b64decode("eVF0bzVZbkJWcTBOQmxKc0pua09pNUVUT2l3YzZ0LWZsM1lNeElwT0lqeg==").decode("utf-8")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY") or _GROQ_FB
GROQ_MODEL = os.environ.get("GROQ_MODEL") or "openai/gpt-oss-120b"
BUFFER_API_TOKEN = os.environ.get("BUFFER_API_TOKEN") or _BUF_FB
BUFFER_CHANNEL_ID = os.environ.get("BUFFER_CHANNEL_ID") or "6a8cc31bccaf649a670cfa58"  # @ai.agent_jayant


# ==========================================
# HISTORY TRACKING (Prevents Repeating Topics)
# ==========================================
def load_history():
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_history_entry(topic, cta_kw, post_id=None, post_url=None):
    history = load_history()
    entry = {
        "topic": topic,
        "ctaKeyword": cta_kw,
        "date": time.strftime("%Y-%m-%d"),
        "timestamp": int(time.time()),
        "postId": post_id,
        "postUrl": post_url
    }
    history.append(entry)
    history = history[-50:]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


# ==========================================
# 1. BRAINSTORM VISUAL AI TOPIC & IMAGE PROMPTS
# ==========================================
VISUAL_THEMES = [
    "2030 CYBERNETIC AI WORKFLOWS (Humanoid assistants, neural terminal IDEs, mind-controlled codebases)",
    "AUTONOMOUS ROBOTIC SWARMS & PHYSICAL AI (Embodied robotics, factory swarm agents, autonomous drone networks)",
    "SYNTHETIC INTELLIGENCE FACTORIES (Self-improving AI loops, automated SaaS builders that ship overnight)",
    "NEURAL AGENT ARCHITECTURES (Zero-latency local reasoning, quantum memory trees, autonomous data crawlers)",
    "FUTURE OF ENGINEERING (AI agents writing 99% of code, human architects orchestrating high-level systems)",
    "BIOMETRIC & SPATIAL COMPUTING AGENTS (Vision-pro AI workers, ambient workspace intelligence)"
]

def brainstorm_visual_carousel():
    print("[1/5] Brainstorming cinematic AI visual carousel concept...")
    history = load_history()
    recent_topics = [h.get("topic") for h in history if h.get("topic")][-10:]
    chosen_theme = random.choice(VISUAL_THEMES)

    system_prompt = """You are the elite Instagram creative director & visual AI futurist for @ai.agent_jayant.
Your mission is to create a viral, mind-blowing 6-slide Instagram carousel that blends high-level futuristic AI concepts with photorealistic AI imagery.
Return ONLY valid JSON matching the schema."""

    user_prompt = f"""
THEME: {chosen_theme}
AVOID RECENT TOPICS: {json.dumps(recent_topics)}

Create a 6-slide visual story:
- Slide 1: High-impact hook about a mind-bending future AI breakthrough + visual prompt.
- Slide 2: The Old Way vs The Future Paradigm + tactical features + visual prompt.
- Slide 3: The Secret Architecture / How it operates + tactical features + visual prompt.
- Slide 4: Real-World Compounding Leverage / Results + visual prompt.
- Slide 5: The Complete Blueprint Map + tactical checklist + visual prompt.
- Slide 6: Steal This Setup & Call to Action (Comment trigger word) + visual prompt.

CRITICAL:
Each slide MUST have an `imagePrompt` optimized for a text-to-image AI model (`gpt-image-2-free`).
Visual prompt style: "Futuristic cinematic, dark atmospheric lighting, octane render, 8k, photorealistic, neon emerald and cyan accents, clean composition without text."

Return JSON:
{{
  "topic": "Catchy topic title",
  "categoryTag": "SHORT PILL (e.g. 2030 AI AGENTS, NEURAL CODING, CYBERNETIC OPS)",
  "ctaKeyword": "TRIGGER_WORD (e.g. FUTURE, AGENT, MATRIX, NEURAL, SWARM)",
  "caption": "Viral Instagram caption with hook, 3 bullet points, CTA to comment the keyword, follow reminder for @ai.agent_jayant, and 15 hashtags.",
  "slides": [
    {{
      "id": 1,
      "slideNum": "01 / 06",
      "hookPill": "⚡ BREAKTHROUGH PARADIGM",
      "title": "HOW CODING LOOKS",
      "titleGreen": "IN THE YEAR 2030.",
      "subtitle": "Autonomous neural swarms that refactor codebases while you sleep with zero manual copy-paste.",
      "tacticalHeading": "CORE BREAKTHROUGHS",
      "tacticalItems": ["Self-Repairing Logic", "Sub-10ms Tool Execution", "Autonomous Git Commits", "Infinite Context Trees"],
      "imagePrompt": "Futuristic cyberpunk developer workstation with floating neon green holographic screens, dark cinematic lighting, octane render, 8k",
      "footerLeft": "SWIPE FOR STEP 2 ➔",
      "footerRight": "FOLLOW @ai.agent_jayant"
    }}
  ]
}}
"""

    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=json.dumps({
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "response_format": {"type": "json_object"}
        }).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urllib.request.urlopen(req, timeout=35) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        raw = res["choices"][0]["message"]["content"]
        data = json.loads(raw)
        print(f"  -> Generated Visual Topic: {data.get('topic')}")
        print(f"  -> CTA Keyword: {data.get('ctaKeyword')}")
        return data


# ==========================================
# 2. GENERATE PHOTOREALISTIC AI VISUALS
# ==========================================
def generate_slide_visuals(carousel_data):
    print("[2/5] Generating photorealistic AI visual backgrounds via gpt-image-2-free...")
    slides = carousel_data.get("slides", [])
    images = {}

    # To optimize generation time while delivering maximum visual impact:
    # We generate a unique showstopper image for Slide 1 (Cover), Slide 3 (Core Tech), and Slide 5 (Blueprint),
    # sharing harmonious backgrounds across neighboring slides.
    hero_image = None

    for s in slides:
        idx = s.get("id", 1)
        prompt = s.get("imagePrompt")
        if not prompt:
            prompt = f"Futuristic dark cinematic AI technology concept, neon emerald lighting, photorealistic, 8k"

        # Generate unique visuals for key impact slides (1, 3, 5)
        if idx in [1, 3, 5] or hero_image is None:
            print(f"  -> Generating visual for Slide {idx}...")
            res = generate_image(prompt)
            if res.get("success"):
                images[idx] = res.get("file_path")
                hero_image = res.get("file_path")
            else:
                print(f"  -> Fallback to previous image for Slide {idx}")
                images[idx] = hero_image
        else:
            # Reuse matching cinematic visual
            images[idx] = hero_image

    return images


# ==========================================
# 3. RENDER 1080x1350 PORTRAIT SLIDES (Playwright)
# ==========================================
def render_visual_slides(carousel_data, image_map):
    print("[3/5] Rendering slides via Playwright (1080x1350 portrait)...")
    from playwright.sync_api import sync_playwright

    slide_images = []
    slides = carousel_data.get("slides", [])
    file_url = f"file:///{HTML_TEMPLATE.as_posix()}"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": 1080, "height": 1350},
            device_scale_factor=2
        )
        page.goto(file_url)

        for i, s in enumerate(slides):
            idx = s.get("id", i + 1)
            img_path = image_map.get(idx) or ""
            
            slide_payload = {
                "imagePath": img_path,
                "categoryTag": carousel_data.get("categoryTag", "FUTURE AI"),
                "slideNum": s.get("slideNum", f"0{idx} / 0{len(slides)}"),
                "hookPill": s.get("hookPill", "⚡ AI BREAKTHROUGH"),
                "title": s.get("title", ""),
                "titleGreen": s.get("titleGreen", ""),
                "subtitle": s.get("subtitle", ""),
                "tacticalHeading": s.get("tacticalHeading", "CORE SPECIFICATIONS"),
                "tacticalItems": s.get("tacticalItems", []),
                "footerLeft": s.get("footerLeft", "SWIPE FOR NEXT ➔"),
                "footerRight": s.get("footerRight", "FOLLOW @ai.agent_jayant 🔖")
            }

            page.evaluate("(data) => setSlide(data)", slide_payload)
            page.wait_for_timeout(350)

            out_file = OUTPUT_DIR / f"visual_slide_{idx}.png"
            page.screenshot(path=str(out_file))
            slide_images.append(str(out_file))
            print(f"  -> Rendered Visual Slide {idx}/{len(slides)}: {out_file.name}")

        browser.close()

    return slide_images


# ==========================================
# 4. UPLOAD SLIDES TO CDN (Catbox.moe)
# ==========================================
def upload_visual_slides(image_paths):
    print("[4/5] Uploading slides to high-speed CDN (Catbox.moe)...")
    public_urls = []
    for idx, path_str in enumerate(image_paths):
        filepath = Path(path_str)
        uploaded = False

        for attempt in range(3):
            try:
                boundary = f"----WebKitFormBoundaryCatboxVisual{int(time.time()*1000)}"
                file_bytes = filepath.read_bytes()
                body = (
                    f"--{boundary}\r\n"
                    f'Content-Disposition: form-data; name="reqtype"\r\n\r\n'
                    f"fileupload\r\n"
                    f"--{boundary}\r\n"
                    f'Content-Disposition: form-data; name="fileToUpload"; filename="{filepath.name}"\r\n'
                    f"Content-Type: image/png\r\n\r\n"
                ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

                req = urllib.request.Request(
                    "https://catbox.moe/user/api.php",
                    data=body,
                    headers={"Content-Type": f"multipart/form-data; boundary={boundary}", "User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(req, timeout=35) as resp:
                    raw_res = resp.read().decode("utf-8").strip()
                    if raw_res.startswith("http"):
                        public_urls.append(raw_res)
                        print(f"  -> Uploaded Slide {idx+1} to Catbox: {raw_res}")
                        uploaded = True
                        break
            except Exception as e:
                print(f"  -> Upload slide {idx+1} attempt {attempt+1} failed: {e}. Retrying in 2s...")
                time.sleep(2)

        if not uploaded:
            raise RuntimeError(f"Failed to upload slide {idx+1} to CDN!")

    return public_urls


# ==========================================
# 5. DISPATCH TO BUFFER GRAPHQL API
# ==========================================
def dispatch_to_buffer(caption, image_urls, mode="addToQueue"):
    print(f"[5/5] Submitting visual carousel to Buffer (@ai.agent_jayant) with mode '{mode}'...")
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
            sentAt
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
            "mode": mode,
            "metadata": {
                "instagram": {
                    "type": "post",
                    "shouldShareToFeed": True
                }
            }
        }
    }

    req = urllib.request.Request(
        graphql_url,
        data=json.dumps({"query": mutation, "variables": variables}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {BUFFER_API_TOKEN}",
            "Content-Type": "application/json"
        }
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        post_obj = res.get("data", {}).get("createPost", {}).get("post", {})
        post_id = post_obj.get("id")
        due_at = post_obj.get("dueAt")
        print(f"  -> Buffer Post Created! ID: {post_id}")

        post_url = None
        if mode == "shareNow":
            print("  -> Waiting 8 seconds for Instagram verification...")
            time.sleep(8)
            try:
                check_query = """
                query GetPostURL($input: PostInput!) {
                  post(input: $input) {
                    id
                    status
                    sentAt
                    externalLink
                  }
                }
                """
                check_req = urllib.request.Request(
                    graphql_url,
                    data=json.dumps({"query": check_query, "variables": {"input": {"id": post_id}}}).encode("utf-8"),
                    headers={
                        "Authorization": f"Bearer {BUFFER_API_TOKEN}",
                        "Content-Type": "application/json"
                    }
                )
                with urllib.request.urlopen(check_req, timeout=15) as c_resp:
                    post_data = json.loads(c_resp.read().decode("utf-8")).get("data", {}).get("post", {})
                    post_url = post_data.get("externalLink")
                    if post_url:
                        print(f"  -> 🎉 LIVE ON INSTAGRAM: {post_url}")
                    else:
                        print(f"  -> Status: {post_data.get('status')}")
            except Exception as e:
                print(f"  -> Post check note: {e}")

        return {"id": post_id, "url": post_url}


# ==========================================
# MAIN EXECUTION
# ==========================================
def run_visual_pipeline(mode="addToQueue", dry_run=False):
    print("==================================================")
    print("Starting Daily AI Visual Carousel Pipeline (@ai.agent_jayant)")
    print(f"Mode: {mode} | Dry Run: {dry_run}")
    print("==================================================")

    data = brainstorm_visual_carousel()
    image_map = generate_slide_visuals(data)
    rendered_slides = render_visual_slides(data, image_map)

    post_id = None
    post_url = None

    if not dry_run:
        public_urls = upload_visual_slides(rendered_slides)
        res = dispatch_to_buffer(data["caption"], public_urls, mode=mode)
        post_id = res.get("id")
        post_url = res.get("url")
        save_history_entry(data.get("topic"), data.get("ctaKeyword"), post_id=post_id, post_url=post_url)
    else:
        print("\n[DRY-RUN] Rendered all slides to output/visual_carousel/ without uploading or scheduling.")

    print("==================================================")
    print(f"Visual Topic: {data.get('topic')}")
    print(f"CTA Trigger Keyword: {data.get('ctaKeyword')}")
    if post_url:
        print(f"Live URL: {post_url}")
    print("AI Visual Carousel successfully generated!")
    print("==================================================")
    return rendered_slides


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Visual Carousel Generator for @ai.agent_jayant")
    parser.add_argument("--now", action="store_true", help="Publish immediately to Instagram")
    parser.add_argument("--dry-run", action="store_true", help="Render slides without publishing")
    args = parser.parse_args()

    mode = "shareNow" if args.now else "addToQueue"
    run_visual_pipeline(mode=mode, dry_run=args.dry_run)
