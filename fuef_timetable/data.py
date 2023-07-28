from openpyxl import load_workbook

import datetime
from typing import List
from nocodb.nocodb import NocoDBProject, APIToken, JWTAuthToken
from nocodb.filters.raw_filter import RawFilter
from nocodb.infra.requests_client import NocoDBRequestsClient
from dotenv import dotenv_values

class Data:
    """Collection of entries."""

    def __init__(
        self,
        path: str,
        today: bool = False,
        debug: bool = False,
        bar: bool = False,
    ):

        env = dotenv_values('.env')

        # Usage with API Token
        client = NocoDBRequestsClient(
            # Your API Token retrieved from NocoDB conf
            APIToken(env["API-TOKEN"]),
            # Your nocodb root path
            env["URL"]
        )

        project = NocoDBProject(
            env["ORGANISATION"],
            env["PROJECT"]
        )

        table_name = env["TABLE"]

        table_rows = client.table_row_list(project, table_name, RawFilter('(when,eq,exactDate,03-08-2023)'))

        print(table_rows)

        wb = load_workbook(filename=path)
        sheet = wb["Acts"]

        self.entries: List[Entry] = []
        if not debug:
            today_date = datetime.date.today()
        else:
            today_date = datetime.date(year=2022, month=7, day=28)
        for i in range(3, sheet.max_row+1):
            entry = Entry(sheet, i, debug)
            if not entry.is_valid:
                continue
            if today and entry.when.date() != today_date:
                continue
            self.entries.append(entry)
        if bar:
            self.entries = self.bar_stuff(debug)

    def bar_stuff(self, debug: bool):
        """Mess with the best, die like the rest."""
        now = datetime.datetime.now()
        tmp = []
        for entry in self.entries:
            if entry.when >= now or entry.is_now_fn(debug):
                print(1)
                tmp.append(entry)
        return tmp[:2]


class Entry:
    """A single entry."""

    def __init__(self, sheet, row_index, debug):
        self.when = sheet.cell(row=row_index, column=1).value
        if not isinstance(self.when, datetime.datetime):
            self.is_valid = False
            return
        self.artist = self.get_value(sheet, row_index, 2)
        self.title = self.get_value(sheet, row_index, 3)
        self.place = self.get_value(sheet, row_index, 5)
        self.duration = self.get_value(sheet, row_index, 6)
        self.genre = self.get_value(sheet, row_index, 7)
        self.is_now = self.is_now_fn(debug)

        # print(ends)
        self.is_valid = True

    def is_now_fn(self, debug: bool) -> bool:
        """
        Determines wether an event is currently happening.
        Inkl. 10 Minutes before.
        """
        if self.duration != "–":
            duration = self.duration
        else:
            duration = 15
        if not debug:
            now = datetime.datetime.now()
        else:
            now = datetime.datetime(
                year=2022,
                month=7,
                day=28,
                hour=19,
                minute=25
            )
        starts = self.when - datetime.timedelta(minutes=10)
        ends = self.when + datetime.timedelta(minutes=duration)
        return now >= starts and now <= ends

    @staticmethod
    def get_value(sheet, row, column):
        """
        Gets the value from the sheet and replaces None with a dash.
        """
        value = sheet.cell(row=row, column=column).value
        if value is None:
            return "–"
        return value
