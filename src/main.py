import pathlib

from models import GroupmeMessages

MESSAGE_JSON_LOCATION = pathlib.Path("./src/static/message.json")


def main():
    messages = GroupmeMessages(MESSAGE_JSON_LOCATION)

    messages.compute_like_statistics(year=2021)
    messages.generate_csv(save_location=pathlib.Path("stats_2021.csv"))

    # most_liked = messages.get_most_liked_messages(year=2021, user="james")
    # for message in most_liked:
    #     print(message.raw)


if __name__ == "__main__":
    main()
