""" IP address calc
* int to ipv4
* ipv4 to int
* ipv6 in progress

"""
### メモ
## structのフォーマット文字列
# '!' ネットワークバイトオーダー(32bit)
# 'I' 符号なし整数(32bit, unsigned integer)
# 'B' バイト、'4B' = 'BBBB' = [0-255, 0-255, 0-255, 0-255]
# 'L' 符号なし整数(32bitまたは64bit, unsigned long)
#     プラットフォームにより変わる場合もあり、NWアドレス計算では'I'を使用したほうがよい
# 
## rubyならこんな感じだったはず
# [631271850].pack('N').unpack('CCCC').join('.')
# => "37.160.113.170"
# "37.160.113.170".split(".").map(&:to_i).pack('CCCC').unpack('N')[0]
# => 631271850
#
## bit shiftで計算する場合、struct不要
# from struct import pack, unpack
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

    ## use struck
    # ipv4_octs = list(map(int, ipv4.split('.')))
    # addr_pack = pack('!4B', *ipv4_octs)    
    # return unpack('!I', addr_pack)[0]

    ## use bit shift
    # 192.168.1.10
    # 11000000.10101000.00000001.00001010
    # 3,232,235,786
    #
    # 10 << (8 * 0) = 10
    # 1 << (8 * 1) = 256
    # 168 << (8 * 2) = 11010048
    # 192 << (8 * 3) = 3221225472
    # sum 3232235786
    #
    # ポイント
    # * [::-1]で逆順にして、enumurateのカウントとオクテットを合わせる
    #   - 最初の: シーケンスの始まり,未指定なので0
    #   - ２番名の: シーケンスの終わり、未指定なので最終要素
    #   - -1 ステップ、ひとつづつ減らすので逆順に取得していく
    # * 例えば、192×(2^(8 * 3)) はbitシフト 192<<24 と同じ
    ipv4_long = sum(int(byte) << (8 * i) for i, byte in enumerate(ipv4.split(".")[::-1]))

    if not ipv4_size_check(ipv4_long):
        return False

    return ipv4_long

def long2ipv4(ipv4_long):
    """int to ipv4

    Args:
        ipv4_long (int): decimal ipv4 address

    Returns:
        [str]: ipv4 format
    """
    if not ipv4_size_check(ipv4_long):
        return False

    ## use struck
    # ipv4_bin = pack('!I', ipv4_long)
    # ipv4_array = list(unpack('!4B', ipv4_bin))
    # ipv4 = '.'.join(map(str, ipv4_array))

    ## use bit shift
    # 192.168.1.10
    # 11000000.10101000.00000001.00001010
    # 3,232,235,786
    # 
    # (3232235786 >> 0) & 0xFF = 10
    # (3232235786 >> 8) & 0XFF  = 169
    # (3232235786 >> 16) & 0xFF = 0 
    # (3232235786 >> 24) & 0XFF = 192
    # ポイント
    # * ビットシフトして、各オクテットをビットシフトして配列に取得
    # * range(3, -1, -1)を利用して第1オクテットから取り出していく
    # * map(str, xx)を使ってjoinできるようにStringに変換

    ipv4 = '.'.join(map(str, [(ipv4_long >> (i * 8)) & 0xFF for i in range(3, -1, -1)]))

    if not ipv4_validate(ipv4):
        return False

    return ipv4


