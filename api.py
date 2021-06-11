
import flask
from flask import request, jsonify
from flask import json
from flask.app import Flask
from flask.views import MethodView
import mysql.connector
from mysql.connector import connect, cursor
from configparser import ConfigParser

# TODO 
# [ ] Add Doxygen Comments
# [ ] Modularize File

def check_conditions(item, conditions):
    """
    Function for checking conditions using a list of conditions. 
    """
    for condition in conditions:
        if item[condition[0]] != condition[1]:
            return False
    return True


def connect_db():
    config = ConfigParser()
    config.read('database.ini')
    conn = mysql.connector.connect(
        host = config['database']['host'],
        database = config['database']['database'],
        user = config['database']['user'],
        password = config['database']['password'],
    )
    return conn


app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Cricket API</h1><p>Cricket League Tournament Application</p>"


class TeamAPI(MethodView):

    field_names = [
            ("id", None),
            ("losses", None),
            ("matches_played", None),
            ("name", None),
            ("wins", None)
        ]
    
    def api_response(self, data):
        for i in range(len(data)):
            for field, foreign in self.field_names:
                if foreign is not None:
                    data[i][field] = request.host_url + "api/v1/resources/" + foreign + "/" + str(data[i][field])
        
        response_data = dict()
        response_data["data"] = data
        response_data["links"] = {"self": request.host_url + "api/v1/resources/teams"}
        response = flask.make_response(jsonify(response_data))
        response.content_type = "application/vnd.api+json"
        return response

    def get(self, team_id):

        if team_id is None:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('select * from team;')
            result = cursor.fetchall()
            return self.api_response(result)
        else:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('select * from team where id = %s;', (team_id,))
            result = cursor.fetchall()
            return self.api_response(result)

    def post(self):
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()
        name = data["name"]
        matches_played = data["matches_played"]
        wins = data["wins"]
        losses = data["losses"]

        cursor.execute(
            "insert into team (name, matches_played, wins, losses)"
            "values (%s, %s, %s, %s);",
            (name, matches_played, wins, losses)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)

    def delete(self):
        pass

    def put(self, team_id):
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()
        for field, value in data.items():
            cursor.execute(
                "UPDATE team SET {} = %s WHERE id = %s;".format(field),
                (value, team_id)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)


class PlayerAPI(MethodView):

    field_names = [
            ("id", None),
            ("age", None),
            ("full_name", None),
            ("playing_role", None),
            ("team_id", "teams"),
            ("country_code", "countries")
        ]
    
    def api_response(self, data):
        for i in range(len(data)):
            for field, foreign in self.field_names:
                if foreign is not None:
                    data[i][field] = request.host_url + "api/v1/resources/" + foreign + "/" + str(data[i][field])
        
        response_data = dict()
        response_data["data"] = data
        response_data["links"] = {"self": request.host_url + "api/v1/resources/players"}
        response = flask.make_response(jsonify(response_data))
        response.content_type = "application/vnd.api+json"
        return response

    def get(self, player_id):

        if player_id is None:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('select * from player;')
            result = cursor.fetchall()
            return self.api_response(result)
        else:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('select * from player where id = %s;', (player_id,))
            result = cursor.fetchall()
            return self.api_response(result)

    def post(self):
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()
        full_name = data["full_name"]
        age = data["age"]
        playing_role = data["playing_role"]
        team_id = data["team_id"]
        country_code = data["country_code"]
        cursor.execute(
            "insert into player (full_name, age, playing_role, team_id, country_code)"
            "values (%s, %s, %s, %s, %s);",
            (full_name, age, playing_role, team_id, country_code)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)

    def delete(self):
        pass

    def put(self, player_id):
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()
        for field, value in data.items():
            cursor.execute(
                "UPDATE player SET {} = %s WHERE id = %s;".format(field),
                (value, player_id)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)


class MatchAPI(MethodView):

    field_names = [
            ("id", None),
            ("match_date", None),
            ("winner", "teams"),
            ("loser", "teams"),
            ("man_of_the_match", "players"),
            ("bowler_of_the_match", "players"),
            ("best_fielder", "players")
        ]
    
    def api_response(self, data):
        for i in range(len(data)):
            for field, foreign in self.field_names:
                if foreign is not None:
                    data[i][field] = request.host_url + "api/v1/resources/" + foreign + "/" + str(data[i][field])
        
        response_data = dict()
        response_data["data"] = data
        response_data["links"] = {"self": request.host_url + "api/v1/resources/matches"}
        response = flask.make_response(jsonify(response_data))
        response.content_type = "application/vnd.api+json"
        return response

    def get(self, match_id):

        if match_id is None:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('select * from `match`;')
            result = cursor.fetchall()
            return self.api_response(result)
        else:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('select * from `match` where id = %s;', (match_id,))
            result = cursor.fetchall()
            return self.api_response(result)

    def post(self):
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()

        match_date = data["match_date"]
        winner = data["winner"]
        loser = data["loser"]
        mom = data["man_of_the_match"]
        bom = data["bowler_of_the_match"]
        bf = data["best_fielder"]

        cursor.execute(
            "insert into `match`"
            "(match_date, winner, loser, man_of_the_match, bowler_of_the_match, best_fielder)"
            "values (%s, %s, %s, %s, %s, %s);",
            (match_date, winner, loser, mom, bom, bf)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)

    def delete(self):
        pass

    def put(self, match_id):
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()
        for field, value in data.items():
            cursor.execute(
                "UPDATE `match` SET {} = %s WHERE id = %s;".format(field),
                (value, match_id)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)


