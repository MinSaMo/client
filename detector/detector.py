import speech_recognition as sr


class Detector:
	def __init__(self):
		self.r = sr.Recognizer()

	def detect(self, hotword: str, callback_func):
		print("Listening for hotword...")

		from main import DEV_MODE
		if DEV_MODE == 1:
			audio_file = sr.AudioFile('./news.wav')

			with audio_file as source:
				audio = self.r.record(source)

			spoken_text = self.r.recognize_google(audio, language="ko-KR")

			if hotword in spoken_text:
				print(f"Hotword '{hotword}' detected!")
				callback_func()

		else:
			with sr.Microphone() as source:
				try:
					audio = self.r.listen(source, timeout=5)
					spoken_text = self.r.recognize_google(
						audio, language="ko-KR").lower()
					if hotword in spoken_text:
						print(f"Hotword '{hotword}' detected!")
						callback_func()
				except sr.UnknownValueError:
					print("Could not understand audio")
				except sr.RequestError as e:
					print(f"Error with the Google API request; {e}")
				except KeyboardInterrupt:
					print("Listening stopped.")
