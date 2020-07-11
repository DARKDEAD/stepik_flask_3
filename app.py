import random
from flask import Flask, render_template, request

from form import RequestForm, BookingForm, ReadData, save_booking

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = "xv3gavkxc04n3mzx7oksd6q"


@app.route("/")
def render_index():
    return render_template(
            "index.html",
            teachers=random.sample(ReadData.teachers, 6),
            pic_goal=ReadData.pic_goal,
            goals=ReadData.goals,
            href_goal=ReadData.href_goal,
    )


@app.route("/all_teachers/")
def render_all_teachers():
    return render_template(
            "index.html",
            teachers=ReadData.teachers,
            pic_goal=ReadData.pic_goal,
            goals=ReadData.goals,
            href_goal=ReadData.href_goal,
    )


@app.route("/goals/<goal>/")
def render_search(goal):
    teachers_goals = []
    for g in ReadData.teachers:
        if goal in g["goals"]:
            teachers_goals.append(g)

    return render_template(
            "goal.html",
            teachers=teachers_goals,
            goal=ReadData.goals[goal],
            pic_goal=ReadData.pic_goal.get(goal, ""),
    )


@app.route("/profiles/<int:id_teacher>/")
def render_profile(id_teacher):
    return render_template(
            "profile.html",
            teacher=ReadData.teachers[id_teacher],
            goals=ReadData.goals,
            day_week=ReadData.day_week,
            id_teacher=id_teacher,
    )


@app.route("/request/")
def render_request():
    form = RequestForm()
    return render_template("request.html", form=form)


@app.route("/request_done/", methods=["POST", "GET"])
def render_request_done():
    form = RequestForm()
    if form.validate_on_submit():
        goal = form.goals.data

        req = {
            "name" : form.clientName.data,
            "phone": form.clientPhone.data,
            "time" : request.form.get("time"),
            "goal" : goal,
        }

        save_booking("request.json", req)

        return render_template(
                "request_done.html", goal=ReadData.goals.get(goal, ""), form=form
        )
    else:
        return render_template("request.html", form=form)


@app.route("/booking/<int:id_teacher>/<day>/<time>/")
def render_booking(id_teacher, day, time):
    form = BookingForm()
    return render_template(
            "booking.html",
            form=form,
            teacher=ReadData.teachers.get(id_teacher, ""),
            day=ReadData.day_week.get(day, ""),
            time=time,
    )


@app.route("/booking_done/", methods=["GET", "POST"])
def render_booking_done():
    teacher = ReadData.teachers[int(request.form.get("clientTeacher"))]
    day = request.form.get("clientWeekday")
    time = request.form.get("clientTime")
    form = BookingForm()
    if form.validate_on_submit():
        name = form.clientName.data
        phone = form.clientPhone.data

        booking = {
            "name"      : name,
            "phone"     : phone,
            "day_week"  : day,
            "time"      : time,
            "teacher_id": teacher["id"],
        }

        save_booking("booking.json", booking)

        return render_template(
                "booking_done.html", name=name, phone=phone, day=day, time=time
        )
    else:
        return render_template(
                "booking.html", form=form, teacher=teacher, day=day, time=time
        )


app.run("127.0.0.1", 8000)
