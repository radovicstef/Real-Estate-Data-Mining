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


def split_data(data):  # Returns train_data and test_data
    data = data.sample(frac=1)
    train_len = int(len(data) * 70 / 100)  # 70% of the data is used for training the model, 30% for the test
    train_data = data.iloc[:train_len, :]
    test_data = data.iloc[train_len:, :]
    return train_data, test_data


def format_data(data):  # Returns the x (input parameters) and y (price) in vector format
    x_vector = np.zeros(shape=(len(data["udaljenost_od_centra"]), 4))
    y_vector = np.zeros(shape=(len(data["udaljenost_od_centra"]), 1))

    x_vector[:, 0] = data["udaljenost_od_centra"]
    x_vector[:, 1] = data["kvadratura"]
    x_vector[:, 2] = data["brsoba"]
    x_vector[:, 3] = data["spratnost"]

    y_vector[:, 0] = data["cena"]

    return x_vector, y_vector


def normalize_data(data):  # Normalize data wit min-max approach
    normalized_data = np.copy(data)
    for i in range(0, data.shape[1]):
        minimum = np.amin(data[:, i])
        maximum = np.amax(data[:, i])
        normalized_data[:, i] = (normalized_data[:, i] - minimum) / (maximum - minimum)
    return normalized_data


def normalize_input_data(data_input, data):  # Normalize first parameter data, based on second parameter which contains un-normalized data
    for i in range(0, data.shape[1]):
        minimum = np.amin(data[:, i])
        maximum = np.amax(data[:, i])
        data_input[i] = (data_input[i] - minimum) / (maximum - minimum)
    return data_input


def un_normalize_data(data_normalized, data):  # Un-normalize first parameter data, based on second parameter which contains un-normalized data
    for i in range(0, data.shape[1]):
        minimum = np.amin(data[:, i])
        maximum = np.amax(data[:, i])
        un_normalized_data = (maximum - minimum) * data_normalized + minimum
    return un_normalized_data


def gradient_descent(x_vector, y_vector, num_iterations=1000, learning_rate=0.1):  # Gradient descent algorithm
    w_0 = 0.0
    w_vector = np.zeros((1, x_vector.shape[1]))  # Initial parameters are equal to 0
    m = x_vector.shape[0]  # m is dataset size
    for i in range(0, num_iterations):
        h = np.dot(x_vector, w_vector.T) + w_0

        temp_w_0 = w_0 - learning_rate * (1/m) * np.sum(h - y_vector)
        temp_w_vector = w_vector - learning_rate * (1/m) * np.dot((h - y_vector).T, x_vector)

        w_0 = temp_w_0
        w_vector = temp_w_vector
    return w_0, w_vector


def predict(x_vector):  # Based on already calculated parameters, returns the predicted value
    global parameter_w_0, parameter_w_vector
    return parameter_w_0 + np.dot(x_vector, parameter_w_vector.T)


def root_mean_squared_error(y, h):  # Calculates RMSE
    return np.sqrt(np.mean((y-h)**2))


if __name__ == "__main__":
    estates_data = read_data("belgrade_estates.csv")  # Read the csv file with Belgrade estates
    estates_data = keep_columns(estates_data, ["cena", "udaljenost_od_centra", "kvadratura", "brsoba", "spratnost"])  # Remove unnecessary columns
    estates_data = fill_nans(estates_data)  # Fill missing values

    estates_data_train, estates_data_test = split_data(estates_data)  # Split the dataset

    # Format test and train dataframe into vectors
    x_vector_train, y_vector_train = format_data(estates_data_train)
    x_vector_test, y_vector_test = format_data(estates_data_test)

    # Normalize data [0, 1]
    x_vector_train_normalized = normalize_data(x_vector_train)
    y_vector_train_normalized = normalize_data(y_vector_train)
    x_vector_test_normalized = normalize_data(x_vector_test)
    y_vector_test_normalized = normalize_data(y_vector_test)

    # Gradient descent method returns parameters value
    parameter_w_0, parameter_w_vector = gradient_descent(x_vector_train_normalized, y_vector_train_normalized)
    print("Calculated parameters:\n w_0 = {}, w_vector = {}".format(parameter_w_0, parameter_w_vector))

    # predicted_data_train = un_normalize_data(predict(x_vector_train_normalized), y_vector_train)
    # predicted_data_test = un_normalize_data(predict(x_vector_test_normalized), y_vector_test)
    # print("RMSE = {}".format(root_mean_squared_error(y_vector_train, predicted_data_train)))
    # print("RMSE = {}".format(root_mean_squared_error(y_vector_test, predicted_data_test)))

    print("Provide real estate information")
    x_0 = input("Distance from center in km?\n")
    x_1 = input("Area in square meters?\n")
    x_2 = input("Number of rooms?\n")
    x_3 = input("Floor?\n")

    input_data = [float(x_0), float(x_1), float(x_2), float(x_3)]  # Format input data as vector
    input_data_normalized = normalize_input_data(input_data, x_vector_train)  # Normalize input data

    # Calculate expected price
    expected_price_normalized = parameter_w_0 + parameter_w_vector[0][0] * input_data_normalized[0] + parameter_w_vector[0][1] * input_data_normalized[1] + parameter_w_vector[0][2] * input_data_normalized[2] + parameter_w_vector[0][3] * input_data_normalized[3]
    expected_price = un_normalize_data(expected_price_normalized, y_vector_train)

    print("Expected price: {}€".format(expected_price))









