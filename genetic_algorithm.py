import math
from math import log2
import random

f = open("input.txt", "r")
g = open("evolution.txt", "w")
dim = int(f.readline())
a, b = [int(x) for x in f.readline().split()]
coef1, coef2, coef3, coef4 = [int(x) for x in f.readline().split()]
precision = int(f.readline())
crossover_prob = float(f.readline())
mutation_prob = float(f.readline())
no_of_steps = int(f.readline())
length = round(log2((b - a) * 10 ** precision))
max_f = -1000000

class Chromosome:
    def __init__(self) -> None:
        self.carray = (''.join(random.choice(['0', '1']) for i in range(length)))
        self.x = round(int(self.carray, base=2) * (b - a) / (2 ** length - 1) + a, precision)
        self.ff = f(self)

def __repr__(c):
    return (c.carray + "  x=" + str(c.x) + "  f=" + str(f(c)))

def f(c): # calculates the result of the quadratic function; equivalent to fitness function
    return (coef1 * c.x ** 3 + coef2 * c.x ** 2 + coef3 * c.x + coef4)

def calc_maxF(p): #returns the maximum value of a population
    f_array = [f(chr) for chr in p]
    return max(f_array)

def binary_search(arr, elem): #binary search for interval
    low = 0
    high = len(arr)
    while low < high:
        mid = math.floor((low + high) / 2)
        if arr[mid] == elem:
            return mid
        elif arr[mid] < elem and mid != low:
            low = mid
        elif arr[mid] > elem and mid != high:
            high = mid
        else:
            high = low = low + 1
    return low

def repeat(population): #function to generate new populations based on a given one; it returns the maximum value and the average performance of the population
    max_f = -1000000
    max_s = -1000000
    max_x = -1000000
    F = sum([f(chr) for chr in population])
    performance = [f(chr) / F for chr in population]
    avg_p1 = sum(performance)/len(performance) #average performance of the initial population

    intervals = [0]
    for i in range(dim - 1):
        intervals.append(intervals[i] + performance[i])
    intervals.append(1)

    best_chr = performance.index(max(performance))
    intermediate_population = [best_chr + 1]
    prop = []
    for i in range(1, dim):  # We select dim-1 chromosomes because we already selected one using elitism selection
        u = random.random()
        prop.append(u)
        chr = binary_search(intervals, u)
        intermediate_population.append(chr)

    new_population = []
    for i in range(dim):
        new_population.append(population[intermediate_population[i] - 1])

    participate = [] #list of selected chromosomes for crossover
    indexes = [] #indexes of the chromosomes; used later for updating the population
    for i in range(1, dim):
        u = random.random()
        if u < crossover_prob:
            participate.append(new_population[i])
            indexes.append(i)

    # Crossover
    ind = 0
    if len(participate) == 1 or len(participate) == 0:
        ind = len(participate) + 1 #we skip the crossover
    if len(participate) % 2 == 1 and ind == 0: #if the number of participants is odd, we start with the first three and then continue with pairs
        point = random.randint(0, length - 1)
        c1 = participate[0]
        c2 = participate[1]
        c3 = participate[2]
        aux = c1.carray[point:]
        c1.carray = c1.carray[:point] + c2.carray[point:]
        c2.carray = c2.carray[:point] + c3.carray[point:]
        c3.carray = c3.carray[:point] + aux
        participate[0] = c1
        participate[1] = c2
        participate[2] = c3
        ind = 3
    for i in range(ind, len(participate), 2):
        point = random.randint(0, length - 1)
        c1 = participate[i]
        c2 = participate[i + 1]
        aux = c1.carray[point:]
        c1.carray = c1.carray[:point] + c2.carray[point:]
        c2.carray = c2.carray[:point] + aux
        participate[i] = c1
        participate[i + 1] = c2

    for i in range(len(participate)):
        new_population[indexes[i]] = participate[i]  # update the chromosomes after crossover
    for i in range(dim):
        new_population[i].x = round(int(new_population[i].carray, base=2) * (b - a) / (2 ** length - 1) + a, precision) #update the data based on the carray
        new_population[i].ff = f(new_population[i])
    if calc_maxF(new_population) > max_f:
        max_f = calc_maxF(new_population) #update the max value after crossover
        for ch in new_population:
            if f(ch) == max_f:
                max_x = ch.x
    F = sum([f(chr) for chr in population])
    performance = [f(chr) / F for chr in new_population]
    avg_p2 = sum(performance)/len(performance) #average performance of the after-crossover population

    # Mutation
    selected_ind = []
    for i in range(1,dim):
        u = random.random()
        if u < mutation_prob:
            selected_ind.append(i + 1)
            p = random.randint(0, length - 1) #random position
            if p == 0:
                new_population[i].carray = str(int(not (new_population[i].carray[0]))) + new_population[i].carray[1:]
            elif p == length - 1:
                new_population[i].carray = new_population[i].carray[:(p)] + str(int(not (new_population[i].carray[p])))
            else:
                #we concatenate the first part before p, then the complement of the number on the position p, then the slice after p
                new_population[i].carray = new_population[i].carray[0:(p)] + str(int(not (new_population[i].carray[p]))) + new_population[i].carray[(p + 1):(length)]
    if calc_maxF(new_population) > max_f:
        max_f = calc_maxF(new_population)  # update the max value after crossover
        for ch in new_population:
            if f(ch) == max_f:
                max_x = ch.x
    F = sum([f(chr) for chr in population])
    performance = [f(chr) / F for chr in new_population]
    avg_p3 = sum(performance)/len(performance) #average performance of the after-mutation population
    avg_p = (avg_p1 + avg_p2 + avg_p3) / 3
    return max_f, avg_p, max_x

