import datetime
import locale
import re


from telegram_python_es.event.domain.event import Event


class TelegramMessageBuilder:
    def execute(self, event: Event):
        return (
            f"🐍 {self.__clean_chars(event.community_name)}\n\n"
            f"*Título:* [{self.__clean_chars(event.title)}]({event.link})\n"
            f"*Fecha:* {self.__get_day(event.date)}\n"
            f"*Hora:* {self.__get_hour(event.date)}\n"
            f"*Lugar:* {self.__clean_chars(event.venue)}\n"
            f"*Descripción:* {self.__clean_chars(event.description)}"
        )

    def __clean_chars(self, text):
        return re.sub(r"[_()*~`>#+-=|{}.!\[\]]", r"\\\g<0>", text)

    def __get_hour(self, date):
        return f"{date.hour}:{date.minute}"

    def __get_day(self, date):
        spanish_locale = locale.setlocale(locale.LC_ALL, "es_ES.UTF-8")
        formatted_date = date.strftime("%A %d de %B")
        return formatted_date
