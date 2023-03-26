from dotenv import load_dotenv
import os


load_dotenv()

TELEGRAM_TOKEN_BOT = os.environ.get("TELEGRAM_TOKEN_BOT")
USER_CHAT_ID = os.environ.get("USER_CHAT_ID")
SITY = "nizhniy_novgorod"
LOWER_PRICE = 80000
HIGHEST_PRICE  = 150000
