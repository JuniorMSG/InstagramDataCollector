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

def data_get(driver, local, tag, process_core):


    url = "https://www.instagram.com/explore/tags/{0}{1}/"
    id_lst = []
    driver.get(url.format(local, tag))

    SCROLL_PAUASE_TIME = 3
    while True:

       status = 0

       last_height = driver.execute_script("return document.body.scrollHeight")
       while True:
           status +=1
           driver.execute_script("window.scrollTo(0, 0);")
           time.sleep(2)
           driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
           time.sleep(2)
           if status == 15:
               break

       new_height = driver.execute_script("return document.body.scrollHeight")
       print(new_height, last_height)
       if new_height == last_height:
           break
       else:
           last_height = new_height
           continue

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


def process_test(local, tag, process_core):
    time.sleep(int(process_core)*1)
    print(local, tag, process_core, "1234")


if __name__ == '__main__':


    local = ["서울", "경기도", "부산", "대구", "대전", "전주", "원주", "광주", "제주도"]
    tag = []
    tag.append("무용")
    tag.append("모델")
    tag.append("운동")
    tag.append("물리치료")
    tag.append("요가강사")
    tag.append("승무원")
    tag.append("헬스트레이너")
    tag.append("회사원")
    tag.append("강사")
    tag.append("골프")
    tag.append("주부")
    tag.append("대학생")
    tag.append("플로리스트")
    tag.append("네일아트")
    tag.append("연예인지망생")
    tag.append("필라테스강사")
    tag.append("필라테스")
    tag.append("pilates")

    id_lst = []
    local_cnt = 0
    tag_cnt = 0

    process_core = list(range(0, 2))


    local_cnt = 0
    tag_cnt = 0
    procs = []
    process_cnt = 0

    while True:

        # for idx, proc in enumerate(procs):
        #     if not proc.is_alive():
        #         del(procs[idx])
        #         break

        # if len(procs) <= len(process_core):
            # time.sleep(10)
            # process_cnt += 1
            # proc = multiprocessing.Process(target=data_get, args=(local[local_cnt], tag[tag_cnt], process_cnt))
            # procs.append(proc)
            # proc.start()

        driver = WD.browser_open('', 'https://www.instagram.com/',
                                 headress_mode=False, proxy_ip="", mobile_mode=False)
        # pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

        data_get(driver, local[local_cnt], tag[tag_cnt], process_cnt)

        lst = []
        while True:
            url = "https://www.instagram.com/explore/tags/{0}{1}/".format(local[local_cnt], tag[tag_cnt])
            driver.get(url)
            lst.append({"{0}{1}".format(local, tag): WD.web_driver_wait(driver, '//*[@id="react-root"]/section/main/header/div[2]/div/div/div/span').text})

            if tag_cnt < len(tag) - 1:
                tag_cnt += 1
            else:
                local_cnt += 1
                tag_cnt = 0
                if local_cnt == len(local) - 1:
                    break

            """
            
            data = 0
                for request in driver.requests:
                
                    if request.response:
                        data += 1
                        try:
                            print(
                                request.url,
                                request.response.status_code,
                                request.response.headers['Content-Type'],
                                data
                                # request.response.body,
                                # print(decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity')).decode('utf-8')),
                                # 
                            )
                        except:
                            print("encoding error")

            
            """

            """
                decode_data = decode(driver.requests[138].response.body, driver.requests[138].response.headers.get('Content-Encoding', 'identity')).decode('utf-8')
                set(re.findall(r'username":"[a-z]+"' , decode_data))
            """
            data = 0
            id_data = []
            for request in driver.requests:

                if request.response:
                    data_response = request.response
                    # https://www.instagram.com/explore/tags/%EC%84%9C%EC%9A%B8%EB%AC%B4%EC%9A%A9/?__a=1&__d=dis
                    try:
                        if len(re.findall('https://www.instagram.com/explore/tags/[^ ]+/?__a=1&__d=dis', request.url)) == 1:
                            print(data)
                            print(request.url)

                            search_word = parse.unquote(request.url)
                            search_word = search_word[search_word.find("tags/")+5:search_word.find("?__a=1&__d=dis")-1]

                            decode_data = decode(data_response.body, data_response.headers.get('Content-Encoding', 'identity')).decode('utf-8')
                            json_data = json.loads(decode_data)

                            # json_data['data']['recent']['sections'][0]['layout_content']['medias'][0]['media']['user']['username']
                            print(len(json_data['data']['recent']['sections']))
                            for sections_data in json_data['data']['recent']['sections']:
                                print(len(sections_data['layout_content']['medias']))
                                for medias in sections_data['layout_content']['medias']:
                                    id_data.append({
                                        "검색어": search_word,
                                        "이름" : medias['media']['user']['username'],
                                        "전체이름" : medias['media']['user']['full_name']})

                            for sections_data in json_data['data']['top']['sections']:
                                print(len(sections_data['layout_content']['medias']))
                                for medias in sections_data['layout_content']['medias']:
                                    id_data.append({
                                        "검색어": search_word,
                                        "이름" : medias['media']['user']['username'],
                                        "전체이름" : medias['media']['user']['full_name']})


                        if len(re.findall('https://i.instagram.com/api/v1/tags/[^ ]+/sections', request.url)) == 1:
                            print(data)
                            print(request.url)
                            search_word = parse.unquote(request.url)
                            search_word = search_word[search_word.find("tags/")+5:search_word.find("sections")-1]

                            decode_data = decode(data_response.body, data_response.headers.get('Content-Encoding', 'identity')).decode('utf-8')
                            json_data = json.loads(decode_data)
                            # id_data.extend(re.findall(r'username":"[a-zA-Z-0-9_]+"', decode_data))
                            # print('서울무용 tags', id_data)

                            # json_data['data']['recent']['sections'][0]['layout_content']['medias'][0]['media']['user']['username']
                            for sections_data in json_data['sections']:
                                print(len(sections_data['layout_content']['medias']))
                                for medias in sections_data['layout_content']['medias']:
                                    id_data.append({
                                        "검색어" : search_word,
                                        "이름" : medias['media']['user']['username'],
                                        "전체이름" : medias['media']['user']['full_name'],
                                        "총 조회건" : len(id_data)}
                                    )
                    except:
                        print("1234")

                    data += 1



                    x = list({name_data['이름']: name_data for name_data in id_data}.values())
                    df = pd.DataFrame(x)

                    df.to_excel("서울운동 id.xlsx")