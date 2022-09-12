import requests
import random
from time import sleep
from twocaptcha import TwoCaptcha
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor


def regYandexMail(proxy) -> None:
	# -----Настройки-----    
	options = webdriver.ChromeOptions()
	options.add_argument("--disable-blink-features=AutomationControlled")
	# -----Прокси-----
	proxy_options = {
		"proxy": {
			"https": f"http://cmn66c:Q36xdV@91.203.6.26:14471"
			}
		}
	# -----Скрытие окна-----
	#options.add_argument('--headless')
	# -----Данные-----
	name_list = ["Ivan", "Nikita", "Maxim", "Vadim", "Evgeniy", "Danila", "Danik", "Liza", "Maria", "Darina", "Dasha", "Ksenia", "Nelli", "Nikolay", "Artem", "Misha", "Anastasia", "Viktoria", "Kristina", "Victor", "Ilia", "Tatiana"]
	lastname_list = ["Kovalenko", "Koval", "Koralchuk", "Koralevich", "Koraluk", "Davidovich", "Davidenko", "Davud", "Dakod", "Dabranrav", "Dabralub", "Kozel", "Kozlenko", "Kozluk", "Zaic", "Polikarp", "Godunovenko", "Gordey"]
	password_list = ["QOPBBtJi", "87duRuc3", "Tj62eh5u", "r9ele92O", "9CUhZT91", "p9nZmX06", "2X94kYCf", "frg8R7z0", "z9E3rt0z", "UO9x9oE5", "5lm8avS6", "5Rjp83Vg0", "PGKI601L", "2lU40rXv", "99Gz0Wqf", "D13Mg7Hi", "xEM328MK", "g0kjS53P", "Z9ya3jv7"]
	url = "https://passport.yandex.by/registration?retpath=https%3A%2F%2Fmail.yandex.by&process_uuid=fd2fa8cc-4a53-4c49-8ca2-fe1f9be725cb"
	driver = webdriver.Chrome( seleniumwire_options=proxy_options, options=options)
	try:
		print("работаю")
		# -----Запуск-----
		driver.get(url)
		#-----Имя и фамилия-----
		driver.find_element(By.XPATH, """//*[@id="firstname"]""").send_keys(random.choice(name_list))
		driver.find_element(By.XPATH, """//*[@id="lastname"]""").send_keys(random.choice(lastname_list))
		#-----Пароль и подтверждение-----
		pass_list = random.choice(password_list)
		driver.find_element(By.XPATH, """//*[@id = "password"]""").send_keys(pass_list)
		driver.find_element(By.XPATH, """//*[@id = "password_confirm"]""").send_keys(pass_list)
		#-----Логин------
		login = driver.find_element(By.XPATH, """//input[@id = "login"]""")
		login.send_keys("s")
		driver.find_element(By.XPATH, """//*[@id = "password"]""").click()
		sleep(2)
		login.click()
		sleep(2)
		login.click()
		login = driver.find_element(By.XPATH, """//label[@tabindex = "0"]""")
		login_data = login.get_attribute("data-login")
		login.click()
		# -----Телефон-----
		sleep(1)
		driver.find_element(By.XPATH, """//span[@tabindex = "0"]""").click()
		driver.find_element(By.XPATH, """//*[@name = "hint_answer"]""").send_keys("Ответ")
		# -----Капча-----
		sleep(2)
		captcha = driver.find_element(By.XPATH, """//*[@class = "captcha__image"]""")
		captcha = requests.get(captcha.get_attribute('src'))
		# -----Решение каптчи-----
		with open('captcha.jpg', 'wb') as img:
			img.write(captcha.content)

		captcha = TwoCaptcha('73e4e0698453973d636da9346ddeec22').normal('captcha.jpg')
		captcha = captcha['code']	
		# -----Ввод капчи-----
		driver.find_element(By.XPATH, """//*[@id = "captcha"]""").send_keys(captcha)
		sleep(2)
		driver.find_element(By.XPATH, """//*[@id="root"]/div/div[2]/div/main/div/div/div/form/div[4]/span/button""").click()
		sleep(2)
		driver.find_element(By.XPATH, """//*[@id="root"]/div/div[2]/div/main/div/div/div/form/div[4]/div/div[2]/div/button""").click()
		sleep(2)
		# -----Подтверждение-----
		driver.find_element(By.XPATH, """//*[@class = "user-account user-account_has-ticker_yes user-account_has-accent-letter_yes legouser__current-account i-bem"]""")
		# -----Выход-----
		driver.close()
	except:
		print("исключение!!!!")
		driver.close()
		amount += 3
		return regYandexMail()
	# -----Сохранение-----
	print("сохранил")
	with open('autoreg.txt', 'a') as data:
		data.write(login_data + ";" + pass_list + '\n')
	sleep(3)

if __name__ == '__main__':
	proxy_list = ['proxy', 'proxy', 'proxy']
	solver = TwoCaptcha('')
	amount = int(input("Введи количество: "))
	while amount != 0:
		# -----Потоки-----
		with ThreadPoolExecutor(max_workers=len(proxy_list)) as executor:
			for proxy in proxy_list:
				executor.submit(regYandexMail, proxy)
		amount -= len(proxy_list)
