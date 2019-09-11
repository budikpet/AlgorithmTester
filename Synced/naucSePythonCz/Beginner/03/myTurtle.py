import turtle
from math import sin, radians

def square(length, rotation = 0):
	turtle.left(rotation)
	for i in range(4):
		turtle.forward(length)
		turtle.left(90)
		
def showFun():
	for x in range(180):
		print(x)

turtle.setworldcoordinates(0, -2, 1000, 2)
turtle.speed(10)
turtle.shape('turtle')

#square(100)
#square(100, 20)
#square(100, 40)

print(sin(180))
for x in range(999):
	y = sin(radians(x))
	turtle.goto(x, y)

turtle.exitonclick()
