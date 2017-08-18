# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import operator

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
    

def maxFrequency(data):
    tmp=''
    large=0
    for (key,value) in data.items():
        if value > large:
            large=value
            tmp=key
    return tmp

def midFrequency(data):
    
    sort_dir = sorted(data.items(), key=operator.itemgetter(1))
    return sort_dir[int(len(data)/2)]


    
    
if __name__== '__main__':
    sentences=['''Our founding Senior Producer Greg Kelly reflects on the start of the program.''','''
"The very first show in Feb 2006 never aired widely. Only to WUNC's audience.  Dick and I had been puzzling for weeks on the show's DNA. I was the Senior Producer and was working with Dick to develop the show's identity. One thing we decided was to get at current events through past experiences, and have those experiences related by the person who had them. So this show featured an interview with Jim Auld, about his experience of being picked up off the streets of Belfast and brutally interrogated by British forces. The context was extreme rendition, photos from Abu Ghraib, the war in Iraq and so on.''',
'''One lovely memory I have sitting in the control room when it was all over was hearing applause coming from the big room where donors and supporters had gathered. Dick and I had a small moment on his side of the glass, then went out to meet all those welcoming, beaming faces."''']
    dic=count(sentences)
#    print(maxFrequency(dic))
    print (midFrequency(dic))