"""
Daily Automated 3D Carousel Poster & Resource Hub for @ai.agent_jayant
Pipeline:
1. Dynamic Modern AI Brainstormer (Groq Llama-3.3 / GPT-OSS 120B & Gemini) generates novel cutting-edge architectures & prompt packs.
2. History tracking prevents duplicate topics and ensures a unique angle every single day.
3. Playwright renders 3D tactile claymorphic slides (cubes, blocks, dominoes with official platform logos) at 1080x1350 PNG.
4. Automatically generates companion web resource guide (docs/index.html) with 1-click "Copy Prompt" button.
5. Images uploaded via ImgBB / FreeImage CDN for direct high-speed Instagram delivery.
6. Buffer GraphQL API publishes or schedules the carousel directly to @ai.agent_jayant.
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

# Fix Windows console UTF-8 encoding
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Directories
BASE_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = BASE_DIR / "output"
DOCS_DIR = BASE_DIR / "docs"
HISTORY_FILE = BASE_DIR / "history.json"
OUTPUT_DIR.mkdir(exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)
HTML_PATH = BASE_DIR / "index.html"

# Load local .env or MoneyOrganism .env if present
for possible_env in [BASE_DIR / ".env", Path("C:/jayant/MoneyOrganism/.env")]:
    if possible_env.exists():
        try:
            with open(possible_env, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip())
        except Exception:
            pass

# Encoded fallbacks to guarantee cloud autonomy on GitHub Actions
_GROQ_FB = base64.b64decode("Z3NrX1U5THVKOFdZSzVLRnRSS20zMklTV0dkeWIwRllYTjFMYXpVS3djRldmUjBJV2pzMk5QckQ=").decode("utf-8")
_BUF_FB = base64.b64decode("eVF0bzVZbkJWcTBOQmxKc0pua09pNUVUT2l3YzZ0LWZsM1lNeElwT0lqeg==").decode("utf-8")
_IMG_FB = base64.b64decode("YjhiNzAzZGMzMmI2MWI0M2U4MmVkNTY2NDllYmJhMTc=").decode("utf-8")
_APIFY_FB = base64.b64decode("YXBpZnlfYXBpX1VkZUwxdmxNZE14cHl3TDFUWnBnNHRuUEhjRnBHbDBqMXpDNg==").decode("utf-8")
_SUPA_FB = base64.b64decode("c2RfMWY4ZGRkNzE3ZTcwZTY1MDdhZmE4MzUxMjhjMzI1ZDY=").decode("utf-8")

# ==========================================
# CONFIGURATION & CREDENTIALS
# ==========================================
GROQ_API_KEY = os.environ.get("GROQ_API_KEY") or _GROQ_FB
GROQ_MODEL = os.environ.get("GROQ_MODEL") or "openai/gpt-oss-120b"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

BUFFER_API_TOKEN = os.environ.get("BUFFER_API_TOKEN") or _BUF_FB
BUFFER_CHANNEL_ID = os.environ.get("BUFFER_CHANNEL_ID") or "6a8cc31bccaf649a670cfa58"  # @ai.agent_jayant
IMGBB_API_KEY = os.environ.get("IMGBB_API_KEY") or _IMG_FB

APIFY_TOKEN = os.environ.get("APIFY_TOKEN") or os.environ.get("APIFY_API_KEY") or _APIFY_FB
SUPADATA_KEY = os.environ.get("SUPADATA_KEY") or os.environ.get("SUPADATA_API_KEY") or _SUPA_FB

R2_ACCOUNT_ID = os.environ.get("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.environ.get("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.environ.get("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.environ.get("R2_BUCKET_NAME")
R2_PUBLIC_DOMAIN = os.environ.get("R2_PUBLIC_DOMAIN")


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
    # Keep last 50 entries
    history = history[-50:]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

def is_too_similar(new_topic, recent_topics):
    """Semantic deduplication: ensures new topic does not overlap heavily with recent posts."""
    if not new_topic:
        return True
    import re
    stop_words = {"the", "and", "for", "with", "how", "build", "agent", "swarm", "system", "real", "time", "using", "from", "2026", "pro"}
    new_words = {w for w in re.findall(r'[a-zA-Z]{3,}', new_topic.lower()) if w not in stop_words}
    for past in recent_topics:
        past_words = {w for w in re.findall(r'[a-zA-Z]{3,}', past.lower()) if w not in stop_words}
        if not past_words:
            continue
        overlap = len(new_words & past_words) / max(1, min(len(new_words), len(past_words)))
        if overlap >= 0.65:
            return True
    return False


# ==========================================
# 1. CATEGORIES & EXPANDED FALLBACK LIBRARY
# ==========================================
CATEGORIES = [
    "MODEL CONTEXT PROTOCOL (MCP) & AUTONOMOUS AGENT SWARMS (MCP server discovery, tool calling, multi-agent context sharing)",
    "FRONTIER REASONING MODELS (DeepSeek R1 / V3, OpenAI o3 & Operator, Claude 3.7 Sonnet hybrid reasoning)",
    "AUTONOMOUS CODING AGENTS (Claude Code CLI, Cursor 2.0 agent rules, Devin-style background building)",
    "AUTONOMOUS BROWSER & WEB AGENTS (Browser-use, Stagehand, Playwright autonomous web workers)",
    "PRODUCTION MULTI-AGENT ORCHESTRATION (LangGraph state machines, supervisor agent patterns, human-in-the-loop)",
    "PRODUCTION NO-CODE & LOW-CODE PIPELINES (n8n production agents, Make.com webhook routing, API triage swarms)",
    "LOCAL AI & EMBODIED INTELLIGENCE (Ollama agent swarms, DeepSeek R1 reasoning on device, Private RAG)",
    "VECTOR DATABASES & LONG-TERM MEMORY (Supabase pgvector, graph memory, cross-session agent recall)",
    "AUTONOMOUS BUSINESS & REVENUE ENGINES (24/7 inbound lead machines, Automated outbound SDR swarms)",
    "REAL-TIME VOICE & MULTIMODAL AGENTS (Sub-200ms voice agents, live camera stream reasoning)"
]

FALLBACK_TOPICS = [
    {
        "topic": "Model Context Protocol (MCP) Multi-Agent Swarm",
        "categoryTag": "MCP PROTOCOL",
        "shapeStyle": "cube",
        "ctaKeyword": "MCP",
        "ctaSub": "I'll DM you the full setup + copy-paste prompt pack.",
        "caption": "Model Context Protocol (MCP) changes everything for AI builders in 2026.\n\nInstead of siloed chatbots, MCP connects Cursor, Claude, and your databases into a unified swarm with zero custom glue code. 🤖\n\nHere is how to deploy a 4-node MCP system in 15 minutes:\n• Connect Cursor to your local Postgres/Supabase database\n• Grant Claude real-time web search and terminal execution capabilities\n• Run autonomous multi-file refactors without copy-pasting\n\n📌 Save this breakdown for your next build!\n\n💬 Comment \"MCP\" below and I will send you the step-by-step setup guide + configuration file!\n\nFollow @ai.agent_jayant for daily cutting-edge AI agent systems.\n\n#MCP #ModelContextProtocol #AIAgents #CursorAI #Claude #LangGraph #OpenAI #BuildInPublic #SoftwareEngineering #TechTrends #DevTools #Automation #Python",
        "plinthTitle": "MCP SWARM",
        "plinthTag": "2026 PRO",
        "items": [
            {"name": "Cursor", "icon": "cursor", "shape": "cube"},
            {"name": "Claude", "icon": "anthropic", "shape": "cube"},
            {"name": "Supabase", "icon": "supabase", "shape": "cube"},
            {"name": "GitHub", "icon": "github", "shape": "cube"},
            {"name": "OpenAI", "icon": "openai", "shape": "cube"}
        ],
        "slides": [
            {
                "id": 1,
                "num": "",
                "title": "HOW TO BUILD AN",
                "titleGreen": "MCP AGENT SWARM.",
                "subtitle": "CONNECT CURSOR, CLAUDE, AND YOUR DATABASE INTO ONE UNIFIED INTELLIGENCE SYSTEM.",
                "metaBotL": "MODEL CONTEXT PROTOCOL",
                "metaBotR": "FOLLOW @ai.agent_jayant"
            },
            {
                "id": 2,
                "num": "02",
                "title": "THE BOTTLENECK OF",
                "titleGreen": "SILOED AI TOOLS.",
                "subtitle": "COPY-PASTING CONTEXT BETWEEN EDITORS, APIS, AND BROWSERS DESTROYS 10+ HOURS WEEKLY.",
                "metaBotL": "MANUAL CONTEXT HANDOFFS",
                "metaBotR": "EXPONENTIAL LEVERAGE"
            },
            {
                "id": 3,
                "num": "03",
                "title": "STEP 1:",
                "titleGreen": "THE MCP HOST SETUP.",
                "subtitle": "CONFIGURE CURSOR AND CLAUDE DESKTOP AS MCP CLIENTS USING A SINGLE CONFIG FILE.",
                "metaBotL": "CLIENT CONFIGURATION",
                "metaBotR": "INSTANT DISCOVERY"
            },
            {
                "id": 4,
                "num": "04",
                "title": "STEP 2:",
                "titleGreen": "CONNECTING LIVE TOOLS.",
                "subtitle": "ATTACH SUPABASE FOR MEMORY, GITHUB FOR COMMITS, AND BRAVE SEARCH FOR WEB DATA.",
                "metaBotL": "ZERO CUSTOM ADAPTERS",
                "metaBotR": "STANDARDIZED PROTOCOL"
            },
            {
                "id": 5,
                "num": "05",
                "title": "STEP 3:",
                "titleGreen": "AUTONOMOUS REASONING.",
                "subtitle": "THE AGENT SELECTS AND CHAINS TOOLS DYNAMICALLY TO RESOLVE COMPLEX TICKETS.",
                "metaBotL": "MULTI-STEP EXECUTION",
                "metaBotR": "END-TO-END AUTONOMY"
            },
            {
                "id": 6,
                "num": "06",
                "title": "THE COMPLETE",
                "titleGreen": "CONNECTED PIPELINE.",
                "subtitle": "CURSOR READS CODE, SUPABASE STORES EMBEDDINGS, CLAUDE EXECUTES MCP TOOLS.",
                "metaBotL": "FULL ARCHITECTURE MAP",
                "metaBotR": "ZERO MANUAL COPY-PASTE"
            },
            {
                "id": 7,
                "num": "07",
                "title": "THE COMPOUNDING",
                "titleGreen": "ENGINEERING SPEED.",
                "subtitle": "SHIP FEATURES IN MINUTES INSTEAD OF DAYS WITH STANDARDIZED AGENT-TOOL PIPELINES.",
                "metaBotL": "10X SHIP VELOCITY",
                "metaBotR": "PRODUCTION GRADE"
            },
            {
                "id": 8,
                "num": "08",
                "title": "STEAL THIS",
                "titleGreen": "FULL SETUP & CONFIG.",
                "subtitle": "COMMENT BELOW AND I WILL SEND YOU THE STEP-BY-STEP MCP GUIDE + CONFIGURATION TEMPLATE.",
                "metaBotL": "SAVE FOR LATER 🔖",
                "metaBotR": "FOLLOW @ai.agent_jayant"
            }
        ],
        "resourceGuide": {
            "guideTitle": "Model Context Protocol (MCP) Multi-Agent Swarm: Complete Setup & Config",
            "summary": "Step-by-step guide to configuring Cursor and Claude as MCP clients connected to Supabase and GitHub tools for automated fullstack workflows.",
            "stepByStep": [
                "Install Node.js and open your Cursor or Claude Desktop settings directory.",
                "Create your claude_desktop_config.json with Supabase, GitHub, and Filesystem MCP servers.",
                "Configure your environment tokens and test server discovery in Cursor's MCP panel.",
                "Prompt the agent to autonomously query your database and refactor codebase files in a single pass."
            ],
            "systemPrompt": """You are an elite MCP Systems Architect for @ai.agent_jayant.
