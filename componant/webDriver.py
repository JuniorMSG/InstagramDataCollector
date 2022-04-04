import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import chromedriver_autoinstaller
# from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import uuid
import random
import re
import time
from bs4 import BeautifulSoup

def web_driver_wait(driver, path, time=20):
    return WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, path)))

# User-Agent 설정
def get_random_ua():
    all_user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        # "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        # "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
        # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        # "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
    ]
    random_ua_index = random.randint(0, len(all_user_agents) - 1)
    ua = re.sub(r"(\s)$", "", all_user_agents[random_ua_index])
    return ua


def browser_open(driver, url, headress_mode=False, proxy_ip="", mobile_mode=False):
    try:
        driver.window_handles
        driver.get(url)
        return driver
    except Exception as e:
        driver = get_driver(headress_mode, proxy_ip, mobile_mode)
        driver.get(url)
        return driver

# 크롬드라이버 환경 설정
def get_driver(headress_mode, proxy_ip, mobile_mode=False):

    options = webdriver.ChromeOptions()

    if headress_mode:
        options.add_argument('headless')

    options.add_argument('window-size=1920x1080')
    options.add_argument('lang=ko_KR')


    # 시크릿모드드
    # options.add_argument('--incognito')
    options.add_argument('--no-sandbox')
    # options.add_argument('--disable-setuid-sandbox')

    # 자동모듈 숨기기
    options.add_argument("--disable-blink-features=AutomationControlled")


    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('acceptInsecureCerts')
    options.add_argument('--allow-insecure-localhost')
    options.add_argument('--able-popup-blocking')
    options.add_argument('--log-level=3')
    options.add_argument("disable-gpu")
    options.add_argument("user-agent=" + get_random_ua())

    # enable-automation 자동화 막대 비활성, load-extension 개발자 모드 확장 사용 비활성
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging", "load-extension"])
    options.add_experimental_option('useAutomationExtension', False)

    # 로그인시 비밀번호창 비활성
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        # 'profile.default_content_setting_values': {'cookies': 1, 'images': 2, 'plugins': 2, 'popups': 2,
        #                                                     'geolocation': 2, 'notifications': 2,
        #                                                     'auto_select_certificate': 2, 'fullscreen': 2,
        #                                                     'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
        #                                                     'media_stream_mic': 2, 'media_stream_camera': 2,
        #                                                     'protocol_handlers': 2, 'ppapi_broker': 2,
        #                                                     'automatic_downloads': 2, 'midi_sysex': 2,
        #                                                     'push_messaging': 2, 'ssl_cert_decisions': 2,
        #                                                     'metro_switch_to_desktop': 2,
        #                                                     'protected_media_identifier': 2, 'app_banner': 2,
        #                                                     'site_engagement': 2, 'durable_storage': 2}
    }

    options.add_experimental_option("prefs", prefs)
    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

    if proxy_ip != 0:
        options.add_argument('--proxy-server={}'.format(proxy_ip))

    if mobile_mode:
        mobile_emulation = {"deviceName": "Nexus 5"}
        options.add_experimental_option("mobileEmulation", mobile_emulation)

    try:
        # "httpProxy": '124.198.55.9',
        driver = webdriver.Chrome(f'./rsc/{chrome_ver}/chromedriver.exe', options=options)
    except:
        chromedriver_autoinstaller.install(path='./rsc')
        driver = webdriver.Chrome(f'./rsc/{chrome_ver}/chromedriver.exe', options=options)

    driver.set_page_load_timeout(120)
    driver.create_options()
    # driver.maximize_window()

    return driver

# alert message 탈출
def escape_alert_message(driver):
    try:
        da = Alert(driver)
        da.accept()
        time.sleep(2)
    except Exception as e:
        print("-- alert창 없음 -- ")

# 공용 팝업 닫기
def popup_close(driver):
    # JS View Task
    """
        https://stackoverflow.com/questions/19669786/check-if-element-is-visible-in-dom
    """
    pop_close_script = []

    includes_tag_lst = ["button", "label", "span", "b", 'div']
    includes_text_lst = ["열람하지 않습니다", "열지 않기", "열지않기", "닫기", "close", "Close"]
    text_script = "Array.from(document.querySelectorAll('{0}')).find(elem => elem.textContent.includes('{1}') ? elem.click() : '')"

    for includes_tag in includes_tag_lst:
        for includes_text in includes_text_lst:
            pop_close_script.append(text_script.format(includes_tag, includes_text))

    text_script_attr = "Array.from(document.querySelectorAll('[{0}*={1}]')).find(elem =>!!(elem.offsetWidth || elem.offsetHeight || elem.getClientRects().length) ? elem.click() : '')"
    view_attr_lst = ['data-toggle', 'class', 'id', 'onclick', ]
    view_attr_text_lst = ['close', "Close", "check", "SetCookie", "pop-close"]

    for includes_tag in view_attr_lst:
        for includes_text in view_attr_text_lst:
            pop_close_script.append(text_script_attr.format(includes_tag, includes_text))

    pop_close_script.append("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")
    pop_close_script.append("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})")
    pop_close_script.append("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")

    for script in pop_close_script:
        try:
            driver.execute_script(script)
        except:
            pass

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    driver = browser_open('', 'https://search.naver.com/search.naver?where=nexearch&sm=top_sug.mbk&fbm=1&acr=1&acq=rhddls+%E3%85%91%E3%85%96&qdt=0&ie=utf8&query=%EA%B3%B5%EC%9D%B8ip',
                           headress_mode=False, proxy_ip="", mobile_mode=False)




    print(1234)