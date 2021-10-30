import pygame
import time
import random
import math
pygame.init()


green1 = (163, 235, 177)
green2 = (30, 81, 40)
blue = (4, 236, 240)
white = (255,255,255)
mauve = (136, 123, 176)
mustard = (226, 194, 117)
peach = (249, 179, 132)
peach2 = (255, 195, 139)
yellow = (250, 208, 44)
happy_yellow = (247, 253, 4)
black = (25, 26, 25)

dis_width, dis_height = 600, 600
snake_block = 10
#count = 0
#snake_speed = 12

font_style = pygame.font.SysFont('Cooper Black',40)
font_intro1 = pygame.font.SysFont('Ink Free Regular', 55)
font_intro2 = pygame.font.SysFont('Bradley Hand ITC Regular', 30)
font_paused = pygame.font.SysFont('Jokerman',65)
font_score = pygame.font.SysFont('Gabriola',30)
#font_style = pygame.font.Font("C:\Windows\Fonts\COOPBL.ttf", 50)


dis = pygame.display.set_mode((dis_width,dis_height))
pygame.display.set_caption("The pp game")
pygame.display.update()

clock = pygame.time.Clock()

#file highscore
f_high = open("pp_highscore.txt", "r+")
highscore = f_high.read()
highscore = int(highscore)

def message(msg, font_style, color, x, y):
	msg = font_style.render(msg, True, color)
	dis.blit(msg, [x , y ])

def your_sore(score):
	global highscore

	val = font_score.render("Happy meter: "+ str(score) , True, yellow )
	dis.blit(val, [2,2])
	paus = font_score.render("Press p to pause", True, peach2)
	dis.blit(paus, [(3*dis_width)/4, 2])
	hscore = font_score.render("Highscore: " + str(highscore), True, yellow)
	dis.blit(hscore,[(3*dis_width)/4, 35])

	#updating highscore
	if score > highscore :
		highscore = score

def our_snake(snake_block , snake_list):
	tog=0
	for x in snake_list:
		if tog%2==0:
			colour = green2

		else :
			colour = green1
		pygame.draw.rect(dis,colour,[x[0],x[1],snake_block,snake_block])
		tog+=1

def game_pause(snake_length):
	global highscore
	dis.fill(black)
	message("GAME PAUSED", font_paused, mauve, dis_width/8-30, dis_height/4)
	message("Your score: "+ str(snake_length-1), font_style, mustard, dis_width/4, dis_height/2)
	message("press p to play", font_score, peach2, dis_width/4+65, (3*dis_height)/4)
	message("press q to quit", font_score, peach2, dis_width/4+65, (3*dis_height)/4+40)
	pygame.display.update()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					return
				if event.key == pygame.K_q:
				
					f_high.seek(0)
					f_high.write(str(highscore))
					f_high.close()
					pygame.quit()
					quit()


def game_start():
	dis.fill(black) #bg color
	message("Hemlo, this is Snakey", font_intro1, mustard, dis_width/4 - 35, dis_height/4)
	message("Since you're already here, ig you wouldn't mind to guide ", font_intro2, mustard, 20, dis_height/4 + 50)
	message("me to some yumm treats hehe", font_intro2, mustard, dis_width/4, dis_height/4 + 80)
	message("press y to play n to quit",font_score, mauve, dis_width/3- 25 , dis_height/2)
	pygame.display.update()

	while True :
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_y:
					game_loop()
				elif event.key == pygame.K_n:
					dis.fill(black)
					message("Snakey got sad and crawled ", font_intro1, peach, 45, dis_height/4)
					message("back into his hole",font_intro1, peach, dis_width/4 - 16, dis_height/4 + 50)
					message("(and bit you on his way)",font_score, peach2, dis_width/4 + 22, dis_height/2)
					pygame.display.update()
					pygame.time.delay(4500)

					global highscore
					f_high.seek(0)
					f_high.write(str(highscore))
					f_high.close()
					pygame.quit()
					quit()


