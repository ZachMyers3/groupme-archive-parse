import pathlib
from models import GroupmeMessages, NAME_LUT

MESSAGE_JSON_LOCATION = pathlib.Path("./src/static/message.json")


def main():
    messages = GroupmeMessages(MESSAGE_JSON_LOCATION)

    messages.generate_word_clouds(
        users=NAME_LUT.values(),
        year=2021,
        save_location=pathlib.Path("images/2021"),
    )


if __name__ == "__main__":
    main()
