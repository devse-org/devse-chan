from typing import Tuple


def rgb_from_str(string: str) -> Tuple[int, int, int]:
    hashcode = hash(string)

    red = hashcode & 0xFF
    blue = (hashcode >> 8) & 0xFF
    green = (hashcode >> 16) & 0xFF

    return (red, blue, green)


def avatar_url_from_nick(nick: str) -> str:
    (red, blue, green) = rgb_from_str(nick)

    avatar_url = "https://eu.ui-avatars.com/api/?background={:02x}{:02x}{:02x}&name={}".format(
        red, blue, green, nick)
    return avatar_url


def irc_colorize_nick(nick: str) -> str:
    colors = [2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13]
    hashcode = hash(nick)

    selected_color = colors[hashcode % len(colors)]
    return f"\x03{selected_color}{nick}\x0F"
