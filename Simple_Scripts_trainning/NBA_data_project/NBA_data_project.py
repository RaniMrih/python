#get reguest for http api get data
from requests import get
#pprint makes output cleaner
from pprint import PrettyPrinter
import os
import json
import sys
import logging

sys.path.append('c:/Users/rmrih/Rani_GitHub/python/Simple_Scripts_trainning/logging')
import employee

printer = PrettyPrinter()
BASE_URL = 'https://data.nba.com/'
All_JSON = 'prod/v1/today.json'
separater ='----------------------------------------------------------'

#-------------------------------------------------- get all links from api ---------------------------------------------
def get_links():
    data = get(BASE_URL + All_JSON).json()
    links = data['links']
    # printer.pprint(data)
    return links

#--------------------------------- get data only for currentScoreboard (todays games)  ----------------------------------
def get_scoreboard():
    scoreboard = get_links()['currentScoreboard']
    #its dict so can grab all keys(games is key with more keys inside)
    games = get(BASE_URL + scoreboard).json['games']

    for game in games:
        home_team = game['hTeam']
        away_team = game['vTeam']
        clock = game['clock']
        period = game['period']

        print('{}'.format(separater))
        print('{} vs {}'.format(home_team['triCode'] , away_team['triCode']))
        print('{} - {}'.format(home_team['score'] , away_team['score']))
        print('{} - {}'.format(clock , period['current']))

#--------------------------------- get data only for currentScoreboard (todays games)  ----------------------------------
def get_stats():
    #getting data from dict (all those are keys)
    stats = get_links()['leagueTeamStatsLeaders']
    teams = get(BASE_URL + stats).json()['league']['standard']['regularSeason']['teams']

    #lambda runs a function aginst each elment in teams list
    #if the function returns true will keep the elment else will remove it because its irrelevant
    #converting to a list because filter function returns an object
    teams = list(filter(lambda x: x['name'] != 'Team' , teams))
    #sort the list according to rank 1 untill rank 30
    teams.sort(key=lambda x : x['gpp']['rank'])

    #loop on all teams
    #enumerate creats numbers
    for i, team in enumerate(teams):
        name = team['name']
        nickname = team['nickname']
        #points per games ppg
        ppg = team['ppg']['avg']
        print('{} - {} - {}'.format(i+1 ,name , nickname))

#-------------------------------------------------------- Start -----------------------------------------------------
if __name__ == '__main__':
    get_links()

