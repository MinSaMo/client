import speech_recognition as sr


class Detector:
	def __init__(self):
		self.r = sr.Recognizer()
		print(sr.Microphone.list_microphone_names())
		self.mic = sr.Microphone(device_index=2)

	def detect(self, hotword: str):
		print("Listening for hotword...")

		response = {
			"success": True,
			"error": None,
			"transcription": None
		}

		from main import DEV_MODE
		if DEV_MODE == 1:
			audio_file = sr.AudioFile('./news.wav')

			with audio_file as source:
				audio = self.r.record(source)

			spoken_text = self.r.recognize_google(audio, language="ko-KR")

			if hotword in spoken_text:
				print(f"Hotword '{hotword}' detected!")

		else:
			with self.mic as source:
				self.r.adjust_for_ambient_noise(source)
				audio = self.r.listen(source)

			try:
				response["transcription"] = self.r.recognize_google(audio, language='ko-KR')
			except sr.RequestError:
				# API was unreachable or unresponsive
				response["success"] = False
				response["error"] = "API unavailable"
			except sr.UnknownValueError:
				# speech was unintelligible
				response["error"] = "Unable to recognize speech"

			print(response)