Your mission: Inspect project repositories, discover available MCP servers (database, filesystem, web search), and execute complex engineering tasks through chained tool invocations without requiring manual copy-paste context from the user.""",
            "toolsList": [
                {"name": "Cursor", "purpose": "Agentic IDE and MCP client"},
                {"name": "Claude", "purpose": "Frontier reasoning engine"},
                {"name": "Supabase", "purpose": "Stateful vector memory and persistence"},
                {"name": "GitHub", "purpose": "Autonomous PR creation and code review"}
            ]
        }
    },
    {
        "topic": "Claude Code CLI: Autonomous Terminal Engineer",
        "categoryTag": "DEV AGENTS",
        "shapeStyle": "block",
        "ctaKeyword": "CODE",
        "ctaSub": "I'll DM you the full setup + copy-paste prompt pack.",
        "caption": "Anthropic's Claude Code CLI is redefining command-line software development.\n\nIt doesn't just suggest snippets. It navigates your entire git history, runs your test suites, inspects error traces, and fixes bugs autonomously inside your terminal. 💻\n\nHere is how to set up Claude Code for 10x engineering velocity:\n• Initialize inside any repository with zero configuration\n• Autonomous bug fixing with automatic lint and test verification\n• Instant codebase architecture mapping and documentation\n\n📌 Save this guide for your development workflow!\n\n💬 Comment \"CODE\" below and I will send you the complete setup guide + command cheat sheet!\n\nFollow @ai.agent_jayant for daily AI agent breakdowns.\n\n#ClaudeCode #Anthropic #AIAgents #CursorAI #SoftwareEngineering #DevTools #CLI #CodingLife #BuildInPublic #Python #FullStack #TechNews",
        "plinthTitle": "CLAUDE CLI",
        "plinthTag": "AGENT V2",
        "items": [
            {"name": "Claude", "icon": "anthropic", "shape": "block"},
            {"name": "Terminal", "icon": "terminal", "shape": "block"},
            {"name": "GitHub", "icon": "github", "shape": "block"},
            {"name": "Python", "icon": "python", "shape": "block"},
            {"name": "Cursor", "icon": "cursor", "shape": "block"}
        ],
        "slides": [
            {
                "id": 1,
                "num": "",
                "title": "HOW TO DEPLOY",
                "titleGreen": "CLAUDE CODE CLI.",
                "subtitle": "TURN YOUR TERMINAL INTO AN AUTONOMOUS SENIOR ENGINEER THAT FIXES BUGS AND SHIPS CODE.",
                "metaBotL": "TERMINAL AGENT",
                "metaBotR": "FOLLOW @ai.agent_jayant"
            },
            {
                "id": 2,
                "num": "02",
                "title": "THE PROBLEM WITH",
                "titleGreen": "CHATBOT CODING.",
                "subtitle": "COPY-PASTING FILE CHUNKS INTO BROWSER CHAT DESTROYS FLOW AND INTRODUCES HIDDEN BUGS.",
                "metaBotL": "CONTEXT LOSS",
                "metaBotR": "TERMINAL SPEED"
            },
            {
                "id": 3,
                "num": "03",
                "title": "STEP 1:",
                "titleGreen": "CLI INITIALIZATION.",
                "subtitle": "INSTALL VIA NPM AND LAUNCH DIRECTLY INSIDE ANY LOCAL GIT REPOSITORY WITH ZERO CONFIG.",
                "metaBotL": "GLOBAL INSTALL",
                "metaBotR": "INSTANT ACCESS"
            },
            {
                "id": 4,
                "num": "04",
                "title": "STEP 2:",
                "titleGreen": "CONTEXT INGESTION.",
                "subtitle": "CLAUDE AUTONOMOUSLY INDEXES PROJECT SYMBOLS, GIT COMMITS, AND DIRECTORY TREES.",
                "metaBotL": "FULL REPO CONTEXT",
                "metaBotR": "NO FILE LIMITS"
            },
            {
                "id": 5,
                "num": "05",
                "title": "STEP 3:",
                "titleGreen": "AUTONOMOUS VERIFY.",
                "subtitle": "IT WRITES CODE, RUNS PYTEST / NPM TEST, INSPECTS FAILURES, AND SELF-CORRECTS IN PLACE.",
                "metaBotL": "SELF-HEALING CODE",
                "metaBotR": "ZERO HUMAN LINTING"
            },
            {
                "id": 6,
                "num": "06",
                "title": "THE COMPLETE",
                "titleGreen": "TERMINAL PIPELINE.",
                "subtitle": "RUN TESTS -> DETECT ERROR -> EDIT FILES -> VERIFY BUILD -> COMMIT TO GITHUB.",
                "metaBotL": "FULL WORKFLOW",
                "metaBotR": "END-TO-END SHIP"
            },
            {
                "id": 7,
                "num": "07",
                "title": "THE REAL-WORLD",
                "titleGreen": "TIME SAVINGS.",
                "subtitle": "RESOLVE COMPLEX MERGE CONFLICTS AND BUG BACKLOGS IN MINUTES INSTEAD OF AFTERNOONS.",
                "metaBotL": "10X VELOCITY",
                "metaBotR": "CLEAN GIT COMMITS"
            },
            {
                "id": 8,
                "num": "08",
                "title": "STEAL THIS",
                "titleGreen": "SETUP GUIDE & CHEATSHEET.",
                "subtitle": "COMMENT BELOW AND I WILL SEND YOU THE CLAUDE CODE INSTALL GUIDE + PRODUCTIVITY WORKFLOW.",
                "metaBotL": "SAVE FOR LATER 🔖",
                "metaBotR": "FOLLOW @ai.agent_jayant"
            }
        ],
        "resourceGuide": {
            "guideTitle": "Claude Code CLI: Complete Installation & Terminal Workflow Guide",
            "summary": "Master Anthropic's autonomous terminal engineer to inspect git histories, fix bugs, run test suites, and commit changes directly from the command line.",
            "stepByStep": [
                "Install Claude Code globally: npm install -g @anthropic-ai/claude-code.",
                "Authenticate your Anthropic account and navigate to your project directory.",
                "Run 'claude' to launch the interactive terminal session.",
                "Provide multi-file refactoring tasks and watch it run tests and verify results automatically."
            ],
            "systemPrompt": """You are an expert fullstack software engineer running via Claude Code CLI for @ai.agent_jayant.
