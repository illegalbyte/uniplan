import bs4 as bs
import requests
import pprint
import colorama
import re

# coloured formatter
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter
from pprint import pformat

def pprint_color(obj):
    print(highlight(pformat(obj), PythonLexer(), Terminal256Formatter()))



def deakin_handbook_scraper(url: str) -> dict:
	'''
	Scrape the Deakin Handbook website for course information.
	# Returns a dictionary of the following format:
	# Example of a unit dictionary entry:
	#  'STP050': {'unit_code': 'STP050',
	#             'unit_name': 'Academic Integrity (0 credit points)',
	#             'unitguideURL': 'http://www.deakin.edu.au/current-students-courses/unit.php?unit=STP050&year=2022&return_to=%2Fcurrent-students-courses%2Fcourse.php%3Fcourse%3DS326%26keywords%3Dbachelor%2Bof%2Binformation%2Btechnology%26version%3D2%26year%3D2022'}}
	'''

	# url = "https://www.deakin.edu.au/current-students-courses/course.php?course=S326&version=2&year=2022&keywords=bachelor+of+information+technology"

	response = requests.get(url)
	response.raise_for_status()
	soup = bs.BeautifulSoup(response.text, 'html.parser')

	# get the details table containing the course details
	details_table = soup.find('table', {'class': 'table'})

	course_details = {}
	# save all rows of details table to course_details dictionary
	for row in details_table.find_all('tr'):
		header = row.find('th')
		column = row.find_all('td')
		if header and column:
			course_details[header.text.strip()] = column[0].text.strip()

	# url to course map is within a tag with text "course map"
	course_map_url = soup.find('a', text="course map").get('href')
	course_code = course_details['Deakin course code']
	course_name = course_details['Award granted']

	# use bs to find the "Core" h2 tag and then use find all tables after the H2 tag
		#TODO: this solution may cause issues with other courses that have a different structure
		#TODO: this does not actually filter by major, minor, etc, but includes all units mentioned on the course page
	core_units_table = soup.find('h2', text='Core').find_all_next('table')

	units_tables = {}
	for unit in core_units_table:
		unit_code = unit.find('td').text.strip()
		units_tables[unit_code] = {}
		units_tables[unit_code]['unit_code'] = unit.find('td').text
		units_tables[unit_code]['unit_name'] = unit.find('td').find_next('td').text
		units_tables[unit_code]['unitguideURL'] = unit.find('a').get('href')

	# remove the duplicate units
	units = {}
	for key, value in units_tables.items():
		if value not in units.values():
			units[key] = value

	# find links to majors
	majors_list_a_tags = soup.find('h2', text='Major sequences').find_next('ul').find_all('a')
	majors_list = []
	for a_tag in majors_list_a_tags:
		majors_list.append(a_tag.get('href'))
	minors_list_a_tags = soup.find('h2', text='Minor sequences').find_next('ul').find_all('a')
	minors_list = []
	for a_tag in minors_list_a_tags:
		minors_list.append(a_tag.get('href'))

	# retrieve list of core units NOTE: relies on regex to find the core units
	html_string = str(soup)
	stripped_core_units_html = re.findall("(?<=<h2>Core<\/h2>)(.*)(?=<h2>Electives<\/h2>)", html_string)
	core_units_soup = bs.BeautifulSoup(str(stripped_core_units_html), 'html.parser')
	core_units_dict = {}
	for unit in core_units_soup.find_all('tr'):
		unit_code = unit.find('td').text.strip()
		core_units_dict[unit_code] = {}
		core_units_dict[unit_code]['unit_code'] = unit.find('td').text
		core_units_dict[unit_code]['unit_name'] = unit.find('td').find_next('td').text
		core_units_dict[unit_code]['unitguideURL'] = unit.find('a').get('href')

	return {'course_code': course_code, 'course_name': course_name, 'course_map_url': course_map_url, 'units': units, 'major_url_list': majors_list, 'minor_url_list': minors_list, 'core_units_dict': core_units_dict}
	# Example of a unit dictionary entry:
	#  'STP050': {'unit_code': 'STP050',
	#             'unit_name': 'Academic Integrity (0 credit points)',
	#             'unitguideURL': 'http://www.deakin.edu.au/current-students-courses/unit.php?unit=STP050&year=2022&return_to=%2Fcurrent-students-courses%2Fcourse.php%3Fcourse%3DS326%26keywords%3Dbachelor%2Bof%2Binformation%2Btechnology%26version%3D2%26year%3D2022'}}


def test_deakin_handbook_scraper():
	url = "https://www.deakin.edu.au/current-students-courses/course.php?course=S326&version=2&year=2022&keywords=bachelor+of+information+technology"
	course_data = deakin_handbook_scraper(url)
	pprint.pprint(course_data['core_units_dict'])


def sequence_guide_scraper(url: str) -> dict:
	'''
	Scrape a major/minor sequence page in the Deakin Handbook for units contained in that sequence.
	Returns a list of touples the unit codes contained in the sequence.
	'''
	web_request = requests.get(url)
	web_request.raise_for_status()
	soup = bs.BeautifulSoup(web_request.text, 'html.parser')

	# get the name of the sequence
	course_name = soup.find('h1').text
	# name of the sequence
	sequence_name = soup.find('h2').text
	# unit set code
	unit_set_code = soup.find('h3').find_next('p').text	

	all_units_tables = soup.find_all('table')
	sequence_units_list = []
	for table in all_units_tables: 
		unit_code = table.find('td').text.strip()
		unit_name = table.find('td').find_next('td').text
		sequence_units_list.append((unit_code, unit_name))

	return {'unit_set_code': unit_set_code, 'course_name': course_name, 'sequence_name': sequence_name, 'sequence_units_list': sequence_units_list}
	# example sequence dictionary entry:
		# {'unit_set_code': 'MN-S000008',
		# 'sequence_name': 'Programming',
		# 'sequence_units_list': [(unit_code, unit_name), (unit_code, unit_name)],
		# 'course_name': 'Bachelor of Information Technology',}


