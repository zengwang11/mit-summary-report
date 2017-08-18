import json
with open('measure.json','r')as f:
	data=json.load(f)
	
f=open('5.json','w+')
for a in range(len(data['results'])):
    z=data['results'][a]['enriched_text']['categories']
    for b in range(len(z)):
    	x= z[b]['label']  
    	y= z[b]['score']   
    	y=str(y)
        f.write("label:  ")
        f.write('\t')
    	f.write(x)
        f.write('\n')
        f.write("score:  ")
        f.write('\t')
    	f.write(y)
    	f.write('\n')

f.close