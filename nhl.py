#!/usr/bin/python
import urllib, json
from bs4 import BeautifulSoup
from collections import defaultdict
import os, argparse

BASEURL = "http://www.nhl.com/ice/gamestats.htm?fetchKey=20132ALLSATAll&viewName=summary&sort=gameDate&pg="
PAGENUMBER = 20

def read_data(load_from_web = False):
	''' Parses through nhl.com data or json data for matches and match report urls '''
 	teams = defaultdict(lambda: [[],[]])
	if not load_from_web:
		with open('nhl.json') as jsonfile:
			teams = json.load(jsonfile)
	else:
		for i in range(1, PAGENUMBER + 1):
			soup = get_soup("%s%s" % (BASEURL, i))
			tables = soup.findAll('table', { 'class': 'data stats' })[0].find('tbody')
			rows = tables.findAll('tr')
			for row in rows:
				match_url = get_match_url(row)
				cells = row.findAll('td')
				home_team = cells[1].string
				away_team = cells[3].string
				home_goals = cells[2].string
				away_goals = cells[4].string

				if int(home_goals) > int(away_goals):
					teams[home_team][0].append('W')
					teams[away_team][0].append('L')
				else:
					teams[away_team][0].append('W')
					teams[home_team][0].append('L')

				teams[home_team][1].append(match_url)
				teams[away_team][1].append(match_url)
	return teams

def get_soup(url):
	''' Returns BeautifulSoup object for given url '''
	return BeautifulSoup(urllib.urlopen(url))

def get_match_url(row):
	''' Extracts correct url from <td>-BeautifulSoup-object '''
	for url in row.findAll('a'):
		if 'www.nhl.com' in url['href']:
			return url['href']

def print_teams(teams):
	''' Prints teams in nice way '''
	for team in sorted(teams.keys()):
		print team,
		print teams[team][0]

def transform(teams):
	''' Transforms WLLWWLLWLW => _LLWWLL___ '''
	transformed = defaultdict(lambda: [[],[]])
	for team in teams.keys():
		games = teams[team][0]
		for i in range(0, len(games)-1):
			if games[i] == games[i+1] or games[i] == games[i-1]:
				transformed[team][0].append(games[i])
			else:
				transformed[team][0].append('')
		# Don't forget the last game
		if games[-2] == games[-1]:
			transformed[team][0].append(games[-1])
		else:
			transformed[team][0].append('')
		transformed[team][1] = teams[team][1]
	return transformed

def write_json(teams, filename):
	''' Writes teams to json file '''
	with open(filename, 'wb') as fname:
		json.dump(teams, fname)

def write_html(teams, filename):
	''' Writes nice html table for streaks '''
	with open(filename, 'wb') as fname:
		fname.write('<table class="winningstreak">\n')
		fname.write('<tr><td>Team</td>')
		for i in range(1, max([len(matches[0]) for team, matches in teams.iteritems()])+1):
			fname.write('<td>%d</td>' % i)
		fname.write('</tr>\n')
		for team in sorted(teams.keys()):
			imagename = team.lower().replace(' ', '')
			imagename = "%s.png" % imagename
			fname.write('<tr>\n')
			fname.write('<td><img src="./logos/%s" class="logo" /> </td>' % imagename)
			wins_and_losses = teams[team][0]
			match_urls = teams[team][1]
			for i in range(0, len(wins_and_losses)):
				fname.write('<td class="%s" onClick="window.open(\'%s\');"></td>' % (wins_and_losses[i], match_urls[i]))
			fname.write('</tr>\n')
		fname.write('</table>\n')

def reverse_lists(teams):
	''' Reverses lists '''
	for team in teams.keys():
		teams[team][0].reverse()
		teams[team][1].reverse()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Load and save NHL data")
    parser.add_argument('--web', action='store_true', dest='web', default=False)
    parser.add_argument('--json', action='store_true', dest='json', default=False)
    parser.add_argument('--html', action='store_true', dest='html', default=False)
    args = parser.parse_args()
    teams = read_data(args.web)
    transformed = transform(teams)
    reverse_lists(transformed)
    if args.html:
        write_html(transformed, 'nhl-temp.html')
        print "HTML written"
    if args.json:
        write_json(transformed, 'nhl.json')
        print "JSON written"

