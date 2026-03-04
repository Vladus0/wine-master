from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import os
from dotenv import load_dotenv


def ending(num, first, second, third):
    if (num % 100 < 21 and num % 100 > 4):
        return third
    num = num % 10
    if num == 1:
        return first
    if num > 1 and num < 5:
        return second
    else:
        return third


def main():
    load_dotenv()
    wines_list = os.getenv("WINES_LIST")

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    now = datetime.datetime.now()
    time_year = 1920
    delta_time = now.year - time_year

    first = "год"
    second = "года"
    third = "лет"


    end = ending(delta_time, first, second, third)
    
    years = (f'{delta_time} {end}')


    excel_data_three = pandas.read_excel(
        io=wines_list,
        sheet_name="Лист1",
        na_values=['N/A', 'NA'], keep_default_na=False
    ).to_dict('records')

    wines_lists = collections.defaultdict(list)
    for wine in excel_data_three:
        wines_lists[wine['Категория']].append(wine)


    rendered_page = template.render(
        time=years,
        wine_collections=wines_lists,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()