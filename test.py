# Test Read Data
f = open("Data.txt")
f1 = f.readlines()
for Input_Data in f1:
    Input_Data = str(Input_Data)
    Co_ID, Pro_ID = Input_Data.split(' ')
    print(Co_ID, Pro_ID)

