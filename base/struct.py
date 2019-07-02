from __future__ import annotations


class Config:
    def __init__(self, cfg: dict) -> None:
        self.bot_token = cfg['bot_token']
        self.postgresql_user = cfg['postgresql_user']
        self.postgresql_password = cfg['postgresql_password']
        self.min_message_xp = cfg['min_message_xp']
        self.max_message_xp = cfg['max_message_xp']
