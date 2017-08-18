#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 5 2017
MIT LIGO Lab, Cambridge, Boston
@author: Xinyu Wang, Zeng Wang, Jianfei Wang
"""

"""
This moudle is designed for deploying on docker platform.
Objective of this moudle is to deply a server on AWS remtoe server
which can be used to deal with audio file uploaded by user
with Watson speech to text service and accounting words in sentences
and restore result in cassandra database. And the word with medium apearing
times will be delivered to watson service serach for news with this word.
"""


#import package
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
#import os and json for file processing
import os
import json
#import cassandra and flask for network 
from cassandra.cluster import Cluster
from flask import Flask,request,make_response
#import watson service and json opreator
import operator
from watson_developer_cloud import SpeechToTextV1
import watson_developer_cloud

#address for file repository in server
#these address can be replaced for local testing
DIRECTORY='/app/video.mp3'
basic_path = '/app/'
file_name='video.mp3'

#used for primary key for records in cassandra
#this variable should be replaced for further development
user_id=0

#IP for docker container communication
IP='172.17.0.1'
PORT=9042
KEYSPACE='k1'

#tell flask which application will be using flask service
app = Flask(__name__)

#author: Jianfei Wang
#while user requesting by HTML GET,POST, parameter will be delivered into this function
@app.route('/video',methods=['GET','POST'])
#this function is used as main function which clarify the flow for processing uploaded documents
###funciton - process()
#   output
#       - html response for user
def process():
    f = request.files['file']
    f.save(os.path.join(basic_path,file_name))
    result=res2string(spe2tex(basic_path+file_name))
    res=count(result)
    cassandra(res)
    keyword=midFrequency(count(res))
    print(keyword)
    discovery(keyword)
    return make_response("keyword is :"+str(keyword))

#author: Jianfei Wang
#this function is used for cassandra record process
###function - cassandra()
#   input
#       - res: input is vocabulary accounting result which is used for inserting into database for further accumulate
def cassandra(res):
    global user_id
    #res is alreday string value
    cluster = Cluster(contact_points=[IP],port=PORT)
    session=cluster.connect(KEYSPACE)
    for key,value in res.items():
        user_id=user_id+1
        prepared_stmt= session.prepare("""
                    INSERT INTO base (id,frequency,word) values (?,?,?)
                    """)
        bound_stmt=prepared_stmt.bind([user_id,value,key])
        session.execute(bound_stmt)

#author: Jianfei Wang
#this function is for initializing cassandra database in case no table exist for data storage
###function - init()
#   output
#       - return the result of table after initialized
def init():
    cluster = Cluster(contact_points=[IP],port=PORT)
    session=cluster.connect(KEYSPACE)
    session.execute("CREATE TABLE IF NOT EXISTS base (id int PRIMARY KEY, frequency int, word text);")
    result=session.execute("select * from base")
    return make_response(result)

#author: Xinyu Wang
#this function is for geting json result from watson service
###function - spec2tex(direcorty)
#   input
#       - directory: address for audio file which will be uploaded to IBM Watson service
#   output
#       - result: json result from IBM Watson service
def spe2tex(directory):
    speech_to_text = SpeechToTextV1(
                                    username='7a20510f-9402-456f-bc13-30caf57a2b56',
                                    password='iqRBHZjWIouq',
                                    x_watson_learning_opt_out=False
                                    )
    with open(directory,'rb')as audio_file:
        return (json.dumps(speech_to_text.recognize(
                                                   audio_file,content_type='audio/mp3',timestamps=True,model='en-US_BroadbandModel',word_confidence=True
                                                   ),indent=2,encoding='UTF-8',ensure_ascii=False))

# author: Jianfei Wang
#this function is for converting json result into dictionary which included the sentence and confidence of each sentence
###function - res2string(res)
#   input
#       - res: json result from watson service
#   ouput
#       - group: list consist of each sentence
def res2string(res):
    sss=json.loads(res)
    final=''
    total=0
    count=0
    group=[]
    confG=[]
    for result in sss['results']:
        sentence=result['alternatives'][0]['transcript']
        confidence=result['alternatives'][0]['confidence']
        print(sentence)
        print(confidence)
        final+=sentence
        total+=confidence
        count+=1
        group.append(sentence)
        confG.append(confidence)
    avg=total/count
    return group

# author: Jianfei Wang
#this function is for counting vocabulary of sentences
###function - count(sentences)
#   input
#       - sentences: string list which consist of every sentence
#   output
#       - word_count: dictionary which has word as key and appearing times as value
def count(sentences):
    word_count={}
    for sentence in sentences:
        sentence.strip()
        sentence=sentence.replace('\n',' ').replace(',',' ').replace('.',' ')
    
        words=sentence.split(" ")
    
        for word in words:
            if word == '' or word == '"' or word == "'":
                words.remove(word)
            
        for word in words:
            if word == '':
                words.remove(word)  
    
        for word in words:
            if word in word_count:
                word_count[word]+=1
            else:
                word_count[word]=1
    
    return word_count

###author:zeng wang

def discovery(keyword):
	discovery = watson_developer_cloud.DiscoveryV1(
    '2016-11-07',
    username="a1582e86-98b0-4041-8fac-9c01aa85f964",
    password="kiDEgM7oCRW7")

	environments = discovery.get_environments()

	news_environments = [x for x in environments['environments'] if
                      x['name'] == "my-first-environment"]
	news_environment_id = news_environments[0]['environment_id']

	collections = discovery.list_collections(news_environment_id)
	news_collections = [x for x in collections['collections']]

	configurations = discovery.list_configurations(
    environment_id=news_environment_id)
	default_config_id = discovery.get_default_configuration_id(
    environment_id=news_environment_id)

	default_config = discovery.get_configuration(
    environment_id=news_environment_id, configuration_id=default_config_id)

	query_options = {'query': keyword}
	query_results = discovery.query(news_environment_id,
                                news_collections[0]['collection_id'],
                                query_options)
	print(query_results)
	with open('measure.json','w') as f:
		f.write(json.dumps(query_results))
	return query_results

# author: Jianfei Wang
# based on buble comapring algorithm which can be replaced with better algorthim 
###function - maxFrequency(data)
#   input
#       - data: Dictionary which has word as key and appearing times as value
#   output
#       - tmp: return the word with 
def maxFrequency(data):
    tmp=''
    large=0
    for (key,value) in data.items():
        if value > large:
            large=value
            tmp=key
    return tmp

#author: Jianfei Wang
###fucntion - midFrequency(data)
#   input
#       - data: Dictionary which has word as key and appearing times as value
#   output
#       - return the word has medium appearing times
def midFrequency(data):
    sort_dir = sorted(data.items(), key=operator.itemgetter(1))
    return sort_dir[int(len(data)/2)]

#author: Jianfei Wang
###this is the main entry of this file
if __name__ == '__main__':
    #set on debugging function of flask
    app.debug=True
    #run flask server with 0.0.0.0 anb port 80
    app.run(host='0.0.0.0',port=80)
    #initialize cassandra database
    init()
    process()
    
