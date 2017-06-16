def read_data(file_path):
	with open(file_path) as f:
		lines = f.read().splitlines()
	return lines