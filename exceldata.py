import pandas as pd
import os

execl_file_lst = os.listdir("excel")

local = ["서울", "경기도", "부산", "대구", "대전", "전주", "원주", "광주", "제주도"]

tag = []
tag.append("무용")
tag.append("모델")
tag.append("운동")
tag.append("물리치료")
tag.append("요가")
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

lst_ga = []
lst_id = []

local_cnt = 0
while True:
    tag_cnt = 0
    while True:
        lst_ga.append(local[local_cnt] + tag[tag_cnt] + " ga.xlsx")
        lst_id.append(local[local_cnt] + tag[tag_cnt] + " id.xlsx")
        tag_cnt += 1
        if tag_cnt == len(tag):
            tan_cnt = 0
            break
    local_cnt += 1
    if local_cnt == len(local):
        break


lst_data_ga = []
df_1 = pd.DataFrame(index=['이름','전체이름','검색어'])
for file_name in lst_ga:
    try:
        read_data = pd.read_excel("excel/{0}".format(file_name), engine="openpyxl")
        if len(read_data) == 0:
            lst_data_ga.append({"name": file_name, "cnt": 0})
        else:
            main_data = read_data[['이름', '전체이름', '검색어']]
            df_1 = pd.concat([df_1, main_data])
            lst_data_ga.append({"name": file_name, "cnt": len(read_data)})

    except:
        lst_data_ga.append({"name": file_name, "cnt": "미수집"})

pd.DataFrame(lst_data_ga).to_excel("keyword_gasimul.xlsx")
df_1.to_excel("keyword_gasimul_data.xlsx")



lst_data_id = []
df_2 = pd.DataFrame(index=['이름','전체이름','검색어'])
for file_name in lst_id:
    try:
        read_data = pd.read_excel("excel/{0}".format(file_name), engine="openpyxl")
        if len(read_data) == 0:
            lst_data_id.append({"name": file_name, "cnt": 0})
        else:
            main_data = read_data[['이름', '전체이름', '검색어']]
            df_2 = pd.concat([df_2, main_data])
            lst_data_id.append({"name": file_name, "cnt": len(read_data)})
    except:
        lst_data_id.append({"name": file_name, "cnt": "미수집"})

pd.DataFrame(lst_data_id).to_excel("keyword.xlsx")
df_2.to_excel("id_data.xlsx")


