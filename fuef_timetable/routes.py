from flask import current_app as app
from flask import render_template


@app.route('/')
def home():
    return render_template(
        'main.html',
        title="FüF Timetable",
        description="The great interactive timetable"
    )
