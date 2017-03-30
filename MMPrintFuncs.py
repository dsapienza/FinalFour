import pymysql
import subprocess as sp
from Globals import *
from march_madness import launch_menu

def print_regions(rgns):
    for r in rgns:
        print "".join(r).rjust(0).ljust(20),
    print ""

def print_bracket(rgns):
    sp.call('clear',shell=True)
    print ""
    print_regions(rgns)
    for s in range(1,17):
        print_by_seed(s)

def print_by_seed(seed):
     seed_query = "SELECT school FROM March_Madness.teams as T WHERE seed = '%s' " % seed
     cursr = conn.cursor()
     cursr.execute(seed_query)
     seeds = cursr.fetchall()
     sds = ["".join(s) for s in seeds]
     c = 0
     while c < 4:
        print sds[c].rjust(0).ljust(20),
        c += 1
     print ""

def print_teams_by_region(rgn):
    print rgn
    team_query = "SELECT school FROM March_Madness.teams as T WHERE region = ( SELECT id FROM regions WHERE name = '%s' )" % rgn
    cursr = conn.cursor()
    cursr.execute(team_query)
    teams = cursr.fetchall()
    return ["".join(tm) for tm in teams]
