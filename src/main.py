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


class HistoryGroupmeStats:
    message_count: dict
    likes_total: dict
    liked_messages: dict
    total_lpp: dict
    total_lpm: dict

    def __init__(self, in_message_count, in_likes_total, in_liked_messages, in_total_lpp, in_total_lpm):
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
    return dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))


def print_dict(dictionary) -> None:
    for key, total in dictionary.items():
        try:
            print(f"{NAME_LUT[key]}\t\t{total:.2f}")
        except KeyError:
            continue


def gather_stats_by_year(year: str):
    with open(MESSAGE_JSON_LOCATION, 'r', encoding='utf-8') as _f:
        message_json = json.load(_f)

    message_count = {}
    likes_total = {}
    liked_messages = {}

    start_date = datetime.date.fromisoformat(f"{year}-12-31")
    end_date = datetime.date.fromisoformat(f"{year+1}-01-01")
    print(start_date, end_date)
    for message in message_json:
        # print(message)
        created_time = datetime.datetime.fromtimestamp(message["created_at"]).date()
        # if created_time.date() > datetime.date.fromisoformat(start_date) and created_time.date() < datetime.date.fromisoformat(end_date):
        if start_date <= created_time <= end_date:
            # print(created_time)
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

    total_lpp = {}
    for key, total_likes in likes_total.items():
        total_messages = message_count[key]
        try:
            lpp = total_likes / total_messages
        except KeyError:
            continue
        total_lpp[key] = lpp

    total_lpm = {}
    for key, total_liked in liked_messages.items():
        total_messages = message_count[key]
        try:
            lpm = total_liked / total_messages
        except KeyError:
            continue
        total_lpm[key] = lpm

    return HistoryGroupmeStats(in_message_count=message_count, in_likes_total=likes_total, in_liked_messages=liked_messages, in_total_lpp=total_lpp, in_total_lpm=total_lpm)


def main():
    stats_2020 = gather_stats_by_year(year=2020)
    stats_2021 = gather_stats_by_year(year=2021)

    print(stats_2020)
    print(stats_2021)

if __name__ == "__main__":
    main()
