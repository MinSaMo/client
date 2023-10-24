import speech_recognition as sr


class Detector:
	def __init__(self):
		self.r = sr.Recognizer()
		print(sr.Microphone.list_microphone_names())
		self.mic = sr.Microphone(device_index=2)

	def detect(self):
		print("Listening...")

		response = {
			"success": True,
			"error": None,
			"transcription": None
		}

		from main import DEV_MODE
		if DEV_MODE == 1:
			try:
				response["transcription"] = 'REST API에 대해 설명해줘'
				response["success"] = True
			except sr.UnknownValueError:
				response["error"] = "Unable to recognize speech"
				response["success"] = False
		else:
			with self.mic as source:
				self.r.adjust_for_ambient_noise(source)
				audio = self.r.listen(source)

			try:
				response["transcription"] = self.r.recognize_google(audio, language='ko-KR')
			except sr.RequestError:
				response["success"] = False
				response["error"] = "API unavailable"
			except sr.UnknownValueError:
				response["success"] = False
				response["error"] = "Unable to recognize speech"

		return response
