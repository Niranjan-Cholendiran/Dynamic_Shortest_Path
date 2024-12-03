from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from shortest_path_computation import compute_shortest_path  # Import the shortest_path function

app = Flask(__name__)

# Load data from the Excel file
city_data = pd.read_excel('city_list.xlsx')

# Variables to hold selected cities and user choices
selected_cities_list = []
user_choices = {"source": None, "   ": None, "traffic_type": None}


@app.route("/", methods=["GET", "POST"])
def select_state_city():
    if request.method == "POST":
        selected_state = request.form.get("state")
        selected_cities = request.form.getlist("city")
        for city in selected_cities:
            selected_cities_list.append(f"{city}, {selected_state}")
        return redirect(url_for("select_route"))

    states = city_data['State'].unique()
    city_dict = city_data.groupby('State')['City'].apply(list).to_dict()
    return render_template("page1.html", states=states, city_data=city_dict)


@app.route("/select-route", methods=["GET", "POST"])
def select_route():
    if request.method == "POST":
        user_choices["source"] = request.form.get("source")
        user_choices["destination"] = request.form.get("destination")
        user_choices["traffic_type"] = request.form.get("traffic_type")
        return redirect(url_for("distance_computation"))

    return render_template("page2.html", cities=selected_cities_list)


@app.route("/distance-computation", methods=["GET"])
def distance_computation():
    # Call the `shortest_path` function with user input
    #result = compute_shortest_path(selected_cities_list, user_choices)
    # Calculate the shortest path
    shortest_time, shortest_path_result = compute_shortest_path(
        selected_cities_list, user_choices
    )
    return render_template(
        "distance_computation.html",
        source=user_choices["source"],
        destination=user_choices["destination"],
        path=shortest_path_result,
        time=int(shortest_time/60),
    )


if __name__ == "__main__":
    app.run(debug=True)
