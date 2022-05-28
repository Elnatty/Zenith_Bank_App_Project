import random

def account_number_generator():
    global acct
    # use random.sample() then define a range of numbers ie range(), and pass the counts for the total numbers.
    integers = random.sample(range(10), 9)
    # using list comprehension to generate 9 random numbers.
    strings = [str(integer) for integer in integers]
    # using ''.join() to convert list back to string
    a = '2' + ''.join(strings)
    acct = int(a)
    return acct
global acct
account_number_generator()
print(acct)