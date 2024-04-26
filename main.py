import os
import sys
from pytube import YouTube, Playlist
from urllib import request
import time
import json
from copy import deepcopy
import yt_dlp
import shutil


def check_file_type():
    files = os.listdir("./file_placing_area")

    if len(files) != 1:
        return None, None

    base, ext = os.path.splitext(files[0])

    return files[0], ext


def link_is_valid(Url):
    if Url.find("youtube") != -1:
        return True

    return False


def convert_playlist_video_url_to_video_url(Url):
    return Url[:Url.find("&list")]


def link_is_playlist(Url):
    if Url.find("list") != -1 and Url.find("watch") == -1:
        return True

    return False


def video_is_valid(Url):
    try:
        YouTube(Url).title
    except:
        if connection_is_ok():
            return False
        else:
            return video_is_valid(Url)

    return True


def video_is_existed(Expected_file, Path):
    files = os.listdir(Path)
    for File in files:
        existing_file = os.path.splitext(File)
        existing_file = existing_file[0].replace(" non_del", "") + existing_file[1]

        if Expected_file == existing_file:
            return True

    return False


def get_video_title(Url, Item_list):
    Error = None
    invalid_symbol_for_file_name = ["#", "<", ">", "$", "+", "%", "!", "`",
                                    "&", "*", "'", "|", "{", "}", "?", '"',
                                    "=", "/", "\ ", ":", "@"]

    Video_title = ""

    for Index in range(3):  # check the connection is ok or not
        try:
            Video_title = YouTube(Url).title
            break
        except Exception as e:
            Error = str(e)
            time.sleep(5)
    else:
        if not connection_is_ok():
            quit_code("\nconnection problem occur", Item_list)
        else:
            quit_code(f"\nAn exception occurred: {Error}", Item_list)

    for invalid_symbol in invalid_symbol_for_file_name:
        while Video_title.find(invalid_symbol) != -1:
            Video_title = Video_title.replace(invalid_symbol, " ")

    return Video_title


def get_playlist_title(Url, Item_list):
    Error = None
    invalid_symbol_for_file_name = ["#", "<", ">", "$", "+", "%", "!", "`",
                                    "&", "*", "'", "|", "{", "}", "?", '"',
                                    "=", "/", "\ ", ":", "@"]

    Playlist_title = ""

    for Index in range(3):  # check the connection is ok or not
        try:
            Playlist_title = Playlist(Url).title
            break
        except Exception as e:
            Error = str(e)
            time.sleep(5)
    else:
        if not connection_is_ok():
            quit_code("\nconnection problem occur", Item_list)
        else:
            quit_code(f"\nAn exception occurred: {Error}", Item_list)

    for invalid_symbol in invalid_symbol_for_file_name:
        while Playlist_title.find(invalid_symbol) != -1:
            Playlist_title = Playlist_title.replace(invalid_symbol, " ")

    return Playlist_title


def connection_is_ok(host='http://google.com'):
    while True:
        try:
            request.urlopen(host, timeout=5)
            return True
        except:
            return False


def create_directory(Path):
    try:
        os.makedirs(Path)
    except:
        pass


def create_upper_directory(Upper_list_path):
    for Index in range(len(Upper_list_path)):
        Path = Upper_list_path[:(Index + 1)]
        create_directory(list_to_path(Path))


def path_content_fix(Current_list_path):
    for Index in range(1, len(Current_list_path)):
        Directory = Current_list_path[Index]

        try:
            Files = os.listdir(list_to_path(Current_list_path[:Index]))
        except:
            return Current_list_path

        for File in Files:
            existing_file = File.replace(" non_del", "")
            if existing_file == Directory:
                Current_list_path[Index] = File
                break

    return Current_list_path


def get_json_title(title):
    invalid_symbol_for_file_name = ["#", "<", ">", "$", "+", "%", "!", "`",
                                    "&", "*", "'", "|", "{", "}", "?", '"',
                                    "=", "/", "\ ", ":", "@"]

    for invalid_symbol in invalid_symbol_for_file_name:
        while title.find(invalid_symbol) != -1:
            title = title.replace(invalid_symbol, " ")

    return title


