import datetime
from datetime import datetime, date
import pandas as pd
from .models import GarminData
from pandas import to_datetime

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter, ColumnDataSource, HoverTool


def create_date_range(
    start_date: datetime.date,
    end_date: datetime.date,
) -> list[datetime.date]:
    """
    function to create a list of dates in between
    a start and end date
    """

    if start_date > end_date:
        return []
    else:
        # https://www.geeksforgeeks.org/python-iterating-through-a-range-of-dates/
        time_diff = pd.date_range(start=start_date, end=end_date)
        return [date.date() for date in time_diff]


def init_api(email, password):
    api = Garmin(email, password)
    api.login()
    return api


def garmin_api_call(
    garmin_username: str,
    garmin_password: str,
    start_date: datetime.date,
    end_date: datetime.date,
) -> list[str]:
    """calls the data from the garmin api"""
    print("Entering garmin_api_call")
    print(f"  user {garmin_username}  - Type : {type(garmin_username)} ")
    print(f"  start_date {start_date} - Type : {type(start_date)}")
    print(f"  end_date {end_date} - Type : {type(end_date)} ")

    try:
        # api = init_api(garmin_username, garmin_password)
        api = Garmin(garmin_username, garmin_password)
        api.login()
        print(api)
        print(start_date.isoformat())
        print(end_date.isoformat())
        # get the steps from the api
        output_steps = (
            api.get_daily_steps(start_date.isoformat(), end_date.isoformat()),
        )
        print(output_steps)
        # output_steps = output_steps[0]
        # get the body weight from the api
        output_weight_kg = (
            api.get_body_composition(
                start_date.isoformat(), end_date.isoformat()
            ),
        )
        print(output_weight_kg)
        # output_weight_kg = output_weight_kg[0]
        # example output
        #  ([{'calendarDate': '2023-08-31', 'totalSteps': 1194, 'totalDistance': 945, 'stepGoal': 7000}, {'calendarDate': '2023-09-01', 'totalSteps': 261, 'totalDistance': 207, 'stepGoal': 7000}],)
        return output_steps, output_weight_kg
    except (
        GarminConnectConnectionError,
        GarminConnectAuthenticationError,
        GarminConnectTooManyRequestsError,
    ) as err:
        print(f"Error occurred during Garmin Connect communication: {err}")
        return [], []

    return [], []


def convert_date_str_to_datetime(date_str):
    """
    convert string to datetime object
    """
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def convert_api_data_to_datetime(garmin_api_data):
    """
    converts the output of the api call into datetime objects
    reason for this function is to make the logic behind the view testable
    """
    return datetime.strptime(
        garmin_api_data["calendarDate"], "%Y-%m-%d"
    ).date()


def convert_api_data_to_steps(garmin_api_data):
    """
    converts the output of the api call into step count
    """
    return int(garmin_api_data["totalSteps"])


def extract_weight(garmin_weight_data, target_date) -> int:
    """
    extracts weight measurment for a specific data
    in a json fetched from garmin api
    """
    date_weight_list = garmin_weight_data["dateWeightList"]

    for weight_entry in date_weight_list:
        current_date = convert_api_data_to_datetime(weight_entry)
        if current_date == target_date:
            return int(weight_entry["weight"] / 1000)

    return 0


