from typing import TypedDict, Tuple
import random


class Invalid(Exception):
    # raised when inavlid values
    pass


class Configs(TypedDict):
    WIDTH: int
    HEIGHT: int
    ENTRY: Tuple[int, int]
    EXIT: Tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int


def parser_contex(config: str) -> dict[str, str]:

    result = {}  # dictionary storage
    for unedited_line in config.splitlines():  # first we split the lines from the context.txt file
        trimmed_line = unedited_line.strip()  # then we trim the whitespaces
        if not trimmed_line or trimmed_line.startswith("#"):  # if the line is empty or if its a comment -> move on
            continue
        if "=" not in trimmed_line:  # if the line does not have an = it means its not a key=value, raise error
            raise Invalid(f"[Error] Invalid line: {unedited_line}")

        key, val = trimmed_line.split("=", 1)  # splits the line on the first =. key -> whats before the '=' and val -> whats after
        key = key.strip()
        val = val.strip()

        if key in result:
            raise Invalid(f"[Error] Duplicated key: {key}")  # i guess this may be considered an "invalid configuration"

        result[key] = val  # adds key=value to the dictionary (if width = 10 -> result[width] = 10)

    return result  # returns parsed context


def parse_coordinates(value: str) -> Tuple[int, int]:
    parts = value.split(",")
    if len(parts) != 2:
        raise Invalid(f"[Error] Invalid coordinates: {value}")
    return (int(parts[0]), int(parts[1]))


def covert_context(result: dict[str, str]) -> Configs:

    mandatory_keys = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
                      "PERFECT", "SEED"}

    missing_keys = mandatory_keys - result.keys()  # find if there is any key missing
    if missing_keys:
        raise Invalid(f"[Error] Missing keys: {missing_keys}")  # if there is, well, "Huston, we have a problem"

    width = int(result["WIDTH"])
    height = int(result["HEIGHT"])
    entry = parse_coordinates(result["ENTRY"])
    exit = parse_coordinates(result["EXIT"])

    if not result["OUTPUT_FILE"].endswith(".txt"):
        raise Invalid("[Error] OUTPUT_FILE must be a txt file")
    output_file = result["OUTPUT_FILE"]

    val = result["PERFECT"].lower()
    if val == "true":
        is_perfect = True
    elif val == "false":
        is_perfect = False
    else:
        raise Invalid("[Error] PERFECT must be True or False")

    seed = result["SEED"]
    if not seed:
        seed_val = random.randrange(0, 100)
    elif not seed.isdigit():
        raise Invalid(f"[Error] SEED given is not numeric: {seed}")
    else:
        seed_val = int(seed)

    return {"WIDTH": width, "HEIGHT": height, "ENTRY": entry, "EXIT": exit,
            "OUTPUT_FILE": output_file, "PERFECT": is_perfect,
            "SEED": seed_val}


def parse_filename(filename: str) -> Configs:
    with open(filename, "r") as f:
        content = f.read()

    result = parser_contex(content)
    config = covert_context(result)

    return config


if __name__ == "__main__":
    try:
        config = parse_filename("config.txt")
        print("Parsed config:")
        for k, v in config.items():
            print(f"{k}: {v}")
    except Invalid as e:
        print(e)
