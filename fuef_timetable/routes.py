from flask import current_app as app
from flask import render_template

from fuef_timetable.data import Data


@app.route('/')
def home():
    data = Data("ablauf-2022.xlsx", today=True, debug=False)

    return render_template(
        'main.html',
        entries=data.entries,
        title="FüF Timetable",
        description="The great interactive timetable"
    )


@app.route('/bar')
def bar():
    data = Data("ablauf-2022.xlsx", today=True, debug=False, bar=True)

    return render_template(
        'bar.html',
        entries=data.entries,
        title="FüF Highlights Bar",
        description="The great interactive timetable even better"
    )
