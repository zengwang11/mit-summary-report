import json
with open('measure.json','r')as f:
	data=json.load(f)
	
f=open('r.json','w+')
for a in range(len(data['results'])):
    z=data['results'][a]['enriched_text']['concepts']
    for b in range(len(z)):
    	x= z[b]['relevance']  
    	y= z[b]['text']  
    	m= z[b]['dbpedia_resource'] 
    	x=str(x)
        f.write("relevance:  ")
        f.write('\t')
    	f.write(x)
        f.write('\n')
        f.write("text:  ")
        f.write('\t')
    	f.write(y)
    	f.write('\n')
    	f.write("dbpedia_resource:  ")
        f.write('\t')
    	f.write(m)
    	f.write('\n')
    f.write('\n')
f.close
