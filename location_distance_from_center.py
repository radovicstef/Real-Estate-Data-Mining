import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector

distance_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="estates"
)

PATH_TO_CHROME_DRIVER = "C:\Program Files (x86)\chromedriver.exe"
URL = "https://www.google.com/maps/dir/%D0%A5%D0%BE%D1%82%D0%B5%D0%BB+%E2%80%9E%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22,+%D0%91%D0%B0%D0%BB%D0%BA%D0%B0%D0%BD%D1%81%D0%BA%D0%B0+1,+%D0%91%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D0%B4+11000/%D0%A1%D1%82%D0%B0%D1%80%D0%B8+%D0%B3%D1%80%D0%B0%D0%B4,+%D0%91%D0%B5%D0%BE%D0%B3%D1%80%D0%B0%D0%B4/@44.815835,20.4574894,16z/data=!3m1!4b1!4m14!4m13!1m5!1m1!1s0x475a7ab209cff051:0x52504f6400d4b777!2m2!1d20.4603392!2d44.8130055!1m5!1m1!1s0x475a7ab51ce20e1d:0x25ea809ecfd66a1a!2m2!1d20.4643411!2d44.8184554!3e2?hl=sr"

driver = webdriver.ChromeOptions()

browser = webdriver.Chrome(options=driver, executable_path=PATH_TO_CHROME_DRIVER)

center = 'Hotel Moskva, Balkanska 1, Beograd 11000'

extracted_distances = []

my_cursor = distance_db.cursor()
my_cursor.execute("SELECT opstina FROM tbl_belgrade_location_distance_from_center WHERE udaljenost_od_centra IS NULL")
my_result = my_cursor.fetchall()

for opstina in my_result:
    opstina = opstina[0]
    browser.get(URL)

    WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located((By.ID, "sb_ifc50")))

    src = browser.find_element_by_xpath("//*[@id='sb_ifc50']/input")
    dest = browser.find_element_by_xpath("//*[@id='sb_ifc51']/input")
    calculate = browser.find_element_by_xpath("//*[@id='directions-searchbox-1']/button[1]")

    src.clear()
    dest.clear()

    src.send_keys(center)
    dest.send_keys(opstina)

    WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='directions-searchbox-1']/button[1]"))).click()

    # wait until page loads distance
    WebDriverWait(browser, 20).until(
        EC.visibility_of_element_located((By.ID, "section-directions-trip-0")))
    time.sleep(2)
    distance = browser.find_element_by_xpath("//*[@id='section-directions-trip-0']/div/div[3]/div[1]/div[2]")

    splited_distance = distance.text.split()
    final_distance = float(splited_distance[0].strip().replace(",", "."))
    if splited_distance[1] == 'm' or splited_distance[1] == 'м':  # final_distance is in km
        final_distance = final_distance / 1000.0

    my_cursor.execute("""
        UPDATE tbl_belgrade_location_distance_from_center
        SET udaljenost_od_centra=%s
        WHERE opstina=%s
    """, (
        final_distance,
        opstina
    ))

    distance_db.commit()


