from datetime import datetime
from devsechan.utils import distance


class ChannelGuard:

    def __init__(self):
        # keep history for antispam feature
        self.history = {}

    def is_spammer(self, nick: str, message: str) -> bool:
        if not nick in self.history.keys():
            self.history[nick] = []

        now = datetime.now()
        similar_message_count = 0
        for hi in self.history[nick][::-1]:
            if (now-hi[0]).total_seconds() > 300:  # if older than 5minute ignore
                break
            if distance.levenshtein(hi[1], message) < 5:
                similar_message_count += 1

        while len(self.history[nick]) >= 3:
            self.history[nick].pop(0)  # remove older

        self.history[nick].append((now, message))
        return True if similar_message_count > 2 else False