def get_garmin_mock_data_for_testing():
    """
    return json strings in the same format
    as obtained from API (to reduce actual API calls avoiding
    a block from Garmin for doing too many API calls )
    """
    garmin_step_data = (
        [
            {
                "calendarDate": "2023-08-31",
                "totalSteps": 1194,
                "totalDistance": 945,
                "stepGoal": 7000,
            },
            {
                "calendarDate": "2023-09-01",
                "totalSteps": 261,
                "totalDistance": 207,
                "stepGoal": 7000,
            },
        ],
    )
    garmin_weight_data = (
        {
            "startDate": "2023-08-25",
            "endDate": "2023-09-01",
            "dateWeightList": [
                {
                    "samplePk": 1693438985313,
                    "date": 1693442578001,
                    "calendarDate": "2023-08-31",
                    "weight": 77199.0,
                    "bmi": None,
                    "bodyFat": None,
                    "bodyWater": None,
                    "boneMass": None,
                    "muscleMass": None,
                    "physiqueRating": None,
                    "visceralFat": None,
                    "metabolicAge": None,
                    "sourceType": "MANUAL",
                    "timestampGMT": 1693438978001,
                    "weightDelta": None,
                },
                {
                    "samplePk": 1693338330726,
                    "date": 1693341923002,
                    "calendarDate": "2023-08-29",
                    "weight": 78500.0,
                    "bmi": None,
                    "bodyFat": None,
                    "bodyWater": None,
                    "boneMass": None,
                    "muscleMass": None,
                    "physiqueRating": None,
                    "visceralFat": None,
                    "metabolicAge": None,
                    "sourceType": "MANUAL",
                    "timestampGMT": 1693338323002,
                    "weightDelta": None,
                },
                {
                    "samplePk": 1693254851757,
                    "date": 1693258445002,
                    "calendarDate": "2023-08-28",
                    "weight": 77400.0,
                    "bmi": None,
                    "bodyFat": None,
                    "bodyWater": None,
                    "boneMass": None,
                    "muscleMass": None,
                    "physiqueRating": None,
                    "visceralFat": None,
                    "metabolicAge": None,
                    "sourceType": "MANUAL",
                    "timestampGMT": 1693254845002,
                    "weightDelta": None,
                },
                {
                    "samplePk": 1693152069834,
                    "date": 1693155664001,
                    "calendarDate": "2023-08-27",
                    "weight": 77699.0,
                    "bmi": None,
                    "bodyFat": None,
                    "bodyWater": None,
                    "boneMass": None,
                    "muscleMass": None,
                    "physiqueRating": None,
                    "visceralFat": None,
                    "metabolicAge": None,
                    "sourceType": "MANUAL",
                    "timestampGMT": 1693152064001,
                    "weightDelta": None,
                },
                {
                    "samplePk": 1693036193597,
                    "date": 1693039786007,
                    "calendarDate": "2023-08-26",
                    "weight": 77599.0,
                    "bmi": None,
                    "bodyFat": None,
                    "bodyWater": None,
                    "boneMass": None,
                    "muscleMass": None,
                    "physiqueRating": None,
                    "visceralFat": None,
                    "metabolicAge": None,
                    "sourceType": "MANUAL",
                    "timestampGMT": 1693036186007,
                    "weightDelta": None,
                },
            ],
            "totalAverage": {
                "from": 1692921600000,
                "until": 1693612799999,
                "weight": 77679.4,
                "bmi": None,
                "bodyFat": None,
                "bodyWater": None,
                "boneMass": None,
                "muscleMass": None,
                "physiqueRating": None,
                "visceralFat": None,
                "metabolicAge": None,
            },
        },
    )
    return garmin_step_data, garmin_weight_data


def extract_user_data(
    garmin_data: list[GarminData],
) -> tuple[list[datetime.date], list[int]]:
    """extract days and steps as input for bokeh plot"""
    days = [to_datetime(db_record.date) for db_record in garmin_data]
    steps = [db_record.steps for db_record in garmin_data]
    weights = [db_record.weight_kg for db_record in garmin_data]

    return days, steps, weights


def create_bokeh_plot(data: pd.DataFrame):
    """
    create and style a bokeh plot of the recent 30 days
    of activity which will be passed into the template
    """
    source = ColumnDataSource(data=data)

    # plot also the step goal
    steps_goal = [7000 for day in data["Date"]]
    source_steps_goal = ColumnDataSource(
        data=dict(days=data["Date"], steps=steps_goal)
    )

    hover = HoverTool(tooltips=[("Date", "@DateString"), ("Steps", "@Steps")])

    fig = figure(
        title="Steps within last 30 days",
        tools="reset",
        toolbar_location=None,
        x_axis_type="datetime",
        background_fill_color=None,
        border_fill_color=None,
        sizing_mode="scale_both",
    )
    # fig.line(source=source, x="days", y="steps", line_width=2)
    # ensure correct scaling - the width unit needs to be scaled to
    # the displayed time range (it's a relativ value - see )
    # https://stackoverflow.com/questions/51642602/bokeh-bar-chart-not-showing-width-properly
    msec_per_sec = 1000
    sec_per_min = 60
    min_per_hour = 60
    hour_per_day = 24
    width_scale_fac = msec_per_sec * sec_per_min * min_per_hour * hour_per_day
    fig.vbar(
        source=source,
        x="Date",
        top="Steps",
        width=0.5 * width_scale_fac,
        fill_alpha=0.8,
    )
    fig.title.align = "center"
    fig.add_tools(hover)
    fig.xaxis.axis_label_text_font_size = "40pt"
    fig.yaxis.axis_label_text_font_size = "40pt"
    fig.xaxis.major_label_text_font_style = "bold"
    fig.yaxis.major_label_text_font_style = "bold"
    fig.xaxis[0].formatter = DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )
    fig.xaxis.major_label_orientation = 3.141 / 4
    fig.line(
        source=source_steps_goal,
        x="days",
        y="steps",
        line_width=2,
        line_color="orange",
        line_dash="dashed",
        line_alpha=0.8,
    )

    script, div = components(fig)

    return script, div


def calculate_bmi_change(
    days: list[datetime.date], weights: list[int], height_cm: int
):
    """
    helper function to calculate the average BMI and the BMI change
    over the recent n days
    returns : average bmi, linear trend of the BMI over recent n days
    """
    print("-->calculating BMI change now")
    return 42, 0
