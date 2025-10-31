import pytest
from src.main import analysis_brands, create_parser


def test_analysis_brands(tmp_path):
    # Подготовка временных CSV-файлов с тестовыми данными
    file1 = tmp_path / "file1.csv"
    file1.write_text("brand,rating,price\nBrandA,4.5,100\nBrandB,3.0,50\n")
    file2 = tmp_path / "file2.csv"
    file2.write_text("brand,rating,price\nBrandA,5.0,150\nBrandB,4.0,60\n")

    # Проверка вычисления среднего рейтинга
    result_rating = analysis_brands([str(file1), str(file2)], 'rating')
    assert result_rating == [['brand', 'rating'], ['BrandA', 4.8], ['BrandB', 3.5]]

    # Проверка вычисления средней цены
    result_price = analysis_brands([str(file1), str(file2)], 'price')
    assert result_price == [['brand', 'price'], ['BrandA', 125.0], ['BrandB', 55.0]]


def test_correct_params():
    parser = create_parser()
    args = parser.parse_args(['--files', 'file1.csv', 'file2.csv', '--report', 'average-rating'])
    assert args.files == ['file1.csv', 'file2.csv']
    assert args.report == 'average-rating'


def test_missing_files():
    parser = create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(['--files'])


def test_wrong_report():
    parser = create_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(['--files', 'file1.csv', '--report', 'wrong-report'])
