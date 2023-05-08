import os
import shutil
import sys

IMAGES = ('JPEG', 'PNG', 'JPG', 'SVG')
VIDEO = ('AVI', 'MP4', 'MOV', 'MKV')
DOCS = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
MUSIC = ('MP3', 'OGG', 'WAV', 'AMR')
ARCHIVES = ('ZIP', 'GZ', 'TAR')
DLLS = ('DLL', 'CSV', 'RDP')
SUMB = """ !"#$%&'()*+№,-/:;<=>?@[\]^_`{|}~"""
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
"f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g"
)
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    

resume = ''

def normalize(name):
    # if '.' not in filename:
    #     return
    find_kyrill = [x for x in CYRILLIC_SYMBOLS if x in name.lower()]
    name_cln = ""
    if len(find_kyrill) > 0:
        result = name.translate(TRANS)
        for el in result:
            if el.isalpha() or el.isalnum() or el == ".":
                name_cln += el
            if el in SUMB:
                name_cln += el.replace(el, "_")
       
        newname = os.path.join(adress, name_cln)
        return newname
    else:
         return name

def process_folder5(folder_path):
    # Створюємо словник для категорій файлів
    categories = {
        'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
        'videos': ['AVI', 'MP4', 'MOV', 'MKV'],
        'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
        'music': ['MP3', 'OGG', 'WAV', 'AMR'],
        'archives': ['ZIP', 'GZ', 'TAR']
    }

    # Створюємо папки для категорій
    for category in categories.keys():
        category_path = os.path.join(folder_path, category)
        os.makedirs(category_path, exist_ok=True)
        # Перебираємо файли та папки в даній папці
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # Ігноруємо папки archives, videos, audio, documents, images
        if item in ['archives', 'videos', 'audio', 'documents', 'images']:
            continue

        # Перевіряємо, чи є поточний елемент папкою
        if os.path.isdir(item_path):
            # Рекурсивно обробляємо підпапку
            process_folder(item_path)
        else:
            # Отримуємо розширення файлу
            extension = item.split('.')[-1].upper()

            # Переміщуємо файли до відповідних категорій
            for category, extensions in categories.items():
                if extension in extensions:
                     # Перейменовуємо файл
                    new_name = normalize(item.split('.')[0])
                    new_path = os.path.join(folder_path, category, new_name + '.' + extension)
                    shutil.move(item_path, new_path)
                    break
            else:
                # Розширення невідоме, залишаємо файл без змін
                unknown_path = os.path.join(folder_path, 'unknown')
                os.makedirs(unknown_path, exist_ok=True)
                shutil.move(item_path, os.path.join(unknown_path, item))

    # Видаляємо порожні папки
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path) and not os.listdir(item_path):
            os.rmdir(item_path)

def process_folder(folder_path):
    categories = {
        'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
        'videos': ['AVI', 'MP4', 'MOV', 'MKV'],
        'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
        'music': ['MP3', 'OGG', 'WAV', 'AMR'],
        'archives': ['ZIP', 'GZ', 'TAR']
    }

    # Create folders for each category if they don't already exist
    for category in categories:
        category_path = os.path.join(folder_path, category)
        os.makedirs(category_path, exist_ok=True)

    # Process files and folders in the given folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if item in categories.keys():
            continue

        if os.path.isdir(item_path):
            process_folder(item_path)
        else:
            extension = item.split('.')[-1].upper()

            for category, extensions in categories.items():
                if extension in extensions:
                    new_name = normalize(item.split('.')[0])
                    new_path = os.path.join(folder_path, category, new_name + '.' + extension)
                    shutil.move(item_path, new_path)
                    break
            else:
                unknown_path = os.path.join(folder_path, 'unknown')
                os.makedirs(unknown_path, exist_ok=True)
                shutil.move(item_path, os.path.join(unknown_path, item))

    # Remove empty subfolders within the category folders
    for category in categories:
        category_path = os.path.join(folder_path, category)
        for item in os.listdir(category_path):
            item_path = os.path.join(category_path, item)
            if os.path.isdir(item_path) and not os.listdir(item_path):
                os.rmdir(item_path)



if __name__ == '__main__':
    try:
        # adress = sys.argv[1]
        adress = 'C:\hlam'
        process_folder(adress)
        # rename_and_transfer(adress)
        # result_sorting_with_arch(adress)
    except IndexError as inst:
            print('Потрібно передати папку сортування')
    except Exception as inst:
            print(inst)    