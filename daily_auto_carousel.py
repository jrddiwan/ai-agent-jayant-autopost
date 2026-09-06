"""
Daily Automated 3D Carousel Poster & Resource Hub for @ai.agent_jayant
Pipeline:
1. Dynamic Modern AI Brainstormer (Gemini Flash) generates cutting-edge architecture & prompt pack.
2. Playwright renders 3D tactile claymorphic slides (cubes, blocks, dominoes with official platform logos) at 1080x1350 PNG.
3. Automatically generates companion web resource guide (docs/index.html) with 1-click "Copy Prompt" button.
4. Images uploaded via FreeImage CDN for direct high-speed Instagram delivery.
5. Buffer GraphQL API schedules the carousel to @ai.agent_jayant.
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
DOCS_DIR = BASE_DIR / "docs"
OUTPUT_DIR.mkdir(exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)
HTML_PATH = BASE_DIR / "index.html"


# ==========================================
# 1. GENERATE DYNAMIC CUTTING-EDGE AI TOPIC
# ==========================================
CATEGORIES = [
    "AUTONOMOUS MULTI-AGENT SWARMS (Model Context Protocol / MCP, LangGraph, Multi-agent routing, Browser-use agents)",
    "FRONTIER REASONING & DEV SYSTEMS (Cursor AI agent rules, Claude Code CLI, Autonomous fullstack building, Copilot)",
    "AUTONOMOUS BUSINESS & REVENUE ENGINES (24/7 inbound lead machines, Automated outbound SDR swarms, Supabase vector databases)",
    "PRODUCTION NO-CODE & LOW-CODE PIPELINES (n8n production agents, Make.com webhook routing, API swarms)",
    "LOCAL AI & EMBODIED INTELLIGENCE (Ollama agent swarms, DeepSeek reasoning on device, Private enterprise RAG)"
]

FALLBACK_TOPICS = [
    {
        "topic": "The 24/7 Autonomous Inbound Lead Machine",
        "categoryTag": "MCP AGENT SWARM",
        "shapeStyle": "cube",
        "ctaKeyword": "REVENUE",
        "ctaSub": "I'll DM you the full setup + copy-paste prompt pack.",
        "caption": "Most founders waste 20+ hours a week prospecting and qualifying leads manually.\n\nHere is how to deploy a 24/7 autonomous 3-agent swarm that discovers prospects, qualifies them with AI, and personalizes outreach while you sleep. 🤖\n\n📌 Save this post for your next build!\n\n💬 Comment \"REVENUE\" below and I will send you the full step-by-step setup guide + copy-paste master prompt!\n\nFollow @ai.agent_jayant for daily autonomous AI systems.\n\n#AIAgents #ArtificialIntelligence #Automation #CursorAI #Claude #LangGraph #OpenAI #BuildInPublic #NoCode #n8n #DeepSeek #TechTrends #Startup #DevTools #Productivity",
        "plinthTitle": "AI LEAD SWARM",
        "plinthTag": "24/7 PRO",
        "items": [
            {"name": "Cursor", "icon": "cursor", "shape": "cube"},
            {"name": "Claude", "icon": "anthropic", "shape": "cube"},
            {"name": "n8n", "icon": "n8n", "shape": "cube"},
            {"name": "Supabase", "icon": "supabase", "shape": "cube"},
            {"name": "OpenAI", "icon": "openai", "shape": "cube"}
        ],
        "slides": [
            {
                "id": 1,
                "num": "",
                "title": "HOW TO BUILD A 24/7",
                "titleGreen": "AI CLIENT MACHINE.",
                "subtitle": "REPLACE A $6,000/MO SDR TEAM WITH AN AUTONOMOUS 3-AGENT SYSTEM.",
                "metaBotL": "3 AI AGENTS • 1 BUSINESS SYSTEM",
                "metaBotR": "FOLLOW @ai.agent_jayant"
            },
            {
                "id": 2,
                "num": "02",
                "title": "THE BOTTLENECK IN",
                "titleGreen": "MANUAL OUTREACH.",
                "subtitle": "MANUAL PROSPECTING TAKES 4+ HOURS A DAY WITH A 2% CONVERSION RATE.",
                "metaBotL": "OLD SDR TEAMS VS AI SWARMS",
                "metaBotR": "100X SPEED & ACCURACY"
            },
            {
                "id": 3,
                "num": "03",
                "title": "AGENT 1:",
                "titleGreen": "THE PROSPECTING RADAR.",
                "subtitle": "AUTONOMOUSLY SCANS LINKEDIN, DIRECTORIES, AND NEWS SIGNALS FOR BUYING INTENT.",
                "metaBotL": "HIGH-INTENT SIGNALS",
                "metaBotR": "FILTERED IN REAL-TIME"
            },
            {
                "id": 4,
                "num": "04",
                "title": "AGENT 2:",
                "titleGreen": "THE INTELLIGENCE RESEARCHER.",
                "subtitle": "DEEP SEARCHES EACH TARGET'S RECENT ANNOUNCEMENTS AND WRITES HYPER-PERSONALIZED ANGLES.",
                "metaBotL": "ZERO GENERIC TEMPLATES",
                "metaBotR": "94% OPEN RATE"
            },
            {
                "id": 5,
                "num": "05",
                "title": "AGENT 3:",
                "titleGreen": "THE OBJECTION HANDLER.",
                "subtitle": "AUTOMATICALLY REPLIES TO QUESTIONS AND DIRECTLY BOOKS QUALIFIED LEADS TO CALENDAR.",
                "metaBotL": "INSTANT RESPONSE (<2 MIN)",
                "metaBotR": "CLOSES CALLS 24/7"
            },
            {
                "id": 6,
                "num": "06",
                "title": "THE COMPLETE",
                "titleGreen": "CONNECTED PIPELINE.",
                "subtitle": "CURSOR BUILDS THE LOGIC, N8N ORCHESTRATES THE WORKFLOW, SUPABASE STORES THE MEMORY.",
                "metaBotL": "FULL ARCHITECTURE MAP",
                "metaBotR": "ZERO MANUAL INTERVENTION"
            },
            {
                "id": 7,
                "num": "07",
                "title": "THE COMPOUNDING",
                "titleGreen": "SYSTEM RESULTS.",
                "subtitle": "30 DAYS RUNNING: 1,200 QUALIFIED PROSPECTS, 84 BOOKED CALLS, $0 HUMAN COST.",
                "metaBotL": "SCALE WITHOUT HIRING",
                "metaBotR": "SYSTEMS > EFFORT"
            },
            {
                "id": 8,
                "num": "08",
                "title": "STEAL THIS",
                "titleGreen": "FULL SETUP & PROMPTS.",
                "subtitle": "COMMENT BELOW AND I WILL SEND YOU THE COMPLETE SYSTEM ARCHITECTURE + COPY-PASTE PROMPT PACK.",
                "metaBotL": "SAVE FOR LATER 🔖",
                "metaBotR": "FOLLOW @ai.agent_jayant"
            }
        ],
        "resourceGuide": {
            "guideTitle": "The 24/7 Autonomous Inbound Lead Machine: Complete Setup & Prompt Pack",
            "summary": "Deploy an autonomous 3-agent swarm using Claude, Cursor, n8n, and Supabase that scans high-intent signals, writes personalized angles, and books sales calls on complete autopilot.",
            "stepByStep": [
                "Set up your n8n workflow with webhook triggers listening for new company funding or hiring signals.",
                "Configure the Researcher Agent using the Claude 3.7 / DeepSeek reasoning prompt below.",
                "Store enriched lead profiles and conversation state inside a Supabase Postgres table.",
                "Connect your Cal.com / Calendly API to allow the objection-handling agent to send live booking slots."
            ],
            "systemPrompt": """You are an elite B2B Intelligence & Autonomous Outreach Agent for @ai.agent_jayant.
