import shelve
import re


def save_value_to_shelf(value):
    with shelve.open("user_data") as shelf:
        shelf["input_value"] = value


def load_value_from_shelf():
    with shelve.open("user_data") as shelf:
        return shelf.get("input_value", "")


def strip_ansi_escape_codes(text):
    ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", text)


if __name__ == "__main__":
    value = {"name": "maple", "age": 24}
    save_value_to_shelf(value)
    input_value = load_value_from_shelf()
    print(input_value.get("name"))
