from rsFunctions import *
import os
import readCN

# case 1 : just lose p

def recover_p(circle_number, file_name, list = []):

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
	pp = open('./Storage/disk_' + str(p_order) + '/' + file_name + '_p', 'wb')
	pp.write(bytes_p)
	pp.close()


# case 2 : just lost q

def recover_q(circle_number, file_name, list = []):

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
	qp = open('./Storage/disk_' + str(q_order) + '/' + file_name + '_q', 'wb')
	qp.write(bytes_q)
	qp.close()

# case 3 : lose 1 d
def recover_d(file_name, disk_number):
	circle_number = readCN.read_file_circle_number(file_name)

	partArr = []
	order_save = -1
	for i in range(0, 6):
		order = (i + circle_number) % 8
		if order != disk_number:
			temp = open('./Storage/disk_' + str(order) + '/' + file_name + '_' + str(i + 1) , 'rb')
			buffer = temp.read()
			partArr.append(buffer)
			temp.close()
		else:
			order_save = order
			order = (6 + circle_number) % 8
			temp = open('./Storage/disk_' + str(order) + '/' + file_name + '_p', 'rb')
			buffer = temp.read()
			partArr.append(buffer)
			temp.close()

	part1 = []
	part2 = []
	part3 = []
	part4 = []
	part5 = []
	part6 = []

	for i in range(0, 6):
		if i == 0:
			part1 = [int(repr(x).encode()) for x in partArr[i]]
		elif i == 1:
			part2 = [int(repr(x).encode()) for x in partArr[i]]
		elif i == 2:
			part3 = [int(repr(x).encode()) for x in partArr[i]]
		elif i == 3:
			part4 = [int(repr(x).encode()) for x in partArr[i]]
		elif i == 4:
			part5 = [int(repr(x).encode()) for x in partArr[i]]
		elif i == 5:
			part6 = [int(repr(x).encode()) for x in partArr[i]]


	length = len(part1)
	str_d = [0] * length
	for i in range(0, length):
		str_d = partArr[0] ^ partArr[1] ^ partArr[2] ^ partArr[3] ^ partArr[4] ^ partArr[5]

	bytes_d = bytes(str_d)
	wd = open('./Storage/disk_' + str(disk_number) + '/' + file_name + '_' + str(order_save), 'wb')
	wd.write(bytes_d)
	wd.close()


# case 4 : lose d and p

def recover_d_p(file_name, disk_number):
	circle_number = readCN.read_file_circle_number(file_name)
	partArr = []
	order_save = -1

	for i in range(0, 6):
		order = (i + circle_number) % 8
		if order != disk_number:
			temp = open('./Storage/disk_' + str(order) + '/' + file_name + '_' + str(i + 1) , 'rb')
			buffer = temp.read()
			partArr.append(buffer)
			temp.close()
		else:
			order_save = order

	order = (7 + circle_number) % 8
	temp = open('./Storage/disk_' + str(order) + '/' + file_name + '_q', 'rb')
	buffer = temp.read()
	partArr.append(buffer)
	temp.close()

	part1 = []
	part2 = []
	part3 = []
	part4 = []
	part5 = []
	part6 = []

	for i in range(0, 6):
		if i == 0:
			part1 = [int(repr(x).encode()) for x in partArr[i]]
		elif i == 1:
			part2 = [int(repr(x).encode()) for x in partArr[i]]
		elif i == 2:
			part3 = [int(repr(x).encode()) for x in partArr[i]]
		elif i == 3:
			part4 = [int(repr(x).encode()) for x in partArr[i]]
		elif i == 4:
			part5 = [int(repr(x).encode()) for x in partArr[i]]
		elif i == 5:
			part6 = [int(repr(x).encode()) for x in partArr[i]]


	length = len(part1)
	partial_q = [0] * length
	str_d = [0] * length


	for i in range(0, length):
		partial_q[i] = gf_add(gf_mul(gf_drive((0 + circle_number) % 8), part1[i]),
							gf_mul(gf_drive((1 + circle_number) % 8), part2[i]),
							gf_mul(gf_drive((2 + circle_number) % 8), part3[i]),
							gf_mul(gf_drive((3 + circle_number) % 8), part4[i]),
							gf_mul(gf_drive((4 + circle_number) % 8), part5[i]),
							part6[i])

		div_result = gf_div(1, gf_drive(order_save))

		str_d[i] = gf_mul(div_result, partial_q[i])



	bytes_d = bytes(str_d)
	wd = open('./Storage/disk_' + str(disk_number) + '/' + file_name + '_' + str(order_save), 'wb')
	wp.write(bytes_d)
	wp.close()

	for i in range(0, 6):
		order = (i + circle_number) % 8
		temp = open('./Storage/disk_' + str(order) + '/' + file_name + '_' + str(i + 1) , 'rb')
		buffer = temp.read()
		partArr[i] = buffer
		temp.close()

	recover_p(circle_number, file_name, partArr)


