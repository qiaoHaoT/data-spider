from bs4 import BeautifulSoup
import requests
import csv
import time
import datetime


now_time = datetime.datetime.now()
header = {
    'cookie':'sessid=1B96764F-31ED-EFC2-FABE-2AA1C65D898C; aQQ_ajkguid=7BEEE216-5F79-E72D-427F-EB2E5339131C; twe=2; _ga=GA1.2.1995018315.1610460263; _gid=GA1.2.1413394280.1610460263; id58=e87rkF/9rGaEN0g4DXVXAg==; 58tj_uuid=e4cce325-0e9e-4b1f-8b4e-d753a9ac76dc; init_refer=https%253A%252F%252Fwww.baidu.com%252Fother.php%253Fsc.0f00000IWzUM_aFMApNZcnD1t0tx7lIbNYgOu_kVPvr1pzkEcuWkFTDvvE__3N7iDGRYGH8cvfrQz-riohNjHKNhiuxAivwoojaJriG5fs-bVUw6SY-rJ7hj1koPUTw7_aZjKFL92txPu-h2acXc8o5obZBD0q1QP9GCtY6cfBOFhlDQWvvYMRcfco389aVFjUUGvEaEkN-yUq80U9syGX5oMIsh.DY_NR2Ar5Od663rj6thm_8jViBjEWXkSUSwMEukmnSrZr1wC4eL_8C5RojPak3S5Zm0.TLFWgv-b5HDkrfK1ThPGujYknHb0THY0IAYq_Q2SYeOP0ZN1ugFxIZ-suHYs0A7bgLw4TARqnsKLULFb5UazEVrO1fKzmLmqnfKdThkxpyfqnHRzn1fYnWTLP6KVINqGujYkPjD4nHm3rfKVgv-b5HDsrjndn1Dd0AdYTAkxpyfqnHDdn1f0TZuxpyfqn0KGuAnqiDFK0APzm1Y1rHbYn0%2526ck%253D6360.3.127.323.154.326.156.712%2526dt%253D1610460258%2526wd%253D%2525E5%2525AE%252589%2525E5%2525B1%252585%2525E5%2525AE%2525A2%2526tpl%253Dtpl_11534_24217_20411%2526l%253D1523442776%2526us%253DlinkName%25253D%252525E6%252525A0%25252587%252525E5%25252587%25252586%252525E5%252525A4%252525B4%252525E9%25252583%252525A8-%252525E4%252525B8%252525BB%252525E6%252525A0%25252587%252525E9%252525A2%25252598%252526linkText%25253D%252525E5%252525AE%25252589%252525E5%252525B1%25252585%252525E5%252525AE%252525A2-%252525E5%25252585%252525A8%252525E6%25252588%252525BF%252525E6%252525BA%25252590%252525E7%252525BD%25252591%252525EF%252525BC%2525258C%252525E6%25252596%252525B0%252525E6%25252588%252525BF%25252520%252525E4%252525BA%2525258C%252525E6%25252589%2525258B%252525E6%25252588%252525BF%25252520%252525E6%2525258C%25252591%252525E5%252525A5%252525BD%252525E6%25252588%252525BF%252525E4%252525B8%2525258A%252525E5%252525AE%25252589%252525E5%252525B1%25252585%252525E5%252525AE%252525A2%252525EF%252525BC%25252581%252526linkType%25253D; new_uv=1; als=0; ctid=12; wmda_uuid=6aa6425c8270b1233526c4cfcfa3322a; wmda_new_uuid=1; wmda_session_id_6289197098934=1610460302834-59032509-eef4-ff79; wmda_visited_projects=%3B6289197098934; new_session=0; obtain_by=2; xxzl_cid=803cf96b77254752a339c0814a61c658; xzuid=b23aa2cc-5b3b-40c0-9107-bef3ee453594',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}
page = 1

out = open('/Users/qiaohaoting/PycharmProjects/data-spider/csv/anjuke_shenzhen_second_hand.csv', 'w', newline='')
csv_write = csv.writer(out, dialect='excel')
csv_write.writerow(['户型', '面积', '楼层', '年份', '小区', '地址', '总价', '单价', '时间'])

while True:
    url = 'https://shenzhen.anjuke.com/sale/p' + str(page) + '/'
    response = requests.get(url, headers=header)

    soup = BeautifulSoup(response.text, 'html.parser')
    list_item = soup.find_all('li', class_="list-item")

    for item in list_item:
        try:
            house_details_str = str(item.find_all('div', class_="house-details"))
            house_soup = BeautifulSoup(house_details_str, 'html.parser')
            details_items_type = BeautifulSoup(str(house_soup.find('div', class_="details-item")))
            house_type_text = details_items_type.text
            house_s = house_type_text.split("|")
            house_type = house_s[0][1:]
            house_area = house_s[1]
            house_high = house_s[2]
            house_year = house_s[3][:-1]

            details_items_address = BeautifulSoup(str(house_soup.find('span', class_="comm-address")))
            details_items_location = details_items_address.text.strip().split("\n")
            house_apartment = details_items_location[0].strip()
            house_address = details_items_location[1].strip()

            pro_price_str = str(item.find_all('div', class_="pro-price"))
            price_soup = BeautifulSoup(pro_price_str, 'html.parser')
            # 总结 单价
            total_price = BeautifulSoup(str(price_soup.find('span', class_="price-det")), 'html.parser').text
            unit_price = BeautifulSoup(str(price_soup.find('span', class_="unit-price")), 'html.parser').text
            csv_write.writerow([house_type, house_area, house_high, house_year, house_apartment, house_address, total_price, unit_price, now_time])
            i = 0
        except:
            print(item.text)

    # 最后一页返回的li标签，不再是a
    is_next = soup.find('a', class_="aNxt")
    if is_next is None:
        # 没有下一页 结束
        break
    page = page + 1
    time.sleep(10)
    print(page)
out.close()
i = 0

