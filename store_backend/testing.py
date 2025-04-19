n=input()
x=input()
a=x.split(" ")
for i in range(len(a)):
    a[i]=int(a[i])

for i in range(len(a)):
    if a[i]>0:
        a[i]=1
    elif a[i]<0:
        a[i]=2
for i in a:
    print(i,end="")
