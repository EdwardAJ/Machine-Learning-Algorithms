import pandas as pd
import numpy as np

from tree_module import *
import math

class myID3:
    # EXAMPLES IS THE DATA!!!!
    def __init__(self, examples, target_attribute, attributes):
        
        # If all examples are in one class
        if (self.areAllValuesSame(examples[target_attribute])):
            self.tree_ = Tree(examples[target_attribute][0])
            return

        if (len(attributes) == 0):
            # Check for most values
            # data adalah nilai yang muncul terbanyak dalam suatu kelas (kelas adalah atribut / kolom)
            data = examples[target_attribute].value_counts().idxmax()
            self.tree_ = Tree(data)
            return

        # Use information gain to get best attr
        # this function just give best attr, just believe
        bestAttribute = self.getBestAttribute(examples, target_attribute, attributes)

        # Get unique values in the attribute
        # remove duplicates in the attribute
        uniqueValues = examples[bestAttribute].unique()

        # Assign new attributes
        # all attributes without the best attribute
        filteredAttributes = attributes
        filteredAttributes.remove(bestAttribute)

        # Create tree
        self.tree_ = Tree(bestAttribute)

        for value in uniqueValues:
            # Filter the example (example::where("attribute", bestAttribute)->where(target==value))
            filteredExamples = examples[examples[bestAttribute] == value].reset_index()

            # If filteredExamples empty
            if (filteredExamples.empty):
                # Assign with most common value...
                # data adalah nilai yang muncul terbanyak dalam suatu kelas (kelas adalah atribut / kolom)
                data = examples[target_attribute].value_counts().idxmax()
                self.tree_.add_child(data)
                self.tree_.add_name(value)
            else:
                # Recursion
                id3 = myID3(filteredExamples, target_attribute, filteredAttributes)
                self.tree_.add_child(id3.tree_)
                self.tree_.add_name(value)

        

    def getBestAttribute(self, examples, target_attribute, attributes):
        # Find the entropy of examples
        classEntropy = self.getEntropy(examples, target_attribute)

        # Assign initial value
        returnAttr = attributes[0]
        maxInformationGain = self.getInformationGain(examples, target_attribute, returnAttr, classEntropy)

        # For each attributes, check the information gain and find the maximum.
        for index in range(1, len(attributes)):
            informationGain = self.getInformationGain(examples, target_attribute, attributes[index], classEntropy)
            if (informationGain > maxInformationGain):
                maxInformationGain = informationGain
                returnAttr = attributes[index]

        # Return the best attribute
        return returnAttr

    def getInformationGain(self, examples, target_attribute, attribute, classEntropy):
        # persentase setiap atribut dibanding total populasi
        classFreqRatios = examples[attribute].value_counts(normalize=True)

        # For each class, find gain
        gain = classEntropy
        for index in range (0, len(classFreqRatios)):
            value = classFreqRatios.keys()[index]
            gain -= classFreqRatios[value] * self.getAttributeEntropy(examples, target_attribute, attribute, value)
        
        return gain

    def getAttributeEntropy(self, examples, target_attribute, attribute, value):
        # Filter examples that only has the value of the attribute
        filterParam = examples[attribute] == value
        filteredExamples = examples[filterParam].reset_index()

        return self.getEntropy(filteredExamples, target_attribute)

    def getEntropy(self, examples, target_attribute):
        # Find class frequency
        # persentase setiap atribut dibanding total populasi
        classFreqRatios = examples[target_attribute].value_counts(normalize=True)

        entropy = 0
        for classfreqRatio in classFreqRatios:
            entropy += -classfreqRatio * math.log2(classfreqRatio)

        return entropy

    def areAllValuesSame (self, data):
        return all(elem == data[0] for elem in data)