#!/usr/bin/env python
# coding: utf-8

# In[10]:


import csv
from collections import defaultdict

# Defining a class called Apriori for association rule mining
class Apriori(object):
    def __init__(self, min_sup, min_conf):
        self.min_sup = min_sup  # Minimum support threshold
        self.min_conf = min_conf  # Minimum confidence threshold
    
    # Method to scan the dataset and generate frequent itemsets
    def scanD(self):
        records = []
        headers = []
        
        # Reading the dataset from the CSV file
        file = open("Play_Tennis_Data_Set.csv")
        spamreader = csv.reader(file, delimiter=',')
            
        for line in spamreader:
            row_items = []
            for item in line:
                row_items.append(item)
            records.append(row_items)

        #Extracting headers and records from the dataset
        headers = records[0]
        records = records[1:]

        raw_records = []
        for record in records:
            a = set([(i, j) for i, j in zip(headers, record)])
            raw_records.append(a)
            self.total_records = len(records)  #Total number of records

        items = set()
        for line in raw_records:
            for item in line:
                items.add(frozenset([item]))
                
        total_count = defaultdict(int)  #Dictionary to store itemset counts
        self.items = items  #Set of unique items in the dataset
        frequency = {}  #Dictionary to store frequent itemsets

        # Generating the 1-term frequent set
        curr_frequency = self.minSupportLevel(raw_records, self.min_sup, items, total_count)
        k = 1
        while curr_frequency != set():
            frequency[k] = curr_frequency
            k = k + 1
            
            updated_itemset = []
            for a in curr_frequency:
                for b in curr_frequency:
                    union = a.union(b)
                    if len(union) == k:
                        updated_itemset.append(union)
            
            updated_itemset = set(updated_itemset)
            curr_frequency = self.minSupportLevel(raw_records, self.min_sup, updated_itemset, total_count)
        self.total_count = total_count  #Storing total counts of each itemset
        self.frequency = frequency  #Storing frequent itemsets of each length

        return total_count, frequency

    #Method to calculate the support of an itemset
    def minSupportLevel(self, records, min_sup, items, frequency):
        item_set = defaultdict(int)  #Dictionary to store itemset counts
        lst = [1]
        
        for item in items:
            for record in records:
                if all(i in record for i in item):
                    frequency[item] += sum(lst)  #Incrementing the itemset count
            for record in records:
                if all(i in record for i in item):
                    item_set[item] += sum(lst)  #Incrementing the itemset count

        records_length = len(records)
        upd_items = set()
        for item, count in item_set.items():
            count1 = float(count)
            if count1 / records_length >= min_sup:
                upd_items.add(item)
        return upd_items  #Returning the updated frequent itemsets

    #Method to generate association rules given a right-hand side (rhs)
    def generateRules(self, rhs):
        rules = {}  # Dictionary to store generated rules
        for k, v in self.frequency.items():
            for item in v:
                if all(i in item for i in rhs):
                    if len(item) > 1:
                        item_supp = self.getSupport(item)
                        item = item - rhs
                        if item_supp / self.getSupport(item) >= self.min_conf:
                            rules[item] = (item_supp, item_supp / self.getSupport(item))
        return rules

    #Method to calculate the support of an itemset
    def getSupport(self, item):
        item_count = self.total_count[item]
        record_length = self.total_records
        supp_count = item_count / self.total_records
        return supp_count
    
    if __name__ == '__main__':
    
        def defaultdict(type):
            class main(dict):
                def __getitem__(self, k):
                    if k not in self:
                        dict.__setitem__(self, k, type())
                    return dict.__getitem__(self, k)
            return main()
    
    # Prompting the user to enter minimum support and minimum confidence
    min_sup = float(input("Please enter the minimum support: "))
    min_conf = float(input("Please enter the minimum confidence: "))
    

    apriori = Apriori(min_sup, min_conf)
   
    frequency, items_count = apriori.scanD()
    
    #Generating an output file named "Rules.txt" and writing results to it
    with open("Rules.txt", "w") as output:
        output.write("1. User Input: \n\n")
        output.write("Support = " + str(min_sup) + "\n")
        output.write("Confidence = " + str(min_conf) +"\n\n")
        output.write("2. Rules: \n\n")

        i = 1
        # Writing the generated rules to the output file and printing them
        for rhs in apriori.items:
            rules = apriori.generateRules(rhs)
            for k, v in rules.items():
                rhs_list = list(rhs)[0]
                k_list = list(k)[0]
                output.write("Rule#{}:".format(i))
                output.write("{{{}={}}}".format(k_list[0], k_list[1]))
                output.write(" => ")
                output.write("{{{}={}}} \n".format(rhs_list[0], rhs_list[1]))
                output.write('(Support=%.2f, ' % v[0])
                output.write('Confidence=%.2f) \n' % v[1])
                output.write("\n")

                # Printing the rule to the console
#                 print("Rule#{}:".format(i))
#                 print("{{{}={}}}".format(k_list[0], k_list[1]), end=" ")
#                 print("=>", end=" ")
#                 print("{{{}={}}}".format(rhs_list[0], rhs_list[1]))
#                 print('(Support=%.2f, Confidence=%.2f)\n' % (v[0], v[1]))

                i = i + 1

    output.close()  # Closing the output file


# In[ ]:




