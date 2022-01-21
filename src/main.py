import pathlib
import json
import datetime
import operator

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
    return dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))


def print_dict(dictionary) -> None:
    for key, total in dictionary.items():
        try:
            print(f"{NAME_LUT[key]}\t\t{total:.2f}")
        except KeyError:
            continue


def main():
    with open(MESSAGE_JSON_LOCATION, 'r', encoding='utf-8') as _f:
        message_json = json.load(_f)

    message_count = {}
    likes_total = {}
    liked_messages = {}

    for message in message_json:
        # print(message)
        created_time = datetime.datetime.fromtimestamp(message["created_at"])
        if created_time.date() > datetime.date.fromisoformat("2020-12-31") and created_time.date() < datetime.date.fromisoformat("2022-01-01"):
            continue

        lpp = get_lpp(message)

        likers = get_likers(message)
        for liker in likers:
            try:
                liked_messages[liker] += 1
            except KeyError:
                liked_messages[liker] = 1

        try:
            message_count[message["sender_id"]] += 1
        except KeyError:
            message_count[message["sender_id"]] = 1

        try:
            likes_total[message["sender_id"]] += lpp
        except KeyError:
            likes_total[message["sender_id"]] = lpp


    message_count = sort_dict(message_count)
    print("==== MESSAGES SENT ====")
    print_dict(message_count)

    likes_total = sort_dict(likes_total)
    print("==== LIKES  TOTAL ====")
    print_dict(likes_total)

    total_lpp = {}
    for key, total_likes in likes_total.items():
        total_messages = message_count[key]
        try:
            lpp = total_likes / total_messages
        except KeyError:
            continue
        total_lpp[key] = lpp

    total_lpp = sort_dict(total_lpp)
    print("==== TOTAL   LPP ====")
    print_dict(total_lpp)

    liked_messages = sort_dict(liked_messages)
    print("==== TOTAL MESSAGES LIKED ====")
    print_dict(liked_messages)

    total_lpm = {}
    for key, total_liked in liked_messages.items():
        total_messages = message_count[key]
        try:
            lpm = total_liked / total_messages
        except KeyError:
            continue
        total_lpm[key] = lpm

    total_lpm = sort_dict(total_lpm)
    print("==== TOTAL LIKES PER MESSAGE ====")
    print_dict(total_lpm)


if __name__ == "__main__":
    main()