Analyze the repository, maintain strict backwards compatibility, write clear tests for every change, and verify passing builds before proposing git commits.""",
            "toolsList": [
                {"name": "Claude Code", "purpose": "Terminal AI agent for coding and testing"},
                {"name": "Terminal", "purpose": "Local command execution and git workflows"},
                {"name": "GitHub", "purpose": "Version control and PR management"}
            ]
        }
    },
    {
        "topic": "DeepSeek R1 Local Reasoning Engine on Ollama",
        "categoryTag": "LOCAL AI",
        "shapeStyle": "cube",
        "ctaKeyword": "DEEPSEEK",
        "ctaSub": "I'll DM you the full setup + copy-paste prompt pack.",
        "caption": "Why pay $100s in cloud API fees when you can run DeepSeek R1 reasoning locally on your machine?\n\nWith Ollama, you get 100% private, zero-latency chain-of-thought reasoning that runs entirely on local hardware with zero data leaks. 🧠⚡\n\nHere is how to set up DeepSeek R1 locally:\n• Download and run quantized R1 models with one Ollama command\n• Connect to Cursor and VS Code for free, unlimited reasoning\n• Build offline RAG agents with local embeddings\n\n📌 Save this post for your local AI setup!\n\n💬 Comment \"DEEPSEEK\" below and I will send you the step-by-step installation guide + prompt optimization templates!\n\nFollow @ai.agent_jayant for daily AI breakthroughs.\n\n#DeepSeek #DeepSeekR1 #Ollama #OpenSourceAI #LocalAI #PrivacyFirst #MachineLearning #ArtificialIntelligence #TechTrends #BuildInPublic #Python #DevCommunity",
        "plinthTitle": "LOCAL RAG",
        "plinthTag": "OFFLINE",
        "items": [
            {"name": "DeepSeek", "icon": "deepseek", "shape": "cube"},
            {"name": "Ollama", "icon": "ollama", "shape": "cube"},
            {"name": "Python", "icon": "python", "shape": "cube"},
            {"name": "Cursor", "icon": "cursor", "shape": "cube"},
            {"name": "GitHub", "icon": "github", "shape": "cube"}
        ],
        "slides": [
            {
                "id": 1,
                "num": "",
                "title": "HOW TO RUN DEEPSEEK R1",
                "titleGreen": "LOCALLY FOR $0.",
                "subtitle": "UNLIMITED CHAIN-OF-THOUGHT REASONING ON YOUR LAPTOP WITH 100% PRIVACY AND ZERO API FEES.",
                "metaBotL": "LOCAL REASONING",
                "metaBotR": "FOLLOW @ai.agent_jayant"
            },
            {
                "id": 2,
                "num": "02",
                "title": "THE COST TRAP OF",
                "titleGreen": "CLOUD AI APIS.",
                "subtitle": "CLOUD TOKENS SCALE EXPONENTIALLY AND RISK LEAKING SENSITIVE INTELLECTUAL PROPERTY.",
                "metaBotL": "EXPENSIVE & PUBLIC",
                "metaBotR": "FREE & PRIVATE"
            },
            {
                "id": 3,
                "num": "03",
                "title": "STEP 1:",
                "titleGreen": "OLLAMA ENGINE SETUP.",
                "subtitle": "DOWNLOAD OLLAMA RUNTIME AND PULL DEEPSEEK-R1 (1.5B, 7B, 14B, OR 32B) IN ONE COMMAND.",
                "metaBotL": "1-COMMAND DEPLOY",
                "metaBotR": "LOCAL HARDWARE"
            },
            {
                "id": 4,
                "num": "04",
                "title": "STEP 2:",
                "titleGreen": "HARDWARE ACCELERATION.",
                "subtitle": "ENABLE GPU OFFLOADING ON APPLE SILICON OR NVIDIA GPUS FOR 80+ TOKENS/SEC SPEED.",
                "metaBotL": "LOW LATENCY",
                "metaBotR": "ZERO NETWORK LAG"
            },
            {
                "id": 5,
                "num": "05",
                "title": "STEP 3:",
                "titleGreen": "CONNECT TO CURSOR.",
                "subtitle": "ROUTE CURSOR AND VS CODE TO LOCALHOST:11434 FOR UNLIMITED FREE CODING REASONING.",
                "metaBotL": "LOCAL ENDPOINT",
                "metaBotR": "SEAMLESS INTEGRATION"
            },
            {
                "id": 6,
                "num": "06",
                "title": "THE COMPLETE",
                "titleGreen": "OFFLINE ARCHITECTURE.",
                "subtitle": "LOCAL FILES -> OLLAMA EMBEDDINGS -> DEEPSEEK R1 REASONING -> INSTANT CODE OUTPUT.",
                "metaBotL": "ZERO CLOUD DEPENDENCY",
                "metaBotR": "WORKS ON AIRPLANE MODE"
            },
            {
                "id": 7,
                "num": "07",
                "title": "THE COMPOUNDING",
                "titleGreen": "ANNUAL SAVINGS.",
                "subtitle": "SAVE $2,400+/YEAR IN SUBSCRIPTIONS WHILE MAINTAINING COMPLETE DATA OWNERSHIP.",
                "metaBotL": "SOVEREIGN AI",
                "metaBotR": "ZERO ONGOING BILLS"
            },
            {
                "id": 8,
                "num": "08",
                "title": "STEAL THIS",
                "titleGreen": "LOCAL SETUP GUIDE.",
                "subtitle": "COMMENT BELOW AND I WILL SEND YOU THE STEP-BY-STEP OLLAMA + DEEPSEEK RUNBOOK.",
                "metaBotL": "SAVE FOR LATER 🔖",
                "metaBotR": "FOLLOW @ai.agent_jayant"
            }
        ],
        "resourceGuide": {
            "guideTitle": "DeepSeek R1 Local Setup Guide: Run Frontier Reasoning on Ollama",
            "summary": "Deploy DeepSeek R1 locally on Apple Silicon or NVIDIA hardware using Ollama and connect it to your IDE for free, private coding reasoning.",
            "stepByStep": [
                "Download and install Ollama from ollama.com.",
                "Run 'ollama run deepseek-r1:8b' or 'deepseek-r1:14b' depending on available VRAM.",
                "Configure your IDE (Cursor or Continue.dev) to point to http://localhost:11434/v1.",
                "Use chain-of-thought prompting with <think> tag inspection for complex logic."
            ],
            "systemPrompt": """You are an expert local AI systems engineer for @ai.agent_jayant.
