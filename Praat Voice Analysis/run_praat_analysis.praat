# reading input data
####################
metadata_list = Create Strings as file list: "textlist", "input_data/*.metadata"
metadata_file_name$ = Get string: 1
metadata = Read from file: "input_data/" + metadata_file_name$
author$ = Get value: 1, "Author"
novel$ = Get value: 1, "Novel"
writeInfo: metadata
audio_list = Create Strings as file list: "audiolist", "input_data/" + author$ + " " + novel$ + " trimmed_recordings/*.mp3"
number_of_recordings = Get number of strings
text_list = Create Strings as file list: "textlist", "input_data/" + author$ + " " + novel$ +  " textgrids/*.TextGrid"
number_of_textgrids = Get number of strings

if number_of_recordings == 0 or number_of_textgrids == 0 or number_of_recordings <> number_of_textgrids
    exitScript: "Please place equal number of sounds and textgrids into appropriate folders first."
endif

writeFileLine: "results/" + author$ + " " + novel$ + " acoustic_statistics.tsv", "index	duration	f0_median	f0_mean	f0_sd	f0_mean_absolute_slope	f0_minimum	f0_maximum	pulses_number	periods_number	period_mean	period_sd	unvoiced_frames_percent	breaks_number	breaks_degree	jitter_local	jitter_absolute	jitter_rap	jitter_ppq5	jitter_ddp	shimmer_local	shimmer_db	shimmer_apq3	shimmer_apq5	shimmer_apq11	shimmer_dda	mean_autocorrelation	mean_noise_to_harmonics_ratio	mean_harmonics_to_noise_ratio	intensity_mean	intensity_sd"


