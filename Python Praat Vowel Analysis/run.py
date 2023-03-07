import math
from folder_utils import get_files_list, get_folders_list
from voice_analysis import VTRProcessor
import settings as s


if __name__ == "__main__":
    tsv_file = open(s.OUTPUT_FILE_NAME, 'w')
    tsv_file.write("speaker	gender	vowel	f0	f1	f2	f3	sr	log_f1_sr	log_f2_f1	log_f3_f2	praat_settings	file\n")
    folders_list = get_folders_list(s.AUDIO_FILES_FOLDER_NAME)
    for folder in folders_list:
        if folder[-12:] != "__pycache__/":
            speakers_gender = folder[-2]
            print(f"speaker's gender: {speakers_gender}")
            speaker = folder[len(s.AUDIO_FILES_FOLDER_NAME):-3]
            print(f"speaker's name: {speaker}")
            files_list = get_files_list(folder)
            folder_length = len(folder)
            for file in files_list:
                vowel = file[folder_length: folder_length+2]
                # file_get_vocal_tract_resonances = get_vtr(file, gender=speakers_gender)
                file_get_vocal_tract_resonances = VTRProcessor().get_vtr(file, gender=speakers_gender)
                sr = (file_get_vocal_tract_resonances[0] / 168) ** (1 / 3) * 168
                tsv_file.write(speaker +
                            "	" + speakers_gender +
                            "	" + str(vowel) +
                            "	" + str(file_get_vocal_tract_resonances[0]) +
                            "	" + str(file_get_vocal_tract_resonances[1]) +
                            "	" + str(file_get_vocal_tract_resonances[2]) +
                            "	" + str(file_get_vocal_tract_resonances[3]) +
                            "	" + str(sr) +
                            "	" + str(math.log10(file_get_vocal_tract_resonances[1] / sr)) +
                            "	" + str(math.log10(file_get_vocal_tract_resonances[2] / file_get_vocal_tract_resonances[1])) +
                            "	" + str(math.log10(file_get_vocal_tract_resonances[3] / file_get_vocal_tract_resonances[2])) +
                            "	" + str(file_get_vocal_tract_resonances[4]) +
                            "	" + str(file) +
                            "\n")
    tsv_file.close()