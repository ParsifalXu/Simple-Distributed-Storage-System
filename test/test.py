import os

file = open('tt', 'rb')
buffer = file.read()
print(type(buffer))
# print(buffer)

str_list = [int(repr(x).encode()) for x in buffer]
print(type(str_list[0]))
print(str_list)
t = bytes(str_list)
print(type(t))
print(t)