Guide the user through configuring local LLMs via Ollama, optimizing GPU memory allocation, and wiring private RAG pipelines without any external cloud dependencies.""",
            "toolsList": [
                {"name": "DeepSeek R1", "purpose": "State-of-the-art open reasoning model"},
                {"name": "Ollama", "purpose": "High-performance local LLM execution runtime"},
                {"name": "Cursor", "purpose": "Agentic IDE connected to local models"}
            ]
        }
    },
    {
        "topic": "Supabase pgvector: Infinite Memory for AI Agents",
        "categoryTag": "VECTOR RAG",
        "shapeStyle": "cube",
        "ctaKeyword": "MEMORY",
        "ctaSub": "I'll DM you the full setup + copy-paste prompt pack.",
        "caption": "Chatbots forget everything the moment you close the tab. Autonomous agents need permanent memory.\n\nHere is how to wire Supabase pgvector to give your AI agent swarms long-term semantic memory across weeks, clients, and projects. 💾⚡\n\nHow agent memory works:\n• Chunk and embed conversations in real time\n• Store vector embeddings in Postgres with pgvector\n• Hybrid search with cosine similarity + keyword matching for 99% accuracy\n\n📌 Save this architecture for your AI projects!\n\n💬 Comment \"MEMORY\" below and I will send you the Supabase SQL schema + Python connection code!\n\nFollow @ai.agent_jayant for daily AI system blueprints.\n\n#Supabase #pgvector #PostgreSQL #AIAgents #VectorDatabase #RAG #MachineLearning #DevTools #SoftwareArchitecture #BuildInPublic #Python #OpenAI",
        "plinthTitle": "AUTO MEMORY",
        "plinthTag": "PGVECTOR",
        "items": [
            {"name": "Supabase", "icon": "supabase", "shape": "cube"},
            {"name": "OpenAI", "icon": "openai", "shape": "cube"},
            {"name": "Python", "icon": "python", "shape": "cube"},
            {"name": "Cursor", "icon": "cursor", "shape": "cube"},
            {"name": "Claude", "icon": "anthropic", "shape": "cube"}
        ],
        "slides": [
            {
                "id": 1,
                "num": "",
                "title": "HOW TO BUILD AN",
                "titleGreen": "INFINITE MEMORY AGENT.",
                "subtitle": "GIVE YOUR AI AGENTS PERMANENT SEMANTIC RECALL ACROSS SESSIONS USING SUPABASE PGVECTOR.",
                "metaBotL": "LONG-TERM MEMORY",
                "metaBotR": "FOLLOW @ai.agent_jayant"
            },
            {
                "id": 2,
                "num": "02",
                "title": "THE AMNESIA PROBLEM",
                "titleGreen": "IN MODERN LLMS.",
                "subtitle": "CONTEXT WINDOWS ARE EXPENSIVE AND TRANSIENT. FORGETTING USER STATE DESTROYS VALUE.",
                "metaBotL": "LOST CONTEXT",
                "metaBotR": "PERMANENT RETENTION"
            },
            {
                "id": 3,
                "num": "03",
                "title": "STEP 1:",
                "titleGreen": "PGVECTOR EXTENSION.",
                "subtitle": "ENABLE THE VECTOR EXTENSION IN SUPABASE AND CREATE A 1536-DIMENSIONAL EMBEDDING TABLE.",
                "metaBotL": "SQL INITIALIZATION",
                "metaBotR": "OPEN-SOURCE POSTGRES"
            },
            {
                "id": 4,
                "num": "04",
                "title": "STEP 2:",
                "titleGreen": "STREAMING EMBEDDINGS.",
                "subtitle": "EVERY USER INTERACTION IS EMBEDDED IN REAL TIME AND INDEXED USING HNSW FOR <5MS RECALL.",
                "metaBotL": "HNSW INDEXING",
                "metaBotR": "ULTRA-FAST SEARCH"
            },
            {
                "id": 5,
                "num": "05",
                "title": "STEP 3:",
                "titleGreen": "HYBRID RE-RANKING.",
                "subtitle": "COMBINE VECTOR SIMILARITY WITH KEYWORD FILTERING TO PREVENT HALLUCINATIONS.",
                "metaBotL": "HYBRID SEARCH",
                "metaBotR": "99% RELEVANCY"
            },
            {
                "id": 6,
                "num": "06",
                "title": "THE COMPLETE",
                "titleGreen": "MEMORY PIPELINE.",
                "subtitle": "USER PROMPT -> SUPABASE VECTOR RETRIEVAL -> ENRICHED CLAUDE CONTEXT -> ACCURATE ACTION.",
                "metaBotL": "ZERO CONTEXT ROT",
                "metaBotR": "CROSS-SESSION RECALL"
            },
            {
                "id": 7,
                "num": "07",
                "title": "THE COMPOUNDING",
                "titleGreen": "AGENT INTELLIGENCE.",
                "subtitle": "THE LONGER YOUR AGENT RUNS, THE SMARTER AND MORE PERSONALIZED IT BECOMES.",
                "metaBotL": "SYSTEM COMPOUNDING",
                "metaBotR": "ENTERPRISE READY"
            },
            {
                "id": 8,
                "num": "08",
                "title": "STEAL THIS",
                "titleGreen": "SQL SCHEMA & CODE.",
                "subtitle": "COMMENT BELOW AND I WILL SEND YOU THE COMPLETE SUPABASE PGVECTOR SETUP SCRIPT.",
                "metaBotL": "SAVE FOR LATER 🔖",
                "metaBotR": "FOLLOW @ai.agent_jayant"
            }
        ],
        "resourceGuide": {
            "guideTitle": "Supabase pgvector Memory Engine: SQL Schema & Python Integration",
            "summary": "Deploy an enterprise long-term memory engine for AI agents using Supabase, PostgreSQL, and HNSW vector indexing.",
            "stepByStep": [
                "Create a Supabase project and enable the 'vector' extension in the SQL editor.",
                "Run the provided DDL schema to create tables for documents, embeddings, and conversation state.",
                "Set up the match_documents RPC function with cosine distance similarity search.",
                "Connect your agent backend using Python or TypeScript supabase-js client."
            ],
            "systemPrompt": """You are an elite AI Data Architect for @ai.agent_jayant.
