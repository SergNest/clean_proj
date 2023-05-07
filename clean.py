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

def normalize(adress: str, filename: str) -> None:
    # if '.' not in filename:
    #     return
    find_kyrill = [x for x in CYRILLIC_SYMBOLS if x in filename.lower()]
    name_cln = ""
    if len(find_kyrill) > 0:
        result = filename.translate(TRANS)
        for el in result:
            if el.isalpha() or el.isalnum() or el == ".":
                name_cln += el
            if el in SUMB:
                name_cln += el.replace(el, "_")
        oldname = os.path.join(adress, filename)
        newname = os.path.join(adress, name_cln)
        os.rename(oldname, newname)

def transfer_files(adress: str, folder_name: str, files: list) -> None:
    if folder_name not in adress:
        os.chdir(adress)
        os.mkdir(folder_name)
    if folder_name == "archives":
        to_unpack_folder = os.path.join(adress, folder_name)
        os.chdir(to_unpack_folder)
        for arch_name in files:
            name = arch_name.split(".")[0]
            os.mkdir(name)
            path_to_unpack = os.path.join(to_unpack_folder, name)
            file_for_unpack = os.path.join(adress, arch_name)
            try:
                shutil.unpack_archive(file_for_unpack, path_to_unpack)
                os.remove(file_for_unpack)
            except shutil.ReadError:
                all_err_arch = []
                error_name = os.path.split(file_for_unpack)
                all_err_arch.append(error_name[-1])
                del_empty_dirs(os.path.join(adress, "archives"))
                global resume
                resume += (
                    f"Файл {all_err_arch} має розширення архіву, проте не є ним.\n"
                )
    if folder_name != "archives":
        file_destination = os.path.join(adress, folder_name)
        for file in files:
            shutil.move(os.path.join(adress, file), file_destination)

def del_empty_dirs(adress: str) -> None:
    for dirs in os.listdir(adress):
        dir = os.path.join(adress, dirs)
        if os.path.isdir(dir):
            del_empty_dirs(dir)
            if not os.listdir(dir):
                os.rmdir(dir)

def find_dlls(adress: str) -> list:
    files = os.listdir(adress)
    type_dll = list(
        filter(
            lambda x: any(filter(lambda y: x.lower().endswith(y.lower()), DLLS)),
            files,
        )
    )
    return type_dll

def find_images(adress: str) -> list:
    files = os.listdir(adress)
    type_img = list(
        filter(
            lambda x: any(filter(lambda y: x.lower().endswith(y.lower()), IMAGES)),
            files,
        )
    )
    return type_img


def find_video(adress: str) -> list:
    files = os.listdir(adress)
    type_video = list(
        filter(
            lambda x: any(filter(lambda y: x.lower().endswith(y.lower()), VIDEO)),
            files,
        )
    )
    return type_video


def find_docs(adress: str) -> list:
    files = os.listdir(adress)
    type_docs = list(
        filter(
            lambda x: any(filter(lambda y: x.lower().endswith(y.lower()), DOCS)),
            files,
        )
    )
    return type_docs


def find_music(adress: str) -> list:
    files = os.listdir(adress)
    type_mus = list(
        filter(
            lambda x: any(filter(lambda y: x.lower().endswith(y.lower()), MUSIC)),
            files,
        )
    )
    return type_mus


def find_archives(adress: str) -> list:
    files = os.listdir(adress)
    type_arch = list(
        filter(
            lambda x: any(
                filter(lambda y: x.lower().endswith(y.lower()), ARCHIVES)
            ),
            files,
        )
    )
    return type_arch

def transfer_without_archives(adress: str, folder_name: str, files: list) -> None:
    if folder_name not in adress:
        os.chdir(adress)
        os.mkdir(folder_name)
    if folder_name != "archives":
        file_destination = os.path.join(adress, folder_name)
        for file in files:
            shutil.move(os.path.join(adress, file), file_destination)

