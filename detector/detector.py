import speech_recognition as sr


class Detector:
	def __init__(self):
		self.r = sr.Recognizer()

	def detect(self, hotword: str, callback_func):
		with sr.Microphone() as source:
			print("Listening for hotword...")
			while True:
				try:
					audio = self.r.listen(source, timeout=5)
					spoken_text = self.r.recognize_google(audio, language="en-US").lower()
					if hotword in spoken_text:
						print(f"Hotword '{hotword}' detected!")
						callback_func()
				except sr.UnknownValueError:
					print("Could not understand audio")
				except sr.RequestError as e:
					print(f"Error with the Google API request; {e}")
				except KeyboardInterrupt:
					print("Listening stopped.")
					break