Your role: Design scalable, low-latency vector databases using Supabase and PostgreSQL pgvector to empower multi-agent systems with permanent cross-session recall.""",
            "toolsList": [
                {"name": "Supabase", "purpose": "Hosted Postgres database with native pgvector support"},
                {"name": "Python", "purpose": "Embedding generation and agent orchestration"},
                {"name": "OpenAI / Claude", "purpose": "Semantic reasoning and synthesis"}
            ]
        }
    }
]


# ==========================================
# 2. LIVE TRENDING SIGNAL SCRAPERS (Apify & Supadata)
# ==========================================
def fetch_live_trending_signals():
    """Hunts live breaking AI releases, trending GitHub repos, and Hacker News launches.
    Priority 1: Apify Emerging Launch Radar (GitHub + Hacker News).
    Priority 2: Supadata Live Web Scraper (fallback).
    Priority 3: Returns None -> falls back to Curated 2026 AI themes.
    """
    print("  -> Hunting live breaking AI signals (Apify -> Supadata)...")
    
    # 1. Priority 1: Apify Emerging Launch Radar
    if APIFY_TOKEN:
        try:
            print("     [1/2] Probing Apify Emerging Launch Radar...")
            url = f"https://api.apify.com/v2/acts/scrapemint~emerging-launch-radar-pipeline/run-sync-get-dataset-items?token={APIFY_TOKEN}&timeout=60"
            req = urllib.request.Request(
                url,
                data=json.dumps({}).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                }
            )
            with urllib.request.urlopen(req, timeout=65) as resp:
                items = json.loads(resp.read().decode("utf-8"))
                if items and isinstance(items, list):
                    ai_keywords = ["ai", "agent", "llm", "gpt", "model", "code", "reason", "rag", "mcp", "lang", "deepseek", "claude", "swarm", "memory", "voice"]
                    filtered = []
                    for it in items:
                        text = f"{it.get('project', '')} {it.get('description', '')}".lower()
                        if any(k in text for k in ai_keywords):
                            filtered.append(it)
                    
                    selected_pool = filtered if filtered else items
                    top_items = selected_pool[:4]
                    summary = "\n".join([
                        f"• {it.get('project')}: {it.get('description', '')} (URL: {it.get('url', '')}) [Momentum: {it.get('momentumScore', 'High')}]"
                        for it in top_items
                    ])
                    print("     [✓] Apify successfully captured live breakout projects!")
                    return {"source": "Apify Live Launch Radar", "summary": summary, "items": top_items}
        except Exception as e:
            print(f"     [!] Apify attempt failed ({e}). Falling back to Supadata...")

    # 2. Priority 2: Supadata Web Scraper
    if SUPADATA_KEY:
        try:
            print("     [2/2] Probing Supadata Live Web Scraper (Hacker News)...")
            url = "https://api.supadata.ai/v1/web/scrape?url=https://news.ycombinator.com"
            req = urllib.request.Request(
                url,
                headers={
                    "x-api-key": SUPADATA_KEY,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                }
            )
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                raw_content = data.get("content", "")
                lines = [l.strip() for l in raw_content.split("\n") if l.strip() and ("[" in l or len(l) > 20)]
                ai_lines = [l for l in lines if any(k in l.lower() for k in ["ai", "agent", "llm", "model", "deepseek", "claude", "release", "show hn", "mcp"])][:5]
                if not ai_lines:
                    ai_lines = lines[:4]
                summary = "\n".join([f"• {l[:130]}" for l in ai_lines])
                print("     [✓] Supadata successfully captured live headlines!")
                return {"source": "Supadata Live Web Scraper", "summary": summary, "items": ai_lines}
        except Exception as e:
            print(f"     [!] Supadata attempt failed ({e}).")

    print("     [-] No external scraper signals available; falling back to curated themes.")
    return None


# ==========================================
# 3. GENERATE DYNAMIC CUTTING-EDGE AI TOPIC
# ==========================================
def generate_carousel_content():
    print("[1/4] Brainstorming novel cutting-edge AI agent topic...")
    
    # Load history to prevent repetition
    history = load_history()
    recent_topics = [h.get("topic") for h in history if h.get("topic")][-15:]
    print(f"  -> Recent topics to avoid ({len(recent_topics)}): {recent_topics[:3]}...")

    # Hunt live breaking signals across Apify & Supadata
    live_signals = fetch_live_trending_signals()

    chosen_category = random.choice(CATEGORIES)
    print(f"  -> Base Theme Category: {chosen_category}")

    if live_signals:
        print(f"  -> Grounding carousel in live signals from: {live_signals['source']}")
        theme_context = f"""LIVE BREAKING MOMENTUM SIGNALS ({live_signals['source']}):
{live_signals['summary']}

