import time
import pandas as pd
import componant.webDriver as WD
import re
import json
from seleniumwire.utils import decode
from urllib import parse
import datetime as datetime
from selenium.webdriver.common.keys import Keys
import random




def searchKeyword(driver, strkeyword):
    url = "https://www.instagram.com/explore/tags/{}/".format(strkeyword)
    driver.get(url)
    time.sleep(3)

def searchUserId(driver, strUserId):
    url = "https://www.instagram.com/{0}/".format(strUserId)
    driver.get(url)
    time.sleep(3)

def set_scrolling2():
    element = driver.find_element_by_xpath("//body")

    while True:
       status = 0
       last_height = driver.execute_script("return document.body.scrollHeight")


       while True:
           status +=1

           if status == 14 or status == 27 or status == 40:
               element.send_keys(Keys.PAGE_UP)

           if status == 10 or status == 32 or status == 48:
               element.send_keys(Keys.SPACE)

           element.send_keys(Keys.PAGE_DOWN)
           element.send_keys(Keys.SPACE)
           time.sleep(random.uniform(1.2, 2.5))

           if status == 40:
               break

       new_height = driver.execute_script("return document.body.scrollHeight")
       print(new_height, last_height)
       if new_height == last_height:
           break
       else:
           last_height = new_height
           continue

def set_scrolling(driver):

    element = driver.find_element_by_xpath("//body")

    while True:
       status = 0
       last_height = driver.execute_script("return document.body.scrollHeight")


       while True:
           status +=1

           if status == 14 or status == 27 or status == 40:
               element.send_keys(Keys.PAGE_UP)

           if status == 10 or status == 32 or status == 48:
               element.send_keys(Keys.SPACE)

           element.send_keys(Keys.PAGE_DOWN)
           # element.send_keys(Keys.SPACE)
           time.sleep(random.uniform(1.5, 2.5))

           if status == 40:
               break

       new_height = driver.execute_script("return document.body.scrollHeight")
       print(new_height, last_height)
       if new_height == last_height:
           break
       else:
           last_height = new_height
           continue

def data_get(driver, local, tag, process_core):

    # 넘기면서 데이터 수집하기 ( 금방 막힌다. )
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

