# Example audio analysis scripts

This repository contains example voice analysis scripts used in my academic projects. Currently, it provides the following examples:

1. Praat Voice Analysis - includes a Praat script which performs a comprehensive acoustic analysis of voice. The script was developed as a part of a larger project that involved texts of novels from English authors of the nineteenth and twentieth centuries sourced from [gutenberg.org](https://gutenberg.org/) and their corresponding audiobooks from [librivox.org](https://librivox.org/). The Python Aeneas library was used to align the text and audio, resulting in textgrid files (see examples in "input_data/thomas_hardy far_from_the_madding_crowd textgrids"). 
The script is designed to split audio recordings into sentence-level fragments, as indicated by the textgrid files, and analyze each fragment acoustically. This analysis includes the extraction of 31 voice features, such as intensity, periodicity, voice breaks, jitter, shimmer, and additive noise.
The obtained results were used to investigate the effects of various sentence-level linguistic features, such as grammatical form and illocutionary force, on voice.
For space reasons, the examples provided in "input_data" include two chapters from "Far from the Madding Crowd" by Thomas Hardy. However, in the research described above, as many as 105 whole novels and corresponding audiobooks were used. This highlights the potential of the script to handle large amounts of data and support more extensive studies in the field of phonetics and linguistics.

2. Python Praat Vowel Analysis - these scripts were used for obtaining measurements of vocal tract resonances of Cardinal Vowel recorded by 15 phoneticians. For space reasons, only three sets of examples of such recordings are provided in the "audio" folder. These measurements were consequently normalized in Miller’s (1989) Auditory-Perceptual Space and utilized as training data for VowelMeter, a program for semi-automatic placement of vowels in the IPA Vowel Diagram. You can find the source code for the program at [github.com/Stolarski-Lukasz/VowelMeter](https://github.com/Stolarski-Lukasz/VowelMeter) and the machine learning scripts at [github.com/Stolarski-Lukasz/ML_Projects](https://github.com/Stolarski-Lukasz/ML_Projects). The acoustic analysis is performed using Python Parselmouth library which provides an interface to Praat. The scripts were written using object-oriented programming (OOP) and adhere to SOLID principles.


#### References:
Miller, J. D. (1989). Auditory-perceptual interpretation of the vowel. *The Journal of the Acoustical Society of America*, 85(5), 2114–2134.


