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
import helper
import datetime
from nltk import word_tokenize
from nltk.tag.stanford import StanfordNERTagger
import time

nltk.download('punkt')
nltk.download('tokenizers');


def named_entities(START_VALUE,END_VALUE,in_dir,in_file):

    properties_json = json.load(open("properties.json"))
    #nltk sentences, built in
    tokenizer = nltk.download('/tokenizers/punkt/english.pickle')
    #STANFORD TAGGER
    # "stanford_classifer":"stanford-ner/english.muc.7class.distsim.crf.ser.gz",
    #"stanford_jar":"stanford-ner/stanford-ner.jar"
    classifier = properties_json["stanford_classifer"]
    jar =properties_json["stanford_jar"]
    st = StanfordNERTagger(classifier,jar)

    with open(in_dir+'/'+in_file,"r") as fp:
        SUPER_JSON = json.load(fp)

    #add sentences
    counter = 0
    for items in SUPER_JSON["@data"]:
        counter = counter + 1
        items["counter"]= counter
        text = items["title"] + ". " + items["body"]
        items["entities"]=[]
        SENTENCES_TO_TAG = tokenizer.tokenize(text)
        items["text"] = text
        #no longer needed original_body
        items["original_body"]=[]
        items["sentences"] = SENTENCES_TO_TAG

    print "START:"
    print datetime.datetime.now().isoformat()
    entity_tags = {"PERSON","ORGANIZATION","LOCATION","DATE"}
    for i in xrange(len(SUPER_JSON["@data"])):
        if i >= START_VALUE and i < END_VALUE:
            # 20 seconds for 1 file
            #try:
                list_tagged_text = []
                jsondata =[]
                print i, SUPER_JSON["@data"][i]["counter"]
                for sentences in SUPER_JSON["@data"][i]["sentences"]:
                    tokenized_text = word_tokenize(helper.encode(sentences))
                    tagged_text = st.tag(tokenized_text)

                    list_tagged_text.append(tagged_text)
                    for j in xrange(len(tagged_text)):
                        for entity_tag in entity_tags:
                            if entity_tag in tagged_text[j][1]:
                                jsondictitem = {entity_tag:tagged_text[j][0]}
                                jsondata.append(jsondictitem)
                SUPER_JSON["@data"][i]["entities"]=jsondata

            #Use this for sentence entities
            #sentence_data = {"sentence":sentences,"entities":sentence_entities}
            #sentence_arr.append(sentence_data)

            #except:
            #    SUPER_JSON["@data"][i]["entities"]=[{"ERROR":"ERROR"}]
    print "END:"
    print datetime.datetime.now().isoformat()

    for i,items in enumerate(SUPER_JSON["@data"]):
        entitytagslist=get_entitytagslist(items["entities"])
        items["entities"]=get_final_entitytagslist(entitytagslist,items["entities"])


    #for j,item in enumerate(SUPER_JSON["@data"]):
    #    for j, sentence_entity in enumerate(item["sentence_entities"]):
    #        entitytagslist=get_entitytagslist(sentence_entity["entities"])
    #        sentence_entity["combined_entities"]=get_final_entitytagslist(entitytagslist,sentence_entity["entities"])

    #@create new json file
    SUPER_JSON["@metadata"]["@time_date_ner"]=str(time.strftime('%X %x %Z'))
    with open(in_dir+'/'+in_file, 'w') as datafile:
        json.dump(SUPER_JSON, datafile, indent=4, sort_keys=True, separators=(',', ':'))


def get_entitytagslist(elist):
    entitytagslist=[]
    for i, entityitem in enumerate(elist):
        for j, keyitem in enumerate(entityitem):
            entitytagslist.append(keyitem)
    return entitytagslist


def get_all_entities(entitytagslist,elist,i, tag):
    string_entity = ""
    if entitytagslist[i-1]==tag and i < len(entitytagslist):
        return string_entity
    while entitytagslist[i]==tag:
        if i < len(entitytagslist):
            string_entity = string_entity + " " + elist[i][tag]
            if i == len(entitytagslist)-1:
                break
            i = i + 1
    return string_entity


def get_final_entitytagslist(entitytagslist,elist):
    combined_entities_array =[]
    for i, tagitems in enumerate(entitytagslist):
        string_entity =  get_all_entities(entitytagslist,elist,i, tagitems)
        if len(string_entity)>0:
            combined_entities_array.append({tagitems:string_entity})
    return combined_entities_array