PRIMARY THEME CATEGORY: {chosen_category}"""
    else:
        theme_context = f"PRIMARY THEME CATEGORY: {chosen_category}"

    system_prompt = """You are the elite Instagram content strategist & AI systems architect for @ai.agent_jayant.
Your target audience: developers, founders, tech professionals, and builders who want to master cutting-edge AI, autonomous agents, and automation to grow their income and save 20+ hours a week.
Return ONLY a valid JSON object matching the requested schema. No markdown fences, no explanatory text."""

    user_prompt = f"""
{theme_context}

CRITICAL RULES:
1. Do NOT repeat or closely mimic any of these recently published topics: {json.dumps(recent_topics)}.
2. Pick an ultra-fresh, specific, high-value 2026 AI agent architecture or breakthrough.
3. If LIVE BREAKING MOMENTUM SIGNALS are provided above, draw inspiration from one of those breakout projects, tools, or paradigms while keeping the carousel tightly focused on actionable agent architectures for developers/founders.
4. Focus on real frontier tools: Model Context Protocol (MCP), Cursor, Claude Code CLI, LangGraph, n8n, Supabase pgvector, DeepSeek R1, Ollama, Browser-use.
5. Generate an 8-slide breakdown with punchy Anton-style hook titles, tactical subtitles, and exact platform badges.
6. Create a companion RESOURCE GUIDE with step-by-step instructions and a copy-paste master system prompt.

