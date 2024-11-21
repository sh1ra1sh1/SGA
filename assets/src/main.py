import random
import numpy as np
import matplotlib.pyplot as plt

from individual import Individual
from utils import coin, rastrigin_function



# パラメータ設定
MAX_GENERATION = 200
POPULATION_SIZE = 20
assert POPULATION_SIZE % 2 == 0
CHROM_LENGTH = 20
DIMENSION = 2
assert CHROM_LENGTH % DIMENSION == 0
ONE_DIMENSION_LENGTH = int(CHROM_LENGTH / DIMENSION)
PROBABILITY_MUTATION = 0.05
FITNESS_MAX = 1.0e33
FITNESS_MIN = -1.0e33
GRAYCODE = True

# デコード時の表現体のとりうる範囲
# ビット長で分割する
X_MAX = 5.12
X_MIN = -5.12

# 評価を最大化するなら MAX_OR_MIN = 1
# 評価を最小化するなら MAX_OR_MIN = -1
MAX_OR_MIN = -1

best_local=Individual(CHROM_LENGTH)
best_global=Individual(CHROM_LENGTH)



# 個体の初期生成
def init_individual():
	ind = Individual(chrom_length=CHROM_LENGTH)
	return ind

# 集団の初期生成
def init_population():
	population = []
	for i in range(0, POPULATION_SIZE):
		ind = init_individual()
		ind.set_value(decode(ind))
		ind.set_fitness(evaluation(ind))
		population.insert(i, ind)
	return population

# 最も優秀な個体を取得
def get_best(population):
	for ind in population:
		# 現世代での最優秀個体について
		if MAX_OR_MIN * ind.get_fitness() > MAX_OR_MIN * best_local.get_fitness():
			best_local.set_value(ind.get_value())
			best_local.set_chromosome(ind.get_chromosome())
			best_local.set_fitness(ind.get_fitness())
		# 全世代での最優秀個体について
		if MAX_OR_MIN * best_local.get_fitness() > MAX_OR_MIN * best_global.get_fitness():
			best_global.set_value(best_local.get_value())
			best_global.set_chromosome(best_local.get_chromosome())
			best_global.set_fitness(best_local.get_fitness())

# 通常二進数からグレイコード二進数の変換: list
def gray_to_binary(gray):
    binary = np.zeros_like(gray)
    binary[0] = gray[0]  # 最上位ビットはそのままコピー
    for i in range(1, ONE_DIMENSION_LENGTH):
        binary[i] = binary[i - 1] ^ gray[i]  # 直前のビットとXOR
    return binary

# 2 -> 10
def normal_binary(binary):
	value = 0
	for j in range(0, ONE_DIMENSION_LENGTH):
		value += ( pow(2, j) ) * ( binary[ONE_DIMENSION_LENGTH - j - 1] )
	return value

# 染色体から表現体への変換
def decode(ind):
	split_chromosome = np.array(ind.get_chromosome()).reshape(DIMENSION, ONE_DIMENSION_LENGTH)
	n_value = []
	for i in range(0, DIMENSION):
		if GRAYCODE == True:
			value = normal_binary(gray_to_binary(split_chromosome[i]))
		else:
			value = normal_binary(split_chromosome[i])
		# 所望の範囲に値を収める
		abs_scale = abs(X_MAX) + abs(X_MIN)
		scaled_value = abs_scale / pow(2, ONE_DIMENSION_LENGTH) * value + X_MIN
		n_value.insert(i, scaled_value)
	return n_value

# 個体の評価
def evaluation(ind):
	value = ind.get_value()
	fx = rastrigin_function(value)
	return fx

# 選択
# 何のひねりもなく個体を二つ選択する
def selection(population):
	selected = []
	for i in range(0, POPULATION_SIZE):
		if i % 2 == 0:
			continue
		# 異なる二つの乱数を引くまでループ
		while(True):
			a = random.randint(0, POPULATION_SIZE - 1)
			b = random.randint(0, POPULATION_SIZE - 1)
			if a != b:
				break
		selected.insert(i, population[a])
		selected.insert(i + 1, population[b])
	return selected

# 交叉
# 選択で選んだ親を直接書き換える
def crossover(parent_1, parent_2):
	child_1 = init_individual()
	child_2 = init_individual()
	site = random.randint(0, CHROM_LENGTH - 1)
	for i in range(0, CHROM_LENGTH):
		p1_chromosome = parent_1.get_ind_chromosome(i)
		p2_chromosome = parent_2.get_ind_chromosome(i)
		if i <= site or site==0:
			child_1.set_pos_chromosome(p1_chromosome,i)
			child_2.set_pos_chromosome(p2_chromosome,i)
		else:
			child_1.set_pos_chromosome(p2_chromosome,i)
			child_2.set_pos_chromosome(p1_chromosome,i)

	parent_1.set_chromosome(child_1.get_chromosome())
	parent_2.set_chromosome(child_2.get_chromosome())

# 突然変異
def mutation(population):
	for ind in population:
		for i in range(0, CHROM_LENGTH):
			if coin(PROBABILITY_MUTATION) == 0:
				if ind.get_ind_chromosome(i) == 1:
					ind.set_pos_chromosome(0, i)
				else:
					ind.set_pos_chromosome(1, i)

# 保存していた優秀個体に置き換える
def elite(population):
    if MAX_OR_MIN*best_local.get_fitness() > MAX_OR_MIN*evaluation(population[0]):
        population[0].set_fitness(best_local.get_fitness())
        population[0].set_value(best_local.get_value())
        population[0].set_chromosome(best_local.get_chromosome())

# 学習過程をプロット
def plot_history(history):
    plt.figure()
    plt.plot(range(0, MAX_GENERATION + 1), history, label='Fitness')
    plt.yscale('log')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('SGA Fitness over Generations')
    plt.legend()
    gray = 'notGRAY'
    if GRAYCODE == True:
        gray = 'GRAY'
    plt.savefig(f'SGA_{DIMENSION}D_{ONE_DIMENSION_LENGTH}L_{gray}')
    plt.show()



def main():
	generation = 0
	population = init_population()
	history = []
	if MAX_OR_MIN==-1:
		best_global.set_fitness(FITNESS_MAX)
		best_local.set_fitness(FITNESS_MAX)
	else:
		best_global.set_fitness(FITNESS_MIN)
		best_local.set_fitness(FITNESS_MIN)

    # メインループ
	while(True):
		# print(f'=== generation: {generation} ===')
		# print(f'best_value: {best_global.get_value()}')
		# print(f'best_fitness: {best_global.get_fitness()}')
		# print(f'best_chromosome: {best_global.get_chromosome()}')
		# print('\n')
		# 優秀個体の保存
		get_best(population)

		# 選択
		selected = selection(population)

		# 交叉
		# ここでは交叉範囲が全体にかかっているので注意
		for i in range(0, POPULATION_SIZE - 1):
			if i % 2 == 0:
				continue
			crossover(selected[i], selected[i + 1])

		# 突然変異
		mutation(population)

		# 評価
		for ind in population:
			ind.set_value(decode(ind))
			ind.set_fitness(evaluation(ind))

        # 保存していた優秀個体に置き換える
		elite(population)

		if generation == MAX_GENERATION:
			print('The main loop has just finished.')
			break
		history.insert(generation, best_global.get_fitness())
		generation += 1

	print(f'value: {best_global.get_value()}')
	print(f'fitness: {best_global.get_fitness()}')
	best_global.print_chromosome()
	history.insert(generation, best_global.get_fitness())
	plot_history(history)



if __name__ == '__main__':
	main()

