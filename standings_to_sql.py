import sqlite3

conn = sqlite3.connect('standings.db')
c = conn.cursor()

c.execute("""CREATE TABLE Standings_2020 (
            Team_ID int,
            Team_Abbrev text,
            Team_Name text,
            Wins int,
            Losses int,
            WLPercent float,
            Games_Behind float)
""")