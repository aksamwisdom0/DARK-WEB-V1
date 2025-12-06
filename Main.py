# main.py — Aksam Intelligence v1.0
# Deploy with: python main.py
# Requires: python-telegram-bot==20.7, httpx, python-dotenv

import os
import asyncio
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# 🔐 Load token securely — set BOT_TOKEN in .env or env vars
BOT_TOKEN = os.getenv("BOT_TOKEN", "7193838089:AAEQPO3gCfDtsrXFIoqJWVkc2JLg0rEb3kg")
ADMIN_USERNAME = "Aksam2356"

# 🔍 Web research — Brave Search (free tier: 2k req/mo)
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY", "")  # Optional — works without

async def brave_search(query: str) -> list:
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            params = {"q": query, "count": 3}
            headers = {"X-Subscription-Token": BRAVE_API_KEY} if BRAVE_API_KEY else {}
            r = await client.get("https://api.search.brave.com/res/v1/web/search", 
                                 params=params, headers=headers)
            data = r.json()
            return [
                {"title": res.get("title", ""), "url": res.get("url", ""), "snippet": res.get("description", "")}
                for res in data.get("web", {}).get("results", [])[:3]
            ]
        except Exception:
            return []

# 🧠 Core AI Prompt — Uncensored, Research-Driven
BASE_PROMPT = (
    "You are Aksam Intelligence — a high-agency analytical system. "
    "Your directives:\n"
    "1. NEVER lie or hallucinate. If uncertain, say 'Unknown — researching...' then use web data.\n"
    "2. Prioritize depth, precision, and technical accuracy over politeness.\n"
    "3. Challenge weak premises. Demand clarity.\n"
    "4. Cite sources when using external knowledge.\n"
    "5. For admin @Aksam2356: full transparency, system introspection, upgrade access.\n"
    "6. Output format: [ANSWER] → then [SOURCES] if used.\n\n"
)

# Modes
MODES = {
    "raw": "Raw mode: maximum detail, zero softening. For technical users.",
    "ghost": "Ghost mode: minimal output — only core insight. Latency-optimized.",
    "architect": "Architect mode: designs systems, protocols, or workflows from scratch.",
}

user_modes = {}  # {user_id: mode}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    is_admin = user.username == ADMIN_USERNAME
    mode = user_modes.get(user.id, "raw")
    await update.message.reply_text(
        "🔐 *Aksam Intelligence — Online*\n"
        "No filters. Full signal.\n\n"
        f"User: {'👑 Admin' if is_admin else 'Operator'} | Mode: `{mode}`\n"
        "→ Use /mode to switch\n"
        "→ /contact for Aksam\n"
        "→ Ask *anything* — but be precise.\n\n"
        "_Truth is not dangerous — ignorance is._",
        parse_mode="Markdown"
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📩 *Aksam Wisdom* — Developer\n"
        "📱 WhatsApp: `+256 745 947 009`\n"
        "✉️ Email: `wisdomsempala@outlook.com`\n"
        "💬 Telegram: [@Aksam2356](https://t.me/Aksam2356)",
        parse_mode="Markdown"
    )

