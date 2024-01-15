"""Tests the creation of files and file paths and retrieving information from files and file paths."""

from data.file_handler import FileHandler

empty = ""
path_to_folder = r"C:\Workspace\1_PyCh_projects\file-compression-exercise\test\example_files"
complete_path = r"C:\Workspace\1_PyCh_projects\file-compression-exercise\test\example_files\adapter_plate.stl"
file_with_extension = "adapter_plate.stl"
file_without_extension = "adapter_plate"
file_extension = ".stl"
data = ("A", "B", "C")


def get_path_info_test(path):
    file_handler = FileHandler()

    path_info = file_handler.get_path_info(path)

    print()
    print("TEST get_path_info with", path)
    print("Path to folder:", path_info[0])
    print("File name:", path_info[1])
    print("File extension:", path_info[2])


def rebuild_file_path_test(path, name, extension):
    file_handler = FileHandler()
    new_path = file_handler.rebuild_file_path(path, name, extension)

    print()
    print("TEST rebuild_file_path_test with", path, name, extension)
    print(new_path)


def write_in_file_read_from_file_test():
    file_handler = FileHandler()
    file_handler.write_in_file(data, "", "test_file", "")
    print()
    print("TEST write_in_file and read_from_file with", data)
    print("A file has been created in the local folder.")

    stored_data = file_handler.read_from_file("test_file")
    print("Retrieved content is", stored_data)



# get_path_info_test(complete_path)
# get_path_info_test(file_with_extension)
# get_path_info_test(file_without_extension)
#
# rebuild_file_path_test(path_to_folder, file_without_extension, file_extension)
# rebuild_file_path_test(empty, file_without_extension, file_extension)
# rebuild_file_path_test(empty, file_without_extension, empty)

# write_in_file_read_from_file_test()
