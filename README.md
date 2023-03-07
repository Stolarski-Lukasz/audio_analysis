# Example audio analysis scripts

This repository contains example voice analysis scripts used in my academic projects. Currently, the repository provides the following examples:

1. Python Praat Vowel Analysis - these scripts were used for obtaining measurements of vocal tract resonances of Cardinal Vowel recorded by 15 phoneticians. For space reasons, only three sets of examples of such recordings are provided in the "audio" folder. These measurements were consequently normalized in Miller’s (1989) Auditory-Perceptual Space and utilized as training data for VowelMeter, a program for semi-automatic placement of vowels in the IPA Vowel Diagram. You can find the source code for the program at [github.com/Stolarski-Lukasz/VowelMeter](https://github.com/Stolarski-Lukasz/VowelMeter) and the machine learning scripts at [github.com/Stolarski-Lukasz/ML_Projects](https://github.com/Stolarski-Lukasz/ML_Projects). The acoustic analysis is performed using Python Parselmouth library which provides an interface to Praat. The scripts were written using object-oriented programming (OOP) and adhere to SOLID principles.


#### References:
Miller, J. D. (1989). Auditory-perceptual interpretation of the vowel. *The Journal of the Acoustical Society of America*, 85(5), 2114–2134.

