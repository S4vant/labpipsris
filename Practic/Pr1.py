import time
print(time.time())

a = 10 #int
b = 10.0 #float
c = "Hello" #string
d = True #bool
e = None #NoneType
f = [1, 2, 3, 4, 5] #list
g = (1, 2, 3, 4, 5) #tuple
h = {1, 2, 3, 4, 5} #set
i = {"name": "Yar", "age": 20} #dict

print(a*b)
print(a+b)
print(a-b)
print(a/b)
print(a//b)
print(a%b)
print(a**b)
print(a==b)
print(a!=b)
print(a>b)
print(a<b)

if __name__ == "__main__":
    if a == b:#1 отступ
        print("a == b") # 2 отступа
    else:
        print("a != b")
    print(type(a))
    print(type(b))
    print(type(c))
    print(type(d))
    print(type(e))
    if a in f:
        print("a in f")
    elif 6 in f:
        print("5 in f")
    elif 7 in f:
        print("3 in f")
    else:
        while a not in f:
            
            f.append(f[-1]+1)
            print(f)
    for i in range(10):
        print(i)
        
    ee = complex(1, 2)
    print(ee)
    print(ee.real)
    print(ee.imag)
    print(ee.conjugate)
    
    print('Yar'+" "+"Ryazantsev")
    print('Yar'*3)
    print('Yar'[1])
    if 'a' in 'Yar':
        print('a in Yar')
    print('Yar'[1:4])
    print('Yar'.lower())
    
    #Списки
    print(f)
    print(f[0])
    print(f[-1])
    print(f[0:2])
    f.append(6)
    print(f)
    f.remove(5)
    
    #кортежи
    print(tuple(f))
    print(tuple(f)[0])
    print(tuple(f)[1])
    
    #Словари
    print(dict(a=1, b=2, c=3))
    print(dict(a=1, b=2, c=3)['a'])
    print(dict(a=1, b=2, c=3)['b'])
    
    open('pr1.txt', 'w').write('Hello world')
    print(open('pr1.txt', 'r').read())
    
    