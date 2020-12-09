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



# for i in range(1,53):
i = 5155

value = numtobase(i)
print(f'value after base 52:  {value}')


offset = 0
temp = 'A'*offset + value


print(f' Value for length of 5: {temp}')
    # value = numtobase(i)
    # offset = 1
    # temp = 'A'*offset + value
    # print(temp)
    # calc = hashlib.md5(value.encode())


    # org = b'\xffDW\n\xca\x82A\x91Hp\xaf\xbc1\x0c\xdb\x85'
    # print(org)
    # print(calc.digest())


    # if org == calc.digest():
        # print('True')
    # else:
        # print("False")


