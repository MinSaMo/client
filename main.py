from socket import *

from detector import detector
from microphone import microphone
from speaker import speaker

DEV_MODE = 1

HOST = '117.16.137.205'
PORT = 8080
BUFSIZE = 1024
ADDR = (HOST, PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(ADDR)


class Bro:
	def __init__(self):
		self.hotword = '윤석열'
		self.detector = detector.Detector()
		self.speaker = speaker.Speaker()
		self.mic = microphone.Microphone()

		self.message_queue = []

	def handle_message_queue(self):
		while self.message_queue:
			message = self.message_queue.pop(0)
			self.speaker.speak(message)

	def handle_socket_message(self, message):
		msg_type = message.get('msg_type', 0)
		if msg_type == 2:  # Assuming priority is indicated by msg_type value
			self.message_queue.append(message['message'])
			self.handle_message_queue()

	def turn_on(self):
		pass

	def turn_off(self):
		pass

	def message_handler(self, data):
		print('I received a message!')
		print(data)

	def listen(self):
		self.speaker.speak('네, 말씀하세요.')

		# record user's voice
		sentence = self.mic.record()

		clientSocket.send('Hello!'.encode())

	def run(self):
		while True:
			self.detector.detect(self.hotword, self.listen)


if __name__ == "__main__":
	bro = Bro()

	bro.run()
