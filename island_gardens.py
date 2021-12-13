import pygame
import time
import requests
import json


YHEIGHTS = {
	'title': 32,
	'plat 1 title': 100,
	'plat 1 first': 150,
	'plat 1 sec': 200,
	'plat 2 title': 250,
	'plat 2 first': 300,
	'plat 2 sec': 350
}

# assigning values to X and Y variable
X = 800
Y = 400

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
platform_1_dest_str = ""
platform_1_timing_1 = ""
platform_1_timing_2 = ""

platform_2_dest_str = ""
platform_2_timing_1 = ""
platform_2_timing_2 = ""

####### 
# Web requests stuff
#######
# Hide me when being shown to the outside world

with open('api_key.json') as file:
    data = json.load(file)
params = data

while True:

	# NOTE: api.tfl is current, api.digital.tfl is LEGACY
	response_isl = requests.get("https://api.tfl.gov.uk/StopPoint/940GZZDLISL/Arrivals", params=params)
	print(response_isl.status_code)
	response_isl_json = response_isl.json()
	response_isl_js = sorted(response_isl_json, key=lambda d: (d['platformName'], d['timeToStation']))
	# counter = 0
	plat_1_ctr = 0
	plat_2_ctr = 0
	print(f"{len(response_isl_js)} elements")
	for i in range(len(response_isl_js)):
		element = response_isl_js[i]
		element_dict = dict(element)
		# Dunno what for do
		if len(response_isl_json) == 0:
			break
		# We got all we need
		if i > 4:
			break

		if((element_dict['platformName'] == 'Platform 1') and (plat_1_ctr == 0)):
			platform_1_dest_str = element_dict['destinationName']
			platform_1_timing_1 = str(round(element_dict['timeToStation'] / 60)) + " Mins"
			plat_1_ctr += 1
			print(platform_1_dest_str, platform_1_timing_1)

		elif((element_dict['platformName'] == 'Platform 1') and (plat_1_ctr == 1)):
			platform_1_timing_2 = str(round(element_dict['timeToStation'] / 60)) + " Mins"
			plat_1_ctr += 1
			print(platform_1_dest_str, platform_1_timing_2)

		elif((element_dict['platformName'] == 'Platform 2') and (plat_2_ctr == 0)):
			platform_2_dest_str = element_dict['destinationName']
			platform_2_timing_1 = str(round(element_dict['timeToStation'] / 60)) + " Mins"
			plat_2_ctr += 1
			print(platform_2_dest_str, platform_2_timing_1)

		elif((element_dict['platformName'] == 'Platform 2') and (plat_2_ctr == 1)):
			platform_2_timing_2 = str(round(element_dict['timeToStation'] / 60)) + " Mins"
			plat_2_ctr += 1
			print(platform_2_dest_str, platform_2_timing_2)

	# create a text surface object,
	# on which text is drawn on it.
	title_text =  font.render('Island Gardens DLR', True, yellowish)
	platform_1_text =  font.render('Platform 1', True, yellowish)
	platform_2_text = font.render('Platform 2', True, yellowish)
	platform_1_dest_1_text =  font.render(platform_1_dest_str, True, yellowish)
	platform_2_dest_1_text = font.render(platform_2_dest_str, True, yellowish)
	platform_1_timing_1_text = font.render(platform_1_timing_1, True, yellowish)
	platform_1_timing_2_text = font.render(platform_1_timing_2, True, yellowish)
	platform_2_timing_1_text = font.render(platform_2_timing_1, True, yellowish)
	platform_2_timing_2_text = font.render(platform_2_timing_2, True, yellowish)

	# create a rectangular object for the
	# text surface object
	title_rect =  title_text.get_rect()
	platform_1_rect = platform_1_text.get_rect()
	platform_2_rect = platform_2_text.get_rect()
	platform_1_dest_1_rect = platform_1_dest_1_text.get_rect()
	platform_2_dest_1_rect = platform_2_dest_1_text.get_rect()
	platform_1_timing_1_rect = platform_1_timing_1_text.get_rect()
	platform_1_timing_2_rect = platform_1_timing_2_text.get_rect()
	platform_2_timing_1_rect = platform_2_timing_1_text.get_rect()
	platform_2_timing_2_rect = platform_1_timing_2_text.get_rect()


	# create the display surface object
	# of specific dimension..e(X, Y).
	display_surface = pygame.display.set_mode((X, Y))
	# display_surface = pygame.display.set_mode((0, 0), int(pygame.FULLSCREEN/2))

	# set the pygame window name
	pygame.display.set_caption('piTFL Board')


	# set the center of the rectangular object.
	title_rect.center = (X / 2, YHEIGHTS['title'])



	platform_1_rect.center = (X / 2, YHEIGHTS['plat 1 title'])
	platform_1_dest_1_rect.left = 20
	platform_1_dest_1_rect.centery = YHEIGHTS['plat 1 first']
	platform_1_timing_1_rect.right = X - 20
	platform_1_timing_1_rect.centery = YHEIGHTS['plat 1 first']
	platform_1_dest_2_rect = platform_1_dest_1_rect.copy()
	platform_1_dest_2_rect.centery = YHEIGHTS['plat 1 sec']
	platform_1_timing_2_rect.right = X - 20
	platform_1_timing_2_rect.centery = YHEIGHTS['plat 1 sec']


	platform_2_rect.center = (X / 2, YHEIGHTS['plat 2 title'])
	platform_2_dest_1_rect.left = 20
	platform_2_dest_1_rect.centery = YHEIGHTS['plat 2 first']
	platform_2_timing_1_rect.right = X - 20
	platform_2_timing_1_rect.centery = YHEIGHTS['plat 2 first']
	platform_2_dest_2_rect = platform_2_dest_1_rect.copy()
	platform_2_dest_2_rect.centery = YHEIGHTS['plat 2 sec']
	platform_2_timing_2_rect.right = X - 20
	platform_2_timing_2_rect.centery = YHEIGHTS['plat 2 sec']


	# completely fill the surface object
	# with white color
	display_surface.fill(black)

	# copying the text surface object
	# to the display surface object
	# at the center coordinate.
	display_surface.blit(title_text, title_rect)

	display_surface.blit(platform_1_text, platform_1_rect)
	display_surface.blit(platform_1_dest_1_text, platform_1_dest_1_rect)
	display_surface.blit(platform_1_timing_1_text, platform_1_timing_1_rect)
	display_surface.blit(platform_1_dest_1_text, platform_1_dest_2_rect)
	display_surface.blit(platform_1_timing_2_text, platform_1_timing_2_rect)

	display_surface.blit(platform_2_text, platform_2_rect)
	display_surface.blit(platform_2_dest_1_text, platform_2_dest_1_rect)
	display_surface.blit(platform_2_timing_1_text, platform_2_timing_1_rect)
	display_surface.blit(platform_2_dest_1_text, platform_2_dest_2_rect)
	display_surface.blit(platform_2_timing_2_text, platform_2_timing_2_rect)


	# iterate over the list of Event objects
	# that was returned by pygame.event.get() method.
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			# deactivates the pygame library
			pygame.quit()
			# quit the program.
			quit()

		# Draws the surface object to the screen.
		pygame.display.flip()
		pygame.time.wait(3000)



