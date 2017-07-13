"""
Credits:
	stats,getConfig,writeTime,readTimes based on code by https://www.reddit.com/user/Storbod
	https://github.com/Storbod/Python-Cube-Timer
	Scrambles are generated with pyTwistyScrambler
	https://github.com/euphwes/pyTwistyScrambler
	subx based on code by https://www.reddit.com/user/yovliporat
	https://drive.google.com/file/d/0B7qI7oJsiTPGcjY2VlpoQi1hLVU/view
"""
from pyTwistyScrambler import scrambler222, scrambler333, scrambler444,\
	scrambler555, scrambler666, scrambler777, squareOneScrambler, \
	pyraminxScrambler, skewbScrambler, clockScrambler
import datetime,time
from collections import OrderedDict
from math import ceil, floor, sqrt
import csv
import os, sys
import configparser
import keyboard

def getConfig():
	configValues = dict()
	config = configparser.ConfigParser()
	config.read("config.ini")
	for key in config["DEFAULT"]:
		configValues[key] = config["DEFAULT"][key]
	
	return configValues

def writeTime(time,scramble,cube):
	with open("{}_times.csv".format(cube), "a", newline="") as times:
		writer = csv.writer(times)
		writer.writerow([time , datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') , scramble])

def readTimes(cube):
	times, timestamps = [], []
	with open("{}_times.csv".format(cube), newline = "") as saveFile:
		reader = csv.reader(saveFile, delimiter=",")
		for row in reader:
			times.append(row[0])
			timestamps.append(row[1])

	times = [float(time) for time in times]
	return times, timestamps

def Timer():
	minutes = 0
	millis = 0
	seconds = 0

	while True:
		sys.stdout.write("\r{minutes}::{seconds}::{millis}".format(minutes=minutes, seconds=seconds, millis=millis))
		sys.stdout.flush()
		millis += 10

		if (millis % 500) != 0:
			time.sleep(0.01)

		if millis >= 1000:
			seconds += 1
			millis = 0

		if seconds >= 60:
			minutes += 1
			seconds = 0

		#if spacebar is pressed stop timer
		if keyboard.is_pressed(' '):
			break 
		if keyboard.is_pressed('esc'):
			return

	print("\n")
	solve_time = (minutes * 60000 + seconds * 1000 + millis) / 1000
	return solve_time

def inspection(insptime):
	time.sleep(0.1)
	secs = int(insptime)
	"""starts at 900 milliseconds instead of 1000 because of the sleep
	needed to avoid conflict when pressing the 'enter' key"""
	millis = 900

	while secs:
		sys.stdout.write("\r{}::{}".format(secs,millis))
		millis -= 10

		if (millis % 500) != 0:		
			time.sleep(0.01)

		#make a beep sound at 8 and 12 seconds
		if secs == 7 and millis == 0 or secs == 3 and millis == 0:
			print ("\a", end='')
		if millis <= 0:
			secs -= 1
			millis = 1000
		if keyboard.is_pressed('enter'):
			break 
		if keyboard.is_pressed('esc'):
			return
	print('\nStart Solving!\n')
	
def newBest():
	print("""
  _   _   ______  __          __    ____    ______    _____   _______   _ 
 | \ | | |  ____| \ \        / /   |  _ \  |  ____|  / ____| |__   __| | |
 |  \| | | |__     \ \  /\  / /    | |_) | | |__    | (___      | |    | |
 | . ` | |  __|     \ \/  \/ /     |  _ <  |  __|    \___ \     | |    | |
 | |\  | | |____     \  /\  /      | |_) | | |____   ____) |    | |    |_|
 |_| \_| |______|     \/  \/       |____/  |______| |_____/     |_|    (_)
	""")

def GetBest(num,times,timeslen):
	index=0
	Best = 1000.00
	for index in range(index,timeslen-(num-2)):
		lastTimes = times[index:index+num-1]
		if num == 5 or num == 12:
			lastTimes.pop(lastTimes.index(max(lastTimes)))
			lastTimes.pop(lastTimes.index(min(lastTimes)))
		elif num == 50:
			for i in range(0,3):
				lastTimes.pop(lastTimes.index(max(lastTimes)))
				lastTimes.pop(lastTimes.index(min(lastTimes)))
		elif num == 100:
			for i in range(0,5):
				lastTimes.pop(lastTimes.index(max(lastTimes)))
				lastTimes.pop(lastTimes.index(min(lastTimes)))
		elif num == 1000:
			for i in range(0,50):
				lastTimes.pop(lastTimes.index(max(lastTimes)))
				lastTimes.pop(lastTimes.index(min(lastTimes)))
		sumLastTimes = sum(lastTimes)
		CurrentBest = round(sumLastTimes / len(lastTimes), 3)
		if(CurrentBest < Best):
			Best = CurrentBest
	print("\tAo{}: \t{:.2f}".format(num,Best))

def GetCurrent(num,times,timeslen):
	lastTimes = times[-num:]
	if num == 5 or num == 12:
		lastTimes.pop(lastTimes.index(max(lastTimes)))
		lastTimes.pop(lastTimes.index(min(lastTimes)))
	elif num == 50:
		for i in range(0,3):
			lastTimes.pop(lastTimes.index(max(lastTimes)))
			lastTimes.pop(lastTimes.index(min(lastTimes)))
	elif num == 100:
		for i in range(0,5):
			lastTimes.pop(lastTimes.index(max(lastTimes)))
			lastTimes.pop(lastTimes.index(min(lastTimes)))
	elif num == 1000:
		for i in range(0,50):
			lastTimes.pop(lastTimes.index(max(lastTimes)))
			lastTimes.pop(lastTimes.index(min(lastTimes)))
	sumLastTimes = sum(lastTimes)
	CurrentBest = round(sumLastTimes / len(lastTimes), 3)
	print("Ao{}: \t{:.2f}".format(num,CurrentBest), end="")

def stats(times, timestamps, configValues):
	timeslen = len(times)

	print("------------------------------")
	print("------------TIMER-------------")
	print("------------------------------")
	if configValues["solves"] == "True":
		print("\tSolves: " + str(timeslen))
		print("------------------------------")

	if timeslen >= 1:
		if configValues["subx"] == "True":
			timeKeys = configValues["timekeys"].split(",")
			timeKeys = [int(key) for key in timeKeys]
			dictonary = OrderedDict()
			
			for value in timeKeys:
				dictonary[float(value)] = 0
		
			for key in dictonary.keys():
				for time in times:
					if time < key:
						dictonary[key] += 1
				
			for key, val in dictonary.items():
				print("Sub-{}:   {}\t[{}%]".format(str(key), str(val), str(float(val) / float(len(times)) * 100.0)[:5]))
			print("------------------------------")
	
	print("  Current\t    Best\n" + "------------------------------")
	if timeslen >= 3:
		if configValues["ao3"] == "True":
			GetCurrent(3,times,timeslen)
			GetBest(3,times,timeslen)
		if timeslen >= 5:
			if configValues["ao5"] == "True": 
				GetCurrent(5,times,timeslen)
				GetBest(5,times,timeslen)
			if timeslen >= 12:
				if configValues["ao12"] == "True":
					GetCurrent(12,times,timeslen)
					GetBest(12,times,timeslen)
				if timeslen >= 50:
					if configValues["ao50"] == "True":
						GetCurrent(50,times,timeslen)
						GetBest(50,times,timeslen)
					if timeslen >= 100:
						if configValues["ao100"] == "True":
							GetCurrent(100,times,timeslen)
							GetBest(100,times,timeslen)
						if timeslen >= 1000:
							if configValues["ao1000"] == "True":
								GetCurrent(1000,times,timeslen)
								GetBest(1000,times,timeslen)
	print("------------------------------")
	if timeslen >= 2:
		if configValues["mean"] == "True":
			totalTime = sum(times)
			print("Mean: \t{:.2f}".format(round(totalTime / len(times), 3)))

		if configValues["median"] == "True":
			sortedTimes = sorted(times)
			if len(sortedTimes) % 2 == 0:
				median = round(sortedTimes[ceil(len(sortedTimes) / 2)], 3)
			else:
				median = round((sortedTimes[floor(len(sortedTimes) / 2)] + sortedTimes[ceil(len(sortedTimes) / 2)]) / 2, 3)
			print("Median: \t{:.2f}".format(median))

		if configValues["standarddeviation"] == "True":
			average = sum(times) / len(times)
			deviations = [(x - average) ** 2 for x in times]
			variance = sum(deviations) / len(deviations)
			standardDeviation = sqrt(variance)
			print("SD: \t{:.2f}".format(round(standardDeviation, 3)))
	
	if timeslen >= 1:
		if configValues["best"] == "True":
			print("Best: \t{:.2f}".format(min(times)))
			
		if configValues["worst"] == "True":
			print("Worst: \t{:.2f}".format(max(times)))
		
		if configValues["latest"] == "True":
			print("Last: \t{:.2f}".format(times[-1]))

def ChooseCube(cube,dictionary):
	if cube == "":
		print(
		'Choose cube type:\n',\
		'(1). One Handed\n',\
		'(2). 2x2\n',\
		'(3). 3x3\n',\
		'(4). 4x4\n',\
		'(5). 5x5\n',\
		'(6). 6x6\n',\
		'(7). 7x7\n',\
		'(b). Blind\n',\
		'(p). Pyraminx\n',\
		'(s1). Square-1\n',\
		'(s). Skewb\n',\
		'(c). Clock\n',\
		'(ctrl+c). Back to menu')
		cube = input(">>")
		cube = dictionary[cube]
	return cube

def GetScramble(cube):
	if cube == "":
		ChooseCube()

	if cube == "222":   
		scramble = scrambler222.get_WCA_scramble() 
	elif cube == "333" or cube == "onehanded" or cube == "blindfolded":	
		scramble = scrambler333.get_WCA_scramble()
	elif cube == "444":	
		scramble = scrambler444.get_WCA_scramble(n=40)
	elif cube == "555":	
		scramble = scrambler555.get_WCA_scramble(n=60)
	elif cube == "666":
		scramble = scrambler666.get_WCA_scramble(n=80)
	elif cube == "777":
		scramble = scrambler777.get_WCA_scramble(n=100)
	elif cube == "pyraminx":
		scramble = pyraminxScrambler.get_WCA_scramble()
	elif cube == "square1":
		scramble = squareOneScrambler.get_WCA_scramble()
	elif cube == "skewb":
		scramble = skewbScrambler.get_WCA_scramble()
	elif cube == "clock":
		scramble = clockScrambler.get_WCA_scramble()
	else:
		print("Didn't recognize input, assuming 3x3 ..")
		scramble = scrambler333.get_WCA_scramble()

	print("\n" + scramble + "\n")
	return scramble

def PrintAoX(times):
	try:
		avg = int(input("Choose how many solves to show: \n>> "))
		last = times[-avg:]
		for time in last:
			print(str(time))
		input("Press Enter to continue...")
	except Exception as e:
		print("Error: " + str(e))

def GetStats(configValues,cube):
	try:
		times, timestamps = [], []
		#if file it's not empty
		if(os.stat("{}_times.csv".format(cube)).st_size != 0):
			times, timestamps = readTimes(cube)
	except IndexError:
		print("Error, no recorded solves.")
	except FileNotFoundError:
		print("File \"{}_times.csv\" not found, creating new one".format(cube))
		file = open('myfile.dat', 'w+')
	except Exception as e:
		print("Error: " + str(e))

	stats(times, timestamps, configValues)
	return times,timestamps

def main():
	dictionary = {"1":"onehanded" , "2":"222" , "3":"333",
				  "b":"blindfolded" , "4":"444" , "5":"555",
				  "6":"666" , "7":"777" , "p":"pyraminx" ,
				  "s1":"square1" , "s":"skewb" , "c":"clock"}
	cube = ""
	configValues = getConfig()
	while True:
		print("------------------------------")
		print("--------CUBE TIMER CLI--------")
		print("------------------------------")
		try:
			print("------------------------------")
			choose = input("1.Timer.\n2.Print last solves.\n3.Exit.\n>> ")
			if choose == '1':
				while True:
					try:
						cube = ChooseCube(cube,dictionary)
						times,timestamps = GetStats(configValues,cube)
						scramble = GetScramble(cube)
						print("[press ctrl+c to go back] Press Enter to start\n")
						keyboard.wait('enter')
						if configValues["inspectiontime"] != '0':
							print("[press esc to exit the inspection timer, Enter start solving]")
							inspection(configValues["inspectiontime"])
						print("[press esc to exit the timer, Spacebar to stop]\n")
						solve_time = Timer()
						#if timer was not stopped by user
						if solve_time != None:
							print("\x1b[6;30;42m" + "\nTIME: " + str(solve_time) + "\x1b[0m")
							#if times is empty
							if not times:
								newBest()
							else:
								if solve_time < min(times):
									newBest()
							writeTime(solve_time,scramble,cube)
						else:
							print("\nExiting timer...")
					except KeyboardInterrupt:
						print("Exiting")
						break
				cube = ""
			elif choose == '2':
				PrintAoX(times)
			elif choose == '3':
				break
			else:
				print("Input was not valid.")
				choose = 0
		except Exception as e:
			print("Error: " + str(e))

if __name__ == '__main__':
	main()
