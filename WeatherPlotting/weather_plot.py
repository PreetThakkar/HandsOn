import pandas
from requests import get
import plotly.express as px
from pandas import DataFrame


def get_data(type: str) -> DataFrame:
    url = {"weather": 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getalllastmeasurement',
           "station": "https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getallstations"}
    data = get(url[type]).json()
    df = DataFrame(data["items"])
    return df


def plot_map():
    station_data = get_data("station")
    weather_data = get_data("weather")
    # dropping columns that are not needed
    weather_data.drop(weather_data.columns[[1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14]], axis=1, inplace=True)
    # Merging the data frames on common column
    df = pandas.merge(left=station_data, right=weather_data,
                      how="inner", on="weather_stn_id")
    # Choose which data to display on hover
    hover_data = {'weather_stn_id': False, 'weather_stn_name': True,
                  'weather_stn_lat': False, 'weather_stn_long': False, 'ambient_temp': True}
    fig = px.scatter_geo(df, lat="weather_stn_lat", lon="weather_stn_long",
                         hover_name="weather_stn_name", projection="natural earth", 
                         hover_data=hover_data, color="ambient_temp", range_color=[0, 50])

    fig.show()


if __name__ == "__main__":
    plot_map()
