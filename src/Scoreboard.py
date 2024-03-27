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
SCORE_DIGIT_COUNT = 12
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

	def __init__(self, size:tuple[int,int], color = (255,255,255), font = -1, row_spacing = 8, col_padding = 12) -> None:
		super().__init__()
		if not Scoreboard.scores_loaded: Scoreboard.loadScores()

		self.color = color
		self.col_padding = col_padding
		self.row_spacing = row_spacing
		
		if font != -1:
			self.font:pygame.font.Font = font
		else:
			self.font:pygame.font.Font = pygame.font.Font(None, 24)

		self.index = 0
		self.rect = pygame.Rect((0,0), size)

	@property
	def size(self): return (self.rect.width, self.rect.height)
	@size.setter
	def size(self, set:tuple[int,int]):
		center = self.rect.center
		self.rect.size = set
		self.rect.center = center
		self.redraw()

	# Two opposing corners of the area of the rect
	@property
	def span(self): return (self.rect.topleft, self.rect.topright)
	@span.setter
	def span(self, set:tuple[tuple[int,int], tuple[int,int]]):
		top = min(set[0][1], set[1][1])
		left = min(set[0][0], set[1][0])
		width = abs(set[0][0] - set[1][0])
		height = abs(set[0][1] - set[1][1])
		self.rect = pygame.Rect(top, left, width, height)
		self.redraw()
	
	def redraw(self):
		char_size = self.font.size('_')
		char_x = char_size[0]
		char_y = char_size[1]

		score_header = "Score"
		user_header = "Username"
		date_header = "Date"

		score_w = max(char_x*SCORE_DIGIT_COUNT, char_x*len(score_header))
		user_w = max(char_x*USR_CHAR_COUNT, char_x*len("Username"))
		date_w = max(char_x*len("YYYY/DD/MM"), char_x*len(date_header))

		tot_content_width = score_w + user_w + date_w + 6 * self.col_padding
		tot_col_space = self.size[0] - tot_content_width
		if tot_col_space < 0:
			self.size = (tot_content_width, self.size[1])
			print("Assigned width of %d" % tot_content_width)
			tot_col_space = 6 * self.col_padding
			left_padding = self.col_padding
			right_padding = self.col_padding
		else:
			left_padding = self.col_padding
			right_padding = tot_col_space - 3 * left_padding


		surface = pygame.Surface(self.size, pygame.SRCALPHA)

		# Define x positions of column contents and dividers
		div1_x = 0
		score_x = left_padding
		div2_x = score_x + user_w + right_padding
		user_x = div2_x + left_padding
		div3_x = user_x + user_w + right_padding
		date_x = div3_x + left_padding
		div4_x = self.size[0] - 1

		# Draw divider lines
		pygame.draw.line(surface, (127,127,127), (div1_x, 0), (div1_x, self.rect.height))
		pygame.draw.line(surface, (127,127,127), (div2_x, 0), (div2_x, self.rect.height))
		pygame.draw.line(surface, (127,127,127), (div3_x, 0), (div3_x, self.rect.height))
		pygame.draw.line(surface, (127,127,127), (div4_x, 0), (div4_x, self.rect.height))

		# Draw header
		surface.blit(self.font.render("Score", True, self.color), (score_x, 0))
		surface.blit(self.font.render("Username", True, self.color), (user_x, 0))
		surface.blit(self.font.render("Date", True, self.color), (date_x, 0))

		self.surface = surface


	
	def redrawOld(self):
		surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		pygame.draw.line(surface, self.color, (0, 0), (0, self.rect.height))
		pygame.draw.line(surface, self.color, (self.rect.width-1, 0), (self.rect.width-1, self.rect.height))
		h = 0

		char_size = self.font.size('_')
		char_x = char_size[0]
		char_y = char_size[1]

		score_header = "Score"
		user_header = "Username"
		date_header = "Date"

		score_w = max(char_x*SCORE_DIGIT_COUNT, char_x*len(score_header))
		user_w = max(char_x*USR_CHAR_COUNT, char_x*len("Username"))
		date_w = max(char_x*len("YYYY/DD/MM"), char_x*len(date_header))

		col_spacing = max(self.min_col_spacing, (self.rect.width - (score_w+user_w+date_w)) // 2)
		half_spacing = col_spacing // 2

		score_x = 0
		user_x = score_x + score_w + col_spacing
		su_border = user_x - half_spacing
		date_x = user_x + user_w + col_spacing
		ud_border = date_x - half_spacing

		print(col_spacing * 2 + (score_w+user_w+date_w))
		pygame.draw.line(surface, (127,127,127), (su_border, 0), (su_border, self.rect.height))
		pygame.draw.line(surface, (127,127,127), (ud_border, 0), (ud_border, self.rect.height))

		# Draw header
		surface.blit(self.font.render("Score", True, self.color), (score_x, 0))
		surface.blit(self.font.render("Username", True, self.color), (user_x, 0))
		surface.blit(self.font.render("Date", True, self.color), (date_x, 0))

		self.surface = surface


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