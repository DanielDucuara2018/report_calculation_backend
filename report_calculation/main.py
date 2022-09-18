from config import logger
from bot import telegram_app

def main():
    logger.info("Initialising App")
    telegram_app.run_polling()

if __name__ == "__main__":
    main()