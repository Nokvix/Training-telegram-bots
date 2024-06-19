from selenium import webdriver
import time
import requests
import json
from typing import Dict, List, Union
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

LIMIT: int = 20


def get_correct_position(position: str) -> int:
    print('Преобразую позицию в корректную')
    new_pos: str = ''
    for char in position:
        if char.isdigit():
            new_pos += char

    print('Преобразовал позицию в корректную\n')
    return int(new_pos)


def get_position_from_html(driver):
    print('Получаю позицию из html')
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')

    tr = soup.find('tr', class_='Body_row__current-user__t-WHY')
    position = tr.find('td').text
    position = get_correct_position(position)
    print('Получил из html\n')

    return position


def get_user_position(nickname: str, driver: webdriver) -> int:
    print('Получаю позицию игрока')
    try:
        nickname_input = driver.find_element(By.ID, 'searchInput')
        nickname_input.clear()
        nickname_input.send_keys(nickname)
        print('Ввёл ник игрока')
        time.sleep(1)
    except Exception:
        print('Форма ввода никнейма не найдена')

    try:
        driver.find_element(By.CLASS_NAME, 'Search_searchButton__t0ENa').click()
        print('Нажал на кнопку поиска')
        time.sleep(1)
    except Exception:
        print('Кнопка поиска не найдена')

    try:
        position = get_position_from_html(driver)
        print(f'Получил позицию игрока {position}\n')
        return position
    except Exception:
        print('Игрок не найден')


def get_offset(position: int) -> int:
    print('Получаю оффсет')
    page_number: int = position // 20
    offset: int = page_number * LIMIT

    return offset


def sort_best_battles(best_battles: List[int]) -> Dict[int, int]:
    print('Сортирую лучшие бои')
    best_battles.sort(reverse=True)

    battles_dict: Dict[int, int] = {}
    for i in range(1, 16):
        battles_dict[i]: int = best_battles[i - 1]

    print('Отсортировал лучшие бои\n')
    return battles_dict


def get_player_data(offset: int, position: int) -> Dict[str, Union[int, Dict[int, int]]]:
    print('Получаю данные об игроке')
    index: int = position - offset - 1
    try:
        req = requests.get(
            f'https://challenge.tanki.su/api/v1/tournaments/585?offset={offset}&limit=20&lang=ru&column=rating')
        json_data: json = json.loads(req.text)
        player_data: json = json_data['data']['participants'][index]
    except Exception as ex:
        print('Что-то пошло не так...')
        print(ex)
        return

    total_exp: int = player_data['rating']
    best_15_battles_list: List[int] = player_data['results']['history']
    best_15_battles_dict: Dict[int, int] = sort_best_battles(best_15_battles_list)
    average_exp: float = player_data['results']['avg']
    nickname: str = player_data['user']['name']

    output_data: Dict[str, Union[int, Dict[int, int]]] = {
        'total_exp': total_exp,
        'average_exp': average_exp,
        'best_15_battles': best_15_battles_dict,
        'position': position,
        'nickname': nickname
    }

    print('Получил данные об игроке\n')
    return output_data


def best_battles_to_string(best_battles) -> str:
    print('Преобразую лучшие бои в строку')
    string: str = ''
    for key, value in best_battles.items():
        string += f'{key}. {value}\n' if key != 15 else f'{key}: {value}'

    print('Преобразовал лучшие бои в строку\n')
    return string


def create_message(player_data) -> str:
    print('Создаю сообщение')
    message: str = (f'Данные игрока: {player_data["nickname"]}\n'
                    f'Текущее место: {player_data["position"]}\n'
                    f'Опыт: {player_data["total_exp"]}\n'
                    f'{best_battles_to_string(player_data["best_15_battles"])}\n'
                    f'Опыт в среднем: {round(player_data["average_exp"], 2)}')

    print('Создал сообщение\n')
    return message


def main(nickname: str):
    MAIN_URL: str = 'https://challenge.tanki.su/challenge/585'
    # options = webdriver.FirefoxOptions()
    # options.add_argument('--no-sandbox')
    # driver: webdriver = webdriver.Firefox(options=options)
    driver: webdriver = webdriver.Firefox()
    driver.get(url=MAIN_URL)
    message = ''

    try:
        user_position: int = get_user_position(nickname, driver)
        offset: int = get_offset(user_position)
        player_data: Dict[str, Union[int, Dict[int, int]]] = get_player_data(offset, user_position)
        message: str = create_message(player_data)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    return message


if __name__ == '__main__':
    message = main('Remiut')
    print(message)