# looping through recording-textgrid pairs
##########################################
for files_loop_index to number_of_recordings
    selectObject: metadata
    chapter$ = Get value: files_loop_index, "Chapter"
    gender$ = Get value: files_loop_index, "Readers_gender"
    selectObject: audio_list
    audio_file_name$ = Get string: files_loop_index
    audio_fileID = Read from file: "input_data/" + author$ + " " + novel$ + " trimmed_recordings/" + audio_file_name$
    selectObject: text_list
    texgrid_file_name$ = Get string: files_loop_index
    textgrid_fileID = Read from file: "input_data/" + author$ + " " + novel$ +  " textgrids/" + texgrid_file_name$
    number_of_intervals = Get number of intervals: 1
    plusObject: audio_fileID
    Extract all intervals: 1, "no"
    extracted_interval = textgrid_fileID + 2
    
    # looping through intervals in a given recording-textgrid pair
    ##############################################################
    for interval_loop_index to number_of_intervals
	selectObject: textgrid_fileID
	tekst$ = Get label of interval: 1, interval_loop_index
	current_interval = textgrid_fileID + interval_loop_index
	selectObject: current_interval
	
	# voice attributes from voice report
	####################################
	# creating pitch and point_process objects; by choosing them and the sound file - voice report
	if gender$ == "m"
	    f0 = To Pitch: 0, 75, 300
	    appendInfoLine: "measured pitch for male"
	    plusObject: current_interval
	    point_process = To PointProcess (cc)
	    plusObject: current_interval, f0
	    voice_report$ = Voice report: 0, 0, 75, 300, 1.3, 1.6, 0.03, 0.45

	elif gender$ == "f"
		f0 = To Pitch: 0, 100, 500
		appendInfoLine: "measured pitch for female"	    
		plusObject: current_interval
		point_process = To PointProcess (cc)
		plusObject: current_interval, f0
		voice_report$ = Voice report: 0, 0, 100, 500, 1.3, 1.6, 0.03, 0.45
	endif
		
	# getting individual values from voice report
	duration = extractNumber(voice_report$, "duration: ")
	
	f0_median = extractNumber(voice_report$, "Median pitch: ")
	f0_mean = extractNumber(voice_report$, "Mean pitch: ")
	f0_sd = extractNumber(voice_report$, "Standard deviation: ")
	f0_minimum = extractNumber(voice_report$, "Minimum pitch: ")
	f0_maximum = extractNumber(voice_report$, "Maximum pitch: ")
	
	pulses_number = extractNumber(voice_report$, "Number of pulses: ")
	periods_number = extractNumber(voice_report$, "Number of periods: ")
	period_mean = extractNumber(voice_report$, "Mean period: ")
	period_sd = extractNumber(voice_report$, "Standard deviation of period: ")
	
	unvoiced_frames_percent = extractNumber(voice_report$, "Fraction of locally unvoiced frames: ")
	breaks_number = extractNumber(voice_report$, "Number of voice breaks: ")
	breaks_degree = extractNumber(voice_report$, "Degree of voice breaks: ")
	
	jitter_local = extractNumber(voice_report$, "Jitter (local): ")
	jitter_absolute = extractNumber(voice_report$, "Jitter (local, absolute): ")
	jitter_rap = extractNumber(voice_report$, "Jitter (rap): ")
	jitter_ppq5 = extractNumber(voice_report$, "Jitter (ppq5): ")
	jitter_ddp = extractNumber(voice_report$, "Jitter (ddp): ")
	
	shimmer_local = extractNumber(voice_report$, "Shimmer (local): ")
	shimmer_db = extractNumber(voice_report$, "Shimmer (local, dB): ")
	shimmer_apq3 = extractNumber(voice_report$, "Shimmer (apq3): ")
	shimmer_apq5 = extractNumber(voice_report$, "Shimmer (apq5): ")
	shimmer_apq11 = extractNumber(voice_report$, "Shimmer (apq11): ")
	shimmer_dda = extractNumber(voice_report$, "Shimmer (dda): ")
	
	mean_autocorrelation = extractNumber(voice_report$, "Mean autocorrelation: ")
	mean_noise_to_harmonics_ratio = extractNumber(voice_report$, "Mean noise-to-harmonics ratio: ")
	mean_harmonics_to_noise_ratio = extractNumber(voice_report$, "Mean harmonics-to-noise ratio: ")

	selectObject: f0
	f0_mean_absolute_slope = Get mean absolute slope: "Hertz"
	
	# Intensity attributes
	selectObject: current_interval
	if gender$ == "m"
		if duration > 0.0854
		intensity = To Intensity: 75, 0, "yes"
		intensity_mean = Get mean: 0, 0, "dB"
		intensity_sd = Get standard deviation: 0, 0
		removeObject: intensity
		else
		intensity_mean = 0
		intensity_sd = 0
		endif

	elif gender$ == "f"
		if duration > 0.065
		intensity = To Intensity: 100, 0, "yes"
		intensity_mean = Get mean: 0, 0, "dB"
		intensity_sd = Get standard deviation: 0, 0
		removeObject: intensity
		else
		intensity_mean = 0
		intensity_sd = 0
		endif
	endif

	# writing results to a tsv file
	###############################
	if interval_loop_index <> 1 and interval_loop_index <> number_of_intervals
	    appendFileLine: "results/" + author$ + " " + novel$ + " acoustic_statistics.tsv", novel$, "_", chapter$, "_", tekst$, "	", fixed$ (duration, 5), "	", fixed$(f0_median, 5), "	", fixed$ (f0_mean, 5), "	", fixed$ (f0_sd, 5), "	", fixed$(f0_mean_absolute_slope, 5), "	", fixed$(f0_minimum, 5), "	", fixed$(f0_maximum, 5), "	", pulses_number, "	", periods_number, "	", fixed$(period_mean, 5), "	", fixed$(period_sd, 5), "	", fixed$(unvoiced_frames_percent,7), "	", breaks_number, "	", fixed$(breaks_degree, 7), "	", fixed$(jitter_local, 7), "	", fixed$(jitter_absolute, 15), "	", fixed$(jitter_rap, 7), "	", fixed$(jitter_ppq5, 7), "	", fixed$(jitter_ddp, 7), "	", fixed$(shimmer_local, 7), "	", fixed$(shimmer_db, 7), "	", fixed$(shimmer_apq3, 7), "	", fixed$(shimmer_apq5, 7), "	", fixed$(shimmer_apq11, 7), "	", fixed$(shimmer_dda, 7), "	", fixed$(mean_autocorrelation, 7), "	", fixed$(mean_noise_to_harmonics_ratio, 7), "	", fixed$(mean_harmonics_to_noise_ratio, 7), "	", fixed$(intensity_mean, 3), "	", fixed$(intensity_sd, 3)
	    selectObject: textgrid_fileID
	endif
	removeObject: current_interval, f0, point_process
	
    endfor
    removeObject: audio_fileID, textgrid_fileID
    
endfor

removeObject: audio_list, text_list, metadata


