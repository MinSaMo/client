import json
import threading
import time

import websocket

from detector import detector
from speaker import speaker

DEV_MODE = 1
WS_URL = 'ws://117.16.137.205:8080/client'
websocket.enableTrace(True)


class Daila:
	def __init__(self):
		self.detector = detector.Detector()
		self.speaker = speaker.Speaker()
		self.socket = websocket.WebSocketApp(
			url=WS_URL,
			on_message=lambda ws, msg: self.on_message(ws, msg),
			on_error=lambda ws, msg: self.on_error(ws, msg),
			on_close=lambda ws: self.on_close(ws),
			on_open=lambda ws: self.on_open(ws))
		self.response_queue = []
		self.request_queue = []

	def on_message(self, ws, msg):
		# msg = json.loads(msg.decode('utf-8'))
		print("on_message", msg)

	def on_error(self, ws, msg):
		print("on_error", msg)

	def on_close(self, ws):
		print("on_close")

	def on_open(self, ws):
		print("on_open")

		while True:
			if len(self.request_queue) > 0:
				req = self.request_queue.pop()
				print(req)
				ws.send(req)

	def run_thread(self):
		self.socket.run_forever()

	def run_detector(self):
		while True:
			if len(self.response_queue) == 0:
				spoken_sentence = self.detector.detect()
				msg = {
					"sender": "CLIENT",
					"data": {
						"script": spoken_sentence['transcription'],
						"dialogId": 1
					}
				}
				str_msg = json.dumps(msg, ensure_ascii=False)
				self.request_queue.append(str_msg)
			time.sleep(10)

	def run_speaker(self):
		while True:
			if len(self.response_queue) > 0:
				print("run_speaker", self.response_queue[-1])
				# self.speaker.ttsKR(self.response_queue[-1])
				self.response_queue.pop()
			time.sleep(1)

	def run(self):
		socket_thread = threading.Thread(target=self.run_thread)
		detector_thread = threading.Thread(target=self.run_detector)
		speaker_thread = threading.Thread(target=self.run_speaker)

		socket_thread.start()
		detector_thread.start()
		speaker_thread.start()

		socket_thread.join()
		detector_thread.join()
		speaker_thread.join()


if __name__ == "__main__":
	daila = Daila()

	daila.run()
#
#
# def on_message(ws, message):
# 	print(message)
#
#
# def on_error(ws, error):
# 	print(error)
#
#
# def on_close(ws, close_status_code, close_msg):
# 	print("### closed ###")
#
#
# def on_open(ws):
# 	def run(*args):
# 		for i in range(3):
# 			# send the message, then wait
# 			# so thread doesn't exit and socket
# 			# isn't closed
# 			ws.send("Hello %d" % i)
# 			time.sleep(1)
#
# 		time.sleep(1)
# 		ws.close()
# 		print("Thread terminating...")
#
# 	threading.Thread(target=run).start()
#
#
# if __name__ == "__main__":
# 	websocket.enableTrace(True)
#
# 	ws = websocket.WebSocketApp(WS_URL,
# 								on_message=on_message,
# 								on_error=on_error,
# 								on_close=on_close)
# 	ws.on_open = on_open
# 	ws.run_forever()
