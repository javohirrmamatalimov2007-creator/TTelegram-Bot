import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ── Config ────────────────────────────────────────────────────────────────────
BOT_TOKEN = "8562242152:AAFtW6imNRfykyRadL7LtgH7hn-VR3pks9g"   # Get from @BotFather

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ── 15 Font/Style Converters ──────────────────────────────────────────────────

STYLES = {
    "1. Bold":              lambda t: "".join(chr(0x1D400 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x1D41A + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "2. Italic":            lambda t: "".join(chr(0x1D434 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x1D44E + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "3. Bold Italic":       lambda t: "".join(chr(0x1D468 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x1D482 + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "4. Script":            lambda t: "".join(chr(0x1D49C + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x1D4B6 + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "5. Fraktur":           lambda t: "".join(chr(0x1D504 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x1D51E + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "6. Double Struck":     lambda t: "".join(chr(0x1D538 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x1D552 + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "7. Monospace":         lambda t: "".join(chr(0x1D670 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x1D68A + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "8. Circled":           lambda t: "".join(chr(0x24B6 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x24D0 + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "9. Squared":           lambda t: "".join(chr(0x1F130 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x1F130 + ord(c.upper()) - ord('A')) if 'a' <= c <= 'z' else c for c in t),
    "10. Fullwidth":        lambda t: "".join(chr(0xFF21 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0xFF41 + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "11. Small Caps":       lambda t: t.upper().translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ")),
    "12. Upside Down":      lambda t: t[::-1].translate(str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "ɐqɔpǝɟɓɥᴉɾʞlɯuodbɹsʇnʌʍxʎzɐqɔpǝɟɓɥᴉɾʞlɯuodbɹsʇnʌʍxʎz")),
    "13. Strikethrough":    lambda t: "".join(c + "\u0336" for c in t),
    "14. Underline":        lambda t: "".join(c + "\u0332" for c in t),
    "15. Dotted":           lambda t: "".join(c + "\u0307" for c in t),
}

STYLE_NAMES = list(STYLES.keys())


def convert(text: str, style_key: str) -> str:
    try:
        return STYLES[style_key](text)
    except Exception:
        return text


def build_keyboard(nickname: str) -> InlineKeyboardMarkup:
    """Build inline keyboard with all 15 style buttons."""
    buttons = []
    row = []
    for i, name in enumerate(STYLE_NAMES):
        row.append(InlineKeyboardButton(name, callback_data=f"{name}|{nickname}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)


# ── Handlers ──────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "✏️ *Nickname Generator Bot*\n\n"
        "Send me any name or word and I'll show it in *15 different font styles*!\n\n"
        "Just type your nickname below 👇",
        parse_mode="Markdown",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    styles_list = "\n".join(f"  {name}" for name in STYLE_NAMES)
    await update.message.reply_text(
        f"ℹ️ *How to use:*\n"
        f"Send any text → tap a style button → copy your styled nickname!\n\n"
        f"*Available styles:*\n{styles_list}",
        parse_mode="Markdown",
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Receive a nickname and show style picker."""
    nickname = update.message.text.strip()
    if not nickname:
        await update.message.reply_text("Please send a non-empty nickname.")
        return

    preview_lines = []
    for name, fn in STYLES.items():
        try:
            styled = fn(nickname)
        except Exception:
            styled = nickname
        preview_lines.append(f"{name}:\n`{styled}`")

    preview = "\n\n".join(preview_lines)

    await update.message.reply_text(
        f"🎨 *Styles for:* `{nickname}`\n\n{preview}\n\n"
        "👆 Tap a button below to get just that style:",
        parse_mode="Markdown",
        reply_markup=build_keyboard(nickname),
    )


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the selected styled nickname as a copyable message."""
    query = update.callback_query
    await query.answer()

    data = query.data
    if "|" not in data:
        return

    style_key, nickname = data.split("|", 1)
    styled = convert(nickname, style_key)

    await query.message.reply_text(
        f"✅ *{style_key}*\n\n`{styled}`\n\n"
        "_Tap the text above to copy it!_",
        parse_mode="Markdown",
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("Nickname bot running... Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()