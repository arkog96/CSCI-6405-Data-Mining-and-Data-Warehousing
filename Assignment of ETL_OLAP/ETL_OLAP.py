#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv

with open('Car_Sales_Data_Set.csv', 'r', encoding='utf-8-sig') as input_file:
    reader = csv.reader(input_file)
    data = list(reader)

#Extract headers and rows
headers = data[0]
data = data[1:]

#Sort the records based on the first column (Country)
first_sort = sorted(data, key=lambda column: (column[0]))

# Add headers back to sorted data
first_sort.insert(0, headers)

# Write the first sorted data to a new CSV file
with open('Car_Sales_Data_Set_First_Sorting.csv', 'w', newline='') as first_sorted_file:
    writer = csv.writer(first_sorted_file)
    writer.writerows(first_sort)
    
# Applying the same process to sort the csv file based on first two columns (Country & Time_Year)
second_sort = sorted(data, key=lambda column: (column[0], column[1]))
second_sort.insert(0, headers)

# Write the second sorted data to a new CSV file
with open('Car_Sales_Data_Set_Second_Sorting.csv', 'w', newline='') as second_sorted_file:
    writer = csv.writer(second_sorted_file)
    writer.writerows(second_sort)
    
# # Applying the same process to sort the csv file based on first three columns (Country, Time_Year & Time_Quarter)
third_sort = sorted(data, key=lambda column: (column[0], column[1], column[2]))
third_sort.insert(0, headers)

# Write the third sorted data to a new CSV file
with open('Car_Sales_Data_Set_Third_Sorting.csv', 'w', newline='') as third_sorted_file:
    writer = csv.writer(third_sorted_file)
    writer.writerows(third_sort)

    
#Function to return a list of unique items from a specific column in records
def unique_items(records, column_index):
    return list(set([i[column_index] for i in records]))

#Function to calculate the total of a specific column in records
def calculate_total(records, column_index):
    return sum([int(column[column_index]) for column in records])

#Function to print a header and corresponding data with proper formatting
def print_data(header, data):
    print(f"{header}\t\t{data}")

#ETL operation to print the total of a specific column in records
def ETL_operation_1(records, column_index):
    print_data(headers[column_index], calculate_total(records, column_index))

#ETL operation to print a summary of totals based on unique items in a header column
def ETL_operation_2(records, header_index, header):
    print_data(header, headers[4])
    item_totals = {}
    for item in unique_items(records, header_index):
        total = sum(int(column[4]) for column in records if column[header_index] == item)
        item_totals[item] = total
        print_data(item, total)

#ETL operation to print a cross-summary of totals based on unique combinations of items from two header columns
def ETL_operation_3(records, header_index_1, header_index_2, header_1, header_2):
    header = f"{headers[header_index_2]}\t\t{headers[header_index_1]}"
    print_data(header, headers[4])

    for item_2 in unique_items(records, header_index_2):
        for item_1 in unique_items(records, header_index_1):
            total = sum(
                int(column[4])
                for column in records
                if column[header_index_1] == item_1 and column[header_index_2] == item_2
            )
            item_label = f"{item_2}\t\t{item_1}"
            print_data(item_label, total)


print("There is the list of 12 tuples:")
print("1. ()\n"
      "2. (Country)\n"
      "3. (Time_Year)\n"
      "4. (Time_Quarter - Time_Year)\n" 
      "5. (Car_Manufacturer)\n" 
      "6. (Country, Time_Year)\n" 
      "7. (Country, Car_Manufacturer)\n"
      "8. (Time_Year, Car_Manufacturer)\n")
num = int(input("Select an option from the list and type a number (1-8): "))
print('')

if num == 1:
    ETL_operation_1(data, headers.index(headers[4]))
elif num == 2:
    ETL_operation_2(data, 0, headers[0])
elif num == 3:
    ETL_operation_2(data, 1, headers[1])
elif num == 4:
    ETL_operation_3(data, 2, 1, headers[2], headers[1])
elif num == 5:
    ETL_operation_2(data, 3, headers[3])
elif num == 6:
    ETL_operation_3(data, 1, 0, headers[1], headers[0])
elif num == 7:
    ETL_operation_3(data, 3, 0, headers[3], headers[0])
elif num == 8:
    ETL_operation_3(data, 1, 3, headers[1], headers[3])


# In[ ]:




