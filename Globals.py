import pymysql
import subprocess as sp

conn = pymysql.connect(host="localhost", port=3306, user="root", passwd="admin", db="March_Madness")
clear_screen = sp.call('clear',shell=True)

# Enter any combinations that must be in the final list
allFinalFours = []
allFinalFoursNums = []
# Enter combinations that should not be included
excludedcombos = []
# Enter target emails
email_list = ['test@gmail.com']
# Desired number of picks. Should be changed based on pool
numofpicks = 155
# Filenames subject to change
filename1 = "finalfour.csv"
filename2 = "finalfourwithnumbers.csv"
