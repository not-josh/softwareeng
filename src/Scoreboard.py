import os
import string
import re
from datetime import datetime
from sortedcontainers import SortedList
import pygame
from Renderable import Renderable

# .sb - Scoreboard file
# .sba - Scoreboard archive file (contains any scores that couldn't load properly)

# Format of scoreboard files
#	[Score] [Username] [Datetime: %Y/%m/%d-%H:%M:%S]

SB_DIR = "Scores/"
SB_FILE = "Scores.sb"
ARCHIVE_DIR = SB_DIR + "Archive/"

DT_FORMAT = "%Y/%m/%d-%H:%M:%S"

USR_CHAR_COUNT = 3
NAME_FORM = re.compile("^[A-Z]{%d}$" % USR_CHAR_COUNT)


class Score():

	def __init__(self, line:str) -> None:
		self.valid = True
		str_list:list[str] = line.split(' ')
		if len(str_list) < 3:
			self.valid = False
			return
		
		# Load score
		try:
			self.score:int = int(str_list[0])
		except:
			self.valid = False
			return
		
		# Load username
		try:
			username = NAME_FORM.match(str_list[1])
			self.username:str = username.string
		except:
			self.valid = False
			return
		
		# Load date
		try:
			self.date:datetime = datetime.strptime(str_list[2], DT_FORMAT)
		except:
			self.valid = False
			return


	def __str__(self) -> str:
		return	self.score.__str__() + \
				" " + self.username + \
				" " + self.date.strftime(DT_FORMAT)
		pass

	
	def fullDetailStr(self) -> str:
		return "Score: " + self.score.__str__() + \
				" | Username: " + self.username + \
				" | Date: " + self.date.strftime(DT_FORMAT)
		pass

# Functions used is sorting lists of scores
def sortScore(obj:Score): return (obj.score, obj.date, obj.username)
def sortDate(obj:Score): return (obj.date, obj.score, obj.username)
def sortUser(obj:Score): return (obj.username, obj.score, obj.date)


# Scoreboard class
#	Static Elements
#		- Score lists: scores_by_scores, scores_by_date, scores_by_user
#		- loadScores(), inserScore(), exportScores(), __loadFile(), __archiveScores()
#	Non-Static Elements:
#		- 
class Scoreboard(Renderable):

	def __init__(self, size:tuple[int,int], min_font_size = 12, row_spacing = 4, col_spacing = 8) -> None:
		super().__init__()
		if not Scoreboard.scores_loaded: Scoreboard.loadScores()
		
		
		pass


	### BEGIN STATIC COMPONENTS ###

	scores_by_score:SortedList = SortedList(key=sortScore)
	scores_by_date:SortedList = SortedList(key=sortDate)
	scores_by_user:SortedList = SortedList(key=sortUser)
	scores_loaded:bool = False
	
	def loadScores():
		if not os.path.exists(SB_DIR):
			os.makedirs(SB_DIR)
		files = os.listdir(SB_DIR)
		# Get all files in scoreboard directory
		for file in files:
			# If a scoreboard file (.sb)
			fl = len(file)
			if fl > 2 and file[fl-3 : fl] == ".sb":
				# If is actually a file (not a dir/folder)
				file_path = SB_DIR + file
				if os.path.isfile(file_path):
					invalids = []
					Scoreboard.__loadFile(file_path, invalids)
					Scoreboard.__archiveScores(invalids, file)
					
					# Remove any extra .sb files
					if file != SB_FILE:
						os.remove(file_path)
		Scoreboard.scores_loaded = True

	# Adds scores to each list (each list holds references to the same items, just sorted in a different order)
	def insertScore(score:Score):
		Scoreboard.scores_by_score.add(score)
		Scoreboard.scores_by_date.add(score)
		Scoreboard.scores_by_user.add(score)


	def __loadFile(file_path:str, invalids:list[str] = -1):
		if invalids != -1: invalids.clear()

		with open(file_path, 'r') as file:
			line = file.readline().strip()
			# For each line (score)
			while line:
				# Genereate and append only if the score is valid
				score = Score(line)
				if score.valid: 
					Scoreboard.insertScore(score)
				else:
					print("Error: Score not valid {%s}" % line)
					if invalids != -1: invalids.append(line)
				# Get next line
				line = file.readline().strip()


	def __archiveScores(invalids:list[str], filename):
		# Archive invalid scores
		if len(invalids) > 0:
			print("Archiving")
			# Generate archive file path
			if not os.path.exists(ARCHIVE_DIR):
				os.makedirs(ARCHIVE_DIR)
			new_file = getNewFilePath(ARCHIVE_DIR + filename + 'a')

			# Write invalid scores to archive file
			with open(new_file, 'w+') as archive:
				for line in invalids:
					archive.write(line + '\n')


	def export():
		# Create a backup of the existing .sb
		main_file = SB_DIR + SB_FILE
		archive_file = main_file + 'a'
		if os.path.exists(main_file): 
			archive_file = getNewFilePath(archive_file)
			os.rename(main_file, archive_file)

		# Write a new .sb file
		with open(main_file, 'w+') as file:
			for score in Scoreboard.scores_by_score:
				file.write(score.__str__() + '\n')
		
		# Delete temporary backup file
		if os.path.exists(archive_file): os.remove(archive_file)


	def toStr() -> str:
		s = ""
		for score in Scoreboard.scores_by_score:
			s += score.fullDetailStr() + '\n'
		return s


# If the desired filepath given already exists, modify until it's unique, return the first unique one
def getNewFilePath(desired_fp:str):
	while os.path.exists(desired_fp):
		dp = desired_fp.rfind('.')
		desired_fp = desired_fp[:dp] + '.' + desired_fp[dp:]
	return desired_fp