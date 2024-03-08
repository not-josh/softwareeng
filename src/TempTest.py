from pygame import Rect

class Temp():
	def __init__(self) -> None:
		self._x:float = 0
		self._y:float = 0
		self.__rect = Rect(0,0,10,10)
		self.__rect.center = (round(self._x), round(self._y))
	
	@property
	def x(self): return self._x
	@property
	def y(self): return self._y
	@property
	def pos(self): return (self._x, self._y)

	@property
	def center(self): return self.__rect.center

	@x.setter
	def x(self, newx):
		print("X-Set: %d -> %d" % (self._x, newx))
		self._x = newx
		self.__rect.centerx = round(newx)
		self._pos = (self._x, self._y)
		pass

	@y.setter
	def y(self, newy):
		print("Y-Set")
		self._y = newy
		self.__rect.centery = round(newy)
		self._pos = (self._x, self._y)
		pass

	@pos.setter
	def pos(self, newp):
		print("Pos-Set")
		pass

	@center.setter
	def center(self, newc):
		print("Center-Set")
		




obj = Temp()
obj.x /= 10
obj.y = 5
obj.__rect = 0
obj.center = (3,3)
obj.pos = (1,2)