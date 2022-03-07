import csv
import pandas as pd

DEBUG = False
DATA_FILE = "data.csv" 
GRADE_INDEX_START = 3
GRADE_INDEX_END = 12

'''
 k: category-names used in client msg (i.e. GL1A, GE4G)
 v: category-names used in csv file
'''
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
ID_INDEX = 1


class csv_handler:
	def __init__(self):
		self.data = pd.read_csv(DATA_FILE, header=0)

	def get_category_mean(self, category):
		if category in COL_NAMES:
			return float(self.data[COL_NAMES[category]].mean())

	def get_grade(self, stud_num, category):
		for index, row in self.data.iterrows():
			if (str(row[ID_INDEX]) == stud_num):
				return float(row[COL_NAMES[category]])

	def get_all_grades(self, stud_num):
		for index, row in self.data.iterrows():
			if (str(row[ID_INDEX]) == stud_num):
				grades = row[GRADE_INDEX_START:GRADE_INDEX_END]
				return remove_last_line_from_string(str(grades))


def remove_last_line_from_string(s):
    return s[:s.rfind('\n')]   

def test_csv_handler():
	# runs the two getters with example params.
	c = csv_handler()
	l1_mean = c.get_category_mean("L1")
	print(f"Lab 1 mean is: {l1_mean}")
	student1_lab1_grade = c.get_grade("1803933", "L1")
	print(f"Student 1803933 grade for Lab 1: {student1_lab1_grade}")

csv_handler()

if DEBUG:	
	test_csv_handler()