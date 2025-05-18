import time
import sys

TIME = 10


def get_cookies():
    try:
        with open("cookie.txt", encoding="utf-8") as file:
            cook = file.readline()
            if len(cook) == 0:
                print(f"В файле cookie.txt нет куков. Отключение через: {TIME} секунд !!!")
                time.sleep(TIME)
                sys.exit(0)

    except FileNotFoundError:
        print(f"Файл cookie.txt не найден.")
        with open("cookie.txt", 'w') as f:
            print(f"Содаем пустой файл cookie.txt")

        print(f"В файл cookie.txt нужно вставить ваши куки")
        print(f"Отключение через {TIME} секунд !!!")
        time.sleep(TIME)
        sys.exit(0)

    else:
        # print("Читаем файл cokies.txt", "*" * 22, sep="\n", end="\n \n")
        cook = {"PHPSESSID": cook}

        return cook


if __name__ == "__main__":
    get_cookies()
