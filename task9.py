'''
Написать программу, которая скачивает изображения с заданных URL-адресов и
сохраняет их на диск. Каждое изображение должно сохраняться в отдельном
файле, название которого соответствует названию изображения в URL-адресе.
� Например URL-адрес: https://example/images/image1.jpg -> файл на диске:
image1.jpg
� Программа должна использовать многопоточный, многопроцессорный и
асинхронный подходы.
� Программа должна иметь возможность задавать список URL-адресов через
аргументы командной строки.
� Программа должна выводить в консоль информацию о времени скачивания
каждого изображения и общем времени выполнения программы.
'''
import time
import requests
from bs4 import BeautifulSoup as bs
import os
import sys
import argparse
import threading
import multiprocessing
import asyncio
import aiohttp


# функция загрузки образа
def download_image(image_url, folder_name):

    start_time = time.time()

    # если путь не существует, сделать этот путь dir
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)

    # получаем имя файла
    filename = os.path.join(folder_name, image_url.split("/")[-1])

    # загружаем изображение
    response = requests.get(image_url, stream=True)

    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
#        f.write(response.content)

    end_time = time.time() - start_time
    print(f"Загружен файл {filename} за {end_time:.2f} секунд")


# функция загрузки образа (asyncio)
async def download_image_async(image_url, folder_name):

    start_time = time.time()

    # если путь не существует, сделать этот путь dir
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)

    # получаем имя файла
    filename = os.path.join(folder_name, image_url.split("/")[-1])

    # загружаем изображение
    response = await asyncio.get_event_loop().run_in_executor(None, requests.get, image_url, {"stream": True})
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    end_time = time.time() - start_time
    print(f"Загружен файл {filename} за {end_time:.2f} секунд")


# получение списка путей образов и результирующей папки
def get_images_folder(url: str | bytes, prefix: str):
    url_images = []
    current_path = os.path.dirname(os.path.abspath(__file__))
    folder_name = os.path.join(current_path, f"{prefix}_image")
    print(folder_name)
    # Возвращает все URL‑адреса изображений по одному `url`
    soup = bs(requests.get(url).content, "html.parser")
    images = soup.find_all("img")
    for image in images:
        ext = os.path.splitext(image["src"])[1]
        if ext == '.jpg':
            url_images.append(image["src"])
    return url_images, folder_name


# потоковая загрузка изображений с сайта
def download_image_threading(url: str | bytes):
    start_time = time.time()
    threads = []

    images, folder_name = get_images_folder(url, "threading")
    for index in range(len(images)):
        if os.path.splitext(images[index])[1] == ".jpg":
            t = threading.Thread(target=download_image, args=(images[index], folder_name,))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()

    end_time = time.time() - start_time
    print(f"Общее время загруски с помощью threading: {end_time:.2f} секунд")


# мультипроцессная загрузка изображений с сайта
def download_image_multiprocessing(url: str | bytes):

    start_time = time.time()
    processes = []

    images, folder_name = get_images_folder(url, "multiprocessing")
    for index in range(len(images)):
        if os.path.splitext(images[index])[1] == ".jpg":
            p = multiprocessing.Process(target=download_image, args=(images[index], folder_name,))
            p.start()
            processes.append(p)

    for p in processes:
        p.join()

    end_time = time.time() - start_time
    print(f"Общее время загруски с помощью multiprocessing: {end_time:.2f} секунд")


# загрузка с помощью asyncio
def download_images_asyncio(url: str | bytes):
    start_time = time.time()
    tasks = []

    images, folder_name = get_images_folder(url, "syncio")

    loop = asyncio.get_event_loop()

    for index in range(len(images)):
        if os.path.splitext(images[index])[1] == ".jpg":
            task = asyncio.ensure_future(download_image_async(images[index], folder_name))
            tasks.append(task)

    loop.run_until_complete(asyncio.wait(tasks))

    end_time = time.time() - start_time
    print(f"Общее время загруски с помощью  asyncio: {end_time:.2f} секунд")


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', nargs='?')
    return parser


if __name__ == "__main__":
    #url = "https://gb.ru"
    parser = createParser()
    url = parser.parse_args(sys.argv[1:]).url
    download_image_threading(url)
    download_image_multiprocessing(url)
    download_images_asyncio(url)


