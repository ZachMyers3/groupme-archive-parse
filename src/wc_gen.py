from email import message
from email.headerregistry import Group
import pathlib
import json
import datetime
import operator
from typing import List

from models import GroupmeMessage, GroupmeMessages

MESSAGE_JSON_LOCATION = pathlib.Path("./src/static/message.json")

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
}


class HistoryGroupmeStats:
    message_count: dict
    likes_total: dict
    liked_messages: dict
    total_lpp: dict
    total_lpm: dict

    def __init__(
        self,
        in_message_count,
        in_likes_total,
        in_liked_messages,
        in_total_lpp,
        in_total_lpm,
    ):
        self.message_count = in_message_count
        self.likes_total = in_likes_total
        self.liked_messages = in_liked_messages
        self.total_lpp = in_total_lpp
        self.total_lpm = in_total_lpm

    def __repr__(self):
        return_str = ""
        self.message_count = sort_dict(self.message_count)
        print("==== MESSAGES SENT ====")
        print_dict(self.message_count)

        self.likes_total = sort_dict(self.likes_total)
        print("==== LIKES  TOTAL ====")
        print_dict(self.likes_total)

        self.total_lpp = sort_dict(self.total_lpp)
        print("==== TOTAL   LPP ====")
        print_dict(self.total_lpp)

        self.liked_messages = sort_dict(self.liked_messages)
        print("==== TOTAL MESSAGES LIKED ====")
        print_dict(self.liked_messages)

        self.total_lpm = sort_dict(self.total_lpm)
        print("==== TOTAL LIKES PER MESSAGE ====")
        print_dict(self.total_lpm)

        return ""


def get_lpp(message) -> int:
    return int(len(message["favorited_by"]))


def get_likers(message):
    return message["favorited_by"]


def sort_dict(dictionary) -> dict:
    return dict(
        sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
    )


def print_dict(dictionary) -> None:
    for key, total in dictionary.items():
        try:
            print(f"{NAME_LUT[key]}\t\t{total:.2f}")
        except KeyError:
            continue


def main():
    messages = GroupmeMessages(MESSAGE_JSON_LOCATION)
    for message in messages.by_year_and_user(year=2021, user="Zach"):
        print(message)


if __name__ == "__main__":
    main()
