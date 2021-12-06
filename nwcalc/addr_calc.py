from struct import pack, unpack
import re

"""
An IP is just a 32-bit integer representing a 4-byte array:

[631271850].pack('N').unpack('CCCC').join('.')
=> "37.160.113.170"
Just for fun, another way to convert IP to int:

"37.160.113.170".split(".").map(&:to_i).pack('CCCC').unpack('N')[0]
=> 631271850
"""

def ipv4_validate(ipv4):
    ipv4_re = re.compile(r'''
        ^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}
        (25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$
    ''', re.VERBOSE)

    if ipv4_re.match(ipv4):
        return True
    else:
        return False

def ipv4_size_check(ipv4_long):
    if type(ipv4_long) is not int:
        return False
    elif 0 <= ipv4_long <= 4294967295:
        return True
    else:
        return False

def ip2long(ipv4):
    '''
    ipv4 to int
    '''
    if not ipv4_validate(ipv4):
        return False

    ipv4_array = list(map(int, ipv4.split('.')))
    addr_pack = pack('BBBB', *ipv4_array)    
    return unpack('!L', addr_pack)[0]

def long2ip(ipv4_long):
    '''
        int to ipv4
    '''

    if not ipv4_size_check(ipv4_long):
        return False
    
    ipv4_bin = pack('I', ipv4_long)
    ipv4_array = list(unpack('BBBB', ipv4_bin))
    # unpackすると逆になってる・・・
    ipv4_array.reverse()
    ipv4 = '.'.join(map(str, ipv4_array))

    if not ipv4_validate(ipv4):
        return False
    
    return ipv4


