from detector.detector import Detector
from microphone.microphone import Microphone
from socket.socket import Socket
from speaker.speaker import Speaker

SOCKET_URL = 'TBD'
DEV_MODE = 1


class Bro:
	def __init__(self):
		self.hotword = 'Bro'
		self.detector = Detector()
		self.speaker = Speaker()
		self.socket = Socket()
		self.mic = Microphone()

		self.socket.connect(SOCKET_URL)
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

	def listen(self):
		self.speaker.speak('네, 말씀하세요.')

		# record user's voice
		sentence = self.mic.record()

		self.socket.emit('bro', {
			'message': sentence,
			'msg_type': 2
		})

	def run(self):
		self.detector.detect(self.hotword, self.listen)

		while True:
			socket_message = self.socket.listen()  # this method waits for incoming messages
			self.handle_socket_message(socket_message)


if __name__ == "__main__":
	bro = Bro()

	bro.run()
