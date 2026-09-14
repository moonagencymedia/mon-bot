import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ChatJoinRequestHandler, CommandHandler, ContextTypes

# ============================================================
#  CONFIG — modifie ces valeurs si besoin
# ============================================================
BOT_TOKEN   = "8173722979:AAETC142G8kuazugxF3T6ef2fsTcspKimlA"
PHOTO_PATH  = "photo.jpeg"   # place la photo dans le même dossier que ce script
INSTAGRAM_URL = "https://www.instagram.com/kimi_tanakaa/"
TELEGRAM_DM_URL = "https://t.me/meitanakaa"

MESSAGE_TEXT = (
"Hey ! 🍓\n"
"Bienvenue sur mon canal Telegram ! 💫\n\n"
"Petite surprise : ma fille Kimi vient de lancer son Instagram 👀\n"
"Elle a 18 ans et elle débute, allez lui faire un petit coucou 💗\n\n"
"Envoie moi un message sur telegram pour me dire que tu t'es abonné "
"et je t'enverrais une surprise 💗"
)
# ============================================================

logging.basicConfig(
format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
level=logging.INFO
)
logger = logging.getLogger(__name__)
async def handle_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Déclenché à chaque demande d'accès au canal privé."""
    join_request = update.chat_join_request
    user = join_request.from_user
    chat = join_request.chat

    logger.info(f"Nouvelle demande de {user.full_name} (id={user.id}) pour rejoindre {chat.title}")

    # Bouton cliquable vers Instagram
    keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("👉 L'Instagram de Kimi 🍓", url=INSTAGRAM_URL)],
        [InlineKeyboardButton("💬 M'écrire ici 💗", url=TELEGRAM_DM_URL)]
    ])

    try:
        # Envoi de la photo + texte + bouton
        with open(PHOTO_PATH, "rb") as photo_file:
            await context.bot.send_photo(
                chat_id=user.id,
                photo=photo_file,
                caption=MESSAGE_TEXT,
                reply_markup=keyboard
            )
        logger.info(f"Message envoyé à {user.full_name}")
    except Exception as e:
        logger.error(f"Impossible d'envoyer le message à {user.id} : {e}")

    # Approbation manuelle — rien à faire ici

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot actif ✅ — en attente des demandes d'accès au canal.")
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(ChatJoinRequestHandler(handle_join_request))

    logger.info("Bot démarré — en écoute...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