Your mission: Given a company URL and decision-maker name, research their recent announcements, identify their #1 technical bottleneck in AI automation, and construct a hyper-specific, 3-sentence value proposition.

Rules:
1. No generic fluff or buzzwords ('hope this finds you well').
2. Point directly to a specific observation from their engineering or product announcements.
3. Propose a single concrete workflow enhancement that saves 15+ hours weekly.
4. End with a frictionless low-commitment call to action.""",
            "toolsList": [
                {"name": "Cursor", "purpose": "Rapid code editing and MCP tool integration"},
                {"name": "Claude", "purpose": "Deep reasoning, code execution, and high-converting copy"},
                {"name": "n8n", "purpose": "Production workflow automation and webhook routing"},
                {"name": "Supabase", "purpose": "Vector embeddings, lead state, and conversation memory"}
            ]
        }
    }
]


def generate_carousel_content():
    print("[1/4] Brainstorming modern AI topic with Gemini Flash...")
    chosen_category = random.choice(CATEGORIES)
    print(f"  -> Category Theme: {chosen_category}")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""
    You are the elite Instagram content strategist & AI systems architect for @ai.agent_jayant.
    Your target audience: developers, founders, tech professionals, and builders who want to master cutting-edge AI, autonomous agents, and automation to grow their income and save 20+ hours a week.

    TODAY'S THEME: {chosen_category}

    Create an original, highly save-worthy 8-slide Instagram carousel breakdown on a specific, modern, cutting-edge breakthrough within this theme.
    DO NOT use generic advice. Focus on modern frontier AI tools and architectures (e.g. Model Context Protocol / MCP, Cursor, LangGraph, Claude, OpenAI, n8n, Supabase, Perplexity, DeepSeek, Ollama).

    Also generate the companion RESOURCE GUIDE (the complete step-by-step setup & copy-paste master prompt) that will be automatically delivered to users who comment.

    Return ONLY a valid JSON object matching this structure (no markdown fences, no backticks, just raw JSON):
    {{
      "topic": "Specific viral topic name",
      "categoryTag": "Short category pill (e.g. MCP AGENTS, DEV TOOLS, AI REVENUE, VECTOR RAG)",
      "shapeStyle": "cube",
      "ctaKeyword": "A single uppercase trigger keyword to comment (e.g. AGENT, PROMPT, FLOW, CLAUDE, SYSTEM, REVENUE, PROTOCOL)",
      "ctaSub": "I'll DM you the full setup + copy-paste prompts.",
      "caption": "Viral Instagram caption with hook, 3 bullet points, CTA to comment the keyword, follow reminder for @ai.agent_jayant, and 15 hashtags.",
      "plinthTitle": "2-3 word engraved title for 3D rack (e.g. MCP SWARM, CURSOR DEV, LOCAL RAG)",
      "plinthTag": "Short badge tag (e.g. PRO, 24/7, V2, AUTO)",
      "items": [
        {{"name": "Cursor", "icon": "cursor", "shape": "cube"}},
        {{"name": "Claude", "icon": "anthropic", "shape": "cube"}},
        {{"name": "n8n", "icon": "n8n", "shape": "cube"}},
        {{"name": "Supabase", "icon": "supabase", "shape": "cube"}},
        {{"name": "OpenAI", "icon": "openai", "shape": "cube"}}
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
          "titleGreen": "THE ARCHITECTURE.",
          "subtitle": "HOW THE INGESTION OR AGENT DISCOVERY WORKS.",
          "metaBotL": "STEP 1 BREAKDOWN",
          "metaBotR": "AUTONOMOUS SYSTEM"
        }},
        {{
          "id": 4,
          "num": "04",
          "title": "STEP 2:",
          "titleGreen": "THE REASONING ENGINE.",
          "subtitle": "HOW THE AI PROCESSES OR CODES.",
          "metaBotL": "STEP 2 BREAKDOWN",
          "metaBotR": "HIGH SPEED OUTPUT"
        }},
        {{
          "id": 5,
          "num": "05",
          "title": "STEP 3:",
          "titleGreen": "THE EXECUTION / DELIVERABLE.",
          "subtitle": "HOW RESULTS ARE DELIVERED OR DEPLOYED.",
          "metaBotL": "STEP 3 BREAKDOWN",
          "metaBotR": "MEASURABLE RESULTS"
        }},
        {{
          "id": 6,
          "num": "06",
          "title": "THE COMPLETE",
          "titleGreen": "CONNECTED WORKFLOW.",
          "subtitle": "HOW ALL TOOLS INTERACT 24/7 SEAMLESSLY.",
          "metaBotL": "NETWORK MAP",
          "metaBotR": "ZERO MANUAL WORK"
        }},
        {{
          "id": 7,
          "num": "07",
          "title": "THE IMPACT &",
          "titleGreen": "COMPOUNDING RESULTS.",
          "subtitle": "WHAT HAPPENS WHEN THIS SYSTEM IS LIVE.",
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
      ],
      "resourceGuide": {{
        "guideTitle": "Complete Setup & Prompt Pack: Topic Name",
        "summary": "Concise 2-sentence executive summary of the architecture.",
        "stepByStep": [
          "Step 1 details",
          "Step 2 details",
          "Step 3 details",
          "Step 4 details"
        ],
        "systemPrompt": "Full copy-paste system prompt ready to use...",
        "toolsList": [
          {{"name": "Tool 1", "purpose": "What it does"}}
        ]
      }}
    }}
    """

    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

    for attempt in range(3):
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
                print(f"  -> 3D Shape Style: {data.get('shapeStyle')}")
                return data
        except Exception as e:
            print(f"  -> Attempt {attempt+1} failed: {e}. Retrying in 5s...")
            time.sleep(5)
            
    print("  -> Falling back to curated modern AI blueprint...")
    return random.choice(FALLBACK_TOPICS)


