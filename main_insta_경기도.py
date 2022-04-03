import time
import os

import pandas as pd

import componant.webDriver as WD
import pickle
import re
import json
from seleniumwire.utils import decode
from urllib import parse
import multiprocessing

from bs4 import BeautifulSoup

def searchKeyword(driver, strkeyword):
    url = "https://www.instagram.com/explore/tags/{}/".format(strkeyword)
    driver.get(url)
    time.sleep(3)

def searchUserId(driver, strUserId):
    url = "https://www.instagram.com/{0}/".format(strUserId)
    driver.get(url)
    time.sleep(3)

def set_scrolling(driver):

    while True:
       status = 0
       last_height = driver.execute_script("return document.body.scrollHeight")
       while True:
           status +=1
           driver.execute_script("window.scrollTo(0, 0);")
           time.sleep(3)
           driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
           time.sleep(3)
           if status == 10:
               break

       new_height = driver.execute_script("return document.body.scrollHeight")
       print(new_height, last_height)
       if new_height == last_height:
           break
       else:
           last_height = new_height
           continue

def data_get(driver, local, tag, process_core):


    url = "https://www.instagram.com/explore/tags/{0}{1}/"
    id_lst = []
    driver.get(url.format(local, tag))

    SCROLL_PAUASE_TIME = 3


    count = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/header/div[2]/div/div[2]/div/span').text


    while True:
        text_find = WD.web_driver_wait(driver, "/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[1]/div/span/a")
        id_lst.append(text_find.text)
        try:
            driver.find_element_by_css_selector("body > div.RnEpo._Yhr4 > div.Z2Inc._7c9RR > div > div.l8mY4.feth3").click()
        except:
            print("수집종료")


            save_data = []
            id_non_dup = set(id_lst)
            for id_data in id_non_dup:

                id_url = "https://www.instagram.com/" + id_data
                driver.get(id_url)

                def find_data(driver, path):
                    try:
                        return driver.find_element_by_xpath(path).text.replace("\n", " ")
                    except:
                        return ""

                name = find_data(driver, '//*[@id="react-root"]/section/main/div/header/section/div[2]/span')
                work_type = find_data(driver, '//*[@id="react-root"]/section/main/div/header/section/div[2]/div[1]/div')
                soge = find_data(driver,      '//*[@id="react-root"]/section/main/div/header/section/div[2]/div[2]')

                if work_type == "" and soge == "":
                    soge =  find_data(driver, '//*[@id="react-root"]/section/main/div/header/section/div[2]/div')
                link = find_data(driver, '//*[@id="react-root"]/section/main/div/header/section/div[2]/a/div')

                gasimul = WD.web_driver_wait(driver, '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/div/span').get_attribute("title")
                if gasimul == "":
                    gasimul = WD.web_driver_wait(driver, '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/div/span').text

                follower =  WD.web_driver_wait(driver, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/div/span').get_attribute("title")

                if follower == "":
                    follower = WD.web_driver_wait(driver, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/div/span').text

                follow =  WD.web_driver_wait(driver, '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/div/span').get_attribute("title")
                if follow == "":
                    follow = WD.web_driver_wait(driver,'//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/div/span').text


                etc =  WD.web_driver_wait(driver, '//*[@id="react-root"]/section/main/div/header/section/div[2]').text.replace("\n", " ")

                save_data.append(
                    {"키워드": "{0}".format(local + tag),
                     "지역": "{0}".format(local),
                     "성별": "수집불가능",
                     "아이디": id_data,
                     "이름": name,
                     "게시물": gasimul,
                     "팔로워": follower,
                     "팔로잉": follow,
                     "직업" : work_type,
                     "소개": soge,
                     "링크": link,
                     "기타":etc,
                     "키워드 검색건수": len(id_lst)
                     })

            df = pd.DataFrame(save_data)
            df.to_excel("{0}.xlsx".format(local + tag))
            driver.close()
            return

def tag_cnt_get():
    local_cnt = 0
    tag_cnt = 0

    url_lst = []
    url_lst.append("https://www.instagram.com/explore/tags/대구무용")
    url_lst.append("https://www.instagram.com/explore/tags/대구모델")
    url_lst.append("https://www.instagram.com/explore/tags/대구요가")
    url_lst.append("https://www.instagram.com/explore/tags/대구운동")
    url_lst.append("https://www.instagram.com/explore/tags/대구물리치료")
    url_lst.append("https://www.instagram.com/explore/tags/대구요가강사")
    url_lst.append("https://www.instagram.com/explore/tags/대구승무원")
    url_lst.append("https://www.instagram.com/explore/tags/대구헬스트레이너")
    url_lst.append("https://www.instagram.com/explore/tags/대구회사원")
    url_lst.append("https://www.instagram.com/explore/tags/대구강사")
    url_lst.append("https://www.instagram.com/explore/tags/대구골프")
    url_lst.append("https://www.instagram.com/explore/tags/대구주부")
    url_lst.append("https://www.instagram.com/explore/tags/대구대학생")
    url_lst.append("https://www.instagram.com/explore/tags/대구플로리스트")
    url_lst.append("https://www.instagram.com/explore/tags/대구네일아트")
    url_lst.append("https://www.instagram.com/explore/tags/대구연예인지망생")
    url_lst.append("https://www.instagram.com/explore/tags/대구필라테스")
    url_lst.append("https://www.instagram.com/explore/tags/대구필라테스강사")
    url_lst.append("https://www.instagram.com/explore/tags/대구pilates")
    url_lst.append("https://www.instagram.com/explore/tags/대전무용")
    url_lst.append("https://www.instagram.com/explore/tags/대전모델")
    url_lst.append("https://www.instagram.com/explore/tags/대전요가")
    url_lst.append("https://www.instagram.com/explore/tags/대전운동")
    url_lst.append("https://www.instagram.com/explore/tags/대전물리치료")
    url_lst.append("https://www.instagram.com/explore/tags/대전요가강사")
    url_lst.append("https://www.instagram.com/explore/tags/대전승무원")
    url_lst.append("https://www.instagram.com/explore/tags/대전헬스트레이너")
    url_lst.append("https://www.instagram.com/explore/tags/대전회사원")
    url_lst.append("https://www.instagram.com/explore/tags/대전강사")
    url_lst.append("https://www.instagram.com/explore/tags/대전골프")
    url_lst.append("https://www.instagram.com/explore/tags/대전주부")
    url_lst.append("https://www.instagram.com/explore/tags/대전대학생")
    url_lst.append("https://www.instagram.com/explore/tags/대전플로리스트")
    url_lst.append("https://www.instagram.com/explore/tags/대전네일아트")
    url_lst.append("https://www.instagram.com/explore/tags/대전연예인지망생")
    url_lst.append("https://www.instagram.com/explore/tags/대전필라테스")
    url_lst.append("https://www.instagram.com/explore/tags/대전필라테스강사")
    url_lst.append("https://www.instagram.com/explore/tags/대전pilates")
    url_lst.append("https://www.instagram.com/explore/tags/전주무용")
    url_lst.append("https://www.instagram.com/explore/tags/전주모델")
    url_lst.append("https://www.instagram.com/explore/tags/전주요가")
    url_lst.append("https://www.instagram.com/explore/tags/전주운동")
    url_lst.append("https://www.instagram.com/explore/tags/전주물리치료")
    url_lst.append("https://www.instagram.com/explore/tags/전주요가강사")
    url_lst.append("https://www.instagram.com/explore/tags/전주승무원")
    url_lst.append("https://www.instagram.com/explore/tags/전주헬스트레이너")
    url_lst.append("https://www.instagram.com/explore/tags/전주회사원")
    url_lst.append("https://www.instagram.com/explore/tags/전주강사")
    url_lst.append("https://www.instagram.com/explore/tags/전주골프")
    url_lst.append("https://www.instagram.com/explore/tags/전주주부")
    url_lst.append("https://www.instagram.com/explore/tags/전주대학생")
    url_lst.append("https://www.instagram.com/explore/tags/전주플로리스트")
    url_lst.append("https://www.instagram.com/explore/tags/전주네일아트")
    url_lst.append("https://www.instagram.com/explore/tags/전주연예인지망생")
    url_lst.append("https://www.instagram.com/explore/tags/전주필라테스")
    url_lst.append("https://www.instagram.com/explore/tags/전주필라테스강사")
    url_lst.append("https://www.instagram.com/explore/tags/전주pilates")
    url_lst.append("https://www.instagram.com/explore/tags/원주무용")
    url_lst.append("https://www.instagram.com/explore/tags/원주모델")
    url_lst.append("https://www.instagram.com/explore/tags/원주요가")
    url_lst.append("https://www.instagram.com/explore/tags/원주운동")
    url_lst.append("https://www.instagram.com/explore/tags/원주물리치료")
    url_lst.append("https://www.instagram.com/explore/tags/원주요가강사")
    url_lst.append("https://www.instagram.com/explore/tags/원주승무원")
    url_lst.append("https://www.instagram.com/explore/tags/원주헬스트레이너")
    url_lst.append("https://www.instagram.com/explore/tags/원주회사원")
    url_lst.append("https://www.instagram.com/explore/tags/원주강사")
    url_lst.append("https://www.instagram.com/explore/tags/원주골프")
    url_lst.append("https://www.instagram.com/explore/tags/원주주부")
    url_lst.append("https://www.instagram.com/explore/tags/원주대학생")
    url_lst.append("https://www.instagram.com/explore/tags/원주플로리스트")
    url_lst.append("https://www.instagram.com/explore/tags/원주네일아트")
    url_lst.append("https://www.instagram.com/explore/tags/원주연예인지망생")
    url_lst.append("https://www.instagram.com/explore/tags/원주필라테스")
    url_lst.append("https://www.instagram.com/explore/tags/원주필라테스강사")
    url_lst.append("https://www.instagram.com/explore/tags/원주pilates")
    url_lst.append("https://www.instagram.com/explore/tags/광주무용")
    url_lst.append("https://www.instagram.com/explore/tags/광주모델")
    url_lst.append("https://www.instagram.com/explore/tags/광주요가")
    url_lst.append("https://www.instagram.com/explore/tags/광주운동")
    url_lst.append("https://www.instagram.com/explore/tags/광주물리치료")
    url_lst.append("https://www.instagram.com/explore/tags/광주요가강사")
    url_lst.append("https://www.instagram.com/explore/tags/광주승무원")
    url_lst.append("https://www.instagram.com/explore/tags/광주헬스트레이너")
    url_lst.append("https://www.instagram.com/explore/tags/광주회사원")
    url_lst.append("https://www.instagram.com/explore/tags/광주강사")
    url_lst.append("https://www.instagram.com/explore/tags/광주골프")
    url_lst.append("https://www.instagram.com/explore/tags/광주주부")
    url_lst.append("https://www.instagram.com/explore/tags/광주대학생")
    url_lst.append("https://www.instagram.com/explore/tags/광주플로리스트")
    url_lst.append("https://www.instagram.com/explore/tags/광주네일아트")
    url_lst.append("https://www.instagram.com/explore/tags/광주연예인지망생")
    url_lst.append("https://www.instagram.com/explore/tags/광주필라테스")
    url_lst.append("https://www.instagram.com/explore/tags/광주필라테스강사")
    url_lst.append("https://www.instagram.com/explore/tags/광주pilates")
    url_lst.append("https://www.instagram.com/explore/tags/제주도무용")
    url_lst.append("https://www.instagram.com/explore/tags/제주도모델")
    url_lst.append("https://www.instagram.com/explore/tags/제주도요가")
    url_lst.append("https://www.instagram.com/explore/tags/제주도운동")
    url_lst.append("https://www.instagram.com/explore/tags/제주도물리치료")
    url_lst.append("https://www.instagram.com/explore/tags/제주도요가강사")
    url_lst.append("https://www.instagram.com/explore/tags/제주도승무원")
    url_lst.append("https://www.instagram.com/explore/tags/제주도헬스트레이너")
    url_lst.append("https://www.instagram.com/explore/tags/제주도회사원")
    url_lst.append("https://www.instagram.com/explore/tags/제주도강사")
    url_lst.append("https://www.instagram.com/explore/tags/제주도골프")
    url_lst.append("https://www.instagram.com/explore/tags/제주도주부")
    url_lst.append("https://www.instagram.com/explore/tags/제주도대학생")
    url_lst.append("https://www.instagram.com/explore/tags/제주도플로리스트")
    url_lst.append("https://www.instagram.com/explore/tags/제주도네일아트")
    url_lst.append("https://www.instagram.com/explore/tags/제주도연예인지망생")
    url_lst.append("https://www.instagram.com/explore/tags/제주도필라테스")
    url_lst.append("https://www.instagram.com/explore/tags/제주도필라테스강사")
    url_lst.append("https://www.instagram.com/explore/tags/제주도pilates")

    lst = []
    url_cnt = 0
    while True:
        # url = "https://www.instagram.com/explore/tags/{0}{1}/".format(local[local_cnt], tag[tag_cnt])
        driver.get(url_lst[url_cnt])
        try:
            cnt = WD.web_driver_wait(driver, '//*[@id="react-root"]/section/main/header/div[2]/div/div/div/span').text
        except:
            cnt = 0

        lst.append({url_lst[url_cnt][url_lst[url_cnt].find("tags/")+5:]:cnt})
        url_cnt += 1


def get_network_header(driver, url):
    id_data = []
    data = 0
    for request in driver.requests:
        if request.response:
            data_response = request.response
            # https://www.instagram.com/explore/tags/%EC%84%9C%EC%9A%B8%EB%AC%B4%EC%9A%A9/?__a=1&__d=dis
            try:
                if len(re.findall('https://www.instagram.com/explore/tags/[^ ]+/?__a=1&__d=dis', request.url)) == 1:
                    print(data)
                    print(request.url)
                    search_word = parse.unquote(request.url)
                    search_word = search_word[search_word.find("tags/") + 5:search_word.find("?__a=1&__d=dis") - 1]

                    decode_data = decode(data_response.body,
                                         data_response.headers.get('Content-Encoding', 'identity')).decode('utf-8')
                    json_data = json.loads(decode_data)

                    # json_data['data']['recent']['sections'][0]['layout_content']['medias'][0]['media']['user']['username']
                    print(len(json_data['data']['recent']['sections']))
                    for sections_data in json_data['data']['recent']['sections']:
                        print(len(sections_data['layout_content']['medias']))
                        for medias in sections_data['layout_content']['medias']:
                            id_data.append({
                                "검색어": search_word,
                                "이름": medias['media']['user']['username'],
                                "전체이름": medias['media']['user']['full_name']})

                    for sections_data in json_data['data']['top']['sections']:
                        print(len(sections_data['layout_content']['medias']))
                        for medias in sections_data['layout_content']['medias']:
                            id_data.append({
                                "검색어": search_word,
                                "이름": medias['media']['user']['username'],
                                "전체이름": medias['media']['user']['full_name']})

                if len(re.findall('https://i.instagram.com/api/v1/tags/[^ ]+/sections', request.url)) == 1:
                    print(data)
                    print(request.url)
                    search_word = parse.unquote(request.url)
                    search_word = search_word[search_word.find("tags/") + 5:search_word.find("sections") - 1]

                    decode_data = decode(data_response.body,
                                         data_response.headers.get('Content-Encoding', 'identity')).decode('utf-8')
                    json_data = json.loads(decode_data)
                    # id_data.extend(re.findall(r'username":"[a-zA-Z-0-9_]+"', decode_data))
                    # print('서울무용 tags', id_data)

                    # json_data['data']['recent']['sections'][0]['layout_content']['medias'][0]['media']['user']['username']
                    for sections_data in json_data['sections']:
                        print(len(sections_data['layout_content']['medias']))
                        for medias in sections_data['layout_content']['medias']:
                            id_data.append({
                                "검색어": search_word,
                                "이름": medias['media']['user']['username'],
                                "전체이름": medias['media']['user']['full_name']})


            except:
                print("1234")

            data += 1
            x = list({name_data['이름']: name_data for name_data in id_data}.values())
            df = pd.DataFrame(x)
            df.to_excel("{0} id.xlsx".format(url[url.find("tags/") + 5:]))


def detail_get(main_id_data):
    save_data = []
    for main_data in main_id_data:
        id_data = main_data['이름']

        id_url = "https://www.instagram.com/" + id_data
        driver.get(id_url)

        def find_data(driver, path):
            try:
                return driver.find_element_by_xpath(path).text.replace("\n", " ")
            except:
                return ""

        name = find_data(driver, '//*[@id="react-root"]/section/main/div/header/section/div[2]/span')
        work_type = find_data(driver, '//*[@id="react-root"]/section/main/div/header/section/div[2]/div[1]/div')
        soge = find_data(driver, '//*[@id="react-root"]/section/main/div/header/section/div[2]/div[2]')

        if work_type == "" and soge == "":
            soge = find_data(driver, '//*[@id="react-root"]/section/main/div/header/section/div[2]/div')
        link = find_data(driver, '//*[@id="react-root"]/section/main/div/header/section/div[2]/a/div')

        gasimul = WD.web_driver_wait(driver,
                                     '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/div/span').get_attribute(
            "title")
        if gasimul == "":
            gasimul = WD.web_driver_wait(driver,
                                         '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/div/span').text

        follower = WD.web_driver_wait(driver,
                                      '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/div/span').get_attribute(
            "title")

        if follower == "":
            follower = WD.web_driver_wait(driver,
                                          '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/div/span').text

        follow = WD.web_driver_wait(driver,
                                    '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/div/span').get_attribute(
            "title")
        if follow == "":
            follow = WD.web_driver_wait(driver,
                                        '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/div/span').text

        etc = WD.web_driver_wait(driver, '//*[@id="react-root"]/section/main/div/header/section/div[2]').text.replace(
            "\n", " ")
        main_data.update(
            {"성별": "수집불가능",
             "아이디": id_data,
             "이름": name,
             "게시물": gasimul,
             "팔로워": follower,
             "팔로잉": follow,
             "직업": work_type,
             "소개": soge,
             "링크": link,
             "기타": etc,
             }
        )



def process_test(local, tag, process_core):
    time.sleep(int(process_core)*1)
    print(local, tag, process_core, "1234")


if __name__ == '__main__':

    local_cnt = 0
    tag_cnt = 0

    url_cnt = 0
    url_lst = []

    url_lst.append("https://www.instagram.com/explore/tags/경기도필라테스")
    url_lst.append("https://www.instagram.com/explore/tags/경기도필라테스강사")
    url_lst.append("https://www.instagram.com/explore/tags/경기도pilates")

    while True:
        driver = WD.browser_open('', 'https://www.instagram.com/', headress_mode=False, proxy_ip="", mobile_mode=False)
        # pickle.dump(driver.get_cookies(), open("cookies_mskpro1234.pkl", "wb"))
        cookies = pickle.load(open("cookies_mskpro1234.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

        lst = []
        url = url_lst[url_cnt]
        driver.get(url)
        set_scrolling(driver)
        get_network_header(driver, url)

        driver.close()
        data = 0
        url_cnt += 1