def directory_is_existed(List_path):
    Directory = List_path[len(List_path) - 1]
    Path = list_to_path(List_path[:len(List_path) - 1])
    files = os.listdir(Path)

    for File in files:
        existing_file = File.replace(" non_del", "")
        if existing_file == Directory:
            return True

    return False


def get_local_directory_name(List_path):
    Directory = List_path[len(List_path) - 1]
    Path = list_to_path(List_path[:len(List_path) - 1])
    files = os.listdir(Path)

    for File in files:
        existing_file = File.replace(" non_del", "")
        if existing_file == Directory:
            return File


def download_mp3(Url, Path, Video_title, Item_list):
    Error = None

    for Index in range(3):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f"{Path}/{Video_title}.mp3"
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download(Url)

            break

        except Exception as e:
            Error = str(e)
            time.sleep(5)

    else:
        Error_occur = delete_file(f"{Path}/{Video_title}.mp3.part")
        if not connection_is_ok():
            quit_code("\nconnection problem occur", Item_list)
        else:
            quit_code(f"\nAn exception occurred: {Error}", Item_list)


def download_mp4(Url, Path, Video_title, Item_list):
    Error = None

    for Index in range(3):
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': f"{Path}/{Video_title}.mp4"
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download(Url)

            break

        except Exception as e:
            Error = str(e)
            time.sleep(5)

    else:
        Error_occur = delete_file(f"{Path}/{Video_title}.mp4.part")
        if not connection_is_ok():
            quit_code("\nconnection problem occur", Item_list)
        else:
            quit_code(f"\nAn exception occurred: {Error}", Item_list)


def quit_code(quit_reason, Item_list):
    print(quit_reason)
    store_information_into_txt(Item_list)
    sys.exit()


def store_information_into_txt(Item_list):
    info = ""
    for Possible_Item_status in ["downloaded_mp3", "downloaded_mp4", "invalid_link", "invalid video", "existed_video",
                                 "created_directory", "non_deleted_directory", "existed_directory", "deleted_file",
                                 "files that don't have access to delete"]:
        info = info + f"These are the {Possible_Item_status}: \n"
        deleted_Item = 0
        for Index, Item in enumerate(deepcopy(Item_list)):
            if Item["status"] == Possible_Item_status:
                Item_title = Item["title"]
                Item_link = Item["link"]
                Item_path = list_to_path(Item["path"])

                info = info + f"{Item_title}    ||||||||||    {Item_link}    ||||||||||    {Item_path} \n"
                del (Item_list[Index - deleted_Item])
                deleted_Item += 1

        info = info + "\n\n"

    with open("info.txt", "w", encoding="utf-8") as F:
        F.write(info)


def delete_file(Path):
    try:
        if local_file_is_directory(Path):
            shutil.rmtree(Path)
        else:
            os.remove(Path)

    except Exception as e:
        print(f"\n{e}")
        return True

    return False


def local_file_is_directory(Path):
    return os.path.isdir(Path)


def find_folder(json_file_input, folder_to_be_downloaded):
    Current_path = ["download"]
    Id_path = [1]

    for Index, File in enumerate(json_file_input):
        Current_path, Id_path = change_to_upper_directory(File, Id_path, Current_path)
        if file_is_directory(File):
            Current_path, Id_path = update_path_for_directory(File, Id_path, Current_path)

        if Current_path[-1] == folder_to_be_downloaded:
            return Index, Id_path, Current_path

    return None, None, None


def find_end_index_of_folder(json_file_input, Id_path, Upper_path, Index_of_json):
    original_Id_path = deepcopy(Id_path)
    Current_Id_path = deepcopy(Id_path)
    Current_path = deepcopy(Upper_path)

    for Index in range(Index_of_json + 1, len(json_file_input)):
        File = json_file_input[Index]
        change_to_upper_directory(File, Current_Id_path, Current_path)
        if file_is_directory(File):
            Current_path, Current_Id_path = update_path_for_directory(File, Current_Id_path, Current_path)

        if Current_Id_path[:len(original_Id_path)] != original_Id_path:
            return Index

    return len(json_file_input)