def set_medais_data(json_data):

    medias_lst = []
    for medias in json_data['layout_content']['medias']:
        address = ""
        try:
            address = medias['media']['location']['address']
        except:
            address = ""

        photoname = ""
        try:
            photoname = medias['media']['location']['short_name']
        except:
            photoname = ""

        next_max_id = ""
        try:
            next_max_id = medias['media']['next_max_id']
        except:
            next_max_id =""

        like_count = ""
        try:
            like_count = medias['media']['like_count']
        except:
            like_count =""

        try:
            comment_count = medias['media']['comment_count']
        except:
            comment_count =""

        try:
            ga_url = "https://www.instagram.com/p/{0}/".format(medias['media']['code'])
        except:
            ga_url = ""

        try:
            user_name = medias['media']['user']['username']
        except:
            user_name = ""
        try:
            full_name = medias['media']['user']['full_name']
        except:
            full_name = ""
        try:
            text = medias['media']['caption']['text']
        except:
            text = ""

        try:
            timeStamp = str(medias['media']['device_timestamp'])
        except:
            timeStamp = ""

        try:
            time = datetime.fromtimestamp(int(timeStamp[0:10])).isoformat()
        except:
            time = ""

        try:
            user_pk = medias['media']['user']['pk']
        except:
            user_pk = ""

        try:
            media_id_pk = medias['media']['id']
        except:
            media_id_pk = ""

        try:
            media_pk = medias['media']['pk']
        except:
            media_pk = ""

        try:
            media_type = medias['media']['media_type']
            if media_type == 1:
                media_type_nm = "이미지"
                image_cnt = 1
                image_url = medias['media']['image_versions2']['candidates'][0]['url']
                image_media_type = medias['media']['media_type']
                image_height = medias['media']['original_height']
                image_width = medias['media']['original_width']
                video_duration = ""
                video_play_cnt = ""
                video_url =  ""

            elif media_type == 2:
                media_type_nm = "동영상"
                image_cnt = 0
                image_url = ""
                image_media_type = ""
                image_height = ""
                image_width = ""
                video_duration = medias['media']['video_duration']
                video_play_cnt = medias['media']['view_count']
                video_url = medias['media']['video_versions'][0]['url']

            elif media_type == 8:
                media_type_nm = "이미지 여러장"
                image_cnt = medias['media']['carousel_media_count']
                image_url = medias['media']['carousel_media'][0]['image_versions2']['candidates'][0]['url']
                image_media_type = medias['media']['carousel_media'][0]['media_type']
                image_height = medias['media']['carousel_media'][0]['original_height']
                image_width = medias['media']['carousel_media'][0]['original_width']
                video_duration = ""
                video_play_cnt = ""
                video_url = ""

            else:
                media_type_nm = ""
                image_cnt = ""
                image_url = ""
                image_media_type = ""
                image_height = ""
                image_width = ""
                video_duration = ""
                video_play_cnt = ""
                video_url =  ""
        except:
            media_type_nm = ""
            image_cnt = ""
            image_url = ""
            image_media_type = ""
            image_height = ""
            image_width = ""
            video_duration = ""
            video_play_cnt = ""
            video_url = ""

        medias_lst.append({
            "이름": user_name,
            "전체이름": full_name,
            "주소": address,
            "사진명": photoname,
            "게시물 텍스트": text,
            "next_max_id": next_max_id,
            "like_count": like_count,
            "comment_count": comment_count,
            "timeStamp":timeStamp,
            "time":time,
            "url": ga_url,
            "유저고유번호" : user_pk,
            "미디어 아이디" : media_id_pk,
            "미디어 PK" : media_pk,
            "미디어 타입" : media_type,
            "미디어 타입명": media_type_nm,
            "이미지 개수" : image_cnt,
            "이미지 URL" : image_url,
            "이미지 타입" : image_media_type,
            "가로사이즈" : image_width,
            "세로사이즈" : image_height,
            "비디오": video_duration,
            "조회수": video_play_cnt,
            "비디오 URL":video_url
        })

    return medias_lst

def set_request_json_data(request):

    search_word = parse.unquote(request.url)
    search_word = search_word[search_word.find("tags/") + 5:search_word.find("?__a=1&__d=dis") - 1]
    # data_response = driver.requests[116].response
    data_response = request.response
    decode_data = decode(data_response.body,
                         data_response.headers.get('Content-Encoding', 'identity')).decode('utf-8')

    json_data = json.loads(decode_data)

    id_data = []
    try:
        temp_lst = []
        for sections_data in json_data['data']['recent']['sections']:
            temp_lst.extend(set_medais_data(sections_data))
            for temp in temp_lst:
                temp.update(
                    {
                        "검색어": search_word,
                        "총건수": json_data['data']['media_count'],
                        "다음페이지": 1
                    }
                )
        id_data.extend(temp_lst)

        temp_lst = []
        for sections_data in json_data['data']['top']['sections']:
            temp_lst.extend(set_medais_data(sections_data))
            for temp in temp_lst:
                temp.update(
                    {
                        "검색어": search_word,
                        "총건수": json_data['data']['media_count'],
                        "다음페이지": "TOP"
                    }
                )
        id_data.extend(temp_lst)
    except:
        print("NONE")

    try:
        temp_lst = []
        for sections_data in json_data['sections']:
            temp_lst.extend(set_medais_data(sections_data))
            for temp in temp_lst:
                try:
                    next_page = json_data['next_page']
                except:
                    next_page = "last_page"

                temp.update(
                    {
                        "검색어": search_word,
                        "총건수": "",
                        "다음페이지": next_page
                    }
                )
        id_data.extend(temp_lst)
    except:
        print("NONE")

    json_data_save = []
    try:
        json_data_save.append(json_data)
    except:
        print('json_Data_ADD ERROR')

    return id_data, json_data_save


