from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
from datetime import datetime
import csv


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=4):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None

        return last_update

token = "799896320:AAHBUXQPqyXqXOFEaqOwOpTMltOA387orMs"

ticket_bot = BotHandler(token)
now = datetime.now()


def main():
    new_offset = None
    d100 = {}
    with open('100.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            d100[int(row['num'])] = int(row['res'])

    while True:
        ticket_bot.get_updates(new_offset)
        last_update = ticket_bot.get_last_update()
        if last_update is not None:
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            try:
                num = int(last_chat_text)
            except ValueError:
                ticket_bot.send_message(last_chat_id, '{} is not integer number'.format(last_chat_text))
            if num >= 10 ** 6:
                ticket_bot.send_message(last_chat_id, 'number should be less than 1000000'.format(last_chat_text))
            else:
                ticket_bot.send_message(last_chat_id, d100[num])
            new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

