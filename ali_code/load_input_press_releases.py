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

import nltk
import json 
import time
import re



taglist = ['NN','NNS','NNP']
#this version is based on patterns already identified 
def linguistic_markers(text_body):
    sentences = []
    searchitems = [
                   
                   {"type":"@Attorney","phrase":"prosecuted the"},\
                   {"type":"@Attorney","phrase":"prosecuting the case"},\
                   {"type":"@Attorney","phrase":"prosecuting this case"},\
                   {"type":"@Attorney","phrase":"prosecuted by"},\
                   {"type":"@Attorney","phrase":"Attorney"},\
                   
                   {"type":"@Defendant","phrase":"was arrested"},\
                   {"type":"@Defendant","phrase":"was indicted"},\
                   {"type":"@Defendant","phrase":"was found guilty"},\
                   {"type":"@Defendant","phrase":"pleaded guilty"},\
                   {"type":"@Defendant","phrase":"was ordered to prison"},\
                   {"type":"@Defendant","phrase":"was ordered to federal prison"},\
                   {"type":"@Defendant","phrase":"has been charged"},\
                   {"type":"@Defendant","phrase":"was charged"},\
                   {"type":"@Defendant","phrase":"a.k.a."},\
                   {"type":"@Defendant","phrase":"aka"},\
                   {"type":"@Defendant","phrase":"sentenced"},\
                   {"type":"@Defendant_age","phrase":"age"},\

                   {"type":"@Defendant","phrase":"pleaded guilty"},\
                   {"type":"@Defendant","phrase":"has been ordered to federal prison"},
                   {"type":"@Sentence","phrase":"to prison"},\
                   {"type":"@Sentence","phrase":"sentenced to"},\
                  
                   {"type":"@Misconduct","phrase":"misconduct"},\

                   
                   {"type":"@Judge","phrase":"Judge"}\
                   ]
    pre_regex = "(?:[a-zA-Z]+[^a-zA-Z]+){0,7}"
    post_regex = "(?:[^a-zA-Z]+[a-zA-Z]+){0,7}"
    

    for items in searchitems:
        regex_general = pre_regex+items["phrase"]+post_regex
        matches = re.search(regex_general,text_body)
        if matches != None:
            sentence = ''.join(matches.group())
            name = "NOT_FOUND"
            titles =""
            #these are confirmed titles, caps sensitive
            if items["type"]=="@Judge" or items["type"]=="@Attorney":
                #print "\t,item type:", items["type"]
                beginning_token = "Judge" if items["type"]=="@Judge" else "Attorney"
            
                post_matches = re.search(beginning_token+post_regex,sentence)
                pre_matches = re.search(pre_regex+beginning_token,sentence)
                
                str_name = []
                if post_matches != None:
                    post_sentence = ''.join(post_matches.group())
                    #print "post_sentence",post_sentence
                    arr_post_sentence = post_sentence.split()
                    for words in arr_post_sentence[1:]:
                        if words[0].isupper():
                            str_name.append(words)
                        else:
                            break
                        
                title_name = []
                if pre_matches != None:
                    pre_sentence = ''.join(pre_matches.group())
                    #print "pre_sentence", pre_sentence
                    arr_pre_sentence = pre_sentence.split()
                    #print arr_pre_sentence
                    arr_pre_sentence.reverse()

                    for words in arr_pre_sentence[0:]:
                        if words[0].isupper():
                            title_name.append(words)
                        else:
                            break
                    title_name.reverse()
                
                name = str(' '.join(str_name))
                titles = str(' '.join(title_name))
            
            str_def_name=[] 
            if items["type"]=="@Defendant_age":
                y = sentence.split(",")
                for i,item in enumerate(y):
                    #this is the ony consistent marker in cases
                    if "age" in y[i]:
                        #print y[i-1].split(".")
                        #print y[i-1].split(".")[-1].split()
                        for words in reversed(y[i-1].split(".")[-1].split()):
                            if words[0].isupper():
                                str_def_name.append(words)
                            else:
                                break
                name = str(' '.join(str_def_name))
                
            if items["type"]=="@Judge" or items["type"]=="@Attorney" or items["type"]=="@Defendant_age":    
                sentences.append({"type":items["type"],"concordance":sentence,"title":titles, "name":name})
            else:
                sentences.append({"type":items["type"],"concordance":sentence, "name":name})
    return {"concordance_entities":sentences}
        

'''
#quick test
teststring = "United States Attorney Brendan V. Johnson announced that Jess Raymond Young, age 36, of Rosebud, South Dakota appeared before U.S. Magistrate Judge Mark A. Moreno on March 21, 2013 and pled guilty to Assault on a Federal Officer. The maximum penalty upon conviction is 20 years' imprisonment and/or a $250,000 fine.      On November 21, 2012, while in custody at the Oglala Sioux Tribal Jail in Pine Ridge, Young shoved a correctional officer against the wall and bit her multiple times. The investigation was conducted by the Bureau of Indian Affairs Office of Justice Services and the Oglala Sioux Tribe Department of Public Safety. The case is being prosecuted by Assistant U.S. Attorney Sarah B. Collins. \t      A presentence investigation was ordered and a sentencing date will be scheduled. The defendant was remanded to the custody of the U.S. Marshal pending sentencing." 
x = linguistic_markers(teststring)
for conc in x['concordance_entities']:
    print conc
'''        
    
    
def load_file(input_directory,input_file, output_dir, output_file):
    try:
        arr_json_file =[]
        error_stack_ids=[]
        arr_metadata = {}
        json_output_file = {}

        max_iter = 0
        count = 0
        with open(input_directory+'/'+input_file) as json_data:
            json_data = json.load(json_data)
        
        for nums in json_data["component"]:
            if max_iter < int(nums):
                max_iter = int(nums)    
        for i in xrange(0,max_iter+1):
            try:
                    str_date = str(json_data["created_date"][str(i)])[:-3]
                    human_date =  time.ctime(int(str_date))
                    clean_body = nltk.clean_html(json_data["body"][str(i)])
                    concordance_entities=linguistic_markers(clean_body.encode('utf-8'))                    
                    
                    arr_json_file.append(
                                            {
                                                "created_date":json_data["created_date"][str(i)],
                                                "human_date":human_date,
                                                "body":clean_body,
                                                "uuid":json_data["uuid"][str(i)],
                                                "title":json_data["title"][str(i)],
                                                "original_body":json_data["body"][str(i)],
                                                "name":json_data["component"][str(i)][0]["name"],
                                                "url":json_data["url"][str(i)],
                                                "id":i,
                                                "concordance_entities":concordance_entities['concordance_entities']
                                            }
                                        )
                    count = count + 1
            except KeyError:
                error_stack_ids.append({"ERROR_ID":i})
        arr_metadata["@count_at_loading"]=str(count)
        arr_metadata["@time_date"]=str(time.strftime('%X %x %Z'))
        arr_metadata["@input_file"]=str(input_file)
        json_output_file["@data"]=arr_json_file
        json_output_file["@metadata"]=arr_metadata
        
        with open(output_dir+'/'+output_file, 'w') as datafile:
            json.dump(json_output_file, datafile, indent=4, sort_keys=True, separators=(',', ':'))
    except Exception as exception:
        print exception
        






