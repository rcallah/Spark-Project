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

import os
import helper
import nltk
import time
import json

def load_files(cases_text_directory, output_dir, output_file):
    tokenizer = nltk.download('/tokenizers/punkt/english.pickle')
    path = cases_text_directory + "/"
    filenames = os.listdir(path)
    count = 0
    arr_json_file =[]
    arr_metadata = {}
    json_output_file = {}
    for filename in filenames:
        outputarray = {}
        if '.pdf.txt' in filename:
            count = count + 1
            with open(path+filename) as fp:
                lines = fp.readlines()
            #read line by line
            lines = [line.rstrip('\n') for line in open(path+filename)]
            text = ' '.join(str(e) for e in lines)
            text = ''.join([i if ord(i) < 128 else ' ' for i in text])
            text = helper.encode(text.replace("  "," "))
            text =text.replace("Williams, Brooke 6/26/2015 For Educational Use Only","")
            outputarray["body"]=text
            outputarray["filename"]=filename
            outputarray["entities"]=[]
            outputarray["title"]=""
            outputarray["file_count"]=count
            arr_json_file.append(outputarray)

    arr_metadata["@count_at_loading"]=str(count)
    arr_metadata["@time_date"]=str(time.strftime('%X %x %Z'))
    arr_metadata["@input_directory"]=str(cases_text_directory)
    json_output_file["@data"]=arr_json_file
    json_output_file["@metadata"]=arr_metadata

    with open(output_dir+'/'+output_file, 'w') as datafile:
            json.dump(json_output_file, datafile, indent=4, sort_keys=True, separators=(',', ':'))