g.write("Initial Population: \n")
population = []
for i in range(dim):
    chr = Chromosome()
    population.append(chr)
for i in range(dim):
    if i<9:
        g.write(" " + str(i + 1) + ": " + __repr__(population[i]) + "\n")
    else:
        g.write(str(i + 1) + ": " + __repr__(population[i]) + "\n")
max_f = max(max_f, calc_maxF(population)) #max value of the initial population
F = sum([f(chr) for chr in population])
performance = [f(chr)/F for chr in population]

g.write("\nSelection probability: \n")
for i in range(dim):
    if i < 9:
        g.write("chromosome    " + str(i + 1) + " probability: " + str(performance[i]) + "\n")
    else:
        g.write("chromosome   " + str(i + 1) + " probability: " + str(performance[i]) + "\n")

g.write("\nSelection intervals: \n")
intervals = [0]
for i in range(dim-1):
    intervals.append(intervals[i] + performance[i])
    g.write("[" + str(intervals[i]) + " , " + str(intervals[i+1]) + ")\n")
g.write("[" + str(intervals[i+1]) + " , " + "1" + ")\n")
intervals.append(1)

g.write("Elitism selection: \n")
best_chr = performance.index(max(performance))
intermediate_population = [best_chr+1]
g.write("We select chromosome " + str(performance.index(max(performance)) +1) + "\n")

g.write("Proportional selection: \n")
prop = []
for i in range(1,dim): #We select dim-1 chromosomes because we already selected one using elitism selection
    u = random.random()
    prop.append(u)
    chr = binary_search(intervals, u)
    intermediate_population.append(chr)
    g.write("u=" + str(u) + " we select chromosome " + str(chr) + "\n")

g.write("After selection: \n")
new_population = []
for i in range(dim):
    if i<9:
        new_population.append(population[intermediate_population[i]-1])
        g.write(" " + str(i + 1) + ": " + __repr__(population[intermediate_population[i]-1]) + "\n")
    else:
        new_population.append(population[intermediate_population[i]-1])
        g.write(str(i + 1) + ": " + __repr__(population[intermediate_population[i]-1]) + "\n")

