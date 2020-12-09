import hashlib


def numtobase(data):
    str = "ABCDEFGHIJKLNMOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    #str = "0123456789ABCDEF"
    s = ""
    if data == 0:
        return str[0] + ""
    

    while data>0:
        if data<52:
            s = str[data] + s
            data = 0
            #print(s)
        else:
            r = data%52
            s = str[r] + s
            data = (data-r)//52
            #print(s)

    
    return s


def generated_hash(data):
    result = hashlib.md5(data.encode())
    return result.hexdigest()

def compareHash(actual, determined):
    if determined == actual:
        return True


org = generated_hash('AAAAz')

for i in range(0, 380204032):
    value = numtobase(i)
    #rint(f'value after base 52:  {value}')
    offset = 5-len(value)
    temp = 'A'*offset + value
    print(f'value after offet:  {temp}')
    calc = generated_hash(temp)

    print(i)
    print(org)
    print(calc)
        
    if org == calc:
        print('True')
        print(temp)
        break
    else:
        print('False')


