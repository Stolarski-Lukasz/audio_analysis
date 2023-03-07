import parselmouth
from parselmouth.praat import call
import pickle
import pandas as pd
import math
from scipy.stats.mstats import gmean
from abc import ABC, abstractclassmethod


class IVTRProcessor(ABC):
    """This is an interface for Voice Tract Resonances (VTR) Processors.
    """

    def _get_mean_formants(self, formants):
        f1_mean = call(formants, "Get mean", 1, 0, 0, "hertz")
        f2_mean = call(formants, "Get mean", 2, 0, 0, "hertz")
        f3_mean = call(formants, "Get mean", 3, 0, 0, "hertz")
        return [f1_mean, f2_mean, f3_mean]
    
    @abstractclassmethod
    def get_vtr(self, sound_file, gender):
        pass


class VTRProcessor(IVTRProcessor):

    # get voice tract resonances (F0, F1, F2, F3)
    def get_vtr(self, sound_file, gender):
        results = []
        sound = parselmouth.Sound(sound_file)
        if gender == "m":
            f0 = call(sound, "To Pitch", 0, 75, 300)
            f0_mean = call(f0, "Get mean", 0, 0, "Hertz")
            formants = call(sound, "To Formant (burg)", 0, 5, 5000, 0.025, 50)
            formants = self._get_mean_formants(formants=formants)
            results = [f0_mean] + formants + ["settings 5 5000"]
        elif gender == "f":
            f0 = call(sound, "To Pitch", 0, 100, 500)
            f0_mean = call(f0, "Get mean", 0, 0, "Hertz")
            formants = call(sound, "To Formant (burg)", 0, 5, 5500, 0.025, 50)
            formants = self._get_mean_formants(formants=formants)
            results = [f0_mean] + formants + ["settings 5 5500"]
        return results


class  VTRProcessorSmart(IVTRProcessor):

    # this uses pcv_gpclassifier which detects high back articulations in male recordings and adjusts settings in Praat
    def get_vtr(self, sound_file, gender):
        results = []
        if gender == "m":
            sound = parselmouth.Sound(sound_file)
            f0 = call(sound, "To Pitch", 0, 75, 300)
            f0_mean = call(f0, "Get mean", 0, 0, "Hertz")
            formants = call(sound, "To Formant (burg)", 0, 6, 5000, 0.025, 50)
            formants = self._get_mean_formants(formants=formants)
            sr = (f0_mean / 168) ** (1 / 3) * 168
            y = math.log10(formants[0] / sr)
            z = math.log10(formants[1] / formants[0])
            x = math.log10(formants[2] / formants[1])

            open_object = open("pcv_gpclassifier.pickle", "rb")
            pcv_gpclassifier = pickle.load(open_object)  # the object will be stored as "classifier"
            open_object.close()

            df = pd.DataFrame({"y": [y],
                            "z": [z],
                            "x": [x]})

            vowel_classification = pcv_gpclassifier.predict(df[['y', 'z', 'x']])

            if vowel_classification[0] == "cv_7" or vowel_classification[0] == "cv_8":
                results = [f0_mean] + formants + ["settings 6 5000"]
            else:
                formants = call(sound, "To Formant (burg)", 0, 5, 5000, 0.025, 50)
                formants = self._get_mean_formants(formants=formants)
                results = [f0_mean] + formants + ["settings 5 5000"]
        elif gender == "f":
            sound = parselmouth.Sound(sound_file)
            f0 = call(sound, "To Pitch", 0, 100, 500)
            f0_mean = call(f0, "Get mean", 0, 0, "Hertz")
            formants = call(sound, "To Formant (burg)", 0, 5, 5500, 0.025, 50)
            formants = self._get_mean_formants(formants=formants)
            results = [f0_mean] + formants + ["settings 5 5500"]

        return results

class  VTRProcessorGmf0(IVTRProcessor):

    # this returns geometric mean f0 instead of artithmetic mean f0
    def get_vtr(self, sound_file, gender):
        results = []
        if gender == "m":
            sound = parselmouth.Sound(sound_file)
            f0 = call(sound, "To Pitch", 0, 75, 300)
            number_of_frames = call(f0, "Get number of frames")
            pitch_listing = []
            for frame_number in range(1, number_of_frames+1):
                pitch_in_frame = call(f0, "Get value in frame", frame_number, "Hertz")
                if math.isnan(pitch_in_frame) != True:
                    pitch_listing.append(pitch_in_frame)
            f0_gmean = gmean(pitch_listing)
            formants = call(sound, "To Formant (burg)", 0, 5, 5000, 0.025, 50)
            formants = self._get_mean_formants(formants=formants)
            results = [f0_gmean] + formants + ["settings 5 5000"]
        elif gender == "f":
            sound = parselmouth.Sound(sound_file)
            f0 = call(sound, "To Pitch", 0, 100, 500)
            number_of_frames = call(f0, "Get number of frames")
            pitch_listing = []
            for frame_number in range(1, number_of_frames+1):
                pitch_in_frame = call(f0, "Get value in frame", frame_number, "Hertz")
                if math.isnan(pitch_in_frame) != True:
                    pitch_listing.append(pitch_in_frame)
            f0_gmean = gmean(pitch_listing)
            formants = call(sound, "To Formant (burg)", 0, 5, 5500, 0.025, 50)
            formants = self._get_mean_formants(formants=formants)
            results = [f0_gmean] + formants + ["settings 5 5500"]
        return results



class PitchProcessor():

    def get_pitch_ac(self, sound_file,
                    time_step=0,
                    pitch_floor=75,
                    max_number_of_candidates=15,
                    very_accurate="no",
                    silence_threshold=0.03,
                    voicing_threshold=0.45,
                    octave_cost=0.01,
                    octave_jump_cost=0.35,
                    voiced_unvoiced_cost=0.14,
                    pitch_ceiling=600):
        f0 = call(sound_file, "To Pitch (ac)", time_step, pitch_floor, max_number_of_candidates, very_accurate,
                silence_threshold, voicing_threshold, octave_cost, octave_jump_cost, voiced_unvoiced_cost, pitch_ceiling)
        return call(f0, "Get mean", 0, 0, "Hertz")



class FormantsProcessor():

    def get_formants_burg(self, sound_file,
                        time_step=0,
                        max_number_of_formants=5,
                        maximum_formant=5500,
                        window_length=0.025,
                        pre_emphasis_from=50):
        formants = call(sound_file, "To Formant (burg)", time_step, max_number_of_formants, maximum_formant,
                        window_length, pre_emphasis_from)
        f1_mean = call(formants, "Get mean", 1, 0, 0, "hertz")
        f2_mean = call(formants, "Get mean", 2, 0, 0, "hertz")
        f3_mean = call(formants, "Get mean", 3, 0, 0, "hertz")
        f4_mean = call(formants, "Get mean", 4, 0, 0, "hertz")
        return ["empty_place", f1_mean, f2_mean, f3_mean, f4_mean]
