def nick_to_hexcolor(nick):
    hash = 0
    for c in nick:
        hash = ord(c) + ((hash << 5) - hash)
    color = ''
    for i in range(3):
        val = (hash >> (i * 8)) & 0xFF
        color +=  ('00' + hex(val)[2:])[-2:]
    return color

def gen_avatar_from_nick(nick):
    return f"https://eu.ui-avatars.com/api/?background={nick_to_hexcolor(nick)}&name={nick}"
