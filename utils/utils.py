from random import choice

from settings import SYMBOLS, LENGTH


def generate_suffix() -> str:
    """Функция генерации случайно суффикса для короткого адреса"""
    suffix: str = ""
    for _ in range(LENGTH):
        suffix += choice(SYMBOLS)
    return suffix
