import json

from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired
from wtforms.validators import Length


class ReadData(object):
    day_week = {
        "mon": "Понедельник",
        "tue": "Вторник",
        "wed": "Среда",
        "thu": "Четверг",
        "fri": "Пятница",
        "sat": "Суббота",
        "sun": "Воскресенье",
    }

    pic_goal = {"travel": "⛱", "study": "🏫", "work": "🏢", "relocate": "🚜"}

    href_goal = {
        "travel": "travel/",
        "study": "study/",
        "work": "work/",
        "relocate": "relocate/",
        "programming": "programming/",
    }

    with open("data.json", "r", encoding="utf-8") as f:
        contents = json.load(f)
        teachers = contents["teachers"]
        goals = contents["goals"]


class RequestForm(FlaskForm):
    goals = RadioField(
        "goal",
        choices=[
            (goal_key, goal_value) for goal_key, goal_value in ReadData.goals.items()
        ],
        validators=[DataRequired()],
        default="travel",
    )
    clientName = StringField("clientName", [InputRequired()])
    clientPhone = StringField(
        "clientPhone", [Length(min=6, message="Длина номера должна быть не менее 6")]
    )
    time = RadioField(
        "time",
        choices=[
            ("1-2", "1-2 часа в неделю"),
            ("3-5", "3-5 часа в неделю"),
            ("5-7", "5-7 часа в неделю"),
            ("7-10", "7-10 часа в неделю"),
        ],
        default="1-2",
    )


class BookingForm(FlaskForm):
    clientName = StringField("clientName", [InputRequired()])
    clientPhone = StringField(
        "clientPhone", [Length(min=6, message="Длина номера должна быть не менее 6")]
    )


def save_booking(file_name, data_to_file):
    old_data = []

    try:
        with open(file_name, "r", encoding="utf-8") as f:
            try:
                old_data = json.load(f)
            except json.decoder.JSONDecodeError:
                old_data = []
            f.close()
    except FileNotFoundError:
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, sort_keys=False, ensure_ascii=False)
            f.close()

    with open(file_name, "w", encoding="utf-8") as f:
        old_data.append(data_to_file)
        json.dump(old_data, f, indent=4, sort_keys=False, ensure_ascii=False)
        f.close()