def get_network_header(driver, url):
    id_data = []
    json_lst_Data = []
    data = 0
    for request in driver.requests:
        if request.response:
            data_response = request.response
            # https://www.instagram.com/explore/tags/%EC%84%9C%EC%9A%B8%EB%AC%B4%EC%9A%A9/?__a=1&__d=dis
            try:
                if len(re.findall('https://www.instagram.com/explore/tags/[^ ]+/?__a=1&__d=dis', request.url)) == 1:
                    id_lst_data, json_data = set_request_json_data(request)
                    id_data.extend(id_lst_data)
                    json_lst_Data.extend(json_data)
                    print(data)
                if len(re.findall('https://i.instagram.com/api/v1/tags/[^ ]+/sections', request.url)) == 1:
                    id_lst_data, json_data = set_request_json_data(request)
                    id_data.extend(id_lst_data)
                    json_lst_Data.extend(json_data)
                    print(data)
            except:
                print("1234")

            data += 1
    try:
        file_path = '{0}'.format(url[url.find("tags/") + 5:])
        with open(file_path, 'w') as outfile:
            json.dump(json_lst_Data, outfile)
    except:
        print("JSON_DUMB ERROR")

    x = list({name_data['이름']: name_data for name_data in id_data}.values())
    df = pd.DataFrame(x)


    df.to_excel("{0} id.xlsx".format(url[url.find("tags/") + 5:]))
    df = pd.DataFrame(id_data)
    df.to_excel("{0} ga.xlsx".format(url[url.find("tags/") + 5:]))


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

def computer_mode(driver, id_pw_cnt, id_lst, pw_lst):
    elem_id = WD.web_driver_wait(driver, '//*[@id="loginForm"]/div/div[1]/div/label/input')
    elem_pw = WD.web_driver_wait(driver, '//*[@id="loginForm"]/div/div[2]/div/label/input')
    elem_id.clear()

    elem_id.send_keys(id_lst[id_pw_cnt])

    time.sleep(1)
    elem_pw.clear()
    elem_pw.send_keys(pw_lst[id_pw_cnt])
    time.sleep(2)
    WD.web_driver_wait(driver, '//*[@id="loginForm"]/div/div[3]/button/div').click()
    time.sleep(5)

def mobile_mode(driver, id_pw_cnt, id_lst, pw_lst):
    # login button
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div/div/div/div[3]/button[1]').click()

    elem_id = WD.web_driver_wait(driver, '//*[@id="loginForm"]/div[1]/div[3]/div/label/input')
    elem_pw = WD.web_driver_wait(driver, '//*[@id="loginForm"]/div[1]/div[4]/div/label/input')
    elem_id.clear()

    elem_id.send_keys(id_lst[id_pw_cnt])

    time.sleep(1)
    elem_pw.clear()
    elem_pw.send_keys(pw_lst[id_pw_cnt])
    time.sleep(2)
    WD.web_driver_wait(driver, '//*[@id="loginForm"]/div[1]/div[6]/button/div').click()
    time.sleep(5)

if __name__ == '__main__':

    local_cnt = 0
    tag_cnt = 0

    url_cnt = 0
    url_lst = []

    url_lst.append("https://www.instagram.com/explore/tags/부산모델")



    # pickle.dump(driver.get_cookies(), open("cookies_mskpro1234.pkl", "wb"))
    # cookies = pickle.load(open("cookies_msgpro00001.pkl", "rb"))
    # for cookie in cookies:
    #     driver.add_cookie(cookie)

    mobile = True
    id_pw_cnt = 1

    id_lst = []
    pw_lst = []



    while True:


        # driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')

        lst = []
        url = url_lst[url_cnt]

        driver = WD.browser_open('', 'https://www.instagram.com/', headress_mode=False, proxy_ip="", mobile_mode=mobile)
        if mobile_mode:
            mobile_mode(driver, id_pw_cnt, id_lst, pw_lst)
        else:
            computer_mode(driver, id_pw_cnt, id_lst, pw_lst)


        driver.get(url)
        set_scrolling(driver)
        get_network_header(driver, url)


        # driver.close()
        print(time.strftime("%y/%m/%d %H:%M:%S"))

        # del driver.requests
        driver.close()

        data = 0
        url_cnt += 1
        id_pw_cnt += 1
        if id_pw_cnt == len(id_lst):
            id_pw_cnt = 0
