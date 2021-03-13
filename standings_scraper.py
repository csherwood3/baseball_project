import json
import baseball_scraper as bs

league_data = bs.standings(2020)


def make_all_standings(data=league_data, league=0):
    """Calls make_standings function repeatedly for each division in the MLB.
    Generates a dictionary with standings for all major league teams in a given year.
    Exports the dictionary to a json file named 'standings.json'."""
    standings_dict = {0: "AL East", 1: "AL Central", 2: "AL West", 3: "NL East", 4: "NL Central", 5: "NL West"}
    all_standings = {}
    while league != 6:
        current_league = standings_dict[league]
        all_standings[current_league] = make_standings(data, league)
        league += 1

    with open("standings.json", "w") as outfile:
        json.dump(all_standings, outfile)
    return all_standings


def make_standings(data, league):
    """A helper function for make_all_standings. This generates one single division (i.e. AL East).
    Calls the 4 get_<standings_stats> for each division, then appends those values to each respective team."""
    league_standings = {}

    wins_list = get_wins(data, league)
    losses_list = get_losses(data, league)
    percents_list = get_wl_percents(data, league)
    gb_list = get_games_behind(data, league)

    counter = 0
    for teams in data[league]["Tm"]:
        if counter != 5:
            league_standings[teams] = {"W": wins_list[counter],
                                       "L": losses_list[counter],
                                       "W-L%": percents_list[counter],
                                       "GB": gb_list[counter]}
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


make_all_standings()
