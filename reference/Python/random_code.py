# Python Notes and Demo's


# function's . . . lowercase with underscores
def some_function():
	return;


# Age calculator
name = input("Name: ")

while True:
	birth_year = input("Birth Year")
	try:
		birth_year = int(birth_year)
	except ValueError:
		continue
	else:
		break
		
current_year = 2017
current_age = current_year - birth_year
turn_25 = (25 - current_age) + current_year
turn_50 = (50 - current_age) + current_year
turn_75 = (75 - current_age) + current_year
turn_100 = (100 - current_age) + current_year

if turn_25 > current_year:
	print("You'll turn 25 in the year {}, {}".format(turn_25, name))
if turn_50 > current_year:
	print("You'll turn 50 in the year {}, {}".format(turn_50, name))
if turn_75 > current_year:
	print("You'll turn 75 in the year {}, {}".format(turn_75, name))
if turn_100 > current_year:
	print("You'll turn 100 in the year {}, {}".format(turn_100, name))
