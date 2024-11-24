import prettytable
from classtime import ClassTime
from genetic import GA


# print data
def PrintData(schedule):
    column_lbl = ['"Schedule"', '"8-10"', '"10-12"', '"12-14"', '"14-16"', '"16-18"', '"18-20"']
    Days = ['SHANBEH', 'YEK SHANBEH', 'DO SHANBEH', 'SEH SHANBEH', 'CHAHAR SHANBEH']
    row_lbl = [[Days[i], '', '', '', '', '', ''] for i in range(5)]
    table = prettytable.PrettyTable(column_lbl, hrules=prettytable.ALL)
    count = 0
    for s in schedule:
        weekDay = s.weekDay
        time = s.time
        text = ('"PROFESSOR": {} \n COURSE: {} \n CLASS: {} '.format(s.Professor_ID, s.Course_ID, s.Class_ID))
        count += 1
        # print('Week:{}, Time:{},  Text{}'.format(s.weekDay, s.time, text))

        row_lbl[weekDay - 1][time] = text

    for row in row_lbl:
        table.add_row(row)

    print(table)


if __name__ == '__main__':

    # Save Data of ClassTime in ClassTimeDat
    ClassTimeData = []

    # Write from Data file
    f = open("Data.txt")
    f1 = f.readlines()
    for Input_Data in f1:
        Input_Data = str(Input_Data)
        Co_ID, Pro_ID = Input_Data.split(' ')
        Co_ID = int(Co_ID)
        Pro_ID = int(Pro_ID)
        ClassTimeData.append(ClassTime(Co_ID, Pro_ID))

    GA_Output = GA(population_size=50, mutation_range=0.4, BCI=10, maximum_iterate=500)
    Evolve_output = GA_Output.Evolution(ClassTimeData)
    # print('LEN FOR TABLE\t', len(Evolve_output))

    PrintData(Evolve_output)
    # Result = []
    # for x in Evolve_output:
    #     Result.append(x)
    # PrintData(Result)
