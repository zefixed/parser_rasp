import json
import requests as rq
from bs4 import BeautifulSoup as BS


def get_groups():
    r = rq.get("https://rasp.dmami.ru")
    html = BS(r.content, 'html.parser')

    def filter_script(tag):
        return 'var globalListGroups' in tag.text if tag.text else False

    script_tags = html.find_all('script')
    filtered_tags = [tag for tag in script_tags if filter_script(tag)]

    if filtered_tags:
        script_tag = filtered_tags[0]  # Берем первый найденный тег <script>

        # Далее выполняем остальную часть кода
        start_index = script_tag.text.find('{')
        end_index = script_tag.text.rfind('}') + 1
        json_data = script_tag.text[start_index:end_index]

        # Преобразуем JSON-данные в словарь
        data = json.loads(json_data)
        
        # Запись в файл
        with open("groups.json", "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
            
        # Получаем список значений групп
        group_values = list(data['groups'].keys())

        # Выводим список значений групп
        return group_values
    else:
        return ""


if __name__ == "__main__":
    get_groups()

# import psycopg2

# # Подключение к базе данных
# conn = psycopg2.connect(
#     host="localhost",
#     port="5432",
#     database="raspyxxx",
#     user="postgres",
#     password="root"
# )

# # Создание курсора
# cur = conn.cursor()

# # Выполнение SQL-запроса
# for group in get_groups():
#     cur.execute(f"INSERT INTO groups (id, \"group\") VALUES (DEFAULT, '{group}')")
# conn.commit()
