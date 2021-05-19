import socket 
import threading
import sys
import pickle



PORT = 12345
connections = dict()
number_of_chatrooms = 0
current_chatrooms = dict()
information = dict()

try:
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print("Socket is created successfully..")
except socket.error as err:
	print("Socket cannot be created...",err)
	sys.exit()

try:
	server.bind(("127.0.0.1",PORT))
	print("Server is binded successfully to port",PORT)
except:
	print("Server binding failed")
	server.close()
	sys.exit()

server.listen(100)
print("Server has started listening ..........")


def unique_nickname(nickname):
	''' Checks whether nickname is available or not'''

	while nickname in connections.keys():
		con.sendall("Notavailable".encode('utf-8'))
		nickname = con.recv(1024).decode('utf-8')
	
	return nickname


def store_messages(msg, room_name):
	# current_chatrooms[room_name]['messages'].append(msg)
	
	information[room_name]['messages'].append(msg)
	

	with open("messages.pickle","wb") as f:
		pickle.dump(information,f)

def broadcast_message(msg, nickname,con,room_name):
	''' sendalls message to everyone in chatroom '''

	msg = nickname +' : '+ msg.decode('utf-8')
	store_messages(msg,room_name)
	user_list = current_chatrooms[room_name]['users']
	for connection in user_list:
		if connection != nickname:
			user_list[connection].sendall(msg.encode('utf-8'))


def client_thread(nickname,con, name):
	''' Main client Thread which recieves message from client and broadcast to other clients'''

	user_list = current_chatrooms[name]['users']
	room_name = name
	while True:
		try:
			message = con.recv(1024)
			print(message.decode('utf-8'))
			broadcast_message(message,nickname,con, name)
		except:
			del current_chatrooms[name]['users'][nickname]
			broadcast_message(f"{nickname} has left chatroom !!!".encode('utf-8'),nickname,con, connections)
			con.close()
			break


def join_chatrooms(con, nickname, room_name):
	print("in join function")
	users = current_chatrooms[room_name]['users']
	users[nickname] = con
	current_chatrooms[room_name]['users'] = users

	information[room_name] = dict()
	information[room_name]['name'] = room_name
	information[room_name]['created_by'] = current_chatrooms[room_name]['created_by']
	information[room_name]['users'] = list(current_chatrooms[room_name]['users'].keys())
	information[room_name]['messages'] = []
	broadcast_message(f"{nickname} has joined the chatroom".encode('utf-8'),nickname,con,name)
	# con.sendall("Connected to server!".encode('utf-8'))
	con.sendall("Welcome to the chatroom !\n".encode('utf-8'))
	t = threading.Thread(target = client_thread, args = (nickname,con,name)).start()



def create_chatroom(con,nickname,room_name):
	room_detail = dict()
	room_detail["name"] = room_name
	room_detail['users'] = dict()
	room_detail['created_by'] = nickname
	# room_detail['messages'] = []
	current_chatrooms[room_name] = room_detail

	print("room_detail",room_detail)

	con.sendall(f"{name} created successfuly..".encode('utf-8'))



while True:
	con, addr = server.accept()
	print("Connection established with address \n",addr)
	con.sendall("Nickname".encode('utf-8'))
	nickname = con.recv(1024).decode('utf-8')
	nickname = 	unique_nickname(nickname)
	connections[nickname] = con
	con.sendall("enter 1 to Create chatroom or 2 to join chatroom \n".encode('utf-8'))
	response = con.recv(1024).decode('utf-8')
	
	if response == '1':
		con.sendall("Enter room name for your new chatrooms: \n".encode('utf-8'))
		name = con.recv(1024).decode('utf-8')
		# room = threading.Thread(target = create_chatroom, args = (con, nickname,name)).start()
		create_chatroom(con,nickname,name)
		# current_chatrooms['name'] = name
		number_of_chatrooms += 1
		con.sendall("Availabel chatrooms: \n".encode('utf-8'))
		for keys in current_chatrooms:
			con.sendall(f"{keys}\n".encode('utf-8'))
		con.sendall("Enter name of chatroom to join: \n".encode('utf-8'))
		answer = con.recv(1024).decode('utf-8')
		join_chatrooms(con,nickname,answer)

	elif response == '2':

		con.sendall("Availabel chatrooms: \n".encode('utf-8'))
		for keys in current_chatrooms:
			con.sendall(f"{keys}\n".encode('utf-8'))
		con.sendall("Enter name of chatroom to join: \n".encode('utf-8'))
		answer = con.recv(1024).decode('utf-8')
		join_chatrooms(con,nickname,answer)


		# con.sendall("Availabel chatrooms: \n".encode('utf-8'))
		# for keys in current_chatrooms:
		# 	con.sendall(keys.encode('utf-8'))
		# con.sendall("Enter name of chatroom to join: \n".encode('utf-8'))
		# answer = con.recv(1024).decode('utf-8')
		# join_chatrooms(con,nickname,answer)