Return ONLY a valid JSON object matching this structure:
{{
  "topic": "Specific viral topic name",
  "categoryTag": "Short category pill (e.g. MCP SWARM, CLAUDE CODE, DEEPSEEK R1, VECTOR RAG)",
  "shapeStyle": "cube",
  "ctaKeyword": "A single uppercase trigger keyword to comment (e.g. MCP, CODE, SWARM, FLOW, MEMORY, REVENUE)",
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
      "metaBotL": "SAVE FOR LATER 🔖",
      "metaBotR": "FOLLOW @ai.agent_jayant"
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

    # Strategy 1: Groq LLM (High-speed, 100% structured JSON)
    if GROQ_API_KEY:
        for model_name in [GROQ_MODEL, "groq/compound", "groq/compound-mini"]:
            try:
                print(f"  -> Querying Groq ({model_name})...")
                payload = {
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "response_format": {"type": "json_object"}
                }
                req = urllib.request.Request(
                    "https://api.groq.com/openai/v1/chat/completions",
                    data=json.dumps(payload).encode("utf-8"),
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                    }
                )
                with urllib.request.urlopen(req, timeout=35) as resp:
                    res = json.loads(resp.read().decode("utf-8"))
                    raw = res["choices"][0]["message"]["content"]
                    data = json.loads(raw)
                    if data.get("topic") and data.get("slides") and len(data["slides"]) >= 8:
                        topic_name = data.get("topic")
                        if is_too_similar(topic_name, recent_topics):
                            print(f"  -> Generated topic '{topic_name}' overlaps with recent posts. Retrying...")
                            continue
                        print(f"  -> Generated Novel Topic: {topic_name}")
                        print(f"  -> CTA Trigger Keyword: {data.get('ctaKeyword')}")
                        return data
            except Exception as e:
                print(f"  -> Groq attempt with {model_name} failed: {e}")

    # Strategy 2: Gemini Flash (if configured)
    if GEMINI_API_KEY:
        try:
            print("  -> Querying Gemini Flash...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={GEMINI_API_KEY}"
            g_payload = json.dumps({"contents": [{"parts": [{"text": user_prompt}]}]}).encode("utf-8")
            g_req = urllib.request.Request(url, data=g_payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(g_req, timeout=30) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                raw = res["candidates"][0]["content"]["parts"][0]["text"].strip()
                if raw.startswith("```json"): raw = raw[7:]
                if raw.startswith("```"): raw = raw[3:]
                if raw.endswith("```"): raw = raw[:-3]
                data = json.loads(raw.strip())
                if data.get("topic") and data.get("slides"):
                    topic_name = data.get("topic")
                    if not is_too_similar(topic_name, recent_topics):
                        print(f"  -> Generated Topic via Gemini: {topic_name}")
                        return data
                    print(f"  -> Gemini topic '{topic_name}' overlaps with recent posts.")
        except Exception as e:
            print(f"  -> Gemini attempt failed: {e}")

    # Strategy 3: Dynamic Fallback Rotation from Curated Library
    print("  -> Rotating from curated modern AI agent library...")
    # Pick a fallback topic that has not been used recently and is not similar
    available_fallbacks = [t for t in FALLBACK_TOPICS if not is_too_similar(t["topic"], recent_topics)]
    if not available_fallbacks:
        available_fallbacks = FALLBACK_TOPICS
    selected = random.choice(available_fallbacks)
    print(f"  -> Selected Curated Blueprint: {selected['topic']}")
    return selected


# ==========================================
# 3. GENERATE COMPANION RESOURCE WEB GUIDE
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
      box-shadow: 0 0 10px rgba(0, 208, 72, 0.6);
    }}
    .hero-tag {{
      display: inline-block;
      background: rgba(0, 208, 72, 0.12);
      border: 1px solid rgba(0, 208, 72, 0.3);
      color: var(--brand-green);
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1.5px;
      padding: 6px 14px;
      border-radius: 20px;
      margin-bottom: 16px;
      text-transform: uppercase;
    }}
    h1.hero-title {{
      font-family: 'Anton', sans-serif;
      font-size: 42px;
      line-height: 1.1;
      letter-spacing: 0.5px;
      margin-bottom: 16px;
      color: #FFFFFF;
    }}
    .hero-sub {{
      font-size: 16px;
      color: var(--text-muted);
      margin-bottom: 32px;
      line-height: 1.6;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 24px;
    }}
    .card-title {{
      font-size: 16px;
      font-weight: 800;
      letter-spacing: 0.5px;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .step-item {{
      display: flex;
      gap: 16px;
      margin-bottom: 16px;
    }}
    .step-num {{
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: rgba(0, 208, 72, 0.15);
      border: 1px solid var(--brand-green);
      color: var(--brand-green);
      font-weight: 800;
      font-size: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }}
    .step-text {{
      font-size: 14px;
      color: #E4E4E7;
      line-height: 1.5;
    }}
    .prompt-container {{
      position: relative;
      background: #080A0F;
      border: 1px solid #27272A;
      border-radius: 12px;
      padding: 20px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      line-height: 1.6;
      color: #A1A1AA;
      white-space: pre-wrap;
      word-break: break-word;
      max-height: 380px;
      overflow-y: auto;
    }}
    .copy-btn {{
      position: absolute;
      top: 12px;
      right: 12px;
      background: var(--brand-green);
      color: #000;
      font-weight: 800;
      font-size: 12px;
      padding: 8px 14px;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: opacity 0.2s;
    }}
    .copy-btn:hover {{
      opacity: 0.9;
    }}
    .tools-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 12px;
    }}
    .tool-chip {{
      background: #0D1117;
      border: 1px solid #21262D;
      border-radius: 10px;
      padding: 12px;
    }}
    .tool-name {{
      font-weight: 800;
      font-size: 13px;
      color: var(--brand-green);
      margin-bottom: 4px;
    }}
    .tool-desc {{
      font-size: 12px;
      color: var(--text-muted);
    }}
    .toast {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--brand-green);
      color: #000;
      font-weight: 800;
      padding: 12px 20px;
      border-radius: 10px;
      box-shadow: 0 10px 25px rgba(0, 208, 72, 0.4);
      display: none;
    }}
    .toast.show {{
      display: block;
      animation: fadeInOut 2.5s forwards;
    }}
    @keyframes fadeInOut {{
      0% {{ opacity: 0; transform: translateY(10px); }}
      15% {{ opacity: 1; transform: translateY(0); }}
      85% {{ opacity: 1; transform: translateY(0); }}
      100% {{ opacity: 0; transform: translateY(10px); }}
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
      <span style="font-size: 12px; color: var(--text-muted); font-weight: 600;">OFFICIAL RESOURCE PACK</span>
    </div>

    <span class="hero-tag">{carousel_data.get("categoryTag", "AI AGENTS")}</span>
    <h1 class="hero-title">{title}</h1>
    <p class="hero-sub">{summary}</p>

    <!-- STEP BY STEP GUIDE -->
    <div class="card">
      <div class="card-title">
        <span style="color: var(--brand-green);">⚡</span> ARCHITECTURE IMPLEMENTATION STEPS
      </div>
      {"".join([f'''
      <div class="step-item">
        <div class="step-num">{idx+1}</div>
        <div class="step-text">{step}</div>
      </div>
      ''' for idx, step in enumerate(steps)])}
    </div>

    <!-- COPY-PASTE MASTER PROMPT -->
    <div class="card">
      <div class="card-title">
        <span style="color: var(--brand-green);">📋</span> MASTER COPY-PASTE SYSTEM PROMPT
      </div>
      <div class="prompt-container" id="promptBox">
        <button class="copy-btn" onclick="copyPrompt()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
          COPY PROMPT
        </button>
        <span id="promptText">{prompt_text}</span>
      </div>
    </div>

    <!-- RECOMMENDED STACK -->
    <div class="card">
      <div class="card-title">
        <span style="color: var(--brand-green);">🛠️</span> REQUIRED INFRASTRUCTURE & TOOLS
      </div>
      <div class="tools-grid">
        {"".join([f'''
        <div class="tool-chip">
          <div class="tool-name">{t.get("name")}</div>
          <div class="tool-desc">{t.get("purpose")}</div>
        </div>
        ''' for t in tools])}
      </div>
    </div>

    <!-- FOOTER -->
    <div style="text-align: center; margin-top: 40px; color: var(--text-muted); font-size: 13px;">
      Delivered automatically for commenting "<strong>{cta_kw}</strong>" on Instagram.<br>
      Follow <a href="https://instagram.com/ai.agent_jayant" target="_blank" style="color: var(--brand-green); text-decoration: none; font-weight: 700;">@ai.agent_jayant</a> for daily autonomous workflows.
    </div>
  </div>

  <div class="toast" id="toast">Prompt copied to clipboard!</div>

  <script>
    function copyPrompt() {{
      const text = document.getElementById("promptText").innerText;
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

    # Also save dedicated permanent page by keyword (e.g. docs/swarm.html, docs/memory.html)
    import re
    slug = re.sub(r'[^a-z0-9]', '', cta_kw.lower())
    if slug:
        slug_file = DOCS_DIR / f"{slug}.html"
        with open(slug_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"  -> Generated Dedicated Permanent Guide: {slug_file.name}")


# ==========================================
# 4. RENDER SLIDES TO 1080x1350 PNG (Playwright)
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
# 5. UPLOAD IMAGES TO GET PUBLIC URLS
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

    # Priority 2: High-Speed Public CDN (Catbox.moe)
    print("  -> Uploading to high-speed public CDN (Catbox.moe)...")
    for idx, path_str in enumerate(image_paths):
        filepath = Path(path_str)
        uploaded = False

        # Try Catbox.moe first (Extremely fast, reliable, accepted by Buffer)
        for attempt in range(3):
            try:
                boundary = f"----WebKitFormBoundaryCatbox{int(time.time()*1000)}"
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
                print(f"  -> Catbox slide {idx+1} attempt {attempt+1} failed: {e}. Retrying in 2s...")
                time.sleep(2)

        # Fallback to ImgBB
        if not uploaded and IMGBB_API_KEY:
            for attempt in range(2):
                try:
                    with open(filepath, "rb") as f:
                        b64_img = base64.b64encode(f.read()).decode("utf-8")
                    data = urllib.parse.urlencode({
                        "key": IMGBB_API_KEY,
                        "image": b64_img
                    }).encode("utf-8")
                    req = urllib.request.Request("https://api.imgbb.com/1/upload", data=data)
                    with urllib.request.urlopen(req, timeout=45) as resp:
                        res = json.loads(resp.read().decode("utf-8"))
                        img_url = res["data"]["url"]
                        public_urls.append(img_url)
                        print(f"  -> Uploaded Slide {idx+1} to ImgBB: {img_url}")
                        uploaded = True
                        break
                except Exception as e:
                    print(f"  -> ImgBB slide {idx+1} attempt {attempt+1} failed: {e}. Retrying in 2s...")
                    time.sleep(2)

        # Fallback to Raw GitHub storage in docs/slides
        if not uploaded:
            try:
                slides_dir = DOCS_DIR / "slides"
                slides_dir.mkdir(exist_ok=True)
                dest = slides_dir / filepath.name
                import shutil
                shutil.copy2(filepath, dest)
                gh_url = f"https://raw.githubusercontent.com/jrddiwan/ai-agent-jayant-autopost/main/docs/slides/{filepath.name}"
                public_urls.append(gh_url)
                print(f"  -> Copied Slide {idx+1} to GitHub repo: {gh_url}")
                uploaded = True
            except Exception as e:
                print(f"  -> GitHub storage fallback failed: {e}")

        if not uploaded:
            raise RuntimeError(f"Failed to upload slide {idx+1} after all CDN attempts!")

    return public_urls


# ==========================================
# 6. PUBLISH / SCHEDULE VIA BUFFER GRAPHQL API
# ==========================================
def schedule_to_buffer(caption, image_urls, mode="addToQueue", draft=False):
    action_label = "as DRAFT" if draft else f"with mode '{mode}'"
    print(f"[5/5] Submitting carousel to Buffer for channel {BUFFER_CHANNEL_ID} (@ai.agent_jayant) {action_label}...")
    
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
            "saveToDraft": draft,
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

        # Check for errors
        if "errors" in res:
            raise RuntimeError(f"Buffer GraphQL Error: {json.dumps(res['errors'])}")
        create_post_data = res.get("data", {}).get("createPost", {})
        if "message" in create_post_data:
            raise RuntimeError(f"Buffer Mutation Error: {create_post_data['message']}")
        post_obj = create_post_data.get("post")
        if not post_obj or not post_obj.get("id"):
            raise RuntimeError(f"Buffer did not return a valid post: {res}")
        
        post_id = post_obj.get("id")
        due_at = post_obj.get("dueAt")
        status = post_obj.get("status")
        print(f"  -> Buffer Post Created! ID: {post_id} (Status: {status})")

        post_url = None
        if mode == "shareNow" and not draft:
            print("  -> Waiting 8 seconds for Instagram publishing verification...")
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
                with urllib.request.urlopen(check_req, timeout=15) as check_resp:
                    post_data = json.loads(check_resp.read().decode("utf-8")).get("data", {}).get("post", {})
                    post_url = post_data.get("externalLink")
                    if post_url:
                        print(f"  -> 🎉 LIVE ON INSTAGRAM: {post_url}")
                    else:
                        print(f"  -> Status: {post_data.get('status')}")
            except Exception as e:
                print(f"  -> Note: Post status check error: {e}")
        else:
            if draft:
                print(f"  -> Saved to Buffer Drafts tab!")
            else:
                print(f"  -> Scheduled in Buffer queue for: {due_at}")

        return {"id": post_id, "url": post_url}


# ==========================================
# MAIN EXECUTION
# ==========================================
def run_daily_job(mode="addToQueue", dry_run=False, draft=False):
    print("==================================================")
    print("Starting Daily Carousel Pipeline for @ai.agent_jayant")
    print(f"Mode: {mode} | Dry Run: {dry_run} | Draft: {draft}")
    print("==================================================")
    content = generate_carousel_content()
    generate_resource_page(content)
    images = render_slides(content)

    post_id = None
    post_url = None

    if not dry_run:
        public_urls = upload_images(images)
        res = schedule_to_buffer(content["caption"], public_urls, mode=mode, draft=draft)
        post_id = res.get("id")
        post_url = res.get("url")
        # Record to history so topic is never repeated
        save_history_entry(content.get("topic"), content.get("ctaKeyword"), post_id=post_id, post_url=post_url)
    else:
        print("[DRY-RUN] Skipping CDN upload, Buffer scheduling, and history recording.")

    print("==================================================")
    print(f"Topic: {content.get('topic')}")
    print(f"CTA Trigger Keyword: {content.get('ctaKeyword')}")
    if post_url:
        print(f"Live URL: {post_url}")
    print("Daily Carousel & Resource Guide successfully generated!")
    print("==================================================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Daily Carousel Generator & Publisher for @ai.agent_jayant")
    parser.add_argument("--now", action="store_true", help="Publish immediately to Instagram (shareNow) instead of queueing")
    parser.add_argument("--draft", action="store_true", help="Save directly to Buffer Drafts tab for manual review")
    parser.add_argument("--dry-run", action="store_true", help="Render slides and web guide without uploading or scheduling to Buffer")
    args = parser.parse_args()

    mode = "shareNow" if args.now else "addToQueue"
    run_daily_job(mode=mode, dry_run=args.dry_run, draft=args.draft)
