import argparse
import csv
from collections import defaultdict

import tabulate


def create_parser():
    parser = argparse.ArgumentParser(description="Анализ данных из CSV файлов")
    parser.add_argument('--files', nargs='+', required=True,
                        help='Список CSV файлов для обработки')
    parser.add_argument('--report', choices=['average-rating', 'average-price'], required=True,
                        help='Тип отчёта')
    return parser


def analysis_brands(files_list: list[str], report: str):
    brands_indicators = defaultdict(list)
    result_list = []

    for filename in files_list:
        try:
            with open(filename, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    brand = row['brand']
                    indicator = float(row[report])
                    brands_indicators[brand].append(indicator)
        except FileNotFoundError:
            print(f"Файл {filename} не найден.\n"
                  f"Отчёт будет построен без учета данных этого файла!")

    for brand, list_indicators in brands_indicators.items():
        average_values = round(sum(list_indicators)/len(list_indicators), 1)
        result_list.append([brand, average_values])

    result = sorted(result_list, key=lambda x: x[1], reverse=True)
    result.insert(0, ['brand', report])
    return result


def main():
    args = create_parser().parse_args()

    if args.report == 'average-rating':
        result = analysis_brands(args.files, 'rating')
        print(tabulate.tabulate(result, tablefmt='grid'))
    if args.report == 'average-price':
        result = analysis_brands(args.files, 'price')
        print(tabulate.tabulate(result, tablefmt='grid'))


if __name__ == '__main__':
    main()
