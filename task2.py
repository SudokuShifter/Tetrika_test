import csv
import asyncio
from bs4 import BeautifulSoup
import aiohttp
from collections import Counter

from string import ascii_uppercase



class WikiParser:
    WIKI_URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    FILE_NAME = "beasts.csv"

    ALPHABET_RUS = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П",
                "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "ь", "Э", "Ю", "Я"]
    DICT_COUNTER = {i: 0 for i in ALPHABET_RUS}


    @staticmethod
    def csv_write(res_dict: dict):
        with open(WikiParser.FILE_NAME, 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for k, v in res_dict.items():
                writer.writerow([k, v])


    @staticmethod
    async def get_text_from_url(params, session):
        async with session.get(WikiParser.WIKI_URL, params=params) as response:
            return await response.text()


    @staticmethod
    async def counter_animals(letter, session, detail=None):
        text = await WikiParser.get_text_from_url(detail, session)
        while True:
            parser = BeautifulSoup(text, 'html.parser')
            animals = parser.find('div', attrs={'class': 'mw-category-columns'})
            animals = animals.text.split("\n")
            list_animals = animals[1:]
            letter_for_check = animals[0]
            list_animals = [1 for i in list_animals if i[0] == letter]
            WikiParser.DICT_COUNTER[letter_for_check] += len(list_animals)
            print(letter_for_check)

            params = {'title': 'Категория:Животные_по_алфавиту', 'pagefrom': animals[-1]}
            text = await WikiParser.get_text_from_url(params, session)
            if len(list_animals) < 200:
                return



    @staticmethod
    async def create_tasks():
        tasks = []
        async with aiohttp.ClientSession() as session:
            for letter in WikiParser.ALPHABET_RUS:
                task = asyncio.create_task(
                    WikiParser.counter_animals(
                        letter, session, detail={'title': 'Категория:Животные_по_алфавиту', 'from': letter})
                )
                tasks.append(task)
            await asyncio.gather(*tasks)


    @staticmethod
    def compilation_result():
        asyncio.run(WikiParser.create_tasks())
        res_dict = dict(sorted(WikiParser.DICT_COUNTER.items()))
        WikiParser.csv_write(res_dict)



wiki_parser = WikiParser()
wiki_parser.compilation_result()
