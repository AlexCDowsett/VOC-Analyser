from datahandler import load
def main():
	import cProfile
	import pstats

	with cProfile.Profile() as pr:
		ml =MachineLearning(load())

	stats = pstats.Stats(pr)
	stats.sort_stats(pstats.SortKey.TIME)
	#stats.print_stats()

class MachineLearning():
	def __init__(self, data):
		self.data = data

	def preprocessing(self, a, b):
		pass


	def train(self):
		pass







if __name__ == "__main__":
	main()

