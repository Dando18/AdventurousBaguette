'''
Daniel Nichols
March 2021
'''

def vprint(flag, msg, **kwargs):
    if flag:
        print(msg, **kwargs)
        