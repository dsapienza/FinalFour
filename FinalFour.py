import pymysql
import re
import random
import csv
from Globals import *
from decimal import Decimal
from sendfile import send_mail

class FinalFour(object):
	""" Create a potential Final Four outcome """

	# Hard coded for now since they don't really change
	regions = ['SOUTH','EAST','WEST','MIDWEST']
	#regions = self.get_region_info()

	def __init__(self):
		self.east	   = None
		self.midwest	   = None
		self.south	   = None
		self.west          = None
		self.winner	   = None
		self.score	   = 150
		self.twsDict       = self._createlistwithnumbers()
		self.finalfour 	   = []
		self.finalfournums = []
		self.verify_winners()

	def _createlistwithnumbers(self):
		""" Add the numerical representation for each team into a list """

		seed_query = "SELECT school, number FROM March_Madness.teams"
		cursr = conn.cursor()
		cursr.execute(seed_query)
		teamswithseed = cursr.fetchall()
		return dict(teamswithseed)

        def _assignteam(self, reg, tm):
                """ Assign the team to the region it belongs """

                if reg == 'EAST':
                        self.east = tm
                elif reg == 'MIDWEST':
                        self.midwest = tm
                elif reg == 'SOUTH':
                        self.south = tm
                elif reg == 'WEST':
                        self.west = tm

        def _assignwinner(self):
                """ Take the final four combination and decide the most likely winner """

                search_string = '\',\''.join(self.finalfour)

                winner_query = "SELECT Winner FROM winners WHERE Winner IN (\'%s\') ORDER BY rank DESC LIMIT 1" % search_string
                cursr = conn.cursor()
                row_count = cursr.execute(winner_query)
                if row_count > 0:
                        win = cursr.fetchone()
                        #self.winner = self.finalfour[0]
                        self.winner = win[0]

        def _assignscore(self):
                """ Take the winner of the current final four combination and attach the score"""

                score_query = "SELECT Score FROM winners WHERE Winner = '%s'" % self.winner
                cursr = conn.cursor()
                row_count = cursr.execute(score_query)
                if row_count > 0:
                        score = cursr.fetchone()
                        self.score = int(score[0])
	
	def get_region_info(self):
		region_query = 'SELECT name FROM March_Madness.regions as R'
		cursr = conn.cursor()
		cursr.execute(region_query)
		regions = cursr.fetchall()
		return regions

	def totalVotesPerRegion(self, r):
		regioncount_query = "SELECT SUM(votes) as TotalVotesPerRegion FROM ranks WHERE region = '%s' " % (r)
		cursr = conn.cursor()
		cursr.execute(regioncount_query)
		regioncount = cursr.fetchone()
		return regioncount[0]

	def teamsWithVotes(self, r):
		teamvoted_query = "SELECT distinct school FROM ranks WHERE region = '%s' " % (r)
		cursr = conn.cursor()
		cursr.execute(teamvoted_query)
		teamvoted = cursr.fetchall()
		return teamvoted

	def votesPerTeam(self, t):
		teamvotes_query = "SELECT SUM(votes) FROM ranks WHERE school = '%s' " % (t)
		cursr = conn.cursor()
		cursr.execute(teamvotes_query)
		teamvotes = cursr.fetchall()
		return int(teamvotes[0][0])

	def get_teams_with_votes(self):
		""" Get all teams that have a vote """

		team_query = "SELECT distinct school FROM March_Madness.ranks as R"
		cursr = conn.cursor()
		cursr.execute(team_query)
		tms = cursr.fetchall()
		return tms

	def get_teams_for_region(self, reg):
		""" Get the list of teams in each region """

		rank_query = "SELECT distinct school FROM March_Madness.ranks as R WHERE region = '%s'" % reg
                cursr = conn.cursor()
                cursr.execute(rank_query)
                tms = cursr.fetchall()
		return tms

	def get_vote_totals(self):
		""" Get the total votes per team in each region """

		for r in self.regions:
			teams = self.get_teams_for_region(r)
			print r.upper()
		        for t in teams:
        			count_query = "SELECT SUM(votes) as TotalVotes FROM March_Madness.ranks WHERE region = '%s' AND school = '%s' " % (r, t[0])
			        cursr = conn.cursor()
				cursr.execute(count_query)
			        votes = cursr.fetchone()
			        print "Total votes for %s is %s" % (t[0], votes[0])

	def ff_combo(self):
		""" Write to list and DB a random final four combination """

		self.finalfour = [self.south, self.east, self.west, self.midwest]
		self._assignwinner()
                self.finalfour.append(self.winner)
		self._assignscore()
		self.finalfour.append(self.score)
		self.finalfournums = [self.twsDict.get(self.south), self.twsDict.get(self.east), self.twsDict.get(self.west), self.twsDict.get(self.midwest), self.twsDict.get(self.winner, 'None'), self.score]
		if self.finalfour not in (allFinalFours):
			allFinalFours.append(self.finalfour)
			allFinalFoursNums.append(self.finalfournums)

	def generate_ff_combo(self):
		""" Generate a random combo of potential Final Four teams """

		teamlistoflists = []
		
		for r in self.regions:
#			print r.upper()
			teamlist = []
			twv = self.get_teams_for_region(r)
			# Hard code region needs to be updated
			votesPerRegion = self.totalVotesPerRegion(r)

			for t in twv:
				votesPerTeam = self.votesPerTeam(t[0])
			        percentOfRegion = round(((Decimal(votesPerTeam)/Decimal(votesPerRegion))*100), 2)
				teams = ([t[0]]*int(percentOfRegion))
				teamlist.extend(teams)
			randomteam = random.choice(teamlist)
			self._assignteam(r, randomteam)
		self.ff_combo()
#		for l in itertools.product(*teamlistoflists):
#			print l

	def addtofile(self, fn, fflist):
		""" Add all final four combination to a local csv file """

		with open(fn, "wb") as f:
			writer = csv.writer(f)
			writer.writerow(["SOUTH", "EAST", "WEST", "MIDWEST", "WINNER", "SCORE"])
			writer.writerows(fflist)

	def verify_winners(self):
		""" Ensure all teams are listed as possible winners """

		teams = self.get_teams_with_votes()
		for t in teams:
			check_query = "SELECT * FROM March_Madness.winners WHERE Winner = '%s'" % t[0]
			cursr = conn.cursor()
			winnerexist = cursr.execute(check_query)
			if winnerexist == 0:
				insertwinner = "INSERT INTO winners (Winner, Score, rank) VALUES ('%s','148',(SELECT SUM(votes) FROM ranks WHERE school = '%s'));" % (t[0],t[0])
				cursr = conn.cursor()
				cursr.execute(insertwinner)
				conn.commit()

