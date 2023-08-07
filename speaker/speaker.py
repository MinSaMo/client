from main import DEV_MODE


class Speaker:
	def speak(self, text):
		if DEV_MODE == 1:
			self.print_console(self, text)
		else:
			self.play_speaker(self, text)

	@staticmethod
	def print_console(text):
		print(text)

	@staticmethod
	def play_speaker(text):
		# TBD
		print(text)
