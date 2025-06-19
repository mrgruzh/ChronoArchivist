import os
import time
import shutil
from datetime import datetime

def initialize_virtual_archaeologist(directory, archive_dir):
    """Инициализирует систему виртуального археолога."""
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    return directory, archive_dir

def find_old_files(directory, days_threshold):
    """Находит файлы, которые не изменялись более заданного количества дней."""
    current_time = time.time()
    old_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            last_modified = os.path.getmtime(file_path)
            if (current_time - last_modified) / (3600 * 24) > days_threshold:
                old_files.append((file_path, datetime.fromtimestamp(last_modified).strftime("%Y-%m-%d %H:%M:%S")))
    return old_files

def categorize_files(file_list):
    """Категоризирует файлы по их типу (расширению)."""
    categories = {}
    for file_path, last_modified in file_list:
        extension = os.path.splitext(file_path)[1].lower()
        if extension not in categories:
            categories[extension] = []
        categories[extension].append((file_path, last_modified))
    return categories

def archive_files(file_list, archive_dir):
    """Архивирует найденные файлы в указанную директорию."""
    for file_path, last_modified in file_list:
        relative_path = os.path.relpath(file_path)
        archive_path = os.path.join(archive_dir, relative_path)
        os.makedirs(os.path.dirname(archive_path), exist_ok=True)
        shutil.copy2(file_path, archive_path)

def generate_report(categories, archive_dir):
    """Создаёт текстовый отчёт о найденных файлах и их архивации."""
    report_path = os.path.join(archive_dir, "report.txt")
    with open(report_path, "w") as report_file:
        report_file.write("Отчёт о виртуальном археологе\n")
        report_file.write("===========================\n\n")
        for category, files in categories.items():
            report_file.write(f"Категория: {category}\n")
            for file_path, last_modified in files:
                report_file.write(f"  {file_path} (последнее изменение: {last_modified})\n")
            report_file.write("\n")
    return report_path

def main():
    print("Добро пожаловать в систему виртуального археолога!")
    directory = input("Введите путь к папке для анализа: ").strip()
    archive_dir = input("Введите путь для архивации: ").strip()
    days_threshold = int(input("Введите порог дней без изменений (например, 730 для 2 лет): "))

    directory, archive_dir = initialize_virtual_archaeologist(directory, archive_dir)
    print("Анализ файлов...")
    old_files = find_old_files(directory, days_threshold)
    print(f"Найдено {len(old_files)} старых файлов.")

    if old_files:
        print("Категоризация файлов...")
        categories = categorize_files(old_files)
        print("Архивирование файлов...")
        archive_files(old_files, archive_dir)
        print("Генерация отчёта...")
        report_path = generate_report(categories, archive_dir)
        print(f"Отчёт создан: {report_path}")
    else:
        print("Старых файлов не найдено.")

    print("Работа завершена!")

if __name__ == "__main__":
    main()
