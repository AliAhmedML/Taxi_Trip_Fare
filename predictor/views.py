from django.shortcuts import render
import pickle
import numpy as np
import pandas as pd
import cudf
import os
from .forms import FarePredictionForm

BASE_DIR = os.path.dirname(__file__)
model = pickle.load(open(os.path.join(BASE_DIR, "model", "Taxi.pkl"), "rb"))
power_transformer = pickle.load(
    open(os.path.join(BASE_DIR, "model", "Power_Transformer.pkl"), "rb")
)
scaler = pickle.load(open(os.path.join(BASE_DIR, "model", "Scaler.pkl"), "rb"))
PCA = pickle.load(open(os.path.join(BASE_DIR, "model", "PCA.pkl"), "rb"))


def home(request):
    if request.method == "POST":
        form = FarePredictionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            extra = {
                "user_id": data.get("user_id", ""),
                "user_name": data.get("user_name", ""),
                "driver_name": data.get("driver_name", ""),
                "key": data.get("key", ""),
                "pickup_datetime": data.get("pickup_datetime", ""),
                "pickup_latitude": data.get("pickup_latitude", ""),
                "pickup_longitude": data.get("pickup_longitude", ""),
                "dropoff_latitude": data.get("dropoff_latitude", ""),
                "dropoff_longitude": data.get("dropoff_longitude", ""),
                "jfk_dist": data.get("jfk_dist", ""),
                "ewr_dist": data.get("ewr_dist", ""),
                "lga_dist": data.get("lga_dist", ""),
            }
            features = [
                data["car_condition"],
                data["weather"],
                data["traffic_condition"],
                data["passenger_count"],
                data["hour"],
                data["day"],
                data["month"],
                data["weekday"],
                data["year"],
                data["sol_dist"],
                data["nyc_dist"],
                data["distance"],
                data["bearing"],
            ]
            feature_names = [
                "Car Condition",
                "Weather",
                "Traffic Condition",
                "passenger_count",
                "hour",
                "day",
                "month",
                "weekday",
                "year",
                "sol_dist",
                "nyc_dist",
                "distance",
                "bearing",
            ]
            features_df = pd.DataFrame(
                [features], columns=feature_names, dtype=np.float32
            )
            columns_to_transform = [
                "passenger_count",
                "sol_dist",
                "nyc_dist",
                "distance",
            ]
            features_df[columns_to_transform] = power_transformer.transform(
                features_df[columns_to_transform]
            ).astype(np.float32)
            features_df = scaler.transform(features_df)
            pca_components = PCA.transform(features_df[:, [9, 10]])
            features_df = np.hstack([features_df, pca_components])
            features_df = np.delete(features_df, [9, 10], axis=1)
            features_df = cudf.DataFrame(features_df).astype("float32")

            prediction = model.predict(features_df)[0]
            return render(request, "predictor/result.html", {"prediction": prediction})
    else:
        form = FarePredictionForm()
    return render(request, "predictor/home.html", {"form": form})
