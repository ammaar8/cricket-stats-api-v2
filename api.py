
import flask
from flask import request, jsonify
from flask import json
from flask.app import Flask
from flask.views import View
import mysql.connector
from mysql.connector import connect, cursor
from configparser import ConfigParser


# TODO
# [x]  /all            -> GET                
# [ ]  /resource/id    -> GET, PUT, DELETE
# [ ]  /resource       -> GET, POST

def check_conditions(item, conditions):
    """
    Function for checking conditions using a list of conditions. 
    """
    for condition in conditions:
        if item[condition[0]] != condition[1]:
            return False
    return True


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Cricket API</h1><p>Cricket League Tournament Application</p>"


class ResourceAll(View):

    def __init__(self, resource_type, table_name, field_names):
        self.resource_type = resource_type
        self.table_name = table_name
        self.field_names = field_names


    def api_response(self, data):
        for i in range(len(data)):
            for field, foreign in self.field_names:
                if foreign is not None:
                    data[i][field] = request.host_url + "api/v1/resources/" + foreign + "/" + str(data[i][field])
        
        response_data = dict()
        response_data["data"] = data
        response_data["links"] = {"self": request.host_url + "api/v1/resources/" + self.resource_type}
        response = flask.make_response(jsonify(response_data))
        response.content_type = "application/vnd.api+json"
        return response

    
    def dispatch_request(self):
        config = ConfigParser()
        config.read('database.ini')
        conn = mysql.connector.connect(
            host = config['database']['host'],
            database = config['database']['database'],
            user = config['database']['user'],
            password = config['database']['password'],
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * from `%s`;" % self.table_name)
        result = cursor.fetchall()
        return self.api_response(result)


app.add_url_rule(
    "/api/v1/resources/players/all",
    methods = ["GET"],
    view_func=ResourceAll.as_view(
        "players_all",
        "players",
        "player",
        [
            ("id", None),
            ("age", None),
            ("full_name", None),
            ("playing_role", None),
            ("team_id", "teams"),
            ("country_code", "countries")
        ]
        )
)

app.add_url_rule(
    "/api/v1/resources/matches/all",
    methods = ["GET"],
    view_func=ResourceAll.as_view(
        "matches_all",
        "matches",
        "match",
        [
            ("id", None),
            ("best_fielder", "players"),
            ("bowler_of_the_match", "players"),
            ("loser", "teams"),
            ("man_of_the_match", "players"),
            ("match_date", None),
            ("winner", "teams"),
        ]
        )
)

app.add_url_rule(
    "/api/v1/resources/teams/all",
    methods = ["GET"],
    view_func=ResourceAll.as_view(
        "teams_all",
        "teams",
        "team",
        [
            ("id", None),
            ("losses", None),
            ("matches_played", None),
            ("name", None),
            ("wins", None)
        ]
        )
)

app.add_url_rule(
    "/api/v1/resources/venues/all",
    methods = ["GET"],
    view_func=ResourceAll.as_view(
        "venues_all",
        "venues",
        "venue",
        [
            ("id", None),
            ("name", None),
            ("country_code", "countries")
        ]
        )
)

app.add_url_rule(
    "/api/v1/resources/countries/all",
    methods = ["GET"],
    view_func=ResourceAll.as_view(
        "countries_all",
        "countries",
        "country",
        [
            ("id", None),
            ("name", None),
        ]
        )
)

app.run()