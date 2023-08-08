from main import DEV_MODE


class Speaker:
	def speak(self, text):
		if DEV_MODE == 1:
			self.print_console(text)
		else:
			self.play_speaker(text)

	def print_console(self, text):
		print(text)

	def play_speaker(self, text):
		# TBD
		print(text)
