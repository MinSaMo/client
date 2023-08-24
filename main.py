import websocket

from detector import detector
from speaker import speaker

DEV_MODE = 0
WS_URL = 'ws://117.16.137.205:8080/client'


class Bro:
	def __init__(self):
		websocket.enableTrace(True)

		self.hotword = '바로'
		self.detector = detector.Detector()
		self.speaker = speaker.Speaker()
		self.ws = websocket.WebSocketApp(WS_URL, on_message=self.on_message)

		self.message_queue = []
		self.ws.run_forever()

	def on_message(self, msg):
		print(msg)

	def handle_message_queue(self):
		while self.message_queue:
			message = self.message_queue.pop(0)
			self.speaker.speak(message)

	def handle_socket_message(self, message):
		msg_type = message.get('msg_type', 0)
		if msg_type == 2:  # Assuming priority is indicated by msg_type value
			self.message_queue.append(message['message'])
			self.handle_message_queue()

	def run(self):
		while True:

			if len(self.message_queue) > 0:
				pass
			else:
				spoken_sentence = self.detector.detect(self.hotword)
				# send spoken_sentence via socket
				pass


if __name__ == "__main__":
	bro = Bro()

	bro.run()