def game_loop():

	global highscore
	game_over = False
	game_close = False
	snake_speed = 12
	ate =  False
	circle_dis = False
	count = 0
	fcount = 0
	xcircle , ycircle = dis_width+10 , dis_height+10

	xS, yS = dis_width/2, dis_height/2
	xS_change, yS_change = 0, 0
	snake_length = 1
	snake_list = []

	xf = round(random.randrange(0+ snake_block, dis_width - 2*snake_block) / 10.0) * 10.0
	yf = round(random.randrange(65, dis_height - 2*snake_block-2) / 10.0) * 10.0

	while not game_over:

		while game_close == True:
			dis.fill(black)
			message("GAME OVER", font_paused, mauve, dis_width/8+30, dis_height/4)
			message("Your score: "+ str(snake_length-1), font_style, mustard, dis_width/4 + 30, dis_height/2)
			if highscore == snake_length-1 :
				message("New Highscore!! ", font_style, mauve, dis_width/4, dis_height/2+50)
			message("Press q to quit", font_score, peach2, dis_width/4 +75, (3*dis_height)/4)
			message("Press c to play again", font_score, peach2, dis_width/4 + 50 , (3*dis_height)/4 + 40)
			pygame.display.update()	

			for event in pygame.event.get():
				if event.type == pygame.QUIT :
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						game_over = True
						game_close = False
					elif event.key == pygame.K_c:
						game_loop()

		#pygame.draw.rect(dis,green1,[dis_width/2,2,snake_block,snake_block]) not effin working

		for event in pygame.event.get():
			#print(event)
			if event.type == pygame.QUIT :
				game_over = True	

			if event.type == pygame.KEYDOWN :
				if event.key == pygame.K_LEFT or event.key== pygame.K_a:
					xS_change = -snake_block
					yS_change = 0
				elif event.key == pygame.K_RIGHT or event.key== pygame.K_d:
					xS_change = snake_block
					yS_change = 0
				elif event.key == pygame.K_DOWN or event.key== pygame.K_s:
					xS_change = 0
					yS_change = snake_block
				elif event.key == pygame.K_UP or event.key== pygame.K_w:
					xS_change = 0
					yS_change = -snake_block	
				#pause
				elif event.key == pygame.K_p:
					game_pause(snake_length)

		xS += xS_change
		yS += yS_change	

		if xS>dis_width or xS<0 or yS>dis_height or yS<0 :   # changed <= to <
			game_close = True	

		#popping bonus
		if count>=200 and not circle_dis:
			xcircle = round(random.randrange(0 + snake_block, dis_width - 2*snake_block)/ 10.0) * 10.0
			ycircle = round(random.randrange(65 , dis_height - 2*snake_block)/ 10.0)* 10.0
			circle_dis = True

		dis.fill(black)
		pygame.draw.rect(dis,blue,[xf,yf,snake_block,snake_block])
		#pygame.draw.rect(dis,yellow,[xcircle, ycircle , snake_block, snake_block ])
		pygame.draw.circle(dis, yellow, (xcircle,ycircle), int(snake_block), int(snake_block)) 
		#pygame.draw.rect(dis,green1,[xS,yS,snake_block,snake_block])

		snake_head = []
		snake_head.append(xS)
		snake_head.append(yS)
		snake_list.append(snake_head)
		if len(snake_list)> snake_length:
			del snake_list[0]

		for x in snake_list[:-1]:
			if x== snake_head:
				game_close = True

		our_snake(snake_block ,snake_list)
		your_sore(snake_length-1)

		pygame.display.update()	

		if fcount>=(100 - snake_speed/5.0):
			xf = round(random.randrange(0+ snake_block, dis_width - 2*snake_block) / 10.0) * 10.0
			yf = round(random.randrange(65, dis_height - 2*snake_block) / 10.0) * 10.0
			fcount = 0

		if xS == xf and yS == yf:
			xf = round(random.randrange(0+ snake_block, dis_width - 2*snake_block) / 10.0) * 10.0
			yf = round(random.randrange(65, dis_height - 2*snake_block) / 10.0) * 10.0
			ate = True
			fcount = 0
			#pygame.display.update()
			snake_length +=1

		#if bonus collected
		dist = math.sqrt ((xcircle - xS)**2 + (ycircle - yS)**2)
		if dist<= snake_block :
			snake_length +=3
			xcircle, ycircle = dis_width+10 , dis_height+10
			count = 0
			circle_dis = False

		#if bonus missed
		if count>=300 and circle_dis:
			#delete circle
			xcircle, ycircle = dis_width+10 , dis_height+10
			count = 0
			circle_dis = False

		if snake_length % 4==0 and ate:
			#global snake_speed 
			snake_speed +=1
			ate = False

		count += 1
		fcount += 1
		clock.tick(snake_speed)

	f_high.seek(0)
	f_high.write(str(highscore))
	f_high.close()
	pygame.quit()
	quit()

	#f_high.close()
	#quit()

game_start()


#game_loop()
