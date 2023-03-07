import glob

# full path: "/media/luke/WORK/some_folder/"
# relative path: "some_folder/"
def get_files_list(files_folder, file_extension="none"):
    if file_extension == "none":
        list_of_files = glob.glob(files_folder + "*.*")
        list_of_files.sort()
    else:
        list_of_files = glob.glob(files_folder + "*." + file_extension)
        list_of_files.sort()
    return list_of_files

# example:
# files_list = get_files_list("rubbish_folder/")
#
# for file in files_list:
#     print(file)





# full path: "/media/luke/WORK/some_folder/"
# relative path: "some_folder/"
def get_folders_list(parent_folder):  
    list_of_folders = glob.glob(parent_folder + "/*/")
    return list_of_folders

# example:
# folders_list = get_folders_list("rubbish_folder/")
#
# for folder in folders_list:
#     print(folder)
