import os
import requests
import json
import pickle
import math
from collections import defaultdict

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

def get_user_submitted_data(status="NR"):
    url = "http://localhost:8000/user_submission"
    try:
        result = requests.get(url)
        if result.status_code == 200:
            result = json.loads(result.text)
            d1 = pd.DataFrame(result, columns=["label", "face_encoding"])
            d2 = pd.DataFrame(
                d1.pop("face_encoding").values.tolist(), index=d1.index
            ).rename(columns=lambda x: "fe_{}".format(x + 1))
            df = d1.join(d2)
            return df
    except Exception as e:
        return None


def match():
    model_name = "classifier.pkl"
    matched_images = defaultdict(list)
    user_submissions_df = get_user_submitted_data()

    if user_submissions_df is None:
        return {"status": False, "message": "Couldn't connect to database"}

    if len(user_submissions_df) == 0:
        return {"status": False, "message": "No submissions found"}

    if os.path.isfile(model_name):
        with open(model_name, "rb") as f:
            (le, clf) = pickle.load(f)
    else:
        return {"status": False, "message": "Please refresh model"}

    for row in user_submissions_df.iterrows():
        label = row[1][0]
        face_encoding = row[1][1:]
        closest_distances = clf.kneighbors([face_encoding])[0][0]
        closest_distance = np.argmin(closest_distances)
        closest_distance = closest_distances[closest_distance]
        print("distances:")
        print(closest_distance)
        print("img label:")
        print(label)
        if closest_distance <= 0.6:
            print("Closest distance matched:")
            print(closest_distance)
            linval = face_distance_to_conf(closest_distance);
            print("Acuraccy :")
            print(linval)
            predicted_label = clf.predict([face_encoding])
            inversed_label = le.inverse_transform([predicted_label])[0]
            matched_images[inversed_label].append(label)

    return {"status": True, "result": matched_images}

def face_distance_to_conf(face_distance, face_match_threshold=0.6):
    if face_distance > face_match_threshold:
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)
        return linear_val
    else:
        range = face_match_threshold
        linear_val = 1.0 - (face_distance / (range * 2.0))
        return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))


if __name__ == "__main__":
    result = match()
    print(result)
