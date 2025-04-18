from backend import *


# network = Network()
# network.tick()
# print(Network.reponse)
# print(Network.status)
# print(Network.data)

# log = LogReader("test.py")

# print(LogWritingUtils.toBinary(56))
print(DataLog.packLog(1, 1, 1, 1))
'''
00100
0 1 11
00100
1 0 11
00100
1 11 1
'''
# print(LogWritingUtils.packStartingBlock(0, 0, 0))

# '''
# 00000
# 1 000 0000 0000 0000 0000 0000
# 1 000 0000
# 1 000 0000 0000 0000 0000 0000
# '''