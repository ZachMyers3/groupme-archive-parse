from os import waitpid
import pathlib
import json

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd

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
    with open(MESSAGE_JSON_LOCATION, "r", encoding="utf-8") as _f:
        message_json = json.load(_f)

    words_by_user = {}

    for message in message_json:
        try:
            name = NAME_LUT[message["sender_id"]]
        except KeyError:
            continue

        message = (
            str(message["text"])
            .lower()
            .strip()
            .replace("\n", " ")
            .replace("\\'", "'")
            .replace(".", "")
            .replace("?", "")
            .replace("!", "")
            + " "
        )

        try:
            words_by_user[name] += message
        except KeyError:
            words_by_user[name] = message

    stopwords = set(STOPWORDS)
    stopwords.update(["s", "m", "t", "don"])
    for name, words in words_by_user.items():
        print(f"Generating cloud for {name}")
        wc = WordCloud(
            width=2500,
            height=2500,
            background_color="white",
            stopwords=stopwords,
            min_font_size=10,
        ).generate(words)

        wc.to_file(f".\\images\\{name}.jpg")


if __name__ == "__main__":
    main()
