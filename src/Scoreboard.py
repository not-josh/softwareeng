import os
import string
import re
from datetime import datetime

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


# Static Scoreboard class
class Scoreboard():

	scores:list[Score] = []
	
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
					Scoreboard.archive(invalids, file)
					
					# Remove any extra .sb files
					if file != SB_FILE:
						os.remove(file_path)

	def __loadFile(file_path:str, invalids:list[str] = -1):
		if invalids != -1: invalids.clear()

		with open(file_path, 'r') as file:
			line = file.readline().strip()
			# For each line (score)
			while line:
				# Genereate and append only if the score is valid
				score = Score(line)
				if score.valid: 
					Scoreboard.scores.append(score)
				else:
					print("Error: Score not valid {%s}" % line)
					if invalids != -1: invalids.append(line)
				# Get next line
				line = file.readline().strip()
		
			

	def archive(invalids:list[str], filename):
		# Archive invalid scores
		if len(invalids) > 0:
			print("Archiving")
			# Generate archive file path
			if not os.path.exists(ARCHIVE_DIR):
				os.makedirs(ARCHIVE_DIR)
			new_file = ARCHIVE_DIR + filename + 'a'
			
			# If file exists, slightly modify until unique
			while os.path.exists(new_file):
				fp = len(new_file)-3
				new_file = new_file[:fp] + '.' + new_file[fp:]

			# Write invalid scores to archive file
			with open(new_file, 'w+') as archive:
				for line in invalids:
					archive.write(line + '\n')

	def export():
		with open(SB_DIR + SB_FILE, 'w+') as file:
			for score in Scoreboard.scores:
				file.write(score.__str__() + '\n')

	def toStr() -> str:
		s = ""
		for score in Scoreboard.scores:
			s += score.fullDetailStr() + '\n'
		return s