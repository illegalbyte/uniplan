import bs4 as bs
import requests
import os
import pprint


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

	return {'course_code': course_code, 'course_name': course_name, 'course_map_url': course_map_url, 'units': units}


	# Example of a unit dictionary entry:
	#  'STP050': {'unit_code': 'STP050',
	#             'unit_name': 'Academic Integrity (0 credit points)',
	#             'unitguideURL': 'http://www.deakin.edu.au/current-students-courses/unit.php?unit=STP050&year=2022&return_to=%2Fcurrent-students-courses%2Fcourse.php%3Fcourse%3DS326%26keywords%3Dbachelor%2Bof%2Binformation%2Btechnology%26version%3D2%26year%3D2022'}}


def sequence_guide_scraper(url: str) -> list:
	'''
	Scrape a major/minor sequence page in the Deakin Handbook for units contained in that sequence.
	Returns a list of touples the unit codes contained in the sequence.
	'''
	response = requests.get(url)
	response.raise_for_status()
	soup = bs.BeautifulSoup(response.text, 'html.parser')

	all_units_tables = soup.find_all('table')

	sequence_units = []

	for table in all_units_tables: 
		unit_code = table.find('td').text.strip()
		unit_name = table.find('td').find_next('td').text
		sequence_units.append(unit_code)

	return sequence_units


def test_sequence_guide():	
	units = sequence_guide_scraper("https://www.deakin.edu.au/current-students-courses/detail.php?customer_cd=C&service_item=S326&version_number=2&element_cd=MAJORS-STRUCTURE&sub_item_number=14&year=2022&return_to=%2Fcurrent-students-courses%2Fcourse.php%3Fcourse%3DS326%26keywords%3Dbachelor%2Bof%2Binformation%2Btechnology%26version%3D2%26year%3D2022")
	print(units)