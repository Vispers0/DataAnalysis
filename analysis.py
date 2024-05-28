import os

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff

# Преобразование набора данных для дальнейшей работы
ds_src = './res/powerconsumption.csv'
ds = pd.read_csv(ds_src)
ds["GeneralPowerConsumption"] = (ds["PowerConsumption_Zone1"] + ds["PowerConsumption_Zone2"] + ds[
    "PowerConsumption_Zone3"]) / 3
ds = ds.drop(["PowerConsumption_Zone1", "PowerConsumption_Zone2", "PowerConsumption_Zone3"], axis=1)

# Путь для вывода файлов
OUTPATH = "./output/"


class Analysis:
    # Проведение EDA
    @staticmethod
    def eda():
        print("ПРЕДВАРИТЕЛЬНЫЙ АНАЛИЗ ДАННЫХ")
        print("Информация о датасете:")
        ds.info()
        print("-----------------------------------------")
        print("Число пустых полей:")
        print(ds.isnull().sum())
        print("-----------------------------------------")
        print("Число дубликатов данных:")
        print(ds.duplicated().sum())
        print("-----------------------------------------")
        print("Описательная статистика:")
        print(ds.describe())
        print("-----------------------------------------")
        print("Первые 5 строк набора данных:")
        print(ds.head(5))
        print("-----------------------------------------")
        input("Чтобы вернуться в главное меню, нажмите Enter")

    # Построение матрицы корреляции
    @staticmethod
    def corr():
        local_ds = ds
        local_ds["Datetime"] = pd.to_datetime(local_ds["Datetime"])
        local_ds_corr = local_ds.corr()
        local_ds = local_ds.set_index("Datetime")

        x = list(local_ds_corr.columns)
        y = list(local_ds_corr.index)
        z = np.array(local_ds_corr)

        figure = ff.create_annotated_heatmap(
            x=x,
            y=y,
            z=z,
            annotation_text=np.around(z, 2)
        )

        figure.layout.width = 1000
        figure.layout.height = 1000

        figure.write_image(OUTPATH + "corr.svg")
        os.system("yandex-browser-stable " + OUTPATH + "corr.svg")
        input("Чтобы вернуться в главное меню, нажмите Enter")

    # Поиск аномалий
    @staticmethod
    def anomaly():
        local_ds = ds
        local_ds["Datetime"] = pd.to_datetime(local_ds["Datetime"])
        local_ds = local_ds.set_index("Datetime")
        graph = px.box(
            local_ds,
            x=local_ds.index.month,
            y="GeneralPowerConsumption",
            color=local_ds.index.month,
            labels={"x": "Месяцы"},
            title="Потребление электроэнергии за 2008 год"
        )
        graph.update_traces(width=0.5)
        graph.show()
        input("Чтобы вернуться в главное меню, нажмите Enter")

    # Поиск экстремумов
    @staticmethod
    def extremum():
        local_ds = ds

        print("Какой экстремум искать?")
        print("1. Максимум")
        print("2. Минимум")
        extr_type = int(input())

        print("По какому столбцу искать экстремум?")
        print("1. Температура\n"
              "2. Влажность\n"
              "3. Скорость ветра\n"
              "4. Общие диффузные потоки\n"
              "5. Диффузные потоки\n"
              "6. Потребление электроэнергии")
        choice = int(input())
        column = None

        # Определение выбранного столбца набора данных
        match choice:
            case 1:
                column = local_ds.Temperature
            case 2:
                column = local_ds.Humidity
            case 3:
                column = local_ds.WindSpeed
            case 4:
                column = local_ds.GeneralDiffuseFlows
            case 5:
                column = local_ds.DiffuseFlows
            case 6:
                column = local_ds.GeneralPowerConsumption

        # Поиск максимума и запись в файл
        if extr_type == 1:
            file = open(OUTPATH + "extremum.txt", "w")
            file.write(local_ds[column == column.max()].to_string())
            print("Результаты поиска записаны в файл extremum.txt в папке output")

            #Запуск системного текстового редактора для просмотра результатов
            os.system("kate " + OUTPATH + "extremum.txt")
            file.close()

        # Поиск максимума и запись в файл
        if extr_type == 2:
            file = open(OUTPATH + "extremum.txt", "w")
            file.write(local_ds[column == column.min()].to_string())
            print("Результаты поиска записаны в файл extremum.txt в папке output")

            #Запуск системного текстового редактора для просмотра результатов
            os.system("kate " + OUTPATH + "extremum.txt")
            file.close()

        input("Чтобы вернуться в меню, нажмите Enter")

    # Вычисление числовых характеристик
    @staticmethod
    def characteristics():
        local_ds = ds

        print("Вычисляются 5 числовых характеристик столбца:\n"
              "1. Среднее арифметическое (Математическое ожидание)\n"
              "2. Медиана (Серединное значение)\n"
              "3. Мода (Наиболее часто встречающееся значение)\n"
              "4. Среднеквадратичное отклонение\n"
              "5. Дисперсия\n")

        print("По какому столбцу вычислять числовые характеристики?")
        print("1. Температура\n"
              "2. Влажность\n"
              "3. Скорость ветра\n"
              "4. Общие диффузные потоки\n"
              "5. Диффузные потоки\n"
              "6. Потребление электроэнергии")
        choice = int(input())
        column = None

        # Определение выбранного столбца набора данных
        match choice:
            case 1:
                column = "Temperature"
            case 2:
                column = "Humidity"
            case 3:
                column = "WindSpeed"
            case 4:
                column = "GeneralDiffuseFlows"
            case 5:
                column = "DiffuseFlows"
            case 6:
                column = "GeneralPowerConsumption"

        # Вычисление числовых характеристик
        result = "Столбец " + column + ":\n"
        result += "Математическое ожидание = " + str(round(local_ds[column].mean(), 3)) + ";\n"
        result += "Медиана = " + str(round(local_ds[column].median(), 3)) + ";\n"
        result += "Мода = " + str(round(local_ds[column].mode(), 3)) + ";\n"
        result += "СКО = " + str(round(local_ds[column].std(), 3)) + ";\n"
        result += "Дисперсия = " + str(round(local_ds[column].var(), 3)) + ";\n"

        # Запись результатов в файл
        file = open(OUTPATH + "characteristics.txt", "w")
        file.write(result)
        print("Результаты поиска записаны в файл characteristics.txt в папке output")

        #Запуск системного текстового редактора для просмотра результатов
        os.system("kate " + OUTPATH + "characteristics.txt")
        file.close()

        input("Чтобы вернуться в меню, нажмите Enter")

    # Поиск конкретного значения
    @staticmethod
    def search_value():
        local_ds = ds

        print("По какому столбцу искать значение?")
        print("1. Температура\n"
              "2. Влажность\n"
              "3. Скорость ветра\n"
              "4. Общие диффузные потоки\n"
              "5. Диффузные потоки\n"
              "6. Потребление электроэнергии")
        choice = int(input())
        column = None

        # Определение выбранного столбца набора данных
        match choice:
            case 1:
                column = "Temperature"
            case 2:
                column = "Humidity"
            case 3:
                column = "WindSpeed"
            case 4:
                column = "GeneralDiffuseFlows"
            case 5:
                column = "DiffuseFlows"
            case 6:
                column = "GeneralPowerConsumption"

        print("Какое значение искать?")
        value = float(input())

        # Поиск значения
        result = local_ds[local_ds[column] == value].to_string()

        if result.__contains__("Empty DataFrame"):
            result = "Значение не найдено"

        file = open(OUTPATH + "value.txt", "w")
        file.write(result)

        print("Результаты поиска записаны в файл value.txt в папке output")

        #Запуск системного текстового редактора для просмотра результатов
        os.system("kate " + OUTPATH + "value.txt")
        file.close()

        input("Чтобы вернуться в меню, нажмите Enter")
