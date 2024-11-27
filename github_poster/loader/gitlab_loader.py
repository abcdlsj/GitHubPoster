import time

import requests
from bs4 import BeautifulSoup
from pendulum import interval, parse
import json
from datetime import datetime

from github_poster.html_parser import GitLabParser
from github_poster.loader.base_loader import BaseLoader, LoadError
from github_poster.loader.config import GITLAB_LATEST_URL, GITLAB_ONE_DAY_URL


class GitLabLoader(BaseLoader):
    track_color = "#ACD5F2"
    unit = "cons"

    def __init__(self, from_year, to_year, _type, **kwargs):
        super().__init__(from_year, to_year, _type)
        self.user_name = kwargs.get("gitlab_user_name", "")
        self.gitlab_base_url = kwargs.get("base_url") or "https://gitlab.com"
        self.gitlab_session = kwargs.get("session")
        self.json_file = kwargs.get("json_file", "gitlab_activities_20241127_105623.json")
        self.left_dates = []

    @classmethod
    def add_loader_arguments(cls, parser, optional):
        parser.add_argument(
            "--gitlab_user_name",
            dest="gitlab_user_name",
            type=str,
            required=optional,
            help="",
        )

        parser.add_argument(
            "--base_url",
            dest="base_url",
            type=str,
            default="https://gitlab.com",
            help="specify the base url of your self-managed gitlab",
        )
        parser.add_argument(
            "--session",
            dest="session",
            type=str,
            default="",
            help="use gitlab_session from Cookies "
            "if your gitlab instance needs to sign in",
        )

    def _make_left_dates(self, last_date):
        dates = list(interval(parse(f"{self.from_year}-01-01"), parse(last_date)))
        self.left_dates = [i.to_date_string() for i in dates]

    def _set_cookies(self):
        if self.gitlab_session:
            return {"_gitlab_session": self.gitlab_session}

        return {}

    def load_activities_from_json(self):
        """Load activities from a JSON file instead of GitLab API."""
        try:
            with open(self.json_file, 'r') as f:
                data = json.load(f)
            
            activities = data.get('activities', [])
            date_dict = {}
            
            for activity in activities:
                activity_time = activity.get('time', '')
                if activity_time:
                    date = datetime.fromisoformat(activity_time.replace('Z', '+00:00')).date().isoformat()
                    date_dict[date] = date_dict.get(date, 0) + 1
            
            self.number_by_date_dict = date_dict
        except Exception as e:
            raise LoadError(f"Cannot load activities from JSON file: {str(e)}")

    def make_latest_date_dict(self):
        """Load activities either from JSON file or GitLab API."""
        if self.json_file:
            self.load_activities_from_json()
            return
        try:
            r = requests.get(
                GITLAB_LATEST_URL.format(
                    gitlab_base_url=self.gitlab_base_url, user_name=self.user_name
                ),
                cookies=self._set_cookies(),
            )
            date_dict = r.json()
            min_date = min(date_dict.keys())
            self.number_by_date_dict = date_dict
            if self.from_year > int(min_date[:4]):
                return
            self._make_left_dates(min_date)
        except Exception as e:
            raise LoadError(f"Can not get gitlab data error: {str(e)}")

    def make_left_data_dict(self):
        for d in self.left_dates:
            try:
                r = requests.get(
                    GITLAB_ONE_DAY_URL.format(
                        gitlab_base_url=self.gitlab_base_url,
                        user_name=self.user_name,
                        date_str=d,
                    ),
                    cookies=self._set_cookies(),
                )
                # spider rule
                time.sleep(0.1)
                activities = self.count_activities_from_html(r.text)
                print(f"{d}: {activities}")
                self.number_by_date_dict[d] = activities
            except Exception:
                # what fucking things happened just pass
                pass

    def count_activities_from_html(self, html_content):
        """Count the number of activities from GitLab HTML response."""
        soup = BeautifulSoup(html_content, 'html.parser')
        activities = soup.select('ul.bordered-list > li')
        return len(activities)

    def make_track_dict(self):
        self.make_latest_date_dict()
        self.make_left_data_dict()
        for _, v in self.number_by_date_dict.items():
            self.number_list.append(v)

    def get_all_track_data(self):
        self.make_track_dict()
        self.make_special_number()
        return self.number_by_date_dict, self.year_list
