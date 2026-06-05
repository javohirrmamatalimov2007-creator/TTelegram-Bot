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
BOT_TOKEN = "8251153783:AAEm6efy4z-nehMK7L3x2wLsp-a82fbrAhY"
 
# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)
 
 
# ── 15 Shrift Konvertori ──────────────────────────────────────────────────────
 
STYLES = {
    "1. Qalin (Bold)":          lambda t: "".join(chr(0x1D400 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x1D41A + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "2. Kursiv (Italic)":       lambda t: "".join(chr(0x1D434 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x1D44E + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "3. Qalin Kursiv":          lambda t: "".join(chr(0x1D468 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x1D482 + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "4. Chiroyli (Script)":     lambda t: "".join(chr(0x1D49C + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x1D4B6 + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "5. Gotik (Fraktur)":       lambda t: "".join(chr(0x1D504 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x1D51E + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "6. Ikki Chiziq":           lambda t: "".join(chr(0x1D538 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x1D552 + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "7. Monospace":             lambda t: "".join(chr(0x1D670 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x1D68A + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "8. Doira (Circled)":       lambda t: "".join(chr(0x24B6 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x24D0 + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "9. Kvadrat (Squared)":     lambda t: "".join(chr(0x1F130 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0x1F130 + ord(c.upper()) - ord('A')) if 'a' <= c <= 'z' else c for c in t),
    "10. Keng (Fullwidth)":     lambda t: "".join(chr(0xFF21 + ord(c) - ord('A')) if 'A' <= c <= 'Z' else chr(0xFF41 + ord(c) - ord('a')) if 'a' <= c <= 'z' else c for c in t),
    "11. Kichik Bosh Harf":     lambda t: t.upper().translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ")),
    "12. Teskari":              lambda t: t[::-1].translate(str.maketrans("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "ɐqɔpǝɟɓɥᴉɾʞlɯuodbɹsʇnʌʍxʎzɐqɔpǝɟɓɥᴉɾʞlɯuodbɹsʇnʌʍxʎz")),
    "13. Chizilgan":            lambda t: "".join(c + "\u0336" for c in t),
    "14. Tagiga Chiziq":        lambda t: "".join(c + "\u0332" for c in t),
    "15. Nuqtali":              lambda t: "".join(c + "\u0307" for c in t),
}
 
STYLE_NAMES = list(STYLES.keys())
 
 
def convert(text: str, style_key: str) -> str:
    try:
        return STYLES[style_key](text)
    except Exception:
        return text
 
 
def build_keyboard(nickname: str) -> InlineKeyboardMarkup:
    buttons = []
    row = []
    for name in STYLE_NAMES:
        row.append(InlineKeyboardButton(name, callback_data=f"{name}|{nickname}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)
 
 
# ── Handlerlar ────────────────────────────────────────────────────────────────
 
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Salom, *{user.first_name}*!\n\n"
        "✏️ *Nickname Generator Bot*ga xush kelibsiz!\n\n"
        "Bu bot ismingizni *15 xil chiroyli shriftda* ko'rsatadi!\n\n"
        "📝 Quyida o'z nickname yoki ismingizni yozing 👇",
        parse_mode="Markdown",
    )
 
 
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    styles_list = "\n".join(f"  {name}" for name in STYLE_NAMES)
    await update.message.reply_text(
        "ℹ️ *Qanday ishlatish:*\n\n"
        "1️⃣ Istalgan matn yozing\n"
        "2️⃣ Shrift tugmasini bosing\n"
        "3️⃣ Chiroyli nickname'ni nusxalab oling!\n\n"
        f"*Mavjud shriftlar:*\n{styles_list}",
        parse_mode="Markdown",
    )
 
 
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    nickname = update.message.text.strip()
    if not nickname:
        await update.message.reply_text("❗ Iltimos, bo'sh bo'lmagan matn yuboring.")
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
        f"🎨 *Shriftlar:* `{nickname}`\n\n{preview}\n\n"
        "👆 Quyidagi tugmalardan birini bosib faqat o'sha shriftni oling:",
        parse_mode="Markdown",
        reply_markup=build_keyboard(nickname),
    )
 
 
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
 
    data = query.data
    if "|" not in data:
        return
 
    style_key, nickname = data.split("|", 1)
    styled = convert(nickname, style_key)
 
    await query.message.reply_text(
        f"✅ *{style_key}*\n\n`{styled}`\n\n"
        "_Yuqoridagi matnni bosib nusxalab oling!_",
        parse_mode="Markdown",
    )
 
 
# ── Main ──────────────────────────────────────────────────────────────────────
 
def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()
 
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
 
    logger.info("Bot ishga tushdi... To'xtatish uchun Ctrl+C bosing.")
    app.run_polling(allowed_updates=["message", "callback_query"])
 
 
if __name__ == "__main__":
    main()
 