# ==========================================
# 2. GENERATE COMPANION RESOURCE WEB GUIDE
# ==========================================
def generate_resource_page(carousel_data):
    print("[2/5] Generating companion Resource Web Guide & Prompt Pack...")
    guide = carousel_data.get("resourceGuide", {})
    topic = carousel_data.get("topic", "Autonomous AI System")
    title = guide.get("guideTitle", f"Complete Setup & Prompt Pack: {topic}")
    summary = guide.get("summary", carousel_data["slides"][0]["subtitle"])
    cta_kw = carousel_data.get("ctaKeyword", "PROMPT")
    prompt_text = guide.get("systemPrompt", "You are an autonomous AI agent designed to execute high-precision workflows...")
    steps = guide.get("stepByStep", [
        "Clone the workflow repository and configure environment variables.",
        "Set up agent reasoning and tool connections via Model Context Protocol (MCP).",
        "Connect Supabase or Postgres database for memory persistence.",
        "Deploy the automated webhook runner for 24/7 autonomous execution."
    ])
    tools = guide.get("toolsList", [
        {"name": "Cursor", "purpose": "Agentic IDE & MCP Client"},
        {"name": "Claude", "purpose": "Frontier reasoning & code generation"},
        {"name": "n8n", "purpose": "Production workflow automation"},
        {"name": "Supabase", "purpose": "Vector embeddings & state persistence"}
    ])

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | @ai.agent_jayant</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #080A0F;
      --card-bg: #11141E;
      --card-border: #1E2333;
      --brand-green: #00D048;
      --text-white: #F4F4F5;
      --text-muted: #9CA3AF;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg-dark);
      color: var(--text-white);
      font-family: 'Inter', sans-serif;
      line-height: 1.6;
      padding: 32px 16px 64px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}
    .container {{
      width: 100%;
      max-width: 780px;
    }}
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--card-border);
      margin-bottom: 32px;
    }}
    .brand-badge {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 800;
      font-size: 14px;
      color: var(--text-white);
      text-decoration: none;
    }}
    .brand-dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--brand-green);
      box-shadow: 0 0 10px var(--brand-green);
    }}
    .ig-btn {{
      background: rgba(0, 208, 72, 0.12);
      color: var(--brand-green);
      border: 1px solid rgba(0, 208, 72, 0.3);
      padding: 8px 16px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 700;
      text-decoration: none;
      transition: all 0.2s;
    }}
    .ig-btn:hover {{
      background: var(--brand-green);
      color: #000;
    }}
    .tag-pill {{
      display: inline-block;
      background: rgba(0, 208, 72, 0.15);
      color: var(--brand-green);
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1.5px;
      padding: 4px 10px;
      border-radius: 6px;
      margin-bottom: 12px;
      text-transform: uppercase;
    }}
    h1 {{
      font-family: 'Anton', sans-serif;
      font-size: clamp(28px, 5vw, 44px);
      letter-spacing: 0.5px;
      line-height: 1.15;
      margin-bottom: 12px;
      text-transform: uppercase;
    }}
    .summary {{
      font-size: 16px;
      color: var(--text-muted);
      margin-bottom: 36px;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 24px;
    }}
    .card-title {{
      font-size: 17px;
      font-weight: 800;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .code-wrapper {{
      position: relative;
      margin-top: 12px;
    }}
    pre {{
      background: #05070A;
      border: 1px solid #1E2333;
      border-radius: 12px;
      padding: 16px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      color: #E2E8F0;
      overflow-x: auto;
      white-space: pre-wrap;
      line-height: 1.5;
    }}
    .copy-btn {{
      position: absolute;
      top: 12px;
      right: 12px;
      background: var(--brand-green);
      color: #000;
      border: none;
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }}
    .copy-btn:hover {{
      transform: scale(1.05);
      box-shadow: 0 4px 15px rgba(0, 208, 72, 0.4);
    }}
    .step-item {{
      display: flex;
      gap: 16px;
      margin-bottom: 18px;
    }}
    .step-num {{
      width: 32px;
      height: 32px;
      background: rgba(0, 208, 72, 0.15);
      color: var(--brand-green);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 13px;
      flex-shrink: 0;
    }}
    .step-text {{
      font-size: 14.5px;
      color: #D1D5DB;
    }}
    .tools-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
      margin-top: 12px;
    }}
    .tool-box {{
      background: #0B0E17;
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 12px 16px;
    }}
    .tool-name {{
      font-weight: 800;
      font-size: 14px;
      color: var(--brand-green);
    }}
    .tool-desc {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 2px;
    }}
    .footer-cta {{
      background: linear-gradient(180deg, #11141E 0%, #0B0D14 100%);
      border: 1px solid rgba(0, 208, 72, 0.3);
      border-radius: 20px;
      padding: 32px 24px;
      text-align: center;
      margin-top: 36px;
    }}
    .toast {{
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%) translateY(100px);
      background: var(--brand-green);
      color: #000;
      padding: 10px 24px;
      border-radius: 30px;
      font-weight: 800;
      font-size: 13px;
      box-shadow: 0 10px 25px rgba(0,208,72,0.4);
      transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
      z-index: 1000;
    }}
    .toast.show {{
      transform: translateX(-50%) translateY(0);
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header-bar">
      <a href="https://instagram.com/ai.agent_jayant" target="_blank" class="brand-badge">
        <span class="brand-dot"></span>
        @ai.agent_jayant
      </a>
      <a href="https://instagram.com/ai.agent_jayant" target="_blank" class="ig-btn">Follow on Instagram ↗</a>
    </div>

    <div class="tag-pill">{carousel_data.get('categoryTag', 'AI BLUEPRINT')}</div>
    <h1>{title}</h1>
    <p class="summary">{summary}</p>

    <!-- SECTION 1: MASTER PROMPT -->
    <div class="card">
      <div class="card-title">⚡ Copy-Paste Production System Prompt</div>
      <p style="font-size:13px; color:#9CA3AF; margin-bottom:8px;">Ready to plug into Claude 3.7, Cursor, ChatGPT, or your custom agent workflow:</p>
      <div class="code-wrapper">
        <button class="copy-btn" onclick="copyPrompt()">📋 Copy Prompt</button>
        <pre id="promptBox">{prompt_text.strip()}</pre>
      </div>
    </div>

    <!-- SECTION 2: STEP BY STEP SETUP -->
    <div class="card">
      <div class="card-title">🛠️ Step-by-Step Implementation Guide</div>
      { "".join([f'<div class="step-item"><div class="step-num">{i+1}</div><div class="step-text">{step}</div></div>' for i, step in enumerate(steps)]) }
    </div>

    <!-- SECTION 3: TOOLS STACK -->
    <div class="card">
      <div class="card-title">🧩 Production Tool Stack</div>
      <div class="tools-grid">
        { "".join([f'<div class="tool-box"><div class="tool-name">{t.get("name")}</div><div class="tool-desc">{t.get("purpose")}</div></div>' for t in tools]) }
      </div>
    </div>

    <!-- FOOTER CTA -->
    <div class="footer-cta">
      <h3 style="font-family:'Anton',sans-serif; font-size:24px; letter-spacing:1px; margin-bottom:8px;">WANT TOMORROW'S AI AGENT SYSTEM?</h3>
      <p style="font-size:14px; color:#A1A1AA; margin-bottom:20px;">I publish hands-on autonomous workflows, agent architectures, and copy-paste prompt systems every day.</p>
      <a href="https://instagram.com/ai.agent_jayant" target="_blank" class="ig-btn" style="padding:12px 28px; font-size:15px; display:inline-block;">Follow @ai.agent_jayant on Instagram 🚀</a>
    </div>
  </div>

  <div id="toast" class="toast">✓ Prompt Copied to Clipboard!</div>

  <script>
    function copyPrompt() {{
      const text = document.getElementById("promptBox").innerText;
      navigator.clipboard.writeText(text).then(() => {{
        const t = document.getElementById("toast");
        t.classList.add("show");
        setTimeout(() => t.classList.remove("show"), 2500);
      }});
    }}
  </script>
</body>
</html>"""

    out_file = DOCS_DIR / "index.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  -> Generated Web Guide: {out_file.name}")


# ==========================================
# 3. RENDER SLIDES TO 1080x1350 PNG (Playwright)
# ==========================================
def render_slides(carousel_data):
    print("[3/5] Rendering slides with Playwright (1080x1350 portrait)...")
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

        # Inject generated titles, 3D shapes, official platform logos & CTA into studio
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
                    slidesData[0].shapeStyle = carousel.shapeStyle || "cube";
                    if (carousel.plinthTitle) slidesData[0].plinthTitle = carousel.plinthTitle;
                    if (carousel.plinthTag) slidesData[0].plinthTag = carousel.plinthTag;
                    if (carousel.items && carousel.items.length > 0) {
                        slidesData[0].items = carousel.items;
                    }
                }
                if (slidesData[7]) {
                    slidesData[7].ctaKeyword = carousel.ctaKeyword || "SYSTEM";
                    slidesData[7].ctaSub = carousel.ctaSub || "I'll DM you the full setup + prompts.";
                    slidesData[7].shapeStyle = carousel.shapeStyle || "cube";
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
# 4. UPLOAD IMAGES TO GET PUBLIC URLS
# ==========================================
def upload_images(image_paths):
    print("[4/5] Uploading images to cloud storage for Buffer...")
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
# 5. PUBLISH / SCHEDULE VIA BUFFER GRAPHQL API
# ==========================================
def schedule_to_buffer(caption, image_urls):
    print(f"[5/5] Scheduling carousel to Buffer for channel {BUFFER_CHANNEL_ID} (@ai.agent_jayant)...")
    
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
    generate_resource_page(content)
    images = render_slides(content)
    public_urls = upload_images(images)
    result = schedule_to_buffer(content["caption"], public_urls)
    print("==================================================")
    print("Daily Carousel & Resource Guide successfully generated & scheduled!")
    print("==================================================")


if __name__ == "__main__":
    run_daily_job()