def rename_and_relocation_without_arch(adress: str) -> None:
    dont_know_files(adress)
    no_type = dont_know_files(adress)
    files = os.listdir(adress)
    for file in files:
        if file not in no_type:
            normalize(adress, file)

    transfer_without_archives(adress, "dlls", find_dlls(adress))
    transfer_without_archives(adress, "images", find_images(adress))
    transfer_without_archives(adress, "music", find_music(adress))
    transfer_without_archives(adress, "video", find_video(adress))
    transfer_without_archives(adress, "documents", find_docs(adress))
    transfer_without_archives(adress, "archives", find_archives(adress))
       

    global resume
    resume += f"Ось це залишаються без зміни: {no_type}\n"

def dont_know_files(adress: str) -> list:
    all_in = find_images(adress)
    all_in.extend(find_video(adress))
    all_in.extend(find_docs(adress))
    all_in.extend(find_music(adress))
    all_in.extend(find_archives(adress))
    all_in.extend(find_dlls(adress))
    files = os.listdir(adress)
    type_any = []
    for file in files:
        if file not in all_in:
            type_any.append(file)
    return type_any

def deep_folders(adress: str) -> None:
    for el in os.listdir(adress):
        way = os.path.join(adress, el)
        if os.path.isdir(way):
            files_in_way = os.listdir(way)
            for file in files_in_way:               
                shutil.move(os.path.join(way, file), adress)                
                del_empty_dirs(adress)
            if not os.path.isdir(adress):
                break
            else:
                deep_folders(adress)

def deep_folders2(adress: str) -> None:
    for el in os.listdir(adress):
        way = os.path.join(adress, el)
        if os.path.isdir(way):
            files_in_way = os.listdir(way)
            if len(files_in_way) == 1 and os.path.isdir(os.path.join(way, files_in_way[0])):
                deep_folders(way)  # Call deep_folders recursively on the inner directory
            else:
                for file in files_in_way:                
                    if os.path.exists(os.path.join(adress, file)): 
                        continue
                    shutil.move(os.path.join(way, file), adress)
                
                del_empty_dirs(adress)
            if not os.path.isdir(adress):
                break
            else:
                deep_folders(adress)

def rename_and_transfer(adress: str) -> None:
    no_type = dont_know_files(adress)
    files = os.listdir(adress)
    for file in files:
        if file not in no_type:
            normalize(adress, file)

    transfer_files(adress, "dlls", find_dlls(adress))
    transfer_files(adress, "images", find_images(adress))
    transfer_files(adress, "music", find_music(adress))
    transfer_files(adress, "video", find_video(adress))
    transfer_files(adress, "documents", find_docs(adress))
    transfer_files(adress, "archives", find_archives(adress))

    global resume
    resume += f"Ось це залишилося там, де й було: {no_type}\n"

def result_sorting_with_arch(adress: str) -> None:
   
    text_resume = resume_with_arch(
        "images", "video", "documents", "music", "dlls", adress=adress
    )
    
    print(text_resume)

def resume_with_arch(*args, adress: str) -> str:
    name = "archives"
    global resume
    for name_fold in args:
        way_for_resume = os.path.join(adress, name_fold)
        files = os.listdir(way_for_resume)
        count_images = len(files)
        line_of_ras = []
        for el in files:
            format = el.split(".")
            line_of_ras.append(format[-1].lower())
        line_of_ras = set(line_of_ras)
        one_el_line = f"До папки {name_fold} було відсортовано файли у кількості {count_images} шт. Їх формати: {[el for el in line_of_ras]}\n"
        resume += one_el_line
    dop_way = os.path.join(adress, "archives")
    files = os.listdir(dop_way)
    count_ar = len(files)
    line = []
    archice_files = find_archives(adress)
    for files in archice_files:
        named = files.split(".")
        line.append(named[-1])
    line = set(line)
    arch_part_of_resume = f'Також розпакували архіви, у кількості {count_ar} шт. Вони тепер у папці "archives".'
    resume += arch_part_of_resume
    return resume


if __name__ == '__main__':
    try:
        adress = sys.argv[1]
        deep_folders(adress)
        rename_and_transfer(adress)
        result_sorting_with_arch(adress)
    except IndexError as inst:
            print('Потрібно передати папку сортування')
    except Exception as inst:
            print(inst)    