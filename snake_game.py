import pygame
import random

white = (255,255,255)
red = (255,0,0)
blue = (30,144,255)
yellow = (255,215,0)
green = (50,205,50)
purple = (128,0,128)
gray = (128,128,128)


class Cube():
	width = 800
	rows = 40
	direction_x = 1
	direction_y = 0

	def __init__(self, start, color, direction_x=1, direction_y=0):
		self.position = start
		self.color = color
		self.direction_x = 1
		self.direction_y = 0

	def move(self, direction_x, direction_y):
		self.direction_x = direction_x
		self.direction_y = direction_y
		self.position = (self.position[0] + direction_y, self.position[1] + direction_x)

	def draw(self, window, head):
		distance = self.width // self.rows
		row = self.position[1]
		column = self.position[0]
		if head:
			pygame.draw.rect(window, yellow,
							 (row * distance + 1, column * distance + 1, distance - 1, distance - 1))
		else:
			pygame.draw.rect(window, self.color,
							 (row * distance + 1, column * distance + 1, distance - 1, distance - 1))


class Snake():
	width = 800
	rows = 40
	body = []
	turns = {}

	def __init__(self, start, body, turns, color):
		self.body = body
		self.turns = turns
		self.color = color
		self.position = start
		self.direction_x = 0
		self.direction_y = 0
		self.head = Cube(self.position, self.color, 1, 0)
		self.body.append(self.head)


	def move(self, up, down, left, right):
		self.up = up
		self.down = down
		self.left = left
		self.right = right

		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				pygame.quit()

		keys = pygame.key.get_pressed()

		for key in keys:
			if keys[self.up]:
				self.direction_x = 0
				self.direction_y = -1
				self.turns[self.head.position[:]] = [self.direction_y, self.direction_x]
			elif keys[self.down]:
				self.direction_x = 0
				self.direction_y = 1
				self.turns[self.head.position[:]] = [self.direction_y, self.direction_x]
			elif keys[self.left]:
				self.direction_x = -1
				self.direction_y = 0
				self.turns[self.head.position[:]] = [self.direction_y, self.direction_x]
			elif keys[self.right]:
				self.direction_x = 1
				self.direction_y = 0
				self.turns[self.head.position[:]] = [self.direction_y, self.direction_x]

		for index, cube in enumerate(self.body):
			positions = cube.position[:]

			if positions in self.turns:
				turn = self.turns[positions]
				cube.move(turn[1], turn[0])
				if index == len(self.body) - 1:
					self.turns.pop(positions)
			else:
				if cube.direction_y == -1 and cube.position[0] < 0:
					cube.position = (cube.rows - 1, cube.position[1])
				elif cube.direction_y == 1 and cube.position[0] >= cube.rows:
					cube.position = (0, cube.position[1])
				elif cube.direction_x == -1 and cube.position[1] < 0:
					cube.position = (cube.position[0], cube.rows - 1)
				elif cube.direction_x == 1 and cube.position[1] >= cube.rows:
					cube.position = (cube.position[0], 0)
				else:
					cube.move(cube.direction_x, cube.direction_y)

	def reset(self, window):
		self.head = Cube(window)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.direction_x = 1
		self.direction_y = 0

	def addCube(self):
		tail = self.body[-1]
		if tail.direction_x == 1 and tail.direction_y == 0:
			self.body.append(Cube((tail.position[0], tail.position[1] - 1), self.color))
		elif tail.direction_x == -1 and tail.direction_y == 0:
			self.body.append(Cube((tail.position[0], tail.position[1] + 1), self.color))
		elif tail.direction_x == 0 and tail.direction_y == 1:
			self.body.append(Cube((tail.position[0] - 1, tail.position[1]), self.color))
		elif tail.direction_x == 0 and tail.direction_y == -1:
			self.body.append(Cube((tail.position[0] + 1, tail.position[1]), self.color))

		self.body[-1].direction_x = tail.direction_x
		self.body[-1].direction_y = tail.direction_y

	def draw(self, window):
		for index, cube in enumerate(self.body):
			if index == 0:
				cube.draw(window, True)
			else:
				cube.draw(window, False)


def draw_grid(width, rows, window):
	gap = width // rows
	x_pos = 0
	y_pos = 0
	for line in range(rows):
		x_pos = x_pos + gap
		y_pos = y_pos + gap
		pygame.draw.line(window, white, (x_pos, 0), (x_pos, width))
		pygame.draw.line(window, white, (0, y_pos), (width, y_pos))


def random_snack(rows):
	x = random.randrange(rows)
	y = random.randrange(rows)
	return (x, y)


def redraw_window(window):
	global rows, width, snake1, snake2, snack
	window.fill((0, 0, 0))
	snake1.draw(window)
	snake2.draw(window)
	snack.draw(window, False)
	draw_grid(width, rows, window)
	pygame.display.update()


def main():
	global width, rows, window, snake1, snake2, snack
	width = 800
	rows = 40
	body1 = []
	body2 = []
	turns1 = {}
	turns2 = {}
	window = pygame.display.set_mode((width, width))
	pygame.display.set_caption('Snake Game')
	snake1 = Snake((5, 5), body1, turns1, blue)
	snake2 = Snake((25, 25),body2, turns2, red)
	snack = Cube(random_snack(rows), green, 1, 0)
	flag = True
	clock = pygame.time.Clock()

	while flag:
		window.fill((0, 0, 0))
		pygame.time.delay(50)
		clock.tick(10)

		snake1.move(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
		snake2.move(pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

		if snake1.body[0].position == snack.position:
			snake1.addCube()
			snack = Cube(random_snack(rows), (0, 255, 0), 1, 0)

		for index, body_element in enumerate(snake1.body[1:]):
			if snake1.body[0].position == body_element.position:
				print('You lost! Your score is:', len(snake1.body))
				snake1.reset((5, 5))
				break

		redraw_window(window)


main()
