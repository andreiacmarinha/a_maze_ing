from typing import Dict, Any
import random

class Invalid(Exception):
    #raised when inavlid values


def parser_contex(config: str) -> dict[str, str]:

    result = {} # dictionary storage
    for unedited_line in config.splitlines(): #first we split the lines from the context.txt file
        trimmed_line = unedited_line.strip() #then we trim the whitespaces
        if not trimmed_line or trimmed_line.startswith("#"): #if the line is empty or if its a comment -> move on
            continue
        if "=" not in trimmed_line: #if the line does not have an = it means its not a key=value, raise error
            raise Invalid(f"[Error] Invalid line: {unedited_line}")
        
    key, val = trimmed_line.split("=", 1) #splits the line on the first =. key -> whats before the '=' and val -> whats after
    key = key.strip()
    val = val.strip()

    if key in result:
        raise Invalid(f"[Error] Duplicated key: {key}") #i guess this may be considered an "invalid configuration"
    
    result[key] = val #adds key=value to the dictionary (if width = 10 -> result[width] = 10)

    return result #returns parsed context 


def covert_context(result: dict[str, str]) -> dict[str, object]:

    mandatory_keys = { "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT", "SEED"}

    missing_keys = mandatory_keys - result.keys() #find if there is any key missing
    if missing_keys:
        raise Invalid(f"[Error] Missing kesy: {missing_keys}") #if there is, well, "Huston, we have a problem"
    
    converted = {} #dictionary that will store the converted configurations of the map (from context.txt)

    converted["WIDTH"] = int(result["WIDTH"])
    converted["HEIGHT"] = int(result["HEIGHT"])
    converted["ENTRY"] = tuple(result["ENTRY"].split(","))
    