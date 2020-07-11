import json
from data import goals, teachers


def create_json():
    contents = {"goals": goals, "teachers": teachers}

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(contents, f, indent=4, sort_keys=False, ensure_ascii=False)
        f.close()
