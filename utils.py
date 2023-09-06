import shelve
import re
import os


def save_value_to_shelf(value):
    with shelve.open("user_data") as shelf:
        shelf["input_value"] = value


def load_value_from_shelf():
    with shelve.open("user_data") as shelf:
        return shelf.get("input_value", "")


def strip_ansi_escape_codes(text):
    ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", text)


# Define the exclude_if decorator
def exclude_if(*patterns):
    def decorator(fn):
        def wrapper(directory_path):
            file_list = os.listdir(directory_path)
            filtered_files = [
                file
                for file in file_list
                if not any(re.search(pattern, file) for pattern in patterns)
            ]
            return filtered_files

        return wrapper

    return decorator


@exclude_if(r"\.bak$", r"\.dat$", r"\.dir$")
def list_files(directory_path):
    return directory_path


if __name__ == "__main__":
    # Example usage:
    directory_path = "."

    filtered_files = list_files(directory_path)

    # Print the filtered file list
    for file in filtered_files:
        print(file)