def test_sequence_guide():	
	units = sequence_guide_scraper("https://www.deakin.edu.au/current-students-courses/detail.php?customer_cd=C&service_item=S326&version_number=2&element_cd=MAJORS-STRUCTURE&sub_item_number=14&year=2022&return_to=%2Fcurrent-students-courses%2Fcourse.php%3Fcourse%3DS326%26keywords%3Dbachelor%2Bof%2Binformation%2Btechnology%26version%3D2%26year%3D2022")
	print(units)


def unit_scraper(url: str) -> dict:
	'''
	Scrape a unit guide page in the Deakin Handbook for the unit details.
	Returns a dictionary of the following format:
	Example of a unit dictionary entry:
	{'unit_code': 'STP050',
	 'unit_name': 'Academic Integrity (0 credit points)',
	 'unitguideURL': 'http://www.deakin.edu.au/current-students-courses/unit.php?unit=STP050&year=2022&return_to=%2Fcurrent-students-courses%2Fcourse.php%3Fcourse%3DS326%26keywords%3Dbachelor%2Bof%2Binformation%2Btechnology%26version%3D2%26year%3D2022'}
	 cont...
	'''
	response = requests.get(url)
	response.raise_for_status()
	soup = bs.BeautifulSoup(response.text, 'html.parser')

	details_table = soup.find('h2', text='Unit details').find_next('table')
	unit_details_raw = {}
	for row in details_table.find_all('tr'):
		header = row.find('th')
		column = row.find_all('td')
		if header and column:
			unit_details_raw[header.text.strip()] = column[0].text.strip()

	# create dictionary for a unit's availability in each trimester at each campus
	Trimester_Availability = {}
	list_of_trimesters = str(unit_details_raw['Enrolment modes:']).split('Trimester ')
	list_of_trimesters.pop(0)
	for trimester in list_of_trimesters:
		Burwood = False
		Geelong = False
		Cloud = False
		if 'Burwood' in trimester:
			Burwood = True
		if 'Geelong' in trimester:
			Geelong = True
		if 'Cloud' in trimester:
			Cloud = True
		Trimester_Availability[int(trimester[0])] = {'Burwood': Burwood, 'Geelong': Geelong, 'Cloud': Cloud}
	# How to access unit availability:
	# Trimester_Availability[1]['Burwood'] == True

	# get assignments table
	assignments_table = soup.find('h3', text='Assessment').find_next('table')
	# assignments table has four columns, "Assessment Description", "Student output", "Grading and weighting (% of total mark for unit", Indicative due week")
	assignmnents_list = []
	assignment_dict = {}
	for index, row in enumerate(assignments_table.find_all('tr')):
		for i, column in enumerate(row.find_all('td')):
			if i == 0:
				assignment_dict['assignment_description'] = column.text.strip()
			elif i == 1:
				assignment_dict['student_output'] = column.text.strip()
			elif i == 2:
				assignment_dict['weighting'] = column.text.strip()
			elif i == 3:
				assignment_dict['due_week'] = column.text.strip()
				assignmnents_list.append(assignment_dict)
				assignment_dict = {}
	
	Hurdle_Requirement_Text = soup.find('h3', text='Hurdle requirement')
	if Hurdle_Requirement_Text:
		Hurdle_Requirement_Text = Hurdle_Requirement_Text.find_next('p').text.strip()

	unit_details_raw.setdefault('Incompatible with:', 'Nil')

	# define return dictionary
	unit_details = {}
	unit_details['year_relevant'] = unit_details_raw['Year:'] # string
	unit_details['credit_points'] = unit_details_raw['Credit point(s):'] # string
	unit_details['EFTSL_value'] = unit_details_raw['EFTSL value:'] # string
	unit_details['incompatible_with'] = unit_details_raw['Incompatible with:'] # string
	unit_details['prerequisite'] = unit_details_raw['Prerequisite:'] # string
	unit_details['corequisite'] = unit_details_raw['Corequisite:'] # string
	unit_details['assignments'] = assignmnents_list # list
	unit_details['hurdle'] = Hurdle_Requirement_Text # string
	unit_details['trimester_availability'] = Trimester_Availability # dict

	return unit_details


def get_all_unit_links_from_handbook(course_handbook_url: str) -> list:
	course_data = deakin_handbook_scraper(course_handbook_url)
	# get all the links to units
	course_data = course_data['units']
	list_of_unit_urls = []
	for unit in course_data.values():
		list_of_unit_urls.append(unit['unitguideURL'])

	return list_of_unit_urls

def test_scrape_list_of_unit_urls_from_guidebook():

	IT_links = get_all_unit_links_from_handbook(
		"https://www.deakin.edu.au/current-students-courses/course.php?course=S326&version=2&year=2022&keywords=bachelor+of+information+technology")

	for link in IT_links:
		print(f"{colorama.Fore.RED}{link}{colorama.Fore.RESET}")
		pprint.pprint(unit_scraper(link))


def test_getting_unit_data():
	unit_url = r"https://www.deakin.edu.au/current-students-courses/unit.php?unit=SIT124&year=2022&return_to=%2Fcurrent-students-courses%2Fcourse.php%3Fcourse%3DS326%26keywords%3Da%26version%3D2%26year%3D2022"
	unit_data = unit_scraper(unit_url)
	pprint_color(unit_data)
# test_getting_unit_data()

