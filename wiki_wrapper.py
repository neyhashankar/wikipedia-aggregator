# Neyha Shankar's Grow Therapy coding challenge, 04/09/2022
import json
import requests
import unittest

from calendar import monthrange
from datetime import datetime, timedelta


class WikiAgg:
    def __init__(self):
        pass

    # Assert YYYY/MM or YYYY/MM/DD format, assuming no hiccups in date values (ex., no 13th month!)
    def assert_time_format(self, time):
        split_date = time.split("/")
        for num in split_date:
            try:
                int(num)
            except:
                raise TypeError("Please only use numbers in date format")
        if (
            2 >= len(split_date) >= 3
            or len(split_date[0]) != 4
            or len(split_date[1]) != 2
        ):
            raise TypeError(
                "Please use a YYYY/MM format for yearly counts or YYYY/MM/DD for weekly counts"
            )
            return False
        elif len(split_date) == 3 and len(split_date[2]) != 2:
            raise TypeError("Please use YYYY/MM/DD for weekly counts")
            return False
        else:
            return True

    # Retrieve a list of the most viewed articles for a week or a month
    def most_viewed_articles(self, time):
        headers = {"User-Agent": "Mozilla/5.0"}
        self.assert_time_format(time)
        split_date = time.split("/")

        # Assume weekly- starts at Monday of input week, ends on Sunday
        if len(split_date) == 3:
            dt = datetime.strptime(time, "%Y/%m/%d")
            start = dt - timedelta(days=dt.weekday())
            date_list = [
                (start + timedelta(days=i)).strftime("%Y/%m/%d") for i in range(7)
            ]

        # Assume monthly
        elif len(split_date) == 2:
            month_start = datetime.strptime(time, "%Y/%m")
            num_days_in_month = monthrange(int(split_date[0]), int(split_date[1]))[1]
            date_list = [
                (month_start + timedelta(days=i)).strftime("%Y/%m/%d")
                for i in range(num_days_in_month)
            ]
        else:
            raise TypeError(
                "Please use a YYYY/MM format for yearly counts or YYYY/MM/DD for weekly counts"
            )
            return

        agg_pageviews_dict = {}
        try:
            for date in date_list:
                url = (
                    "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/%s"
                    % date
                )
                response = requests.get(url, headers=headers)
                pageviews_dict = json.loads(response.text)
                for article in pageviews_dict["items"][0]["articles"]:
                    if article["article"] in agg_pageviews_dict:
                        agg_pageviews_dict[article["article"]]["views"] += article[
                            "views"
                        ]
                        if (
                            article["views"]
                            > agg_pageviews_dict[article["article"]]["highest_views"][0]
                        ):
                            agg_pageviews_dict[article["article"]]["highest_views"] = (
                                article["views"],
                                date,
                            )
                    else:
                        agg_pageviews_dict[article["article"]] = {}
                        agg_pageviews_dict[article["article"]]["views"] = article[
                            "views"
                        ]
                        agg_pageviews_dict[article["article"]]["highest_views"] = (
                            article["views"],
                            date,
                        )
        except:
            raise RuntimeError("Something went wrong in pulling counts")

        return agg_pageviews_dict

    # For any given article, get the view count of that specific article
    def article_view_count(self, date, article):
        return self.most_viewed_articles(date)[article]["views"]

    # Retrieve the day of the month where an article got the most page views
    def article_most_viewed_day(self, date, article):
        return self.most_viewed_articles(date)[article]["highest_views"][1]


class test_WikiAgg(unittest.TestCase):
    def test(self):
        test = WikiAgg()
        # Time format tests
        self.assertRaises(TypeError, test.assert_time_format, "201/10")
        self.assertRaises(TypeError, test.assert_time_format, "201510")
        self.assertRaises(TypeError, test.assert_time_format, "abcd/12")
        self.assertRaises(TypeError, test.assert_time_format, "")
        self.assertEqual(test.assert_time_format("2015/10"), True)

        # Most viewed article tests
        self.assertIn(
            "List_of_Canadian_federal_general_elections",
            test.most_viewed_articles("2015/10"),
        )
        self.assertEqual(test.article_view_count("2021/12/31", "New_Year"), 61224)
        self.assertEqual(
            test.article_most_viewed_day("2020/02", "Groundhog_Day"), "2020/02/02"
        )
        self.assertEqual(
            test.article_most_viewed_day("2019/02", "Groundhog_Day"), "2019/02/02"
        )
        self.assertRaises(TypeError, test.article_view_count, "201020", "Gordon_Ramsay")
        self.assertRaises(
            TypeError, test.article_most_viewed_day, "201020/", "Gordon_Ramsay"
        )
        self.assertRaises(RuntimeError, test.article_view_count, "2008/01/01", "iPhone")

        print("Tests passed! :)")


test = test_WikiAgg()
test.test()
