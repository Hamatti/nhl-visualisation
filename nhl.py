import urllib, json
from bs4 import BeautifulSoup as bs
from collections import defaultdict
import os, argparse

baseurl = "http://www.nhl.com/ice/gamestats.htm?fetchKey=20132ALLSATAll&viewName=summary&sort=gameDate&pg="
PAGENUMBER = 16

def readData(loadFromWeb=False):
    teams = defaultdict(list)
    if not loadFromWeb:
        with open('nhl.json') as jsonfile:
            teams = json.load(jsonfile)
    else:
        for i in range (1,PAGENUMBER+1):
            pageurl = "%s%s" % (baseurl, i)
            soup = bs(urllib.urlopen(pageurl))
            all_tables = soup.findAll('table', { 'class' : 'data stats' })[0].find('tbody')
            trs = all_tables.findAll('tr')
            for tr in trs:
                team_success = {}
                tds = tr.findAll('td')
                home_team = tds[1].string
                away_team = tds[3].string
                home_goals = tds[2].string
                away_goals = tds[4].string
                home_win = int(home_goals) > int(away_goals)
                away_win = not home_win
                if home_win:
                    teams[home_team].append('W')
                    teams[away_team].append('L')
                else:
                    teams[home_team].append('L')
                    teams[away_team].append('W')            
    print max([len(matches) for team, matches in teams.items()])
    return teams            

def printData(teams):
    for team in sorted(teams.keys()):
        print team, 
        print teams[team],
        print len(teams[team])
        
def transform(teams):
    transformed = defaultdict(list)
    for team in teams.keys():
        games = teams[team]
        for i in range(0, len(games)-1):
            if games[i] == games[i+1] or games[i] == games[i-1]:
                if games[i] == 'W':
                    transformed[team].append('W')
                elif games[i] == 'L':
                    transformed[team].append('L')
            else:
                transformed[team].append('')
        # Last game
        if games[-2] == games[-1]:
            if (games[-1] == 'W'):
                transformed[team].append('W')
            else:
                transformed[team].append('L')
        else:
            transformed[team].append('')
    return transformed


def writeJSON(teams, filename):
    with open(filename, 'wb') as fname:
        json.dump(teams, fname)

def writeHTML(teams, filename):
    with open(filename, 'wb') as fname:
        fname.write('<table class="winningstreak">\n')
        fname.write('<tr><td>Team</td>')
        for i in range(1, max([len(matches) for team, matches in teams.iteritems()])+1): 
            fname.write('<td>%d</td>' % i)
        fname.write('</tr>')
        for team in sorted(teams.keys()):
            imagename = team.lower()
            imagename = imagename.replace(' ', '')
            imagename = "%s.png" % imagename
            fname.write('<tr>')
            fname.write('<td><img src="./logos/%s" width="75px" height="50px"></td>' % imagename)
            for element in teams[team]:
                fname.write('<td class="%s"></td>' % element)
            fname.write('</tr>\n')
        fname.write('</table>\n')

def rev(teams):
    for team in teams.keys():
        teams[team].reverse()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Load and save NHL data")
    parser.add_argument('--web', action='store_true', dest='web', default=False)
    parser.add_argument('--json', action='store_true', dest='json', default=False)
    parser.add_argument('--html', action='store_true', dest='html', default=False)
    args = parser.parse_args()
    teams = readData(args.web)
    transformed = transform(teams)
    rev(transformed)
    if args.html:
        writeHTML(transformed, 'nhl-temp.html')
        print "HTML written"
    if args.json:
        writeJSON(transformed, 'nhl.json')
        print "JSON written"