# case 5 : lose d and q

def recover_d_q(file_name, disk_number):
	# recover d first
	recover_d(file_name, disk_number)
	# then recover q
	circle_number = readCN.read_file_circle_number(file_name)
	partArr = []

	for i in range(0, 6):
		order = (i + circle_number) % 8
		temp = open('./Storage/disk_' + str(order) + '/' + file_name + '_' + str(i + 1) , 'rb')
		buffer = temp.read()
		partArr.append(buffer)
		temp.close()

	recover_q(circle_number, file_name, partArr)




# case 6 : lose p and q
# p_path disk_
def recover_p_q(file_name):
	circle_number = readCN.read_file_circle_number(file_name)
	partArr = []

	for i in range(0, 6):
		order = (i + circle_number) % 8
		temp = open('./Storage/disk_' + str(order) + '/' + file_name + '_' + str(i + 1) , 'rb')
		buffer = temp.read()
		partArr.append(buffer)
		temp.close()

	recover_p(circle_number, file_name, partArr)
	recover_q(circle_number, file_name, partArr)


# case 7 : lose 2d
def recover_2d(file_name, disk_number_1, disk_number_2):
	circle_number = readCN.read_file_circle_number(file_name)
	partArr = [] * 6
	order_d1 = -1
	order_d2 = -1

	for i in range(0, 6):
		order = (i + circle_number) % 8
		if order == disk_number_1:
			order_d1 = order
		elif order == disk_number_2:
			order_d2 = order
		else:
			temp = open('./Storage/disk_' + str(order) + '/' + file_name + '_' + str(i + 1) , 'rb')
			buffer = temp.read()
			partArr.append(buffer)
			temp.close()

	temp_p = open('./Storage/disk_' + str(order) + '/' + file_name + '_p', 'rb')
	buffer = temp_p.read()
	partArr[4] = buffer
	temp_p.close()

	temp_q = open('./Storage/disk_' + str(order) + '/' + file_name + '_q', 'rb')
	buffer = temp_q.read()
	partArr[5] = buffer
	temp_q.close()

	part1 = []
	part2 = []
	part3 = []
	part4 = []
	part5 = []
	part6 = []

	for i in range(0, 6):
		if i == 0:
			part1 = [int(repr(x).encode()) for x in partArr[i]]
		elif i == 1:
			part2 = [int(repr(x).encode()) for x in partArr[i]]
		elif i == 2:
			part3 = [int(repr(x).encode()) for x in partArr[i]]
		elif i == 3:
			part4 = [int(repr(x).encode()) for x in partArr[i]]
		elif i == 4:
			part5 = [int(repr(x).encode()) for x in partArr[i]]
		elif i == 5:
			part6 = [int(repr(x).encode()) for x in partArr[i]]

	length = len(part1)
	partial_p = [0] * length
	partial_q = [0] * length
	str_d1 = [0] * length
	str_d2 = [0] * length

	for i in range(0, length):
		partial_p[i] = gf_add(part1[i], part2[i], part3[i], part4[i])
		partial_q[i] = gf_add(gf_mul(gf_drive((0 + circle_number) % 8), part1[i]),
							gf_mul(gf_drive((1 + circle_number) % 8), part2[i]),
							gf_mul(gf_drive((2 + circle_number) % 8), part3[i]),
							gf_mul(gf_drive((3 + circle_number) % 8), part4[i]))

		g = gf_div(1, gf_add(gf_drive(order_d1), gf_drive(order_d2)))

		xored_p = gf_add(partial_p[i], part5[i])
		xored_q = gf_add(partial_q[i], part6[i])

		mid = gf_add(gf_mul(gf_drive(order_d2), xored_p), xored_q)

		# Regenerate data for D1.
		data = gf_mul(mid, g)
		str_d1[i] = data

		# Regenerate data for D2.
		str_d2[i] = gf_add(part1[i], str_d1[i], partial_p[i])


	bytes_d1 = bytes(str_d1)
	wd1 = open('./Storage/disk_' + str(disk_number) + '/' + file_name + '_' + str(order_d1), 'wb')
	wd1.write(bytes_d1)
	wd1.close()

	bytes_d2 = bytes(str_d2)
	wd2 = open('./Storage/disk_' + str(disk_number) + '/' + file_name + '_' + str(order_d2), 'wb')
	wd2.write(bytes_d2)
	wd2.close()







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
