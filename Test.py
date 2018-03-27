import time
from threading import Thread
import os
import vlc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

download_directory='/home/rohan/Music/Selenium'

options = Options()
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=options)
song_list=os.listdir(download_directory)

def initialize():								#Options to hide chrome,so the player is terminal only
	#options.add_argument('--headless')
	#options.add_argument('--disable-gpu')
	prefs = {'download.default_directory' : download_directory}
	options.add_experimental_option('prefs', prefs)
	print("Type h for help")

def search(quick):
	song_list=os.listdir(download_directory)
	flag=True
	print("Enter the name of the song")
	name=input()
	for songs in song_list:
		if name in songs:
			flag=False
			song = vlc.MediaPlayer(download_directory+'/'+songs)
			song.play()
			break
	if flag==True:		#Checks if file aldready exists in downloads
		if quick:		#QuickPlay requires just the song name
			save_file='n'
		else:
			save_file=input("Download Song?(y/n) ")
		if save_file == 'y':
			download(name)
		else:
			url='https://www.youtube.com/results?search_query='+name
			driver.get(url)
			elem=driver.find_element_by_css_selector('.yt-simple-endpoint.style-scope.ytd-video-renderer')		#First Link in YOutube Search
			elem.click()

def download(name):
	url='https://y2mate.com/'
	driver.get(url)
	elem=driver.find_element_by_css_selector('.form-control.input-lg')
	elem.click()
	elem.send_keys(name)
	elem.send_keys(Keys.RETURN)
	driver.implicitly_wait(6)
	for i in range (1,11,1):			#Returns first 10 results
		elem=driver.find_element_by_xpath('//*[@id="search-result"]/div['+str(i)+']/div/div/a')
		name=elem.get_attribute('text').replace("\n","")
		name=name.replace('                        ','  ')
		print(str(i)+name)
	while True:
		index=input("Enter the index number: ")
		if int(index)>=1 and int(index)<=10:
			break
	

	elem=driver.find_element_by_xpath('//*[@id="search-result"]/div['+str(index)+']/div/div/a')		#Gets the Xpath of selected index
	name=elem.get_attribute('text').replace("\n","")
	name=name.replace('                        ','')
	
	driver.get(elem.get_attribute('href'))
	driver.implicitly_wait(5)		#Wait for page to load otherwise elements might not load
	try:
		elem=driver.find_element_by_xpath('//*[@id="mp4"]/table/tbody/tr[4]/td[3]/a')		#Check if 144p exists
	except:
		elem=driver.find_element_by_xpath('//*[@id="mp4"]/table/tbody/tr[3]/td[3]/a')		#If tr[4] doesn't exist try tr[3]
	elem.click()
	name=name	
	check_download(name)
	

def check_download(name):
	#driver.get('chrome://downloads/')		#Havn't figured this out yet :P
	while True:
		print("#", end='')
		if 'videoplayback' in os.listdir('/home/rohan/Downloads/'):			#Check if download is complete every 1 second
			break
		time.sleep(5);
	rename_download(name)

def rename_download(name):
	os.rename('/home/rohan/Downloads/videoplayback',download_directory+'/'+name)	#Rename file(default videoplayback) to <file_name>
	song = vlc.MediaPlayer(download_directory+'/'+name)
	song.play()

initialize()
print('Press: \n n to search \n l to list all songs \n q for quicksearch \n e to exit \n')
while True:

	option=input("Option: ")
	if option == 'l':
		index=1
		print("")
		song_list=os.listdir(download_directory)
		for songs in song_list:
			print(str(index)+'. '+songs)
			index=index+1
	elif option == 'e':
		driver.close()
		break
	elif option == 'n':
		search(False)
	elif option == 'q':
		search(True)
	elif option == 'h':
		print('Press: \n n to search \n l to list all songs \n q for quicksearch \n e to exit \n')
