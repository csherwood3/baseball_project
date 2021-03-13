import json
import baseball_scraper as bs
import sqlite3

user_year = input("Enter the year you wish to scrape: ")
league_data = bs.standings(int(user_year))


class Team:
    """Represents a team object.
    Contains all of the standings statistics for a team for a given year"""
    def __init__(self, team_id, abbrev, team_name, division, wins, losses, wlp, gb):
        self._team_id = team_id
        self._team_abbrev = abbrev
        self._team_name = team_name
        self._division = division
        self._wins = wins
        self._losses = losses
        self._WLP = wlp
        self._GB = gb


def make_all_standings(data=league_data, league=0):
    """Calls make_standings function repeatedly for each division in the MLB.
    Generates a dictionary with standings for all major league teams in a given year.
    Exports the dictionary to a json file named 'standings.json'."""
    league_dict = {0: "AL East", 1: "AL Central", 2: "AL West", 3: "NL East", 4: "NL Central", 5: "NL West"}
    all_standings = {}
    while league != 6:
        current_league = league_dict[league]
        all_standings[current_league] = make_standings(data, league)
        league += 1

    with open("standings.json", "w") as outfile:
        json.dump(all_standings, outfile)


def make_standings(data, league):
    """A helper function for make_all_standings. This generates one single division (i.e. AL East).
    Calls the 4 get_<standings_stats> for each division, then appends those values to each respective team."""
    league_standings = {}
    counter = 0
    wins_list = get_wins(data, league)
    losses_list = get_losses(data, league)
    percents_list = get_wl_percents(data, league)
    gb_list = get_games_behind(data, league)
    abbr_list = get_team_abbreviation(data[counter]["Tm"])


    for teams in data[league]["Tm"]:
        if counter != 5:
            league_standings[teams] = {"W": wins_list[counter],
                                       "L": losses_list[counter],
                                       "W-L%": percents_list[counter],
                                       "GB": gb_list[counter],
                                       "Abbr":
        counter += 1
    return league_standings


def get_wins(data, league):
    """This function generates a list of the total wins for each team in a division."""
    wins_list = []
    for wins in data[league]["W"]:
        wins_list.append(int(wins))
    return wins_list


def get_losses(data, league):
    """This function generates a list of the total losses for each team in a division."""
    losses_list = []
    for losses in data[league]["L"]:
        losses_list.append(int(losses))
    return losses_list


def get_wl_percents(data, league):
    """This function generates a list of the win percentages for each team in a division."""
    percents_list = []
    for WLPercents in data[league]["W-L%"]:
        percents_list.append(float(WLPercents))
    return percents_list


def get_games_behind(data, league):
    """This function generates a list of the games behind first for each team in a division.
    If a team is in first, their games behind will be 0 instead of '--'."""
    games_behind_list = []
    for GamesBehind in data[league]["GB"]:
        if GamesBehind == "--":
            games_behind_list.append(float(0))
        else:
            games_behind_list.append(float(GamesBehind))
    return games_behind_list


def get_team_abbreviation(team_name):
    """This function takes a team name and then returns an abbreviation for the team
    (i.e. New York Yankees = NYY)."""
    team_dict = {"Arizona Diamondbacks": "ARI",
                 "Atlanta Braves": "ATL",
                 "Baltimore Orioles": "BAL",
                 "Boston Red Sox": "BOS",
                 "Chicago Cubs": "CHC",
                 "Chicago White Sox": "CHW",
                 "Cincinnati Reds": "CIN",
                 "Cleveland Indians": "CLE",
                 "Colorado Rockies": "COL",
                 "Detroit Tigers": "DET",
                 "Houston Astros": "HOU",
                 "Kansas City Royals": "KAN",
                 "Los Angeles Angels": "LAA",
                 "Los Angeles Dodgers": "LAD",
                 "Miami Marlins": "FLA",
                 "Milwaukee Brewers": "MIL",
                 "Minnesota Twins": "MIN",
                 "New York Mets": "NYM",
                 "New York Yankees": "NYY",
                 "Oakland Athletics": "OAK",
                 "Philadelphia Phillies": "PHI",
                 "Pittsburgh Pirates": "PIT",
                 "San Diego Padres": "SD",
                 "San Francisco Giants": "SF",
                 "Seattle Mariners": "SEA",
                 "St. Louis Cardinals": "STL",
                 "Tampa Bay Rays": "TB",
                 "Texas Rangers": "TEX",
                 "Toronto Blue Jays": "TOR",
                 "Washington Nationals": "WAS"
                 }
    team_abbrev = team_dict[team_name]
    return team_abbrev


make_all_standings()
