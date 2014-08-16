import ika


font = ika.Font("font.fnt")
lane1 = 130
lane2 = 160
win_height = 250		



donkeyroad = ika.Image("donkeyroad.png")
youwon = ika.Image("youwon.png")
youlost = ika.Image("youlost.png")

class Entity:

	#Color = ika.RGB(255,0,0)

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = 8
		self.height = 16
		self.ox = x #Origin x and y.
		self.oy = y
		
	def Update(self):
		pass

	def Render(self):
		ika.Video.Blit(self.img, self.x, self.y, False)

				

class Donkey(Entity):
	
	alive = 1
	
	img = ika.Image("donkey.png")

	def Update(self):
		self.y -= 1
        #if ika.Input.keyboard["UP"].Position():
        #    self.y -= 1
        #elif ika.Input.keyboard["DOWN"].Position():
        #    self.y += 1
		if self.y < 0:
			Entities[0].alive = 2

		if ika.Input.keyboard["LEFT"].Position():
			self.x = lane1
		
		elif ika.Input.keyboard["RIGHT"].Position():
			self.x = lane2
		           

class Car(Entity):
	
	img = ika.Image("car.png")

	def Update(self):
		self.y += 1
		if self.y > win_height:
			del self

Entities = [Donkey(lane1,win_height), Car (lane1, 0)]
   
   
def DetectCollision (box1, box2):
	"Returns a boolean evaluation of whether two boxes collide"
	if (box1.x  + box1.width >= box2.x
		and box1.x <= box2.x + box2.width
		and box1.y + box1.height >= box2.y
		and box1.y <= box2.y + box2.height):
			return True
	return False

def playagain():
	if ika.Input.keyboard['Y'].Pressed():
		Entities[0].alive = 1
		reset()
	if ika.Input.keyboard['N'].Pressed():
		ika.Exit()
		
def reset():
	length = len(Entities)
	while length > 2:
		Entities.pop(2)
		length = length - 1
	#Entities = Entities[:2]
	Entities[0].y = win_height
	Entities[1].y = 0
		

def MyRender():
	if Entities[0].alive == 1:
		ika.Image.Blit(donkeyroad, 0, 0, False)
		for entity in Entities:
			entity.Render()
	elif Entities[0].alive == 0:
		ika.Image.Blit(youlost, 0, 0, False)
		font.Print(90,220,"Yes (Y)")
		font.Print(200,220,"No (N)")
	elif Entities[0].alive == 2:
		ika.Image.Blit(youwon,0,0,False)
		font.Print(90,220,"Yes (Y)")
		font.Print(200,220,"No (N)")
	
	
def MyUpdate():
	
	if Entities[0].alive == 1:
		addEntity()
		for entity in Entities:
			entity.Update()
		for x in Entities[1:]:
			if DetectCollision(Entities[0], x):
				Entities[0].alive = 0
	if Entities[0].alive == 0:
		playagain()
	if Entities[0].alive == 2:
		playagain()
		
def addEntity():
	min = 0
	max = 10000
	if ika.Random(min, max) < 100:
		if ika.Random(1, 3) < 2:
			lane = lane1
		else: 
			lane = lane2
		Entities.append(Car(lane,0))
				
	
def MainLoop():
       
    last_update = 0

    ika.SetCaption("Get the donkey to the end of the road")

    while 1:
        #If 1/100th of a second has passed since the last update.

        if ika.GetTime() > last_update:

            """
            Updates ika's input functions with whatever the player
            is currently pressing.
            """
            ika.Input.Update()
           
            """
            Custom Update here. This is where your
            game's update code goes.
            """
            MyUpdate()
            ika.ProcessEntities() #Processes the map entities.


            """
            Sets the variable to the current time plus 1 so
            it knows what to check for the next update.
            """
            last_update = ika.GetTime()+1
               
        ika.Render() #Draws the map to screen

        """
        Custom Render Here. This is where things
        your game draws to screen go.
        """
        MyRender()

        """
        This is what actually puts all
        the new screen updates on the screen.
        """
        ika.Video.ShowPage()

MainLoop() #And finally this executes your new main loop so it actually runs.


