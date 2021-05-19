import socket
import threading
import sys

PORT = 12345
# HOST = socket.gethostbyname(socket.gethostname())
HOST = '127.0.0.1'

try:
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except:
	print("Socket cannot be created..")
	sys.exit()

try:
	client.connect((HOST, PORT))
except:
	print("Cannot connected to server")
	client.close()
	sys.exit()

nickname = input("Enter nickname: ")


def recieve_message():
	global nickname
	while True:
	# 	msg = ''
	# 	while True:
	# 		m = client.recv(8).decode('utf-8')
	# 		if len(m) == 0:
	# 			break
	# 		msg += m
		msg = client.recv(1024).decode('utf-8')
		# print("........Every time message.............. ",msg)
		if msg == "Nickname":
			client.send(nickname.encode('utf-8'))
		elif msg == "Notavailable":
			# nickname =  input("Nickname is already taken please try another one: ")
			# client.send(nickname.encode('utf-8')) 
			print("Nickname is already taken please try another one: ")
			send_message()
		elif msg == "enter 1 to Create chatroom or 2 to join chatroom":
			# answer = input("Enter 1 to create new chatroom or 2 to join chatroom: ")
			# client.send(answer.encode('utf-8'))
			print(("Enter 1 to create new chatroom or 2 to join chatroom: "))
			send_message()
		elif msg == "Enter room name for your new chatrooms: ":

			# room_name = input("Enter room name for your new chatroom:  ")
			# client.send(room_name.encode('utf-8'))
			print("Enter room name for your new chatroom:  ")
			send_message()
		elif msg == "Enter name of chatroom to join: ":
			# room_name = input("Enter name of chatroom to join:  ")
			# client.send(room_name.encode('utf-8'))
			print("Enter name of chatroom to join:  ")
			send_message()
		else:
			print(msg)


def send_message():
	while True:
		message ='{}'.format(input(''))
		client.send(message.encode('utf-8'))

# lock = threading.Lock()

recieve_thread = threading.Thread(target = recieve_message)
recieve_thread.start()

send_thread = threading.Thread(target = send_message)
send_thread.start()