def file_is_directory(File):
    return len(File) == 6


def update_path_for_directory(File, Id_path, Current_path):
    Current_path = Current_path + [get_json_title(File["title"])]
    Id_path = Id_path + [File["id"]]

    return Current_path, Id_path


def change_to_upper_directory(File, Id_path, Current_path):
    Delete_index = -1
    for Index in range(len(Id_path) - 1, -1, -1):
        if Id_path[Index] == int(File["parentId"]):
            Delete_index = Index + 1
            break

    if Delete_index < len(Id_path) and Delete_index != -1:
        for _ in range(len(Id_path) - Delete_index):
            del (Id_path[Delete_index])
            del (Current_path[Delete_index])

    return Current_path, Id_path


def list_to_path(List_path):
    Path = "."
    for directory in List_path:
        Path = Path + "/" + directory

    return Path


def delete_useless_file(Item_list):
    non_deleted_mode = False
    New_Item_list = deepcopy(Item_list)
    non_deleted_directory_path = []

    for Item in Item_list:
        if non_deleted_mode:
            if Item["path"][:len(non_deleted_directory_path)] == non_deleted_directory_path:
                continue

            non_deleted_mode = False

        if Item["status"] == "non_deleted_directory":
            non_deleted_mode = True
            non_deleted_directory_path = Item["path"] + [Item["title"]]
            continue

        if Item["status"] in ["directory", "existed_directory"]:
            Expected_included_files = find_all_expected_included_file(Item, Item_list)
            Files = os.listdir(list_to_path(Item["path"] + [Item["title"]]))

            for File in Files:
                if File.find("non_del") != -1:
                    continue

                for Expected_included_file in Expected_included_files:
                    if Expected_included_file["title"] == File:
                        break

                else:
                    Error_occur = delete_file(list_to_path(Item["path"] + [Item["title"]] + [File]))

                    if Error_occur:
                        New_Item_list = item_list_update \
                            (title=File, path=Item["path"] + [Item["title"]],
                             status="files that don't have access to delete",
                             Item_list=New_Item_list)

                    else:
                        New_Item_list = item_list_update \
                            (title=File, path=Item["path"] + [Item["title"]], status="deleted_file",
                             Item_list=New_Item_list)

    return New_Item_list


def find_all_expected_included_file(Item, Item_list):
    Included_file = []

    for Included_item in Item_list:
        if Included_item["path"] == Item["path"] + [Item["title"]]:
            Included_file = Included_file + [Included_item]

    return Included_file


def item_list_update(title=None, link=None, path=None, status=None, Item_list=None):
    if Item_list is None:
        Item_list = []

    Item_info = {
        "title": title,
        "link": link,
        "path": path,
        "status": status
    }

    return Item_list + [deepcopy(Item_info)]