g.write("Crossover probability = " + str(crossover_prob) + "\n")
participate = []
indexes = []
for i in range(1,dim):
    u = random.random()
    if u < crossover_prob:
        participate.append(new_population[i])
        indexes.append(i)
        g.write(str(i+1) + " " + new_population[i].carray + " u=" + str(u) + " < " + str(crossover_prob) + " participates\n")
    else:
        g.write(str(i+1) + " " + new_population[i].carray + " u=" + str(u) + "\n")

#Crossover
ind = 0
if len(participate) == 1 or len(participate) == 0:
    ind = len(participate) + 1 #i did this in order to skip the for loop below
if len(participate) % 2 == 1 and ind == 0:
    point = random.randint(0, length - 1)
    g.write("Crossover between chromosomes " + str(indexes[0]+1) + " " + str(indexes[1]+1) + " " + str(indexes[2]+1) + "\n")
    c1 = participate[0]
    c2 = participate[1]
    c3 = participate[2]
    g.write(c1.carray + " " + c2.carray + " " + c3.carray + " point = " + str(point) +  "\n")
    aux = c1.carray[point:]
    c1.carray = c1.carray[:point] + c2.carray[point:]
    c2.carray = c2.carray[:point] + c3.carray[point:]
    c3.carray = c3.carray[:point] + aux
    g.write("Result: " + c1.carray + " " + c2.carray + " " + c3.carray + "\n")
    participate[0] = c1
    participate[1] = c2
    participate[2] = c3
    ind = 3
for i in range(ind, len(participate), 2):
    point = random.randint(0, length - 1)
    g.write("Crossover between chromosomes " + str(indexes[i]+1) + " " + str(indexes[i+1]+1) + "\n")
    c1 = participate[i]
    c2 = participate[i+1]
    g.write(c1.carray + " " + c2.carray + " point = " + str(point) + "\n")
    aux = c1.carray[point:]
    c1.carray = c1.carray[:point] + c2.carray[point:]
    c2.carray = c2.carray[:point] + aux
    g.write("Result: " + c1.carray + " " + c2.carray + "\n")
    participate[i] = c1
    participate[i+1] = c2

for i in range(len(participate)):
    new_population[indexes[i]] = participate[i]  #update the chromosomes after crossover

g.write("After crossover: \n")
for i in range(dim):
    if i<9:
        new_population[i].x = round(int(new_population[i].carray, base=2) * (b - a) / (2 ** length - 1) + a, precision)
        new_population[i].ff = f(new_population[i])
        g.write(" " + str(i + 1) + ": " + __repr__(new_population[i]) + "\n")
    else:
        new_population[i].x = round(int(new_population[i].carray, base=2) * (b - a) / (2 ** length - 1) + a, precision)
        new_population[i].ff = f(new_population[i])
        g.write(str(i + 1) + ": " + __repr__(new_population[i]) + "\n")

#Mutation
g.write("Mutation probability for each gene: " + str(mutation_prob) + "\n")
selected_ind = []
for i in range(1,dim):
    u = random.random()
    if u < mutation_prob:
        selected_ind.append(i+1)
        p = random.randint(0, length-1)
        if p == 0:
            new_population[i].carray =str(int(not(new_population[i].carray[0]))) + new_population[i].carray[1:]
        elif p == length-1:
            new_population[i].carray = new_population[i].carray[:(p)] + str(int(not(new_population[i].carray[p])))
        else:
            new_population[i].carray = new_population[i].carray[0:(p)] + str(int(not(new_population[i].carray[p]))) + new_population[i].carray[(p+1):(length)]

g.write("These chromosomes have been modified: ")
for i in range(len(selected_ind)):
    g.write(str(selected_ind[i]) + " ")
g.write("\n")

g.write("After mutation: \n")
for i in range(dim):
    if i<9:
        g.write(" " + str(i + 1) + ": " + __repr__(new_population[i]) + "\n")
    else:
        g.write(str(i + 1) + ": " + __repr__(new_population[i]) + "\n")

g.write("Maximum function evolution and average performance: \n")
for i in range(1, no_of_steps):
    max_f, avg_p, max_x = repeat(new_population)
    g.write(str(max_f) + "  " + str(avg_p)  + " x= " + str(max_x) + "\n")