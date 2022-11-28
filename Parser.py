# parsing the prada site and loading in json file all products and photos

import json
import  os
import csv
import re
import time
import requests
from bs4 import BeautifulSoup

def get_products(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36"
    }
    req = requests.get(url, headers=headers)
    return req

# save page code and return open document
def create_read_file(name, src):

    with open(f"{name}", "w", encoding="utf-8") as file:
        file.write(src)

    with open(f"{name}", "r", encoding="utf-8") as file:
        src = file.read()

    return src

def create_json_file(name, src):
    # saving dictionary in json file
    with open(f"{name}", "w", encoding="utf-8") as file:
        json.dump(src, file, indent=4, ensure_ascii=False)

    # open each page and save to file
    with open(f"{name}", encoding="utf-8") as file:
        all_categories = json.load(file)

    return all_categories

def create_folder(name_folder, src):

    # creating a folder with the code of all pages
    if not os.path.isdir(name_folder):
        os.mkdir(name_folder)

        # creating a file with the code of the main page
        src = create_read_file(f"{name_folder}/index.html", src)

def download_information(href, name_folder):
    # find and download info and jpg
    src = get_products(href).text
    soup = BeautifulSoup(src, "lxml")
    all_products = soup.find_all(class_="productQB__desc")
    info = []
    count = 1
    for el in all_products:
        title = el.find("div", class_="productQB__title")
        price = el.find(class_="productQB__infoPrice")
        name = title.text.strip()
        price = price.text.strip()
        if name in info:
            count += 1
            info.append(
                {
                    "Name": f"{name}_{count}",
                    "Price": price
                }
            )

        else:
            info.append(
                {
                    "Name": name,
                    "Price": price
                }
            )

        with open(f"{name_folder}.csv", "a") as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    name,
                    price
                )
            )
        # create_json_file(f"{name_folder}.json", str(info))
    return info

def main():
    # creating the main page in json format
    start_folder = 'main_folder'
    url = "https://www.prada.com/gb/en.html/"
    req = get_products(url)
    src = req.text
    create_folder(start_folder, src)
    soup = BeautifulSoup(src, "lxml")

    # creating list of all folders
    # all_href = set()
    # for el in soup.find_all("a"):
    #     if "www.prada.com" in str(el.get("href")).split("/") and "gb" in str(el.get("href")).split("/"):
    #         all_href.add(el.get("href"))
    # src = create_read_file("main_folder/all_href.csv", "\n".join(sorted(list(all_href))))

    # parsing the categories
    # for el in src.split("\n"):
        # categories = el.split("/")
        # path = f"{start_folder}"
        # for categorie in categories[5:]:
        #     if os.path.exists(f"{path}/{categorie}") == False:
        #         os.mkdir(f"{path}/{categorie.split('.')[0]}")
        #     path += f"/{categorie.split('.')[0]}"
        #     print(path)

        # src = get_products(el).text
        # download all site
        # create_read_file(f"{path}/index_{'_'.join(categories[5:])}", src)
        # create_read_file(f"{path}/index_{'_'.join(categories[5:]).split('.')[0]}.csv", el)
    try:
        print(download_information("https://www.prada.com/gb/en/men/accessories/belts.html", r"C:\Users\vsavc\OneDrive\Desktop\GIT\Parsing_Prada\main_folder\men\accessories\belts\index_men_accessories_belts"))
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
