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

    words = ""

    for message in message_json:
        try:
            if NAME_LUT[message["sender_id"]] != "Chance":
                continue
        except KeyError:
            continue

        message = (
            str(message["text"])
            .lower()
            .strip()
            .replace("\n", " ")
            .replace(" s ", " ")
            + " "
        )
        if " s " in message:
            print(message)
        words += message

    wc = WordCloud(
        width=800,
        height=800,
        background_color="white",
        stopwords=set(STOPWORDS),
        min_font_size=10,
    ).generate(words)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wc)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.show()


if __name__ == "__main__":
    main()
