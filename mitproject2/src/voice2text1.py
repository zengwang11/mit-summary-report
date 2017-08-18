# encoding: UTF-8
import json
from os.path import join,dirname
from watson_developer_cloud import SpeechToTextV1

DIRECTORY='demo2.mp3'

##used to transform speech to text
#argument
#    directory -- path to file
#result
#   string -- json format answer, need further operation
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
    print final,avg
    f=open("sentence.txt", "w")
    f.write(final)      
    return final,avg
    #return final,avg,group,confG
    #print final,avg,group,confG

    
#    transcript= sss['results'][0]['alternatives'][0]['transcript']
#    confidence= sss['results'][0]['alternatives'][0]['confidence']
#    print transcript
#    print confidence
#    f=open("Output.txt", "w")
#    f.write(transcript)
    
        
if __name__ == "__main__":
    res=spe2tex(DIRECTORY)
    res2string(res)