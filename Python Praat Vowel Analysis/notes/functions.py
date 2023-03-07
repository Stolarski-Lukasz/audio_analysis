import settings as s

tsv_file = open(output_file_name, 'w')
tsv_file.write("speaker	gender	vowel	f0	f1	f2	f3	sr	log_f1_sr	log_f2_f1	log_f3_f2	praat_settings	file\n")

folders_list = get_folders_list(s.AUDIO_FILES_FOLDER_NAME)

for folder in folders_list:
    if folder[-12:] != "__pycache__/":
        speakers_gender = folder[-2]
        print(speakers_gender)
        speaker = folder[len(s.AUDIO_FILES_FOLDER_NAME):-3]
        print(speaker)
        files_list = get_files_list(folder)
        folder_length = len(folder)
        for file in files_list:
            vowel = file[folder_length: folder_length+2]
            file_harmonics = harmonics(file, gender=speakers_gender)
            sr = (file_harmonics[0] / 168) ** (1 / 3) * 168
            tsv_file.write(speaker +
                           "	" + speakers_gender +
                           "	" + str(vowel) +
                           "	" + str(file_harmonics[0]) +
                           "	" + str(file_harmonics[1]) +
                           "	" + str(file_harmonics[2]) +
                           "	" + str(file_harmonics[3]) +
                           "	" + str(sr) +
                           "	" + str(math.log10(file_harmonics[1] / sr)) +
                           "	" + str(math.log10(file_harmonics[2] / file_harmonics[1])) +
                           "	" + str(math.log10(file_harmonics[3] / file_harmonics[2])) +
                           "	" + str(file_harmonics[4]) +
                           "	" + str(file) +
                           "\n")

tsv_file.close()