import csv

def mean(values):
    return sum(values) / len(values)

def standard_deviation(values, mean_value):
    variance = sum((x - mean_value) ** 2 for x in values) / len(values)
    return variance ** 0.5

def normalize(values):
    mean_value = mean(values)
    std_dev = standard_deviation(values, mean_value)
    return [(x - mean_value) / std_dev for x in values]

def load_data(file_path, input_var1, input_var2, output_var):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        data = [row for row in reader]
    
    idx1, idx2, idx_out = header.index(input_var1), header.index(input_var2), header.index(output_var)
    
    inputs1 = [float(row[idx1]) if row[idx1] else None for row in data]
    inputs2 = [float(row[idx2]) if row[idx2] else None for row in data]
    outputs = [float(row[idx_out]) for row in data]
    
    mean1, mean2 = mean([x for x in inputs1 if x is not None]), mean([x for x in inputs2 if x is not None])
    inputs1 = [x if x is not None else mean1 for x in inputs1]
    inputs2 = [x if x is not None else mean2 for x in inputs2]
    
    inputs1, inputs2, outputs = normalize(inputs1), normalize(inputs2), normalize(outputs)
    return inputs1, inputs2, outputs

def train_test_split(inputs1, inputs2, outputs, train_ratio=0.8):
    train_size = int(len(inputs1) * train_ratio)
    
    train_x1 = inputs1[:train_size]
    train_x2 = inputs2[:train_size]
    train_y = outputs[:train_size]
    
    test_x1 = inputs1[train_size:]
    test_x2 = inputs2[train_size:]
    test_y = outputs[train_size:]
    
    return train_x1, train_x2, train_y, test_x1, test_x2, test_y

def compute_coefficients(train_x1, train_x2, train_y):
    n = len(train_y)
    sum_x1, sum_x2, sum_y = sum(train_x1), sum(train_x2), sum(train_y)
    sum_x1y = sum(x * y for x, y in zip(train_x1, train_y))
    sum_x2y = sum(x * y for x, y in zip(train_x2, train_y))
    sum_x1x2 = sum(x * y for x, y in zip(train_x1, train_x2))
    sum_x1_sq = sum(x ** 2 for x in train_x1)
    sum_x2_sq = sum(x ** 2 for x in train_x2)
    
    denom = (sum_x1_sq * sum_x2_sq - sum_x1x2 ** 2)
    w1 = (sum_x2_sq * sum_x1y - sum_x1x2 * sum_x2y) / denom
    w2 = (sum_x1_sq * sum_x2y - sum_x1x2 * sum_x1y) / denom
    w0 = (sum_y - w1 * sum_x1 - w2 * sum_x2) / n
    
    return w0, w1, w2

def predict(w0, w1, w2, x1, x2):
    return [w0 + w1 * xi1 + w2 * xi2 for xi1, xi2 in zip(x1, x2)]

def mean_squared_error(actual, predicted):
    return sum((a - p) ** 2 for a, p in zip(actual, predicted)) / len(actual)

# Load data
file_path = 'D:/lab5/v1_world-happiness-report-2017.csv'
inputs1, inputs2, outputs = load_data(file_path, 'Economy..GDP.per.Capita.', 'Freedom', 'Happiness.Score')

# Split into training and validation
train_x1, train_x2, train_y, test_x1, test_x2, test_y = train_test_split(inputs1, inputs2, outputs)

# Train model
w0, w1, w2 = compute_coefficients(train_x1, train_x2, train_y)
print(f'The learnt model: f(x1, x2) = {w0} + {w1} * x1 + {w2} * x2')

# Predict on test data
test_predictions = predict(w0, w1, w2, test_x1, test_x2)

# Compute error
error = mean_squared_error(test_y, test_predictions)
print('Prediction error:', error)
