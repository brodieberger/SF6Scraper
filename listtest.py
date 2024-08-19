battle_data = ['1817 MR', '1900 MR', '1823 MR', '1894 MR', '1869 MR', '1886 MR', '1860 MR', '1895 MR', '1868 MR', '1887 MR', '1886 MR', '1468 MR', '1885 MR', '1469 MR', '1615 MR', '1882 MR', '1618 MR', '1879 MR', '1908 MR', '1870 MR']

# Convert to integers
battle_data = [int(data.replace(' MR', '')) for data in battle_data]

name_data = ['TTV/SimplyEgo', 'Stingrays110', 'TTV/SimplyEgo', 'Stingrays110', 'Ramsey', 'Stingrays110', 'Ramsey', 'Stingrays110', 'Ramsey', 'Stingrays110', 'Stingrays110', 'DonnanDwarf', 'Stingrays110', 'DonnanDwarf', 'hello', 'Stingrays110', 'hello', 'Stingrays110', 'TheFatManatee', 'Stingrays110']

username = "Stingrays110"
data_amount= len(battle_data)

MRList = []
MRTotal = 0

print("\nMatch History: ")
for i in range(0, int(data_amount),2):
    if name_data[i] == username:
        #If the left name (i) matches user
        print(str(name_data[i]) + " (" + str(battle_data[i]) + "MR) VS " + str(name_data[i+1]) + "(" + str(battle_data[i+1]) + "MR)")
        MRList.append(battle_data[i])
    else:
        #If the right name (i+1) matches user
        print(str(name_data[i+1]) + " (" + str(battle_data[i+1]) + "MR) VS " + str(name_data[i]) + "(" + str(battle_data[i]) + "MR)")
        MRList.append(battle_data[i+1])
        
for item in MRList:
    MRTotal += item

print("\nAverage over the last 10 games: " + str(MRTotal / (data_amount/2)))