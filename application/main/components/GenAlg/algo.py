import pandas as pd
import numpy as np
import random
import copy
from application.main.components.GenAlg.town import *


class Mutation:
    def __init__(self, ff: object, initPop: object, numFacilities: int):
        self.ff = ff
        self.pop = initPop
        self.mutation_rate = 0.2
        self.crossover_rate = 0.5
        self.numBest = 5
        self.tries = numFacilities
        
    def findDifferentValue(self) -> [int]:
        probList = list()
        for i in range(self.numBest):
            p = 1 - self.ff.fitnessValues[i]/sum(self.ff.fitnessValues[:self.numBest])
            probList.append(p)
        return probList
        
    def pickBest(self) -> None:
        self.bestIndividuals = list()
        ps = self.findDifferentValue()
        
        for _ in range(self.numBest):
            randomNum = random.random()
            counter = 0
            for i in range(len(ps)):
                counter += ps[i]
                if counter > randomNum:
                    self.bestIndividuals.append(copy.deepcopy(self.pop.population[i]))
                    break

    def randomPicker(self) -> [int]:
        randomPickedPop = list()
        
        for i in range(self.pop.population_size - (self.numBest * 2)):
            idx = random.randint(0, self.pop.population_size-1)
            randomPickedPop.append(copy.deepcopy(self.pop.population[idx]))
        return randomPickedPop
    
    def checkFacility(self, chromosome):
        reward1 = REWARD
        for gen in chromosome:
            if gen > 15 and gen != 1:
                reward1 -= 0.015
        if reward1 < 0:
            reward1 = 0
        
        return round(abs(reward1),2)
    
    def mutationClassic(self, chromosome: [int]) -> [int]:
        midPointsTog = list()
        for num in range(self.tries):
            i = random.randint(RANGE, len(chromosome)-RANGE-1)
            j = random.randint(RANGE, len(chromosome[i])-RANGE-1)
            midPointsTog.append([i,j])
            for k in range(RANGE):
                chromosome[i-k][j-RANGE:j+RANGE] += self.checkFacility(chromosome[i-k][j-RANGE:j+RANGE])

            for k in range(1,RANGE):
                chromosome[i+k][j-RANGE:j+RANGE] += self.checkFacility(chromosome[i+k][j-RANGE:j+RANGE])
                
        self.ff.midPoints.append(midPointsTog)
        return chromosome

    def selection(self, randomPickedPop: [int]) -> None:
        self.ff.resetEssentials()
        numbers = [i for i in range(len(randomPickedPop))]
        
        for i in range(0,len(randomPickedPop)):
            if random.random() <= self.mutation_rate:
                randomPickedPop[i] = self.mutationClassic(randomPickedPop[i])
            else:
                self.ff.midPoints.append([0])
            self.pop.population.append(copy.deepcopy(randomPickedPop[i]))
        

        for i in range(len(self.bestIndividuals)):
            self.pop.population.append(copy.deepcopy(self.bestIndividuals[i]))

        self.ff.fitness_function()
        
    def mainLoop(self) -> None:
        self.pickBest()
        randomPickedPop = self.randomPicker()
        
        for i in range(len(self.bestIndividuals)):
            randomPickedPop.append(copy.deepcopy(self.bestIndividuals[i]))
            
        random.shuffle(randomPickedPop)
        self.selection(randomPickedPop)

class Population:
    def __init__(self):
        self.population = list()
        self.population_size = 1000
        
    def generate_population(self, city):
        for i in range(self.population_size):
            self.population.append(copy.deepcopy(city))


def create_facility(toSelect: str) -> [[float]]:
    # df = pd.read_csv("kosice_radius_2.csv")
    df = pd.read_csv("./models/kosice_radius_2.csv")
    
    df = df[df["aminity"] == toSelect]

    
    df['lat'] = df['lat'].astype(float)
    df['lon'] = df['lon'].astype(float)
    df['lat_calc'] = df['lat'] - df['lat'].min()
    df['lon_calc'] = df['lon'] - df['lon'].min()

    df['lon_calc'] = df['lon_calc'].apply(lambda x : round(x,8))
    df['lat_calc'] = df['lat_calc'].apply(lambda x : round(x,8))

    df['lon_calc'] = df['lon_calc'] * 1000
    df['lat_calc'] = df['lat_calc'] * 1000
    
    #rows, cols = int(df['lon_calc'].max()), int(df['lat_calc'].max())
    rows, cols = 91, 52
    print(f"rows - {rows}, cols- {cols}")

    # create a (5,5) array of zeros
    arr = np.zeros((cols,rows))

    latMax = int(df['lat_calc'].max())
    lonMax = int(df['lon_calc'].max())
    for index, row in df.iterrows():
        lat = int(row['lat_calc']) - 1
        lon = int(row['lon_calc']) - 1
        for i in range(max(0, lon - RANGE), min(lonMax-1, lon + RANGE)):
            for j in range(max(0, lat - RANGE), min(latMax-1, lat + RANGE)):
                arr[j][i] += 0.5
        arr[lat-1][lon-1] = 1
    arr = np.flipud(arr)
    return arr, df


class FitnessFunction:
    def __init__(self, pop):
        self.reward = 0.5
        self.pop = pop
        self.fitnessValues = list() 
        self.midPoints = list()
            
    def fitness_function(self):
        for city in self.pop.population:
            self.fitnessValues.append(np.sum(city))
            self.midPoints.append([0])
        self.insertion_sort()
    
    def insertion_sort(self) -> None:
        for i in range(1, len(self.fitnessValues)):
     
            keyFitness = copy.deepcopy(self.fitnessValues[i])
            keyPopulation = copy.deepcopy(self.pop.population[i])
            keyMidPoint = copy.deepcopy(self.midPoints[i])
            j = i-1
            
            while j >= 0 and keyFitness > self.fitnessValues[j]:
                self.fitnessValues[j + 1] = self.fitnessValues[j]
                self.pop.population[j + 1] = self.pop.population[j]
                self.midPoints[j + 1] = self.midPoints[j]
                j -= 1
                
            self.fitnessValues[j + 1] = keyFitness
            self.pop.population[j + 1] = keyPopulation
            self.midPoints[j + 1] = keyMidPoint
        
    def resetEssentials(self) -> None:
        self.fitnessValues = list()
        self.pop.population = list()
        self.midPoints = list()


def make_result(toVisual):
    newOne = toVisual[0] + toVisual[1]
    
    for i in range(2,len(toVisual)):
        newOne += toVisual[i]    
    return newOne
        

def request_func(toSelect: [str], numFacilities: [int], radius: int):
    global RANGE
    global REWARD
    
    REWARD = 3
    if len(toSelect) == 1:
        REWARD = 2
    RANGE = radius
    
    
    toVisual = list()
    midPoints = list()
    for i in range(len(toSelect)):
        arr, selected_df = create_facility(toSelect[i])

        pop = Population()   
        pop.generate_population(arr)
            
        ff = FitnessFunction(pop)
        ff.fitness_function()
        
        mut = Mutation(ff, pop, numFacilities[i])
        mut.mainLoop()

        toVisual.append(copy.deepcopy(pop.population[0]))
        midPoints.append(copy.deepcopy(ff.midPoints[0]))
        print(ff.fitnessValues[:5])
    
    if len(toVisual) == 1:
        # sns.heatmap(toVisual[0])
        return toVisual, midPoints
    else:
        toVisual1 = make_result(toVisual)
        # sns.heatmap(toVisual1)
        return toVisual1, midPoints
