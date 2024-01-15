"""Tests the creation of files and file paths and retrieving information from files and file paths."""

from data.file_handler import FileHandler

# Paths, file names and extensions fpr the test functions.
empty = ""
path_to_folder = r"C:\Workspace\1_PyCh_projects\file-compression-exercise\test\example_files"
complete_path = r"C:\Workspace\1_PyCh_projects\file-compression-exercise\test\example_files\adapter_plate.stl"
file_with_extension = "adapter_plate.stl"
file_without_extension = "adapter_plate"
file_extension = ".stl"

# Data for the test functions.
data = ("A", "B", "C")
data_2 = b"ABC"


def get_path_info_test(path: str):
    """Tests the correct split of the components of a path.

    Args:
         path (str): Complete or incomplete paths.
    """

    file_handler = FileHandler()

    path_info = file_handler.get_path_info(path)

    print()
    print("TEST get_path_info with", path)
    print("Path to folder:", path_info[0])
    print("File name:", path_info[1])
    print("File extension:", path_info[2])


def rebuild_file_path_test(path: str, name: str, extension: str):
    """Tests the correct assembling of a path.

    Args:
        path (str): Path to containing folder.
        name (str): File name.
        extension (str): File extension.
    """

    file_handler = FileHandler()
    new_path = file_handler.rebuild_file_path(path, name, extension)

    print()
    print("TEST rebuild_file_path_test with", path, name, extension)
    print(new_path)


def write_in_file_read_from_file_test():
    """Tests serialization of a python object and retrieving it."""

    file_handler = FileHandler()
    file_handler.write_in_file(data, "", "test_file", "")
    print()
    print("TEST write_in_file and read_from_file with", data)
    print("A file has been created in the local folder.")

    stored_data = file_handler.read_from_file("test_file")
    print("Retrieved content is", stored_data)


def recreate_file_get_file_bytes_test():
    """Tsts writing and reading bytes in/from files."""

    file_handler = FileHandler()
    file_handler.recreate_file(data_2, "", "test_file_2", "")
    print()
    print("TEST recreate_file and get_file_bytes. Input data", data_2)
    print("A file has been created in the local folder.")

    bytes_from_file = file_handler.get_file_bytes("test_file_2")
    print("Retrieved content is", bytes_from_file)


# Execution of the tests.

get_path_info_test(complete_path)
get_path_info_test(file_with_extension)
get_path_info_test(file_without_extension)

rebuild_file_path_test(path_to_folder, file_without_extension, file_extension)
rebuild_file_path_test(empty, file_without_extension, file_extension)
rebuild_file_path_test(empty, file_without_extension, empty)

write_in_file_read_from_file_test()

recreate_file_get_file_bytes_test()
