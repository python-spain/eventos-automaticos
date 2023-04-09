import re

from src.event.domain.event import Event


class TelegramMessageBuilder:

    def execute(self, event: Event):

        return (
            f'🐍 {self.__clean_chars(event.community_name)}\n\n'
            f'*Título:* [{self.__clean_chars(event.title)}]({event.link})\n'
            f'*Fecha:* {self.__clean_chars(event.day)}\n'
            f'*Hora:* {self.__clean_chars(event.hour)}\n'
            f'*Lugar:* {self.__clean_chars(event.venue)}\n'
            f'*Descripción:* {self.__clean_chars(event.description)}'
        )

    def __clean_chars(self, text):
        return re.sub(r"[_()*~`>#+-=|{}.!\[\]]", r"\\\g<0>", text)

