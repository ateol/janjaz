file=open('results.txt', 'r')
file1=open('uni_dics.txt', 'w')
res=[]
counter=0
obj={}
for line in file:
    if counter%3==0:
        obj={}
        obj['name']=line.strip('\n').strip('**')
    elif counter%3==1:
        obj['city']=line.strip('\n')
    else:
        obj['address']=line.strip('\n')
    res.append(obj)

    counter+=1

res.remove(res[len(res)-1])
print (res)
file1.write(str(res))