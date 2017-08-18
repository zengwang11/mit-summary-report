import json

with open('measure.json', 'r') as f:
    data = json.load(f)
    z = data['results']
f=open('5.json','w+')
for n in range(4):
    x = z[n]['score']
    x = str(x)
    #f.close
    #f=open('5.json','a')
    f.write(x)
    f.write('\n')
f.close


