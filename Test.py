import os
import vlc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

download_directory='/home/rohan/Music/Selenium'

options = Options()
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver",chrome_options=options)
song_list=os.listdir(download_directory)

def initialize():
	#options.add_argument('--headless')
	#options.add_argument('--disable-gpu')
	prefs = {'download.default_directory' : download_directory}
	options.add_experimental_option('prefs', prefs)

def search(name):
	flag=True
	for songs in song_list:
		if name in songs:
			flag=False
			song = vlc.MediaPlayer(download_directory+name)
			song.play()
			break
	if flag==True:
		save_file=input("Download Song?(y/n) ")
		if save_file == 'y':
			download(name)
		else:
			url='https://www.youtube.com/results?search_query='+name
			driver.get(url)
			elem=driver.find_element_by_css_selector('.yt-simple-endpoint.style-scope.ytd-video-renderer')
			elem.click()

def download(name):
	url='https://y2mate.com/'
	driver.get(url)
	elem=driver.find_element_by_css_selector('.form-control.input-lg')
	elem.click()
	elem.send_keys(name)
	elem.send_keys(Keys.RETURN)
	driver.implicitly_wait(6)
	for i in range (1,11,1):
		elem=driver.find_element_by_xpath('//*[@id="search-result"]/div['+str(i)+']/div/div/a')
		name=elem.get_attribute('text').replace("\n","")
		name=name.replace('                        ','  ')
		print(str(i)+name)
	while True:
		index=input("Enter the index number: ")
		if int(index)>=1 and int(index)<=10:
			break
	elem=driver.find_element_by_xpath('//*[@id="search-result"]/div['+str(index)+']/div/div/a')
	driver.get(elem.get_attribute('href'))
	elem=driver.find_element_by_xpath('//*[@id="mp4"]/table/tbody/tr[3]/td[3]/a')		
	elem.click()
	check_download()

def check_download():
	driver.get('chrome://downloads/')
	
initialize()
search()
while True:

	option=input()
	if option == 'l':
		print(song_list)
	elif option == 'q':
		driver.close()
		break
	elif option == 'n':
		print("Enter the name of the song")
		name=input()
		search(name)
	elif option == 'h':
		print('Press: \n n to search \n l to list all songs  \n q to quit \n')

