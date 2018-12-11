#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

'''
Python Version: 2.7.5 (default, Mar  9 2014, 22:15:05) 
[GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.0.68)]
JAR:stanford-ner/stanford-ner.jar
CLASSIFIER:stanford-ner/english.muc.7class.distsim.crf.ser.gz
The nltk version is 2.0.4.
The scikit-learn version is 0.15-git.
'''
 
import json
import sys
import load_input_press_releases
import load_cases
import named_entities_tagger
import nltk
import sklearn
import os
from subprocess import call


class objectRun:
    def __init__(self):
        self.properties_json = json.load(open("properties.json"))
        #input 
        self.INPUT_PR_DIRECTORY =  self.properties_json["input_press_release_directory"]
        self.INPUT_PR_FILE =  self.properties_json["input_press_release_file"]
        
        #output
        self.OUTPUT_PR_DIRECTORY =  self.properties_json["output_press_release_directory"]
        self.OUTPUT_PR_FILE =  self.properties_json["output_press_release_file"]
        
        #cases
        self.INPUT_DIRECTORY =  self.properties_json["pdf_cases_input"]
        self.OUTPUT_DIRECTORY = self.properties_json["pdf_cases_output"]

        #cases
        self.OUTPUT_CASES_DIRECTORY =  self.properties_json["output_cases_directory"]
        self.OUTPUT_CASES_FILE =  self.properties_json["output_cases_file"]
        
        
        
    def versionPYTHON(self):
        print(('Python Version: ' + sys.version))
        print(self.INPUT_PR_DIRECTORY)
        print("JAR:"+self.properties_json["stanford_jar"])
        print("CLASSIFIER:"+self.properties_json["stanford_classifer"])
        print('The nltk version is {}.'.format(nltk.__version__))
        print('The scikit-learn version is {}.'.format(sklearn.__version__))


'''
########################
DRIVER
######################## 
'''
def main():
        print("PROCESSING.....")
        obj=objectRun() 
        obj.versionPYTHON()
        #pre-used entities, cannot use sentences parser because of V. X. acronyms
        load_input_press_releases.load_file(obj.INPUT_PR_DIRECTORY, obj.INPUT_PR_FILE, obj.OUTPUT_PR_DIRECTORY, obj.OUTPUT_PR_FILE)
        #enrich, using NER
        named_entities_tagger.named_entities(START_VALUE=0,END_VALUE=1,in_dir=obj.OUTPUT_PR_DIRECTORY,in_file=obj.OUTPUT_PR_FILE)
        #load
        load_cases.load_files(cases_text_directory=obj.OUTPUT_DIRECTORY,output_dir=obj.OUTPUT_CASES_DIRECTORY, output_file=obj.OUTPUT_CASES_FILE )
        #enrich
        named_entities_tagger.named_entities(START_VALUE=0,END_VALUE=1,in_dir=obj.OUTPUT_CASES_DIRECTORY,in_file=obj.OUTPUT_CASES_FILE)
        
if  __name__ =='__main__':main()
        
