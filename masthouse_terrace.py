import pygame
import time
import requests
import json


YHEIGHTS = {
	'title': 32,
	'inbound title': 100,
	'inbound first': 150,
	'inbound sec': 200,
	'outbound title': 250,
	'outbound first': 300,
	'outbound sec': 350
}

# assigning values to X and Y variable
X = 800
Y = 400

# give a cooldown time of half a second - 500ms
COOLDOWN = 3000

# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

# define the RGB value for white,
# green, blue colour .
black = (0, 0, 0)
yellowish = (255, 211, 0)


# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font
font = pygame.font.Font('freesansbold.ttf', 32)


#init strings for storage later
inbound_dest_str = ""
outbound_dest_str = ""


####### 
# Web requests stuff
#######
# Hide api_key.json when being shown to the outside world

with open('api_key.json') as file:
    data = json.load(file)
params = data


while True:
	inbound_timing_1 = ""
	inbound_timing_2 = ""
	outbound_timing_1 = ""
	outbound_timing_2 = ""

	# NOTE: api.tfl is current, api.digital.tfl is LEGACY
	response_mht = requests.get("https://api.tfl.gov.uk/StopPoint/930GMHT/Arrivals", params=params)
	# print(response_mht.status_code)
	response_mht_json = response_mht.json()
	response_mht_js = sorted(response_mht_json, key=lambda d: (d['platformName'], d['timeToStation']))
	# counter = 0
	inbound_ctr = 0
	outbound_ctr = 0
	print(f"{len(response_mht_js)} elements")
	for i in range(len(response_mht_js)):
		element = response_mht_js[i]
		element_dict = dict(element)
		print(element_dict)
		print("")
		# Dunno what for do
		if len(response_mht_json) == 0:
			break
		# We got all we need
		if i > 4:
			break

		if((element_dict['direction'] == 'inbound') and (inbound_ctr == 0)):
			inbound_dest_str = element_dict['destinationName']
			inbound_timing_1 = str(round(element_dict['timeToStation'] / 60)) + " Mins"
			inbound_ctr += 1
			print(inbound_dest_str, inbound_timing_1)

		elif((element_dict['direction'] == 'inbound') and (inbound_ctr == 1)):
			inbound_timing_2 = str(round(element_dict['timeToStation'] / 60)) + " Mins"
			inbound_ctr += 1
			print(inbound_dest_str, inbound_timing_2)

		elif((element_dict['direction'] == 'outbound') and (outbound_ctr == 0)):
			outbound_dest_str = element_dict['destinationName']
			outbound_timing_1 = str(round(element_dict['timeToStation'] / 60)) + " Mins"
			outbound_ctr += 1
			print(outbound_dest_str, outbound_timing_1)

		elif((element_dict['direction'] == 'outbound') and (outbound_ctr == 1)):
			outbound_timing_2 = str(round(element_dict['timeToStation'] / 60)) + " Mins"
			outbound_ctr += 1
			print(outbound_dest_str, outbound_timing_2)


	# iterate over the list of Event objects
	# that was returned by pygame.event.get() method.
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			# deactivates the pygame library
			pygame.quit()
			# quit the program.
			quit()


	# create a text surface object,
	# on which text is drawn on it.
	title_text =  font.render('Masthouse Terrace Pier', True, yellowish)
	inbound_text =  font.render('Inbound', True, yellowish)
	outbound_text = font.render('Outbound', True, yellowish)
	inbound_dest_1_text =  font.render(inbound_dest_str, True, yellowish)
	outbound_dest_1_text = font.render(outbound_dest_str, True, yellowish)
	inbound_timing_1_text = font.render(inbound_timing_1, True, yellowish)
	if(inbound_ctr == 2):
		inbound_timing_2_text = font.render(inbound_timing_2, True, yellowish)
	outbound_timing_1_text = font.render(outbound_timing_1, True, yellowish)
	if(outbound_ctr == 2):
		outbound_timing_2_text = font.render(outbound_timing_2, True, yellowish)

	# create a rectangular object for the
	# text surface object
	title_rect =  title_text.get_rect()
	inbound_rect = inbound_text.get_rect()
	outbound_rect = outbound_text.get_rect()
	inbound_dest_1_rect = inbound_dest_1_text.get_rect()
	outbound_dest_1_rect = outbound_dest_1_text.get_rect()
	inbound_timing_1_rect = inbound_timing_1_text.get_rect()
	if(inbound_ctr == 2):
		inbound_timing_2_rect = inbound_timing_2_text.get_rect()
	outbound_timing_1_rect = outbound_timing_1_text.get_rect()
	if(outbound_ctr == 2):
		outbound_timing_2_rect = outbound_timing_2_text.get_rect()

	# create the display surface object
	# of specific dimension..e(X, Y).
	display_surface = pygame.display.set_mode((X, Y))
	# display_surface = pygame.display.set_mode((0, 0), int(pygame.FULLSCREEN/2))

	# set the pygame window name
	pygame.display.set_caption('piTFL Board')

	# set the center of the rectangular object.
	title_rect.center = (X / 2, YHEIGHTS['title'])

	inbound_rect.center = (X / 2, YHEIGHTS['inbound title'])
	inbound_dest_1_rect.left = 20
	inbound_dest_1_rect.centery = YHEIGHTS['inbound first']
	inbound_timing_1_rect.right = X - 20
	inbound_timing_1_rect.centery = YHEIGHTS['inbound first']
	if(inbound_ctr == 2):
		inbound_dest_2_rect = inbound_dest_1_rect.copy()
		inbound_dest_2_rect.centery = YHEIGHTS['inbound sec']
		inbound_timing_2_rect.right = X - 20
		inbound_timing_2_rect.centery = YHEIGHTS['inbound sec']


	outbound_rect.center = (X / 2, YHEIGHTS['outbound title'])
	outbound_dest_1_rect.left = 20
	outbound_dest_1_rect.centery = YHEIGHTS['outbound first']
	outbound_timing_1_rect.right = X - 20
	outbound_timing_1_rect.centery = YHEIGHTS['outbound first']
	if(outbound_ctr == 2):
		outbound_dest_2_rect = outbound_dest_1_rect.copy()
		outbound_dest_2_rect.centery = YHEIGHTS['outbound sec']
		outbound_timing_2_rect.right = X - 20
		outbound_timing_2_rect.centery = YHEIGHTS['outbound sec']


	# completely fill the surface object
	# with white color
	display_surface.fill(black)

	# copying the text surface object
	# to the display surface object
	# at the center coordinate.
	display_surface.blit(title_text, title_rect)

	display_surface.blit(inbound_text, inbound_rect)
	display_surface.blit(inbound_dest_1_text, inbound_dest_1_rect)
	display_surface.blit(inbound_timing_1_text, inbound_timing_1_rect)
	if(inbound_ctr == 2):
		display_surface.blit(inbound_dest_1_text, inbound_dest_2_rect)
		display_surface.blit(inbound_timing_2_text, inbound_timing_2_rect)

	display_surface.blit(outbound_text, outbound_rect)
	display_surface.blit(outbound_dest_1_text, outbound_dest_1_rect)
	display_surface.blit(outbound_timing_1_text, outbound_timing_1_rect)
	if(outbound_ctr == 2):
		display_surface.blit(outbound_dest_1_text, outbound_dest_2_rect)
		display_surface.blit(outbound_timing_2_text, outbound_timing_2_rect)

	# Draws the surface object to the screen.
	pygame.display.update()
	pygame.time.wait(10000)



