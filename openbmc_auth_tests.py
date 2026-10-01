from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def create_driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.accept_insecure_certs = True

    return webdriver.Chrome(options=options)


def login(driver):
    driver.get("https://127.0.0.1:2443")

    driver.find_element(By.ID, "username").send_keys("root")
    driver.find_element(By.ID, "password").send_keys("0penBmc")

    driver.find_element(
        By.CSS_SELECTOR,
        "[data-test-id='login-button-submit']"
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-test-id='nav-item-overview']")
        )
    )


def test_successful_login():
    driver = create_driver()

    login(driver)

    print("Успешная авторизация: PASS")

    driver.quit()


def test_wrong_login():
    driver = create_driver()

    driver.get("https://127.0.0.1:2443")

    driver.find_element(By.ID, "username").send_keys("root")
    driver.find_element(By.ID, "password").send_keys("wrongpassword")

    driver.find_element(
        By.CSS_SELECTOR,
        "[data-test-id='login-button-submit']"
    ).click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.ID, "username")
        )
    )

    print("Неверные данные отклонены: PASS")

    driver.quit()


def test_server_power():
    driver = create_driver()

    login(driver)

    driver.get(
        "https://127.0.0.1:2443/#/operations/server-power-operations"
    )

    power_on_buttons = driver.find_elements(
        By.CSS_SELECTOR,
        "[data-test-id='serverPowerOperations-button-powerOn']"
    )

    shut_down_buttons = driver.find_elements(
        By.CSS_SELECTOR,
        "[data-test-id='serverPowerOperations-button-shutDown']"
    )

    if power_on_buttons:
        power_on_buttons[0].click()
        print("Нажата кнопка Power on")

    elif shut_down_buttons:
        shut_down_buttons[0].click()
        print("Нажата кнопка Shut down")

    else:
        print("Кнопка управления питанием не найдена")
        driver.quit()
        return

    # Ждём окно подтверждения
    confirm_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//footer[contains(@class, 'modal-footer')]//button[normalize-space()='Confirm']"
            )
        )
    )

    confirm_button.click()

    print("Нажата кнопка Confirm")

    # Проверяем, что операция началась
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "alert-msg"),
            "power operation is in progress"
        )
    )

    print("Операция управления питанием запущена: PASS")

    driver.quit()


def test_temperature():
    driver = create_driver()

    login(driver)

    driver.get(
        "https://127.0.0.1:2443/#/hardware-status/sensors"
    )

    sensors_count = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.mt-2 p")
        )
    )

    if sensors_count.text == "0 items":
        print("Датчики температуры отсутствуют: FAIL")
    else:
        print("Датчики температуры найдены: PASS")

    driver.quit()


# test_successful_login()
# test_wrong_login()
# test_server_power()
test_temperature()