class VenueAPI(MethodView):

    field_names = [
            ("id", None),
            ("name", None),
            ("country_code", "countries")
        ]
    
    def api_response(self, data):
        for i in range(len(data)):
            for field, foreign in self.field_names:
                if foreign is not None:
                    data[i][field] = request.host_url + "api/v1/resources/" + foreign + "/" + str(data[i][field])
        
        response_data = dict()
        response_data["data"] = data
        response_data["links"] = {"self": request.host_url + "api/v1/resources/venues"}
        response = flask.make_response(jsonify(response_data))
        response.content_type = "application/vnd.api+json"
        return response

    def get(self, venue_id):

        if venue_id is None:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('select * from venue;')
            result = cursor.fetchall()
            return self.api_response(result)
        else:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('select * from venue where id = %s;', (venue_id,))
            result = cursor.fetchall()
            return self.api_response(result)

    def post(self):
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()
        
        name = data["name"]
        country_code = data["country_code"]

        cursor.execute(
            "insert into venue (name, country_code)"
            "values (%s, %s);",
            (name, country_code)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)

    def delete(self):
        pass

    def put(self, venue_id):
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()
        for field, value in data.items():
            cursor.execute(
                "UPDATE venue SET {} = %s WHERE id = %s;".format(field),
                (value, venue_id)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)


class CountryAPI(MethodView):

    field_names = [
            ("id", None),
            ("name", None),
        ]

    def api_response(self, data):
        for i in range(len(data)):
            for field, foreign in self.field_names:
                if foreign is not None:
                    data[i][field] = request.host_url + "api/v1/resources/" + foreign + "/" + str(data[i][field])
        
        response_data = dict()
        response_data["data"] = data
        response_data["links"] = {"self": request.host_url + "api/v1/resources/countries"}
        response = flask.make_response(jsonify(response_data))
        response.content_type = "application/vnd.api+json"
        return response

    def get(self, country_id):

        if country_id is None:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('select * from country;')
            result = cursor.fetchall()
            return self.api_response(result)
        else:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('select * from country where id = %s;', (country_id,))
            result = cursor.fetchall()
            return self.api_response(result)

    def post(self):
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()
        
        name = data["name"]
        id = data["id"]

        cursor.execute(
            "insert into country (id, name)"
            "values (%s, %s);",
            (id, name)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)

    def delete(self):
        pass

    def put(self, country_id):
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()
        for field, value in data.items():
            cursor.execute(
                "UPDATE country SET {} = %s WHERE id = %s;".format(field),
                (value, country_id)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True)


## Player

player_view = PlayerAPI.as_view('player_api')

app.add_url_rule(
    '/api/v1/resources/players/',
    defaults={'player_id': None},
    view_func=player_view,
    methods=['GET',]
    )

app.add_url_rule(
    '/api/v1/resources/players/',
    view_func=player_view,
    methods=['POST',]
    )

app.add_url_rule(
    '/api/v1/resources/players/<int:player_id>',
    view_func=player_view,
    methods=['GET', 'PUT',]
    )

## End Player


## Team

team_view = TeamAPI.as_view('team_api')

app.add_url_rule(
    '/api/v1/resources/teams/',
    defaults={'team_id': None},
    view_func=team_view,
    methods=['GET',]
    )

app.add_url_rule(
    '/api/v1/resources/teams/',
    view_func=team_view,
    methods=['POST',]
    )

app.add_url_rule(
    '/api/v1/resources/teams/<int:team_id>',
    view_func=team_view,
    methods=['GET', 'PUT',]
    )

## End Team

## Match

match_view = MatchAPI.as_view('match_api')

app.add_url_rule(
    '/api/v1/resources/matches/',
    defaults={'match_id': None},
    view_func=match_view,
    methods=['GET',]
    )

app.add_url_rule(
    '/api/v1/resources/matches/',
    view_func=match_view,
    methods=['POST',]
    )

app.add_url_rule(
    '/api/v1/resources/matches/<int:match_id>',
    view_func=match_view,
    methods=['GET', 'PUT',]
    )

## End Match


## Venue

venue_view = VenueAPI.as_view('venue_api')

app.add_url_rule(
    '/api/v1/resources/venues/',
    defaults={'venue_id': None},
    view_func=venue_view,
    methods=['GET',]
    )

app.add_url_rule(
    '/api/v1/resources/venues/',
    view_func=venue_view,
    methods=['POST',]
    )

app.add_url_rule(
    '/api/v1/resources/venues/<int:venue_id>',
    view_func=venue_view,
    methods=['GET', 'PUT',]
    )

## End Venue


## Country

country_view = CountryAPI.as_view('country_api')

app.add_url_rule(
    '/api/v1/resources/countries/',
    defaults={'country_id': None},
    view_func=country_view,
    methods=['GET',]
    )

app.add_url_rule(
    '/api/v1/resources/countries/',
    view_func=country_view,
    methods=['POST',]
    )

app.add_url_rule(
    '/api/v1/resources/countries/<int:country_id>',
    view_func=country_view,
    methods=['GET', 'PUT',]
    )

## End Country

app.run()

