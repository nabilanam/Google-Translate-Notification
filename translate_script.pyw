import time
import json
import requests
import keyboard
import pyperclip
from plyer import notification


class GTNotification:
    def __init__(self, source, target, trigger_key, release_key):
        self.source_language = source
        self.target_language = target
        self.trigger_key = trigger_key
        self.release_key = release_key

    def wait(self):
        keyboard.add_hotkey(self.trigger_key, self.hotkey_callback)
        keyboard.wait(self.release_key)
        keyboard.clear_all_hotkeys()

    def hotkey_callback(self):
        keyboard.press('ctrl+c')
        time.sleep(0.1)

        word = str(pyperclip.paste()).strip()
        if word.find(' ') > 0:
            word = word.partition(' ')[0]

        translation = self.translate(word)
        self.notify(word, translation)

    def translate(self, text: str) -> str:
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}&dt=t&q={}" \
            .format(self.source_language, self.target_language, text)

        req = requests.get(url)
        req.raise_for_status()

        translation = req.json()[0][0][0]
        return translation

    def notify(self, word: str, translation: str):
        notification.notify(title=word, message=translation, app_name='Noodle', app_icon='icon.ico')


def load_config():
    with open('config.json') as f:
        data = json.load(f)
        f.close()
        return data


if __name__ == '__main__':
    config = load_config()
    gtn = GTNotification(config['source'], config['target'], config['trigger_key'], config['release_key'])
    gtn.wait()
