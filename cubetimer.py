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
	secs = int(insptime)
	millis = 1000
	time.sleep(0.1)

	while secs:
		sys.stdout.write("\r{}::{}".format(secs,millis))
		#timeformat = '{:02d}:{:03d}'.format(secs, millis)
		#print(timeformat, end='\r')
		millis -= 10

		if (millis % 500) != 0:		
			time.sleep(0.01)

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
	
	
	if timeslen >= 3:
		if configValues["ao3"] == "True":
			last3Times = times[-3:]
			sumLast3Times = sum(last3Times)
			print("Ao3: \t\t" + str(round(sumLast3Times / len(last3Times), 3)))
		
		if timeslen >= 5:
			if configValues["ao5"] == "True": 
				last5Times = times[-5:]
				sumLast5Times = sum(last5Times)
				print("Ao5: \t\t" + str(round(sumLast5Times / len(last5Times), 3)))
				
			if timeslen >= 12:
				if configValues["ao12"] == "True":
					last12Times = times[-12:]
					last12Times.pop(last12Times.index(max(last12Times)))
					last12Times.pop(last12Times.index(min(last12Times)))
					sumLast12Times = sum(last12Times)
					print("Ao12: \t\t" + str(round(sumLast12Times / len(last12Times), 3)))
				
				if timeslen >= 50:
					if configValues["ao50"] == "True":
						last50Times = times[-50:]
						sumLast50Times = sum(last50Times)
						print("Ao50: \t\t" + str(round(sumLast50Times / len(last50Times), 3)))
					
					if timeslen >= 100:
						if configValues["ao100"] == "True":
							last100Times = times[-100:]
							sumLast100Times = sum(last100Times)
							print("Ao100: \t\t" + str(round(sumLast100Times / len(last100Times), 3)))
						
						if timeslen >= 1000:
							if configValues["ao1000"] == "True":
								last1000Times = times[-1000:]
								sumLast1000Times = sum(last1000Times)
								print("Average: \t" + str(round(totalTime / len(times), 3)))
				
	if timeslen >= 2:
		if configValues["average"] == "True":
			totalTime = sum(times)
			print("Average: \t" + str(round(totalTime / len(times), 3)))
			

		if configValues["median"] == "True":
			sortedTimes = sorted(times)
			if len(sortedTimes) % 2 == 0:
				median = round(sortedTimes[ceil(len(sortedTimes) / 2)], 3)
			else:
				median = round((sortedTimes[floor(len(sortedTimes) / 2)] + sortedTimes[ceil(len(sortedTimes) / 2)]) / 2, 3)

			print("Median: \t" + str(median))
		
		
		if configValues["standarddeviation"] == "True":
			average = sum(times) / len(times)
			deviations = [(x - average) ** 2 for x in times]
			variance = sum(deviations) / len(deviations)
			standardDeviation = sqrt(variance)
			print("SD: \t\t" + str(round(standardDeviation, 3)))
	
	if timeslen >= 1:
		if configValues["best"] == "True":
			print("Best: \t\t" + str(min(times)))
			
		
		if configValues["worst"] == "True":
			print("Worst: \t\t" + str(max(times)))
		
		
		if configValues["latest"] == "True":
			print("Latest: \t" + str(times[-1]))

def ChooseCube(cube,dictionary):
	if cube == "":
		cube = input("Choose cube type:\n2x2 (2),3x3 (3),One Handed (oh),Blind (b),4x4 (4),5x5 (5),6x6 (6),7x7 (7),Pyraminx (p),Square-1 (s1),Skewb (s),Clock (c)\n>> ")
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
	dictionary = {"2":"222" , "3":"333","oh":"onehanded",
				  "b":"blindfolded" , "4":"444" , "5":"555",
				  "6":"666" , "7":"777" , "p":"pyraminx" ,
				  "s1":"square1" , "s":"skewb" , "c":"clock"}
	cube = ""
	choose = 0
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
						flag = input("[press ctrl+c to go back] Press Enter to start, Spacebar to stop...\n")
						if configValues["inspectiontime"] != 0:
							print("[press esc to exit the inspection timer, Enter to stop]\n")
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
