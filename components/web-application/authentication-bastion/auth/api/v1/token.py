from collections import defaultdict
from typing import Set


class TokenManager:
    def __init__(self):
        self._tokens_per_user = defaultdict(set)

    def tokens_for_user(self, username: str) -> Set[str]:
        return self._tokens_per_user[username]

    def add_token_for_user(self, username: str, token: str):
        self._tokens_per_user[username].add(token)
