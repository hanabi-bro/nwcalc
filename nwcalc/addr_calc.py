""" IP address calc
* int to ipv4
* ipv4 to int
* ipv6 in  progress


# structのフォーマット文字列
'!' ネットワークバイトオーダー(32bit)
'I' 符号なし整数(32bit, unsigned integer)
'B' バイト、'4B' = 'BBBB' = [0-255, 0-255, 0-255, 0-255]
'L' 符号なし整数(32bitまたは64bit, unsigned long)
    プラットフォームにより変わる場合もあり、NWアドレス計算では'I'を使用したほうがよい


ちなみにrubyならこんな感じだったはず
[631271850].pack('N').unpack('CCCC').join('.')
=> "37.160.113.170"

"37.160.113.170".split(".").map(&:to_i).pack('CCCC').unpack('N')[0]
=> 631271850
"""
from struct import pack, unpack
import re


def ipv4_validate(ipv4):
    """validate ipv4 format

    Args:
        ipv4 (str): ipv4 format

    Returns:
        boole: valid: True
    """
    ipv4_re = re.compile(r"""
        ^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}
        (25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$
    """, re.VERBOSE)

    if ipv4_re.match(ipv4):
        return True
    else:
        return False


def ipv4_size_check(ipv4_long):
    """size chek ipv4 decimal

    Args:
        ipv4_long (int): ipv4 decimal

    Returns:
        boole: valid: True
    """
    if type(ipv4_long) is not int:
        return False
    elif 0 <= ipv4_long <= 4294967295:
        return True
    else:
        return False


def ipv42long(ipv4):
    """ipv4 to int

    Args:
        ipv4 (str): ipv4 format

    Returns:
        [int]: decimal ipv4 address
    """

    if not ipv4_validate(ipv4):
        return False

    ipv4_octs = list(map(int, ipv4.split('.')))
    addr_pack = pack('!4B', *ipv4_octs)    
    return unpack('!I', addr_pack)[0]


def long2ipv4(ipv4_long):
    """int to ipv4

    Args:
        ipv4_long (int): decimal ipv4 address

    Returns:
        [str]: ipv4 format
    """
    if not ipv4_size_check(ipv4_long):
        return False

    ipv4_bin = pack('!I', ipv4_long)
    ipv4_array = list(unpack('!4B', ipv4_bin))
    ipv4 = '.'.join(map(str, ipv4_array))

    if not ipv4_validate(ipv4):
        return False

    return ipv4


