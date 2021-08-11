import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def read_data(file):
    return pd.read_csv(file)


def keep_columns(data, columns_to_keep):  # Keep only the columns specified in columns_to_keep from data
    columns = list(data.columns)
    columns_to_delete = list(set(columns) - set(columns_to_keep))
    return estates_data.drop(columns_to_delete, axis=1)  # axis = 0 for rows and 1 for columns


def fill_nans(data):  # Fill NaNs with median values
    return data.fillna(data.mean())


def format_data(data):  # Returns the x (input parameters) and y (price) vectors
    x_vector = np.zeros(shape=(len(data["udaljenost_od_centra"]), 4))
    y_vector = np.zeros(shape=(len(data["udaljenost_od_centra"]), 1))

    x_vector[:, 0] = data["udaljenost_od_centra"]
    x_vector[:, 1] = data["kvadratura"]
    x_vector[:, 2] = data["brsoba"]
    x_vector[:, 3] = data["spratnost"]

    y_vector[:, 0] = data["cena"]

    return x_vector, y_vector


def split_data(data):  # Returns train_data and test_data
    data = data.sample(frac=1)
    train_len = int(len(data) * 70 / 100)  # 70% of the data is used for training the model, 30% for the test
    train_data = data.iloc[:train_len, :]
    test_data = data.iloc[train_len:, :]
    return train_data, test_data


def classify(price):
    """
        class 1: <= 49 999e
        class 2: 50 000 - 99 999e
        class 3: 100 000 - 149 999e
        class 4: 150 000 - 199 999e
        class 5: >= 200 000e
    """
    if price < 50000:
        return 1
    elif 50000 <= price <= 99999:
        return 2
    elif 100000 <= price <= 149999:
        return 3
    elif 150000 <= price <= 199999:
        return 4
    else:
        return 5


def determine_value_range(class_number):
    if class_number == 1:
        return "Price is less than 50 000e"
    elif class_number == 2:
        return "Price is between 50 000e and 99 999e"
    elif class_number == 3:
        return "Price is between 100 000e and 149 999e"
    elif class_number == 4:
        return "Price is between 150 000e and 199 999e"
    else:
        return "Price is higher than 200 000e"


def determine_distance(data_input, data, distance_type):
    distances = []
    if distance_type == 1:  # Euclidean distance
        for i in range(0, data.shape[0]):
            distance = sum((euclidean_distance(x, _x) for x, _x in zip(data_input, data[i][:])))
            distances.append(distance)
    else:  # Manhattan distance
        for i in range(0, data.shape[0]):
            distance = sum((manhattan_distance(x, _x) for x, _x in zip(data_input, data[i][:])))
            distances.append(distance)

    return distances


def euclidean_distance(x, _x):
    return math.sqrt((x - _x) ** 2)


def manhattan_distance(x, _x):
    return abs(x - _x)


def determine_class(distances_and_classes, k):
    classes_frequency = [0, 0, 0, 0, 0]  # Initial frequency is zero for each of 5 classes
    for i in range(0, k):
        classes_frequency[distances_and_classes[i][1]-1] += 1
    maximum_frequency = max(classes_frequency)
    return classes_frequency.index(maximum_frequency)


estates_data = read_data("belgrade_estates.csv")  # Read the csv file with Belgrade estates
estates_data = keep_columns(estates_data, ["cena", "udaljenost_od_centra", "kvadratura", "brsoba", "spratnost"])  # Remove unnecessary columns
estates_data = fill_nans(estates_data)  # Fill missing values

estates_data_train, estates_data_test = split_data(estates_data)  # Split the dataset

x_vector_train, y_vector_train = format_data(estates_data_train)
x_vector_test, y_vector_test = format_data(estates_data_test)

y_classified = np.zeros(shape=(1, y_vector_train.shape[0]))
y_classified = np.asarray([classify(price) for price in y_vector_train])

k = int(np.sqrt(y_classified.shape[0]))

print("It is calculated that the k={} is optimal value. Would you like to change k? (Yes-1, No-0)".format(k))
change_k = int(input())
if change_k == 1:
    print("Enter new k:\n")
    k = int(input())

print("Provide real estate information")
x_0 = input("Distance from center?\n")  # Distance from center
x_1 = input("Square meters?\n")
x_2 = input("Number of rooms?\n")
x_3 = input("Number of storey?\n")

input_data = [float(x_0), float(x_1), float(x_2), float(x_3)]

print("Calculate euclidean or manhattan distance? (Euclidean-1, Manhattan-0)")
is_euclidean_distance = int(input())

calculated_distances = determine_distance(input_data, x_vector_train, is_euclidean_distance)

distances_and_classes = list(zip(calculated_distances, y_classified))

distances_and_classes.sort(key=lambda x: x[0])  # Sort (distance, class) by distance

predicted_class = determine_class(distances_and_classes, k)

print(determine_value_range(predicted_class))