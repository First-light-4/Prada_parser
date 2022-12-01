# parsing the prada site and loading in json file all products and photos

import json
import os
import csv
import requests
from bs4 import BeautifulSoup

def get_products(url, name):
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Mobile Safari/537.36"
    }

    req = requests.get(url, headers=headers)
    src = req.text
    with open(f"{name}.html", "w", encoding="utf-8") as file:
        file.write(src)

    with open(f"{name}.html", "r", encoding="utf-8") as file:
        src = file.read()

    return src

# save page code and return open document
def create_csv_file(name_folder, name, price):

    with open(f"{name_folder}.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                name,
                price
            )
        )

    with open(f"{name_folder}.csv", "r", encoding="utf-8") as file:
        src = file.read()

    return src

def create_json_file(name, src):
    # saving dictionary in json file
    with open(f"{name}.json", "w", encoding="utf-8") as file:
        json.dump(src, file, indent=4, ensure_ascii=False)

    # open each page and save to file
    with open(f"{name}.json", encoding="utf-8") as file:
        all_categories = json.load(file)

    return all_categories

def create_folder(name_folder):

    # creating a folder with the code of all pages
    if not os.path.isdir(name_folder):
        os.mkdir(name_folder)

def download_information(href, name_folder):

    with open(f"{name_folder}.csv", "w") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Name",
                "Price"
            )
        )

    # find and download info and jpg
    src = get_products(href, name_folder)
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

        create_csv_file(name_folder, name, price)
    create_json_file(name_folder, info)
    return info

def main():

    # creating the main page in json format
    start_folder = 'main_folder'
    create_folder(start_folder)
    url = "https://www.prada.com/gb/en.html"
    src = get_products(url, fr"{start_folder}\main")
    soup = BeautifulSoup(src, "lxml")

    # creating list of all folders
    all_href = set()
    for el in soup.find_all("a"):
        if "www.prada.com" in str(el.get("href")).split("/") and "gb" in str(el.get("href")).split("/"):
            all_href.add(el.get("href"))
    src = "\n".join(sorted(list(all_href)))

    with open(fr"{start_folder}\all_href.csv", "w", encoding="utf-8") as file:
        file.write(src)
    print(len(src.split("\n")))
    # parsing the categories
    for el in src.split("\n"):
        categories = el.split("/")
        path = f"{start_folder}"
        for categorie in categories[5:]:
            create_folder(f"{path}/{categorie.split('.')[0]}")
            path += f"\{categorie.split('.')[0]}"
            print(path)
        try:
            print(download_information(el, path+"\\"+path.replace("\\", "_")))
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    main()
