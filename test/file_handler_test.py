from data.file_handler import FileHandler

path = r"C:\Workspace\1_PyCh_projects\file-compression-exercise\test\example_files\adapter_plate.stl"
compression = "lzw"
new_filename = "compressed_plate"


def compress_file_step_by_step(path, compression, new_filename):

    file_handler = FileHandler()

    file_handler.get_path_info(path)
    print(file_handler.file_path)
    print(file_handler.file_name)
    print(file_handler.file_extension)

    file_handler.initiate_encode(path, compression, new_filename)


compress_file_step_by_step(path, compression, new_filename)
