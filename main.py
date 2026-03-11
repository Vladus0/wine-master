from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import os
from dotenv import load_dotenv


def get_the_ending(num):
    first_ending = "год"
    second_ending = "года"
    third_ending = "лет"
    if (num % 100 < 21 and num % 100 > 4):
        return third_ending
    num = num % 10
    if num == 1:
        return first_ending
    if num > 1 and num < 5:
        return second_ending
    else:
        return third_ending


def main():
    load_dotenv()
    wines_xlsx = os.getenv("WINES_LIST")

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    now = datetime.datetime.now()
    foundation_year = 1920
    winery_age = now.year - foundation_year
    

    ending_of_date = get_the_ending(winery_age)
    
    years = f'{winery_age} {ending_of_date}'


    excel_data_three = pandas.read_excel(
        io=wines_xlsx,
        sheet_name="Лист1",
        na_values=['N/A', 'NA'], keep_default_na=False
    ).to_dict('records')

    wines = collections.defaultdict(list)
    for wine in excel_data_three:
        wines[wine['Категория']].append(wine)


    rendered_page = template.render(
        time_with_you=years,
        wine_collections=wines,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()