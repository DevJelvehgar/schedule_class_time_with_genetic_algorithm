import copy
import numpy as np


# Genetic Algorithm


class GA:

    def __init__(self, population_size=35, mutation_range=0.4, BCI=5, maximum_iterate=150):

        # list for population
        self.population = []
        # population size
        self.population_size = population_size
        # mutation range for mutate in population
        self.mutation_range = mutation_range
        # Best Conflict Index
        self.BCI = BCI
        # maximum iteration number
        self.maximum_iterate = maximum_iterate

    def RndFunc(self, s):
        # print('hello1')
        if s.Professor_ID == 1202:
            # print('helooooooooooooooooo')
            s.weekDay = np.random.randint(1, 4)
        elif s.Professor_ID == 1203:
            # print('heloooooooooooooooooo')
            s.weekDay = np.random.randint(1, 5)
        elif s.Professor_ID == 1204:
            # print('heloooooooooooooooooo')
            s.weekDay = np.random.randint(2, 6)
        elif s.Professor_ID == 1205:
            # print('hellooooooooooooooooooooooooo')
            s.weekDay = np.random.randint(1, 6)
        # print('hello2')
        s.Class_ID = np.random.randint(1, 5)
        s.time = np.random.randint(1, 7)
        return s

    def CreatePopulation(self, ClassTimeData):
        # population size = 50
        # count = 0

        # print("LEN\t",len(ClassTimeData))
        for i in range(self.population_size):
            existence = []

            # len of ClassTimeData = 16

            for s in ClassTimeData:
                # s = np.array(s)
                # print('len s\t', s.shape)
                news = self.RndFunc(s)

                # copy s data into existence with deepcopy
                existence.append(copy.deepcopy(news))
                # count += 1
            # population has 50 rows and in each row has 16 column ----> list[50 * 16] = 1100 items
            self.population.append(existence)
        # print('LEN OF POPULATION\t', len(self.population))

    # 10 of best populations are BCI_population
    def Mutation1(self, BCI_population):
        # print("LEN OF BCI POPULATIONS", len(BCI_population))
        # RoomRange is Number of Classroom

        # Rnd_BCI is Between [0 , 10)
        Rnd_BCI = np.random.randint(0, self.BCI, 1)[0]
        # print('Rnd_BCI\t', Rnd_BCI)

        rnd_value = copy.deepcopy(BCI_population[Rnd_BCI])
        # print('EP:\t', len(rnd_value))
        for value in rnd_value:
            # Random number between (0,1)
            position = np.random.randint(0, 2, 1)[0]

            # random number between (0 : 1)
            operation = np.random.rand()
            # position 0 = Room

            if position == 0:
                value.Class_ID = self.Mutation2(value.Class_ID, operation, 4)
            # position 2 = time
            if position == 1:
                value.time = self.Mutation2(value.time, operation, 6)
        # POPULATION AFTER ITERATIONS
        return rnd_value

    def Mutation2(self, InputValue, operate, ValueRange):

        # 0.4 is mutate range
        if operate > 0.4:
            if InputValue < ValueRange:
                InputValue += 1
            else:
                InputValue -= 1
        else:
            # time = '8-10' or days = ' shanbeh' or room = 1
            if InputValue - 1 > 0:
                InputValue -= 1
            else:
                InputValue += 1
        # return InputValue after Mutation2
        return InputValue

    def Crossover(self, BCI_population):
        # self.BCI = 10
        cross1 = np.random.randint(0, self.BCI, 1)[0]
        cross2 = np.random.randint(0, self.BCI, 1)[0]
        # position = [ 0 , 1)
        position = np.random.randint(0, 2, 1)[0]

        operation1 = copy.deepcopy(BCI_population[cross1])
        operation2 = copy.deepcopy(BCI_population[cross2])

        for op1, op2 in zip(operation1, operation2):
            if position == 0:
                op1.time = op2.time
            if position == 1:
                op1.Class_ID = op2.Class_ID
        # population after Crossover you can return operation1 or operation2
        return operation1

    def Fitness(self, population, BCI):
        conflicts = []
        # n = 16 ( number of column in population )
        n = len(population[0])

        for p in population:
            conflict = 0
            for i in range(0, n - 1):
                for j in range(i + 1, n):
                    # check course for one class in same time
                    if p[i].Class_ID == p[j].Class_ID and p[i].weekDay == p[j].weekDay and p[i].time == p[j].time:
                        conflict += 1
                        # print('heloo\t', conflicts)
                    # check course for one teacher in same time
                    if p[i].Professor_ID == p[j].Professor_ID and p[i].weekDay == p[j].weekDay \
                            and p[i].time == p[j].time:
                        conflict += 1
                        # print('heloo\t', conflicts)
                    # check same course for one class in same day
                    if p[i].Class_ID == p[j].Class_ID and p[i].Course_ID == p[j].Course_ID \
                            and p[i].weekDay == p[j].weekDay:
                        conflict += 1
                        if p[i].Professor_ID != p[j].Professor_ID and p[i].Course_ID == p[j].Course_ID \
                                and p[i].weekDay == p[j].weekDay and p[i].time == p[j].time:
                            conflict += 1

                        # print('heloo\t', conflicts)
            conflicts.append(conflict)
            # print('conflict\t', conflicts)

        # sorted with arguments
        index = np.array(conflicts).argsort()
        # print('INDEX\t', index[ :BCI])
        # return best result and best index of 5 result
        return index[: BCI], conflicts[index[0]]

    def Evolution(self, ClassTimeData):

        BestClassTime = None

        # Create new population
        self.CreatePopulation(ClassTimeData)
        # maximum iteration is 500
        count = 0
        for i in range(self.maximum_iterate):
            count += 1
            # self.BCI = 10
            # print("LEN POPULATION1", len(self.population))
            BCI_Index, BestScore = self.Fitness(self.population, self.BCI)
            # print('BestScore :\t', BCI_Index)
            # print('Iterations: {} -----> Best conflicts is: {}'.format(i + 1, BestScore))
            # BestScore is Result of Best Conflicts
            if BestScore == 0:
                # print('bye\t', count)
                BestClassTime = self.population[BCI_Index[0]]
                break

            # BCI_Index = 10
            # population is list [ 50 * 22 ]
            # NewPopulation is list[ 10 * 22 ]
            # We want start with 10 of BCI_Index then NewPopulation is [ 10 * 22 ]
            NewPopulation = [self.population[index] for index in BCI_Index]
            # print("BCI_INDEX:\t", len(BCI_Index))
            # print("new population\t", NewPopulation)
            # NewPopulation = np.array(NewPopulation)
            # print("NewPopulation.shape", NewPopulation.shape)
            # print("LEN POPULATION2", self.population)
            # self.population = np.array(self.population)
            # print('self.population.shape', self.population.shape)

            # Add mutated of winners
            # len(NewPopulation) = 10 & len(self.population_size) = 50
            while len(NewPopulation) < self.population_size:
                # random between (0 , 1)
                # mutation range = 0.4
                if np.random.rand() < self.mutation_range:
                    # Do Mutation
                    NewPop = self.Mutation1(NewPopulation)
                else:
                    # Do Crossover
                    NewPop = self.Crossover(NewPopulation)

                NewPopulation.append(NewPop)
            # print('len(NewPopulation)', len(NewPopulation))
            self.population = NewPopulation

        return BestClassTime
