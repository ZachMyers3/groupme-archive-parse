from os import mkdir
from pyexpat.errors import messages
from typing import List
import pathlib
from wordcloud import WordCloud, STOPWORDS

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
}


class GroupmeMessage:
    sender_id: str
    message_text: str
    favorited_by: List[str]
    created_at: datetime
    attachments: List[dict]
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
        self.attachments = groupme_message["attachments"]
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

    def by_year_and_users(self, year: int, users: List[str]):
        start_date = datetime.fromisoformat(f"{year}-01-01")
        end_date = datetime.fromisoformat(f"{year}-12-31")
        for message in self.messages:
            if start_date <= message.created_at <= end_date:
                if message.name.lower() in [x.lower() for x in users]:
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

    def compute_like_statistics(self, year: int):
        print(f"Generating statistics for year {year}...")
        self.total_likes_given = {}
        self.total_likes_recieved = {}
        self.total_messages = {}
        self.total_image_posts = {}
        for user in NAME_LUT.values():
            user = user.lower()
            self.total_likes_given[user] = 0
            self.total_likes_recieved[user] = 0
            self.total_messages[user] = 0
            self.total_image_posts[user] = 0

        for message in self.by_year(year=year):
            if len(message.attachments) > 0:
                if message.attachments[0]["type"] == "image":
                    self.total_image_posts[message.name.lower()] += 1
            self.total_messages[message.name.lower()] += 1
            self.total_likes_recieved[
                message.name.lower()
            ] += message.favorited_count
            for favoritee in message.favorited_by:
                self.total_likes_given[favoritee.lower()] += 1

        self.average_likes_recieved_per_message = {}
        self.average_likes_given_per_message = {}
        for name, value in self.total_messages.items():
            self.average_likes_given_per_message[name] = (
                self.total_likes_given[name.lower()] / value
            )
            self.average_likes_recieved_per_message[name] = (
                self.total_likes_recieved[name.lower()] / value
            )

        self.total_messages = self.sort_dict(self.total_messages)
        self.total_likes_given = self.sort_dict(self.total_likes_given)
        self.total_likes_recieved = self.sort_dict(self.total_likes_recieved)
        self.total_image_posts = self.sort_dict(self.total_image_posts)
        self.average_likes_recieved_per_message = self.sort_dict(
            self.average_likes_recieved_per_message
        )
        self.average_likes_given_per_message = self.sort_dict(
            self.average_likes_given_per_message
        )

    def generate_csv(self, save_location=pathlib.Path):
        csv = "name,total_messages,total_likes_given,total_likes_recieved,total_image_posts,average_likes_recieved_per_message,average_likes_given_per_messsage\n"
        for name in self.total_messages.keys():
            name = name.lower()
            csv_line = f"{name},"
            csv_line += f"{self.total_messages[name]},"
            csv_line += f"{self.total_likes_given[name]},"
            csv_line += f"{self.total_likes_recieved[name]},"
            csv_line += f"{self.total_image_posts[name]},"
            csv_line += f"{self.average_likes_recieved_per_message[name]},"
            csv_line += f"{self.average_likes_given_per_message[name]}\n"
            csv += csv_line

        with open(save_location, "w") as _w:
            _w.write(csv)

    def generate_word_clouds(
        self, year: int, users: List[str], save_location=pathlib.Path
    ):
        words_dictionary = {}
        for user in users:
            words_dictionary[user.lower()] = ""

        for message in self.by_year_and_users(year=year, users=users):
            scrubbed_message = (
                str(message.message_text)
                .lower()
                .strip()
                .replace("\n", " ")
                .replace("\\'", "'")
                .replace(".", "")
                .replace("?", "")
                .replace("!", "")
                + " "
            )
            words_dictionary[message.name.lower()] += scrubbed_message

        stopwords = set(STOPWORDS)
        stopwords.update(["s", "m", "t", "don", "re"])
        for name, words in words_dictionary.items():
            print(f"Generating word cloud {name}/{year}")
            wc = WordCloud(
                width=1500,
                height=1500,
                background_color="white",
                stopwords=stopwords,
                min_font_size=10,
            ).generate(words)

            save_location.mkdir(exist_ok=True)
            wc.to_file(str(save_location / f"{name}.jpg"))

    @staticmethod
    def sort_dict(dictionary) -> dict:
        return dict(
            sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
        )

    def __init__(self, json_file):
        with open(json_file, "r", encoding="utf-8") as _f:
            message_json = json.load(_f)

        print("Loading messages from JSON...")
        self.messages = []
        for message in message_json:
            if self.filter_message(message):
                continue
            groupme_msg = GroupmeMessage(message)
            self.messages.append(groupme_msg)
