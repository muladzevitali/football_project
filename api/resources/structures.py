from collections import deque


class TerminalText:
    def __init__(self):
        self.queue = dict()

    def set_user(self, user_id):
        self.queue[user_id] = deque()

    def get_user(self, user_id):
        return self.queue.get(user_id, None)

    def insert_text(self, user_id, text):
        if not self.get_user(user_id):
            self.set_user(user_id)
        self.queue[user_id].append(text)

    def get_text(self, user_id):
        if not self.get_user(user_id):
            return ""
        text = "".join("".join(str(x) for x in self.queue[user_id]))
        self.clear_user_text(user_id)
        return text

    def clear_user_text(self, user_id):
        if self.get_user(user_id):
            self.set_user(user_id)
