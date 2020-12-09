import hashlib


def numtobase(data):
    str = "0ABCDEFGHIJKLNMOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
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



for i in range(1,12):
    value = numtobase(i)
    print(f'value:  {value}')
    offset = 5 - len(value)
    temp = 'A'*offset + value
    print(temp)
    calc = hashlib.md5(value.encode())


    org = b'\xffDW\n\xca\x82A\x91Hp\xaf\xbc1\x0c\xdb\x85'
    print(org)
    print(calc.digest())


    if org == calc.digest():
        print('True')
    else:
        print("False")


