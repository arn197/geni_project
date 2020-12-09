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



for i in range(0, 140607):

    value = numtobase(i)
    # print(f'value after base 52:  {value}')
    offset = 3-len(value)
    temp = 'A'*offset + value
    if temp == 'abc':
        print("hello")


    # temp = 'A'*offset + value


    # print(f' Value for length of 5: {temp}')
    # value = numtobase(i)
    # offset = 1
    # temp = 'A'*offset + value
    # print(temp)
        calc = hashlib.md5(temp.encode())


        org = "900150983cd24fb0d6963f7d28e17f72"
    # print(org)
    # print(calc.digest())
        print(calc.hexdigest(), org)

        if org == calc.digest():
            print('True')


