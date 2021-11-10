import itertools
import threading
import time
import sys

class Animate:
	AnimationType = "encrypt" or "decrypt"
	def __init__(self) -> None:
		self.done = False

	def animate(self, text:str)->None:
		for c in itertools.cycle([".  ", ".. ", "...", "   "]):
			if self.done:
				self.done = False
				break
			sys.stdout.write(f"\r{text}ing {c}")
			sys.stdout.flush()
			time.sleep(0.5)
		sys.stdout.write(f"\r{text}ed!     \n")


	def startAnimation(self, animationType:AnimationType)->None:
		t = threading.Thread(target=self.animate, args=[animationType])
		t.start()

	def stopAnimation(self)->None:
		self.done = True
		time.sleep(0.8)