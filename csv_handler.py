import csv
import pandas as pd


DATA_FILE = "data.csv" 
ID_INDEX = 1			# student id
PW_INDEX = 2			# password id
GRADE_INDEX_START = 3 	# lab1
GRADE_INDEX_END = 12  	# exam4
#	'''
#	 k: category-names used in client msg (i.e. GL1A, GE4G)
#	 v: category-names used in csv file
#	'''`
COL_NAMES = {
	"L1" : "Lab 1", 
	"L2" : "Lab 2", 
	"L3" : "Lab 3", 
	"L4" : "Lab 4", 
	"M" : "Midterm", 
	"E1" : "Exam 1", 
	"E2" : "Exam 2", 
	"E3" : "Exam 3", 
	"E4" : "Exam 4"
}


class csv_handler:
	def __init__(self):
		self.data = pd.read_csv(DATA_FILE, header=0)
		print(f"\n\nCSV DATA:\n{self.data}")

	def get_category_mean(self, category):
		if category in COL_NAMES:
			return float(self.data[COL_NAMES[category]].mean())

	def get_grade(self, stud_num, category):
		for index, row in self.data.iterrows():
			if (str(row[ID_INDEX]) == stud_num):
				return float(row[COL_NAMES[category]])

	def get_all_grades(self, stud_num):
		output = ""
		for index, row in self.data.iterrows():
			if (str(row[ID_INDEX]) == str(stud_num)):
				for i, grade in enumerate(row[GRADE_INDEX_START:GRADE_INDEX_END]):
					output += f" {list(COL_NAMES.keys())[i]} : {grade}, "
		return output[:-2]

	def get_ids_and_passwords(self):
		l = []
		for index, row in self.data.iterrows():
			id = str(row[ID_INDEX])
			pw = str(row[PW_INDEX])
			l.append((id, pw))
		return l

def remove_last_line_from_string(s):
    return s[:s.rfind('\n')]
