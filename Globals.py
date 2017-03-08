import MySQLdb
import subprocess as sp

conn = MySQLdb.connect(host="localhost", port=3306, user="admin", passwd="admin", db="March_Madness")
clear_screen = sp.call('clear',shell=True)

# Enter any combinations that must be in the final list
allFinalFours = []
allFinalFoursNums = []
# Enter combinations that should not be included
excludedcombos = []
# Enter target emails
email_list = []
# Desired number of picks. Should be changed based on pool
numofpicks = 20
# Filenames subject to change
filename1 = "finalfour.csv"
filename2 = "finalfourwithnumbers.csv"
