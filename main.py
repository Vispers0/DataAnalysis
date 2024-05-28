from analysis import Analysis
import os

da = Analysis()
choices = [
    "1. Предварительный анализ данных",
    "2. Корреляция данных",
    "3. Поиск аномалий",
    "4. Поиск экстремумов",
    "5. Числовые характеристики",
    "6. Поиск конкретного значения"
]


#Вызов необходимого метода
def call(option):
    os.system("clear")
    match option:
        case "eda": da.eda()
        case "correl": da.corr()
        case "anomaly": da.anomaly()
        case "extremum": da.extremum()
        case "characteristics": da.characteristics()
        case "search_value": da.search_value()

    os.system("clear")
    main()


def main():
    choice = ""
    print("Осуществить поиск:")

    for i in range(0, len(choices)):
        print(choices[i])

    choice = input("Выберите действие (введите q, чтобый выйти): ")
    print(choice)
    match choice:
        case "1": call("eda")
        case "2": call("correl")
        case "3": call("anomaly")
        case "4": call("extremum")
        case "5": call("characteristics")
        case "6": call("search_value")
        case "q": quit()


if __name__ == "__main__":
    main()
