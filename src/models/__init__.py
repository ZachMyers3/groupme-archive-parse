from sqlite3 import Date
from tokenize import group
from typing import List

import json

from datetime import datetime


NAME_LUT = {
    "27952020": "Paul",
    "10947804": "T Sparr",
    "12478441": "Zach",
    "12478651": "Murph",
    "12478465": "Zody",
    "12481995": "Nardy",
    "6789777": "John",
    "12478598": "James",
    "17287394": "Bricker",
    "12478609": "Chance",
    "12478582": "Jared",
    "system": "system",
    "calendar": "calendar",
}


class GroupmeMessage:
    sender_id: str
    message_text: str
    favorited_by: List[str]
    created_at: datetime
    raw: dict

    def parse_favorites(self, favorite_list) -> List[str]:
        return_list = []
        for favorite in favorite_list:
            try:
                name = NAME_LUT[favorite]
            except KeyError:
                continue

            return_list.append(name)

        return return_list

    def __init__(self, groupme_message):
        self.sender_id = groupme_message["sender_id"]
        self.name = NAME_LUT[self.sender_id]
        self.message_text = groupme_message["text"]
        self.favorited_count = len(groupme_message["favorited_by"])
        self.favorited_by = self.parse_favorites(
            groupme_message["favorited_by"]
        )
        self.created_at = datetime.fromtimestamp(groupme_message["created_at"])
        self.raw = groupme_message

    def __repr__(self):
        return f"{self.name}: {self.message_text}"


class GroupmeMessages:
    messages: List[GroupmeMessage]

    def filter_message(self, message_json) -> bool:
        if message_json["system"]:
            return True
        # omit non-users
        if message_json["sender_type"] != "user":
            return True
        # omit users not in the look up table
        if message_json["user_id"] not in NAME_LUT.keys():
            return True

        return False

    def by_year(self, year: int):
        start_date = datetime.fromisoformat(f"{year}-01-01")
        end_date = datetime.fromisoformat(f"{year}-12-31")
        for message in self.messages:
            if start_date <= message.created_at <= end_date:
                yield message

    def by_user(self, user: str):
        for message in self.messages:
            if user == message.name:
                yield message

    def by_year_and_user(self, year: int, user: str):
        start_date = datetime.fromisoformat(f"{year}-01-01")
        end_date = datetime.fromisoformat(f"{year}-12-31")
        for message in self.messages:
            if start_date <= message.created_at <= end_date:
                if user.lower() == message.name.lower():
                    yield message

    def get_most_liked_messages(self, year: int, user: str):
        most_liked = []
        most_liked_int = 0

        for message in self.by_year_and_user(year=year, user=user):
            if len(most_liked) == 0:
                most_liked = [message]
                most_liked_int = message.favorited_count
                continue

            if message.favorited_count > most_liked_int:
                most_liked = [message]
                most_liked_int = message.favorited_count
            elif message.favorited_count == most_liked_int:
                most_liked.append(message)

        return most_liked

    def __init__(self, json_file):
        with open(json_file, "r", encoding="utf-8") as _f:
            message_json = json.load(_f)

        self.messages = []
        for message in message_json:
            if self.filter_message(message):
                continue
            groupme_msg = GroupmeMessage(message)
            self.messages.append(groupme_msg)
