import re
from datetime import datetime
import os


class Average():
	'''Solution one takes list and finds average and assigns to dictionary'''

	def __init__(self, args):
		self.my_list = args
		self.answers = {}

	def calculate_average(self):
		avg = sum(self.my_list)/len(self.my_list)
		
		
		if avg < 6:
			self.answers['A']= 'Low Average'
		elif avg >= 6 and avg < 12:
			self.answers['B'] = 'Medium Average' 
		else:
			self.answers['C'] = 'High Average'
		return self.answers

my_avg = Average([15,-4,5])
print(my_avg.calculate_average())


#for solution number two, finds number from string and calls the function

input_number = map(int, re.findall(r'\d+' ,'3deepak adf 13d 4'))
print input_number
new_avg = Average(input_number)
print (new_avg.calculate_average())


#Solution3
class DateCalculator():
	def __init__(self, folder_name):
		self.folder_name = folder_name


	def date_calculator(self):
		file_name = os.path.basename(self.folder_name)
		date_object = re.findall(r'\d+', self.folder_name)
		date_in_string_format = '-'.join(date_object)
		new_date = datetime.strptime(date_in_string_format, '%Y-%m-%d')
		no_of_days = (datetime.now() - new_date).days
		return (' File name: {} \n Date: {} \n No.of days: {}'. format(file_name, new_date, no_of_days))

my_obj = DateCalculator("articles/2010/10/21/my_summer")
print (my_obj.date_calculator())