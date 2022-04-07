import time
import pandas as pd
import componant.webDriver as WD
import random

import urllib.request
import time

def searchKeyword(driver, strkeyword):
    url = "https://www.instagram.com/explore/tags/{}/".format(strkeyword)
    driver.get(url)
    time.sleep(3)

def searchUserId(driver, strUserId):
    url = "https://www.instagram.com/{0}/".format(strUserId)
    driver.get(url)
    time.sleep(3)


def find_data(driver, path):
    try:
        return driver.find_element_by_xpath(path).text.replace("\n", " ")
    except:
        return ""

def computer_mode(driver):

    id_url = "https://www.instagram.com/" + id_data
    time.sleep(random.uniform(7, 10))
    # //*[@id="react-root"]/section/main/div/ul/li[1]/div/span
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

    etc = WD.web_driver_wait(driver, '//*[@id="react-root"]/section/main/div/header/section/div[2]').text.replace("\n", " ")

def mobile_data_get_detail(driver, url):
    driver.get(url)
    time.sleep(random.uniform(6, 12))

    try:

        main_data = driver.execute_script("return window._sharedData")
        user_data = main_data['entry_data']["ProfilePage"][0]['graphql']['user']

        edge_followed_by = user_data['edge_followed_by']['count']
        edge_follow = user_data['edge_follow']['count']
        edge_owner_to_timeline_media = user_data['edge_owner_to_timeline_media']['count']
        edge_felix_video_timeline = user_data['edge_felix_video_timeline']['count']
        full_name = user_data['full_name']
        id_pk = user_data['id']
        is_business_account = user_data['is_business_account']
        is_professional_account = user_data['is_professional_account']
        business_category_name = user_data['business_category_name']
        category_enum = user_data['category_enum']
        category_name = user_data['category_name']
        username = user_data['username']
        external_url = user_data['external_url']
        profile_pic_url_hd = user_data['profile_pic_url_hd']
        colc_time = time.strftime('%Y%m%d/%I%M%S')

        # time check
        start = time.time()
        # 이미지 요청 및 다운로드
        urllib.request.urlretrieve(user_data['profile_pic_url_hd'], "./id_img/{0}.jpg".format(id_pk))
        # 이미지 다운로드 시간 체크
        print(time.time() - start)
    except:
        edge_followed_by = ""
        edge_follow = ""
        edge_owner_to_timeline_media = ""
        edge_felix_video_timeline = ""
        full_name = ""
        id_pk = ""
        is_business_account = ""
        is_professional_account = ""
        business_category_name = ""
        category_enum = ""
        category_name = ""
        username = ""
        external_url = ""
        profile_pic_url_hd = ""
        colc_time = time.strftime('%Y%m%d/%I%M%S')
        print("ERROR?")

    return  {
            "edge_followed_by": edge_followed_by, "edge_follow":edge_follow, "edge_owner_to_timeline_media":edge_owner_to_timeline_media,
            "edge_felix_video_timeline": edge_felix_video_timeline, "full_name":full_name, "id_pk":id_pk,
            "is_business_account": is_business_account, "is_professional_account":is_professional_account, "business_category_name":business_category_name,
            "category_enum": category_enum, "category_name":category_name, "username":username,
            "external_url": external_url, "colc_time":colc_time, "profile_pic_url_hd": profile_pic_url_hd,
     }


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
    WD.web_driver_wait(driver, '//*[@id="react-root"]/section/main/article/div/div/div/div[3]/button[1]').click()

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


    mobile = True
    id_pw_cnt = 1


    id_lst = ["id"]
    pw_lst = ['pw']



    df_1 = pd.read_excel("id_data.xlsx", engine="openpyxl")

    id_data = pd.DataFrame(df_1, columns=['이름', 'URL', '전체이름', '검색어'
        , 'edge_follow', 'edge_followed_by', 'edge_owner_to_timeline_media', 'edge_felix_video_timeline'
        , 'username', 'full_name', 'id_pk'
        , 'is_business_account', 'is_professional_account'
        , 'business_category_name', 'category_enum', 'category_name'
        , 'external_url', 'colc_time', 'profile_pic_url_hd'
    ])

    while True:
        id_cnt = 0
        # driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        lst = []
        url = ""

        driver = WD.browser_open('', 'https://www.instagram.com/', headress_mode=False, proxy_ip="", mobile_mode=mobile)
        if mobile_mode:
            mobile_mode(driver, id_pw_cnt, id_lst, pw_lst)
        else:
            computer_mode(driver, id_pw_cnt, id_lst, pw_lst)

        for id_data_index in id_data[id_data['edge_follow'].isnull()].index:
            serach_id = id_data['이름'][id_data_index]
            ret_data = mobile_data_get_detail(driver, "https://www.instagram.com/" + serach_id)
            print(ret_data)

            index = id_data.index[id_data['이름'] == serach_id]
            for inx in index:
                id_data['edge_follow'][inx] = ret_data['edge_follow']
                id_data['edge_followed_by'][inx] = ret_data['edge_followed_by']
                id_data['edge_owner_to_timeline_media'][inx] = ret_data['edge_owner_to_timeline_media']
                id_data['edge_felix_video_timeline'][inx] = ret_data['edge_felix_video_timeline']
                id_data['full_name'][inx] = ret_data['full_name']
                id_data['id_pk'][inx] = ret_data['id_pk']
                id_data['is_business_account'][inx] = ret_data['is_business_account']
                id_data['is_professional_account'][inx] = ret_data['is_professional_account']
                id_data['business_category_name'][inx] = ret_data['business_category_name']
                id_data['category_enum'][inx] = ret_data['category_enum']
                id_data['category_name'][inx] = ret_data['category_name']
                id_data['username'][inx] = ret_data['username']
                id_data['external_url'][inx] = ret_data['external_url']
                id_data['colc_time'][inx] = ret_data['colc_time']
                id_data['profile_pic_url_hd'][inx] = ret_data['profile_pic_url_hd']

            id_data.to_excel("id_data.xlsx", engine="openpyxl")

            # if id_cnt % 250 == 0:
            #     break

        driver.close()
        id_pw_cnt += 1
        if id_pw_cnt == len(id_lst):
            id_pw_cnt = 0
