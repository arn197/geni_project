import hashlib


def numtobase(data):
    str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLNMOPQRSTUVWXYZ"
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
    return result.digest()



org = generated_hash('hi')
print(org)



# value = numtobase(140607)
# print(f'value after base 52:  {value}')




# offset = 5 - len(value)
# temp = 'A'*offset + value


# print(f' Value for length of 5: {temp}')