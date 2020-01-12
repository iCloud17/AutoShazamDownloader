#---------------------------------SHAZAM SECTION-------------------------------------
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
#from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import sys
import time


#FOR FACEBOOK LOGIN
username = "YOUR USERNAME"
password = "YOUR PASSWORD"
displayRate = 20 #Shazam shows 20 songs at a time
songsNeeded = 20 #Songs to download


#LAUNCH URL
#ChromeDriverManager().install()
#INSTALL CHROMEDRIVER
print("Opening Window!")
driver = webdriver.Chrome('CHROMEDRIVER.EXE PATH')
driver.implicitly_wait(30)
url = "https://www.shazam.com/myshazam"
driver.get(url)


#LOGIN
print("Logging in...")
fb_Loginbutton = driver.find_element_by_link_text('CONTINUE WITH FACEBOOK')
email_Loginbutton = driver.find_element_by_link_text('CONTINUE WITH EMAIL')
#print(len(driver.window_handles))
main_window = driver.window_handles[0]
fb_Loginbutton.click()
time.sleep(3)
login_window = driver.window_handles[1]
'''
for handle in driver.window_handles:
	print(handle)
	driver.switch_to.window(handle)
'''
driver.switch_to.window(login_window)
email = driver.find_element_by_name("email")
email.send_keys(username)
psswd = driver.find_element_by_name("pass")
psswd.send_keys(password)
psswd.send_keys(Keys.RETURN)
driver.switch_to.window(main_window)

#Wait for 20 seconds max for login to complete
print("Logged in and waiting for my Shazams!")
timeout = 20
try:
    WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//header[@class=\"panel-hd\"]")))
except TimeoutException:
    print("Timed out waiting for page to load")
    driver.quit()
    sys.exit("NOT RUNNING CORRECTLY! 1")

print("Loaded Page and now scraping starts!")


#GET LIST NAMES
def get_names_df():
	title_elements = driver.find_elements_by_xpath("//div[@class='title']")
	artist_elements = driver.find_elements_by_xpath("//div[@class='artist']")
	dlist = []

	for x in range(0, len(title_elements)):
		tlst = []
		title = title_elements[x].find_element_by_class_name('ellip').text
		artist = artist_elements[x].find_element_by_class_name('ellip').text
		tlst.append(title)
		tlst.append(artist)
		dlist.append(tlst)

	df = pd.DataFrame(dlist, columns=['Title', 'Artist'])
	df.drop_duplicates(inplace=True)
	return df

ndf = get_names_df()
#driver.quit()
#print(ndf)

x = 0
while len(ndf.index) < songsNeeded:
	x = x + 1
	num = x * displayRate
	num = num + 1
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	timeout = 20
	try:
		WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//span[@class=\"number\"][contains(text(), '" + str(num) + "')]")))
	except TimeoutException:
		print("Timed out waiting for page to load")
		driver.quit()
		sys.exit("NOT RUNNING CORRECTLY! 2")

	ndf = get_names_df()
	#print(len(ndf.index))

#driver.quit()
ndf = ndf.head(songsNeeded)
#print("\n\n---------LIST---------\n")
#print(ndf)

while True:
	try:
		ndf.to_csv("Songs2Download.csv")
		print("Song List Saved!")
		break  
	except Exception as e:
		choice = input("Error in writing file! Try again (y/n)? ")
		if choice == "n" or choice == "N":
			print("Song List Save Failed!")
			break

#-------------------------------YOUTUBE SECTION-----------------------------------

url = "https://www.youtube.com/"
driver.get(url)
