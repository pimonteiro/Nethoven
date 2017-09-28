def teste(note):
	e = 0
	x = 0
	for i in range(0, len(note)):
		x = 2**e + x
		e += 1
		print(x)

teste([1,1,1,1])
