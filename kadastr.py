#!/bin/python3
# -*- coding: utf-8 -*-
#
# Получение информации о кадастровой стоитмости земельных участков. Так как среди всех тех актов невозмодно найти в каком именно 
# внесены данные о участке, то сделал такой код, который скачивает все файлы, и создаёт csv файл со списком кадастровых
# данных и в каком файле они расположены.
# чтобы узнать с каком файле ваш акт, достаточно  ввести команду:
#    cat kadastr.csv | grep "50:00:0000000:0"
# где "50:00:0000000:0" - кадастровый номер вашего участка
# Данные находятся в открытом источнике, согласно рассылка от ИФНС:
# С предварительными результатами новой кадастровой стоимости вы сможете ознакомиться 1 августа 2022 года.
# Они будут опубликованы на официальных сайтах Министерства имущественных отношений Московской области 
# https://mio.mosreg.ru/ и Центра кадастровой оценки https://ckomo.ru/
#
# Исходный код расположен https://github.com/DimkaInc/Kadastr


import os, sys
# os.system("python3 -m pip install requests beautifulsoup4 pyexcel pyexcel-ods3 --upgrade")
import requests, zipfile, pyexcel as pe
from bs4 import BeautifulSoup
from urllib.parse import urlencode

# Работа в одном файле или через вызов дочернего процесса
only_one = False
# Создание файла результата с нуля
renew_file = False

pg_url = "https://ckomo.ru/01.01.05.14/329"
html_text = requests.get(pg_url).text
soup = BeautifulSoup(html_text, 'html.parser')
base_url = "https://cloud-api.yandex.net/v1/disk/public/resources/download?"

out_file_name = "kadastr.csv"
csv_out_file = open(out_file_name, "a+")

def download(url, file_name):
    print("%s %s скачиваю" % (url, file_name))
    final_url = "%s%s" % (base_url, urlencode(dict(public_key = disk_url)))
    responce = requests.get(final_url)
    del(final_url)
    download_url = responce.json()["href"]
    del(responce)
    download_response = requests.get(download_url)
    with open(file_name, 'wb') as f:
        f.write(download_response.content)
        f.close()
        del(f)
    del(download_response)

def do_zip(file_name):
    if zipfile.is_zipfile(file_name):
        with zipfile.ZipFile(file_name, "r") as zarc:
            for file_info in zarc.infolist():
                if file_info.filename.find(".ods") > -1:
                    stream = zarc.open(file_info, "r").read()
                    ods_work(stream, file_name)
                    del(stream)
                del(file_info)
            zarc.close()
            del(zarc)

def ods_work(stream, file_name):
    global ods_out_file
    ods_book = pe.get_book(file_type = "ods", file_content = stream)
    lines = len(ods_book[0])
    row = 0
    for rows in ods_book[0]:
        row += 1
        print("Строка %d/%d" % (row, lines), end = "\r")
        if str(rows[2]).find(":") > -1:
            csv_out_file.write("'%s','%s'\n" % (rows[2], file_name))
        del(rows)
    del(ods_book)
    del(stream)

lists = []

for link in soup.find_all("a"):
    disk_url = link.get("href")
    if disk_url.find("https://disk.yandex.ru/d/") > -1:
        zip_file = link.text.replace("/", "_") + ".zip"
        lists.append([disk_url, zip_file])
    del(disk_url)
    del(link)
del(soup)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        if renew_file:
            csv_out_file = open(out_file_name, "w")
            csv_out_file.write("'Кадастровый номер','Файл с кадастровым номером'\n")
        else:
            csv_out_file = open(out_file_name, "a+")
        for item in lists:
            if not os.path.exists(item[1]):
                download(item[0], item[1])
                if only_one:
                    do_zip(item[1])
                else:
                    cmd = "%s '%s'" % (sys.argv[0],item[1])
                    res = os.system(cmd)
                    del(res)
            else:
                print(item[0], item[1])
            if renew_file:
                if only_one:
                    do_zip(item[1])
                else:
                    cmd = "%s '%s'" % (sys.argv[0],item[1])
                    res = os.system(cmd)
                    del(res)
            del(item)
        del(lists)
    else:
        csv_out_file = open(out_file_name, "a+")
        for item in sys.argv[1:]:
            do_zip(item)
        csv_out_file.close()
        del(csv_out_file)