from django import forms

CAR_CONDITION_CHOICES = [(0, "Bad"), (1, "Good"), (2, "Very Good"), (3, "Excellent")]

WEATHER_CHOICES = [
    (0, "Stormy"),
    (1, "Rainy"),
    (2, "Windy"),
    (3, "Cloudy"),
    (4, "Sunny"),
]

TRAFFIC_CONDITION_CHOICES = [
    (0, "Congested Traffic"),
    (1, "Dense Traffic"),
    (2, "Flow Traffic"),
]


class FarePredictionForm(forms.Form):
    passenger_count = forms.IntegerField(label="Passenger Count", min_value=1)
    hour = forms.IntegerField(label="Hour", min_value=0, max_value=23)
    day = forms.IntegerField(label="Day", min_value=1, max_value=31)
    month = forms.IntegerField(label="Month", min_value=1, max_value=12)
    weekday = forms.IntegerField(label="Weekday (0=Mon)", min_value=0, max_value=6)
    year = forms.IntegerField(label="Year", min_value=2000, max_value=2100)
    sol_dist = forms.FloatField(label="Solar Distance")
    nyc_dist = forms.FloatField(label="NYC Distance")
    distance = forms.FloatField(label="Trip Distance")
    bearing = forms.FloatField(label="Bearing")
    car_condition = forms.ChoiceField(
        label="Car Condition", choices=CAR_CONDITION_CHOICES, required=False
    )
    weather = forms.ChoiceField(
        label="Weather", choices=WEATHER_CHOICES, required=False
    )
    traffic_condition = forms.ChoiceField(
        label="Traffic Condition", choices=TRAFFIC_CONDITION_CHOICES, required=False
    )
    # Extra unused inputs
    user_id = forms.CharField(label="User ID", required=False)
    user_name = forms.CharField(label="User Name", required=False)
    driver_name = forms.CharField(label="Driver Name", required=False)
    key = forms.CharField(label="Key", required=False)
    pickup_datetime = forms.DateTimeField(
        input_formats=["%Y-%m-%d %H:%M"],
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )
    pickup_longitude = forms.FloatField(label="Pickup Longitude", required=False)
    pickup_latitude = forms.FloatField(label="Pickup Latitude", required=False)
    dropoff_longitude = forms.FloatField(label="Dropoff Longitude", required=False)
    dropoff_latitude = forms.FloatField(label="Dropoff Latitude", required=False)
    jfk_dist = forms.FloatField(label="JFK Distance", required=False)
    ewr_dist = forms.FloatField(label="EWR Distance", required=False)
    lga_dist = forms.FloatField(label="LGA Distance", required=False)
