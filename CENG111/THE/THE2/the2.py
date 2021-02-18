
import math
import random
from evaluator import *    # get_data() will come from this import


def new_move():

	return get_infected()

datatt = get_data()
row = get_data()[0] #M
column = get_data()[1] #N
mu_constant = get_data()[5]
data = get_data()[6:]
lambda_constant = datatt[4]
k_constant = datatt[3]
d_constant = datatt[2]

def find_new_direction():
#returns the direction from which it came

	direction_list = []
	get_data_list = data
	yellow = (1/8) * mu_constant #yellow probability
	blue = (1/2) * (1-mu_constant-(mu_constant**2)) #blue probability
	purple = (2/5) * (mu_constant**2) #purple probability
	gray = (1/5) * (mu_constant**2) #gray probability
	green = (1/2) * mu_constant #green probability
	weights_list = [green,yellow,blue,purple,gray,purple,blue,yellow]
	for i in get_data_list[0]:
		if i[1] == 0:
			mylist = [0,1,2,3,4,5,6,7]
			new_direction = random.choices(mylist,weights=weights_list,k =1) #gittiğim kare yönü
			direction_list.append(new_direction)

		elif i[1] == 1:
			mylist = [1,2,3,4,5,6,7,0]
			new_direction = random.choices(mylist,weights=weights_list, k=1)
			direction_list.append(new_direction)

		elif i[1] ==2:
			mylist = [2,3,4,5,6,7,0,1]
			new_direction = random.choices(mylist, weights=weights_list, k=1)
			direction_list.append(new_direction)

		elif i[1] ==3:
			mylist = [3,4,5,6,7,0,1,2]
			new_direction = random.choices(mylist,weights=weights_list, k=1)
			direction_list.append(new_direction)

		elif i[1] ==4:
			mylist = [4,5,6,7,0,1,2,3]
			new_direction = random.choices(mylist,weights=weights_list, k=1)
			direction_list.append(new_direction)

		elif i[1] ==5:
			mylist = [5,6,7,0,1,2,3,4]
			new_direction = random.choices(mylist,weights=weights_list, k=1)
			direction_list.append(new_direction)

		elif i[1] ==6:
			mylist = [6,7,0,1,2,3,4,5]
			new_direction = random.choices(mylist,weights=weights_list, k=1)
			direction_list.append(new_direction)

		elif i[1] ==7:
			mylist = [7,0,1,2,3,4,5,6]
			new_direction = random.choices(mylist,weights=weights_list, k=1)
			direction_list.append(new_direction)

	return direction_list

def get_infected():
	a = new_dir_and_new_coordinates()[0]
	liste_new = []
	for i in range(len(a)):
		for x in range(i+1,len(a)):
			if (a[i][3] == "infected" and  a[x][3] == "notinfected") or (a[i][3] == "notinfected" and a[x][3] == "infected"):
				distance = math.dist(a[i][0],a[x][0])
				if distance <= d_constant:
					probability_of_infected = min(1,k_constant/distance**2)
					if a[x][2] == "masked" and a[i][2] == "masked":
						probability_of_infected = probability_of_infected / (lambda_constant ** 2)
					elif a[x][2] == "notmasked" and a[i][2] == "masked":
						probability_of_infected = probability_of_infected / (lambda_constant)
					elif a[x][2] == "masked" and a[i][2] == "notmasked":
						probability_of_infected = probability_of_infected / (lambda_constant)
					elif a[x][2] == "notmasked" and a[i][2] == "notmasked":
						probability_of_infected = probability_of_infected

					state_of_infection = random.choices(["infected", "notinfected"], [probability_of_infected, 1 - probability_of_infected])[0]

					if state_of_infection == "infected": #son durumda hasta olan varsa asıl listede onu değiştirmek için durumu kontrol ediyoruz.
						if a[i][3] == "infected": #hangisinin hastalığı bulaştırdığını bulmak için durumu kontrol ediyoruz.
							liste_new.append([x,"infected"]) #hastalığı kapanın indexiyle beraber bir listeye atıyoruz.
						elif a[x][3] == "infected":
							liste_new.append([i,"infected"])

	for k in liste_new: #hastalığı kapanın state'ini değiştiriyoruz
		a[k[0]][3] = "infected"
	return a