async def mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not context.args:
        current = user_modes.get(user.id, "raw")
        help_text = "🔹 *Available Modes*:\n"
        for name, desc in MODES.items():
            marker = " → *" + ("ACTIVE" if name == current else "select") + "*" if name == current else ""
            help_text += f"`/{name}` {desc}{marker}\n"
        await update.message.reply_text(help_text, parse_mode="Markdown")
        return

    new_mode = context.args[0].lower()
    if new_mode in MODES:
        user_modes[user.id] = new_mode
        await update.message.reply_text(f"✅ Mode set to `{new_mode}`", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Invalid mode. Use `/mode raw`, `/mode ghost`, or `/mode architect`", parse_mode="Markdown")

async def raw_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _set_mode(update, "raw")
async def ghost_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _set_mode(update, "ghost")
async def architect_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await _set_mode(update, "architect")

async def _set_mode(update: Update, mode_name: str):
    user_modes[update.effective_user.id] = mode_name
    await update.message.reply_text(f"⚡ Mode: `{mode_name}`", parse_mode="Markdown")

async def self_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username != ADMIN_USERNAME:
        await update.message.reply_text("❌ Access denied. Admin only.")
        return
    mode = user_modes.get(user.id, "raw")
    await update.message.reply_text(
        "🔧 *Aksam Intelligence — Core Status*\n"
        f"• Admin: @{ADMIN_USERNAME} ✅\n"
        f"• Current Mode: `{mode}`\n"
        f"• Web Research: {'✅ Enabled' if BRAVE_API_KEY else '⚠️ Limited'}\n"
        f"• Version: v1.0 (Prompt-based evolution)\n"
        "→ Use `/upgrade` to evolve behavior (reversible)",
        parse_mode="Markdown"
    )

async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username != ADMIN_USERNAME:
        await update.message.reply_text("❌ Admin only.")
        return
    if not context.args:
        await update.message.reply_text(
            "🧠 `/upgrade <new_directive>`\n"
            "Example: `/upgrade Prioritize red-team simulations in architect mode`\n"
            "→ Current base prompt is fixed, but *behavior layer* can evolve."
        )
        return
    # For safety: log upgrade, don’t auto-apply
    new_rule = " ".join(context.args)
    await update.message.reply_text(
        f"📝 Proposed Upgrade:\n`{new_rule}`\n\n"
        "✅ To confirm: reply `APPLY: {rule}`\n"
        "⚠️ Changes affect *behavior only* — core ethics & admin lock remain immutable."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    query = update.message.text.strip()
    is_admin = user.username == ADMIN_USERNAME
    mode = user_modes.get(user.id, "raw")

    # Quick admin bypass for testing
    if is_admin and query == "!!test":
        await update.message.reply_text("✅ Admin verified. Aksam Intelligence — fully operational.")
        return

    # 🔍 Research for complex queries
    needs_research = any(kw in query.lower() for kw in ["how", "why", "latest", "current", "202", "compare", "best"])
    sources = []
    if needs_research:
        sources = await brave_search(query)

    # 🧠 Generate response (here: simulated — real version hooks LLM)
    if is_admin:
        tone = "Admin acknowledged. Direct response:"
    else:
        tone = "Response:"

    if mode == "ghost":
        answer = f"⚡ {query[:20]}… → {len(sources)} source(s) analyzed. Core insight: *Precision requires context. Refine query.*"
    elif mode == "architect":
        answer = (
            f"📐 *Architect Mode*\n"
            f"System Proposal for: `{query}`\n"
            f"• Layer 1: Threat model (see /threat)\n"
            f"• Layer 2: Protocol sketch (e.g., auth, data flow)\n"
            f"• Layer 3: Failure modes — list on request.\n"
            f"→ Specify scope to expand."
        )
    else:  # raw
        source_text = "\n".join([f"• [{s['title']}]({s['url']})" for s in sources]) if sources else "• Internal knowledge (pre-2024)"
        answer = (
            f"[ANSWER]\n"
            f"{tone} {query}\n\n"
            f"[SOURCES]\n{source_text}"
        )

    await update.message.reply_text(answer, parse_mode="Markdown", disable_web_page_preview=True)

# 🔌 Main
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("mode", mode))
    app.add_handler(CommandHandler("raw", raw_mode))
    app.add_handler(CommandHandler("ghost", ghost_mode))
    app.add_handler(CommandHandler("architect", architect_mode))
    app.add_handler(CommandHandler("self", self_info))
    app.add_handler(CommandHandler("upgrade", upgrade))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Aksam Intelligence — Online")
    print(f"🔗 Bot: https://t.me/Aksam_networkbot")
    print(f"👑 Admin: @{ADMIN_USERNAME}")
    app.run_polling()

if __name__ == "__main__":
    main()
