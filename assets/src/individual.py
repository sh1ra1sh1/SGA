import random

# 個体を管理するクラス
class Individual:

	# 初期化
	def __init__(self, chrom_length):
		self.value = 0			# 表現体
		self.fitness = 0		# 評価値
		self.chromosome = []	# 染色体
		for i in range(chrom_length):
			self.chromosome.insert(i, random.randint(0, 1))

	# 値の取得
	def get_value(self):
		return self.value
	def get_fitness(self):
		return self.fitness
	def get_chromosome(self):
		return self.chromosome
	def get_ind_chromosome(self, index):
		return self.chromosome[index]

	# ターミナル表示
	def print_chromosome(self):
		out = ''
		for i in range(0, len(self.chromosome)):
			out += str( self.get_ind_chromosome(i) )
		print(f'chromosome: {out}')

	# 値の設定
	def set_value(self, new_value):
		self.value = new_value
	def set_fitness(self, new_fitness):
		self.fitness = new_fitness
	def set_pos_chromosome(self, val, pos):
		self.chromosome[pos] = val
	def set_chromosome(self, new_chromosome):
		for i in range(0, len(self.chromosome)):
			self.chromosome[i] = new_chromosome[i]

