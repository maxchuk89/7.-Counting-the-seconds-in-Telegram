import os
import ptbot
import pytimeparse
from dotenv import load_dotenv


def render_progressbar(total, iteration, prefix='', suffix='', length=15, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)

def reply(chat_id, text):
    delay = pytimeparse.parse(text)
    if delay is None:
        return
    initial_message = "Осталось {} секунд".format(delay)
    message_id = bot.send_message(chat_id, initial_message)
    bot.create_countdown(delay, notify_progress, chat_id=chat_id, message_id=message_id, total=delay)

def notify_progress(secs_left, chat_id, message_id, total):
 
    progress_bar = render_progressbar(total, total - secs_left, length=15)
    if secs_left > 0:
        new_text = "Осталось {} секунд\n{}".format(secs_left, progress_bar)
        bot.update_message(chat_id, message_id, new_text)
    elif secs_left == 0:
        new_text = "Осталось 0 секунд\n{}".format(progress_bar)
        bot.update_message(chat_id, message_id, new_text)
        bot.send_message(chat_id, "Время вышло")

def main():
    load_dotenv()
    global bot
    TG_TOKEN = os.getenv("TG_TOKEN")
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(reply)
    bot.run_bot()

if __name__ == '__main__':
    main()