def new_dir_and_new_coordinates():
	m = []
	new_direction = find_new_direction() #list of new directions respectively

	for i in range(len(new_direction)):
		if new_direction[i] == [0]:
			new_x = data[0][i][0][0] # i'inci kişinin x'inin yeni koordinatları
			new_y = data[0][i][0][1] + 1 # i'inci kişinin y'sinin yeni koordinatları
			if new_y < row and new_y >= 0 and new_x < column and new_x >= 0: #out of arena
				new_coordinates = (new_x, new_y)
				dont_go = data[0][:] #aynı koordinatlarda bulunan başka birinin üstüne gitmemesi için kontrol edilen liste
				for coordinates in dont_go:
					m.append(coordinates[0])
				if new_coordinates not in m: #aynı koordinatlarda değilse yeni koordinatları updateliyoruz.
					data[0][i][0] = new_coordinates
					data[0][i][1] = 0
				m = []

		elif new_direction[i] == [1]:
			new_x = data[0][i][0][0] - 1
			new_y = data[0][i][0][1] + 1
			if new_y < row and new_y >= 0 and new_x < column and new_x >= 0:
				new_coordinates = (new_x, new_y)
				dont_go = data[0][:]
				for coordinates in dont_go:
					m.append(coordinates[0])
				if new_coordinates not in m:
					data[0][i][0] = new_coordinates
					data[0][i][1] = 1
				m = []

		elif new_direction[i] == [2]:
			new_x = data[0][i][0][0] - 1
			new_y = data[0][i][0][1]
			if new_y < row and new_y >= 0 and new_x < column and new_x >= 0:
				new_coordinates = (new_x, new_y)
				dont_go = data[0][:]
				for coordinates in dont_go:
					m.append(coordinates[0])
				if new_coordinates not in m:
					data[0][i][0] = new_coordinates
					data[0][i][1] = 2
				m = []

		elif new_direction[i] == [3]:
			new_x = data[0][i][0][0] - 1
			new_y = data[0][i][0][1] - 1
			if new_y < row and new_y >= 0 and new_x < column and new_x >= 0:
				new_coordinates = (new_x, new_y)
				dont_go = data[0][:]
				for coordinates in dont_go:
					m.append(coordinates[0])
				if new_coordinates not in m:
					data[0][i][0] = new_coordinates
					data[0][i][1] = 3
				m = []

		elif new_direction[i] == [4]:
			new_x = data[0][i][0][0]
			new_y = data[0][i][0][1] - 1
			if new_y < row and new_y >= 0 and new_x < column and new_x >= 0:
				new_coordinates = (new_x, new_y)
				dont_go = data[0][:]
				for coordinates in dont_go:
					m.append(coordinates[0])
				if new_coordinates not in m:
					data[0][i][0] = new_coordinates
					data[0][i][1] = 4
				m = []

		elif new_direction[i] == [5]:
			new_x = data[0][i][0][0] + 1
			new_y = data[0][i][0][1] - 1
			if new_y < row and new_y >= 0 and new_x < column and new_x >= 0:
				new_coordinates = (new_x, new_y)
				dont_go = data[0][:]
				for coordinates in dont_go:
					m.append(coordinates[0])
				if new_coordinates not in m:
					data[0][i][0] = new_coordinates
					data[0][i][1] = 5
				m = []

		elif new_direction[i] == [6]:
			new_x = data[0][i][0][0]+ 1
			new_y = data[0][i][0][1]
			if new_y < row and new_y >= 0 and new_x < column and new_x >= 0:
				new_coordinates = (new_x, new_y)
				dont_go = data[0][:]
				for coordinates in dont_go:
					m.append(coordinates[0])
				if new_coordinates not in m:
					data[0][i][0] = new_coordinates
					data[0][i][1] = 6
				m = []

		elif new_direction[i] == [7]:
			new_x = data[0][i][0][0]+ 1
			new_y = data[0][i][0][1] + 1
			if new_y < row and new_y >= 0 and new_x < column and new_x >= 0:
				new_coordinates = (new_x, new_y)
				dont_go = data[0][:]
				for coordinates in dont_go:
					m.append(coordinates[0])
				if new_coordinates not in m:
					data[0][i][0] = new_coordinates
					data[0][i][1] = 7
				m = []

	return data
