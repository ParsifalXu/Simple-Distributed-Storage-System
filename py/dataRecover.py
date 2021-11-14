from rsFunctions import *
import os
# case 1 : just lose p

def recover_p(circle_number, current_node, file_name, list = []):

	part1 = []
	part2 = []
	part3 = []
	part4 = []
	part5 = []
	part6 = []

	for i in range(0, 6):
		if i == 0:
			part1 = [int(repr(x).encode()) for x in list[i]]
		elif i == 1:
			part2 = [int(repr(x).encode()) for x in list[i]]
		elif i == 2:
			part3 = [int(repr(x).encode()) for x in list[i]]
		elif i == 3:
			part4 = [int(repr(x).encode()) for x in list[i]]
		elif i == 4:
			part5 = [int(repr(x).encode()) for x in list[i]]
		elif i == 5:
			part6 = [int(repr(x).encode()) for x in list[i]]


	length = len(part1)
    # p_parity
	str_p = [0] * length
	for i in range(0, length):
		str_p[i] = part1[i] ^ part2[i] ^ part3[i] ^ part4[i] ^ part5[i] ^ part6[i]

	p_order = (6 + circle_number) % 8

	bytes_p = bytes(str_p)
	pp = open(current_node + '/disk_' + str(p_order) + '/' + file_name + '_p', 'wb')
	pp.write(bytes_p)
	pp.close()


# case 2 : just lost q

def recover_q(circle_number, current_node, file_name, list = []):

	part1 = []
	part2 = []
	part3 = []
	part4 = []
	part5 = []
	part6 = []

	for i in range(0, 6):
		if i == 0:
			part1 = [int(repr(x).encode()) for x in list[i]]
		elif i == 1:
			part2 = [int(repr(x).encode()) for x in list[i]]
		elif i == 2:
			part3 = [int(repr(x).encode()) for x in list[i]]
		elif i == 3:
			part4 = [int(repr(x).encode()) for x in list[i]]
		elif i == 4:
			part5 = [int(repr(x).encode()) for x in list[i]]
		elif i == 5:
			part6 = [int(repr(x).encode()) for x in list[i]]

	length = len(part1)
	str_q = [0] * length
	q_order = (7 + circle_number) % 8
	for i in range(0, length):
		str_q[i] = gf_add(gf_mul(gf_drive((0 + circle_number) % 8), part1[i]),
							gf_mul(gf_drive((1 + circle_number) % 8), part2[i]),
							gf_mul(gf_drive((2 + circle_number) % 8), part3[i]),
							gf_mul(gf_drive((3 + circle_number) % 8), part4[i]),
							gf_mul(gf_drive((4 + circle_number) % 8), part5[i]),
							gf_mul(gf_drive((5 + circle_number) % 8), part6[i]))

	bytes_q = bytes(str_q)
	qp = open(current_node + '/disk_' + str(q_order) + '/' + file_name + '_q', 'wb')
	qp.write(bytes_q)
	qp.close()

# case 3 : lose d and p

def recover_d_p(arg):
	pass


# case 4 : lose d and q

def recover_d_q(q_path, file_name):
	# recover d first, then recover q
	disk_number = int(os.path.basename(path)[-1])
	circle_number = (8 - (7 - 1 - disk_number)) % 8
	current_node = os.path.dirname(path)

	# for i in range







# case 5 : lose p and q
# circle_number, current_node, file_name, list = []
# p_path disk_
def recover_p_q(p_path, file_name):
	disk_number = int(os.path.basename(path)[-1])
	circle_number = (8 - (7 - 1 - disk_number)) % 8
	current_node = os.path.dirname(path)

	partArr = []
	for i in range(0, 6):
		order = (i + circle_number) % 8
		temp = open(current_node + '/disk_' + str(order) + '/' + file_name + '_' + str(i + 1) , 'rb')
		buffer = temp.read()
		partArr.append(buffer)
		temp.close()

	recover_p(circle_number, current_node, file_name, partArr)
	recover_q(circle_number, current_node, file_name, partArr)


#
# path = '../Nodes/node_1/disk_4'
#
# recover_p_q(path, 'xrp.pdf')



# case 6 : lose 2d

def recover_2d(arg):
	pass

# def isBroken(file_name):
# 	recover_p


#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