if __name__ == "__main__":
    input_file, input_file_format = check_file_type()
    item_list = []

    if input_file is None:
        print("more or less than 1 file exist")
        sys.exit()

    if input_file_format not in [".txt", ".json"]:
        print("wrong file format")
        sys.exit()

    for i in range(3):
        if not connection_is_ok():
            time.sleep(5)
        else:
            break
    else:
        quit_code("connection error occur", item_list)

    file_format_for_downloading = ""
    while file_format_for_downloading not in ["mp3", "mp4"]:
        file_format_for_downloading = input("Input the file format u would like to download (mp3/mp4) ")
        print()

    default = None
    while default not in ["Yes", "No"]:
        default = input("would u like everything work in default mode? (Yes/No) ")
        print()

    if default == "Yes":
        separate_playlist = True
        descending_order = True

    else:
        separate_playlist = None
        descending_order = None

        while separate_playlist not in ["Yes", "No"]:
            separate_playlist = input("Do you want to separate playlist? (Yes/No) ")
            print()

        if separate_playlist == "Yes":
            while descending_order not in ["Yes", "No"]:
                descending_order = input(
                    "Do you want to make your playlist descending order(or else without order)? (Yes/No) ")
                print()

            if descending_order == "Yes":
                descending_order = True
            else:
                descending_order = False

            separate_playlist = True
        else:
            separate_playlist = False

    if input_file_format == ".txt":
        create_directory(list_to_path(["download"]))

        with open(f"./file_placing_area/{input_file}", "r") as f:
            Input = f.read().split("\n")

        for url in Input:
            if url == "":
                continue

            current_path = ["download"]
            index_for_playlist = 0
            link_is_really_playlist = False

            if not link_is_valid(url):
                print(f"'{url}' is invalid link")
                item_list = item_list_update(path=["download"], link=url, status="invalid_link", Item_list=item_list)

                continue

            urls = [url]

            if link_is_playlist(url):
                urls = Playlist(url)
                link_is_really_playlist = True

                if separate_playlist:
                    current_path = current_path + [get_playlist_title(url, item_list)]

                    if not directory_is_existed(current_path):
                        create_directory(list_to_path(current_path))
                        item_list = item_list_update \
                            (title=get_playlist_title(url, item_list), path=["download"],
                             status="created_directory", Item_list=item_list)

                    else:
                        item_list = item_list_update \
                            (title=get_playlist_title(url, item_list), path=["download"],
                             status="existed_directory", Item_list=item_list)

            for URL in urls:
                URL = convert_playlist_video_url_to_video_url(URL)
                if not video_is_valid(URL):
                    print(f"'{URL}' is invalid video")
                    item_list = item_list_update(path=current_path, link=URL, status="invalid_video",
                                                 Item_list=item_list)

                    continue

                video_title = get_video_title(URL, item_list)
                if separate_playlist and link_is_really_playlist and descending_order:
                    index_for_playlist += 1
                    video_title = "0" * (len(str(len(urls))) - len(str(index_for_playlist))) + str(
                        index_for_playlist) + ". " + video_title

                if video_is_existed(f"{video_title}.{file_format_for_downloading}", list_to_path(current_path)):
                    print(f"'{video_title}' has already existed")
                    item_list = item_list_update(title=f"{video_title}.{file_format_for_downloading}",
                                                 path=current_path,
                                                 link=URL, status="existed_video", Item_list=item_list)

                    continue

                if file_format_for_downloading == "mp3":
                    download_mp3(URL, list_to_path(current_path), video_title, item_list)
                    print(f"'{video_title}' is downloaded\n")
                    item_list = item_list_update \
                        (title=f"{video_title}.{file_format_for_downloading}", link=URL, path=current_path,
                         status="downloaded_mp3",
                         Item_list=item_list)

                elif file_format_for_downloading == "mp4":
                    download_mp4(URL, list_to_path(current_path), video_title, item_list)
                    print(f"'{video_title}' is downloaded\n")
                    item_list = item_list_update \
                        (title=f"{video_title}.{file_format_for_downloading}", link=URL, path=current_path,
                         status="downloaded_mp4",
                         Item_list=item_list)

    elif input_file_format == ".json":
        folder_has_to_be_downloaded = input("which folder u would like to download? ")
        print()

        with open(f"./file_placing_area/{input_file}", "r", encoding="utf-8") as f:
            Input = json.load(f)

        if folder_has_to_be_downloaded == "all":
            index_of_json = 0
            end_index_of_json = len(Input)
            current_path = ["download"]
            id_path = [1]
            create_upper_directory(current_path)

        else:
            index_of_json, id_path, upper_path = find_folder(Input, folder_has_to_be_downloaded)

            if index_of_json is None:
                quit_code("No directory found", item_list)

            end_index_of_json = find_end_index_of_folder(Input, id_path, upper_path, index_of_json)
            upper_path = path_content_fix(upper_path)
            create_upper_directory(upper_path)
            current_path = upper_path
            delete_index = 0

        for index in range(index_of_json, end_index_of_json):
            file = Input[index]
            current_path, id_path = change_to_upper_directory(file, id_path, current_path)

            if file_is_directory(file):
                current_path, id_path = update_path_for_directory(file, id_path, current_path)
                file_title = get_json_title(file["title"])

                if not directory_is_existed(current_path):
                    create_directory(list_to_path(current_path))
                    item_list = item_list_update \
                        (title=file_title, path=current_path[:(len(current_path) - 1)],
                         status="created_directory", Item_list=item_list)

                elif path_content_fix(deepcopy(current_path)) != current_path:
                    current_path = path_content_fix(current_path)
                    file_title = current_path[(len(current_path) - 1)]
                    item_list = item_list_update \
                        (title=file_title, path=current_path[:(len(current_path) - 1)],
                         status="non_deleted_directory", Item_list=item_list)

                else:
                    item_list = item_list_update \
                        (title=file_title, path=current_path[:(len(current_path) - 1)],
                         status="existed_directory", Item_list=item_list)

            else:
                link_is_really_playlist = False
                index_for_playlist = 0
                video_path = current_path
                url = file["url"]
                video_title = get_json_title(file["title"])

                if not link_is_valid(url):
                    print(f"'{url}' is invalid link")
                    item_list = item_list_update \
                        (title=f"{video_title}.{file_format_for_downloading}", path=current_path, link=url,
                         status="invalid_link", Item_list=item_list)

                    continue

                urls = [url]

                if link_is_playlist(url):
                    link_is_really_playlist = True
                    urls = Playlist(url)

                    if separate_playlist:
                        video_path = video_path + [video_title]

                        if not directory_is_existed(video_path):
                            create_directory(list_to_path(video_path))
                            item_list = item_list_update \
                                (title=video_title, path=current_path,
                                 status="created_directory", Item_list=item_list)

                        else:
                            item_list = item_list_update \
                                (title=video_title, path=current_path,
                                 status="existed_directory", Item_list=item_list)

                elif video_is_existed(f"{video_title}.{file_format_for_downloading}", list_to_path(video_path)):
                    print(f"'{video_title}' has already existed")
                    item_list = item_list_update \
                        (title=f"{video_title}.{file_format_for_downloading}", path=video_path, link=url,
                         status="existed_video", Item_list=item_list)

                    continue

                for URL in urls:
                    URL = convert_playlist_video_url_to_video_url(URL)
                    if link_is_really_playlist:
                        video_title = get_video_title(URL, item_list)

                        if separate_playlist and descending_order:
                            index_for_playlist += 1
                            video_title = "0" * (len(str(len(urls))) - len(str(index_for_playlist))) + str(
                                index_for_playlist) + ". " + video_title

                        if video_is_existed(f"{video_title}.{file_format_for_downloading}", list_to_path(video_path)):
                            print(f"'{video_title}' has already existed")
                            item_list = item_list_update \
                                (title=f"{video_title}.{file_format_for_downloading}", path=video_path, link=url,
                                 status="existed_video", Item_list=item_list)

                            continue

                    if not video_is_valid(URL):
                        print(f"'{URL}' is invalid video")
                        item_list = item_list_update \
                            (title=f"{video_title}.{file_format_for_downloading}", path=video_path, link=url,
                             status="invalid_video", Item_list=item_list)

                        continue

                    if file_format_for_downloading == "mp3":
                        print()
                        download_mp3(URL, list_to_path(video_path), video_title, item_list)
                        print(f"'{video_title}' is downloaded\n")
                        item_list = item_list_update \
                            (title=f"{video_title}.{file_format_for_downloading}", path=video_path, link=url,
                             status="downloaded_mp3", Item_list=item_list)

                    elif file_format_for_downloading == "mp4":
                        print()
                        download_mp4(URL, list_to_path(video_path), video_title, item_list)
                        print(f"'{video_title}' is downloaded\n")
                        item_list = item_list_update \
                            (title=f"{video_title}.{file_format_for_downloading}", path=video_path, link=url,
                             status="downloaded_mp4", Item_list=item_list)

    item_list = delete_useless_file(item_list)
    quit_code("\n\nVideos are downloaded, check to see more information by assessing info.txt", item_list)
