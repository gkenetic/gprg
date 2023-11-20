import operator
import numpy as np
from deap import creator, base, tools, gp, algorithms
from functools import partial
import random
from datetime import datetime
import warnings

warnings.filterwarnings("ignore", message="Ephemeral rand function cannot be pickled.*")
warnings.filterwarnings("ignore", message="overflow encountered in exp")
warnings.filterwarnings("ignore", message="invalid value encountered in log")
warnings.filterwarnings("ignore", message="invalid value encountered in sqrt")
warnings.filterwarnings("ignore", message="divide by zero encountered in log")
warnings.filterwarnings("ignore", message="invalid value encountered in sin")
warnings.filterwarnings("ignore", message="invalid value encountered in cos")
warnings.filterwarnings("ignore", message="invalid value encountered in scalar subtract")
warnings.filterwarnings("ignore", message="divide by zero encountered in scalar divide")
warnings.filterwarnings("ignore", message="invalid value encountered in scalar multiply")



# Define the problem
def evaluate(individual, timestamps, target_values):
    func = gp.compile(expr=individual, pset=pset)

    predicted_values = [func(timestamp) for timestamp in timestamps]

    # Ensure the length of predicted_values matches the length of target_values
    if len(predicted_values) != len(target_values):
        raise ValueError("Length of predicted_values does not match the length of target_values.")

    # Handle invalid values (e.g., NaN, Inf)
    predicted_values = [0.0 if np.isnan(value) or np.isinf(value) or np.isneginf(value) else value for value in predicted_values]

    # Assuming the length of target_values and predicted_values are the same
    fitness = np.sum(np.abs(np.subtract(target_values, predicted_values)))

    # Penalize individuals producing invalid values
    if any(np.isnan(value) or np.isinf(value) or np.isneginf(value) for value in predicted_values):
        fitness += 1e6  # Add a large penalty

    return fitness,

# Define protectedDiv as a primitive
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1.0  # Return a default value to avoid division by zero

def parse_data(file_path):
    with open(file_path, 'r') as file:
        data = [line.strip().split(',') for line in file]

    data = [(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S UTC').timestamp(), float(value)) for timestamp, value in data]
    return data

# Create the types for the individual and the fitness
pset = gp.PrimitiveSet("MAIN", arity=1)
pset.addPrimitive(operator.add, arity=2)
pset.addPrimitive(operator.sub, arity=2)
pset.addPrimitive(operator.mul, arity=2)
pset.addPrimitive(np.sin, arity=1)
pset.addPrimitive(np.cos, arity=1)
pset.addPrimitive(np.exp, arity=1)
pset.addPrimitive(np.log, arity=1)
pset.addPrimitive(np.sqrt, arity=1)
pset.addPrimitive(protectedDiv, arity=2)  # Use protectedDiv here

# Define functions explicitly with unique names
def sin_func(x):
    return np.sin(x)

def cos_func(x):
    return np.cos(x)

def exp_func(x):
    return np.exp(x)

def log_func(x):
    return np.log(x)

def sqrt_func(x):
    return np.sqrt(x)

# Use unique names for addPrimitive
pset.addPrimitive(sin_func, arity=1, name="sin_func")
pset.addPrimitive(cos_func, arity=1, name="cos_func")
pset.addPrimitive(exp_func, arity=1, name="exp_func")
pset.addPrimitive(log_func, arity=1, name="log_func")
pset.addPrimitive(sqrt_func, arity=1, name="sqrt_func")

pset.addEphemeralConstant("rand", lambda: random.uniform(-1, 1))

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("compile", gp.compile, pset=pset)

data_file_path = '/root/gprg/tsla_data_h.txt'
data = parse_data(data_file_path)

# Split data into training and test sets
split_ratio = 0.8  # Adjust this ratio based on your preference
split_index = int(len(data) * split_ratio)

training_data = data[:split_index]
test_data = data[split_index:]

# Extract timestamps and values for training and test sets
training_timestamps, training_values = zip(*training_data)
test_timestamps, test_values = zip(*test_data)

# Define the problem for training set
def evaluate_training(individual, timestamps, target_values):
    func = gp.compile(expr=individual, pset=pset)

    predicted_values = [func(timestamp) for timestamp in timestamps]

    # Ensure the length of predicted_values matches the length of target_values
    if len(predicted_values) != len(target_values):
        raise ValueError("Length of predicted_values does not match the length of target_values.")

    # Handle invalid values (e.g., NaN, Inf)
    predicted_values = [0.0 if np.isnan(value) or np.isinf(value) or np.isneginf(value) else value for value in predicted_values]

    # Assuming the length of target_values and predicted_values are the same
    fitness = np.sum(np.abs(np.subtract(target_values, predicted_values)))

    # Penalize individuals producing invalid values
    if any(np.isnan(value) or np.isinf(value) or np.isneginf(value) for value in predicted_values):
        fitness += 1e6  # Add a large penalty

    return fitness,

# Register the new evaluation function for training
toolbox.register("evaluate", evaluate_training, timestamps=training_timestamps, target_values=training_values)

toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():
    random.seed(42)

    population = toolbox.population(n=500)
    generations = 50

    for gen in range(generations):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.7, mutpb=0.1)
        fits = toolbox.map(toolbox.evaluate, offspring)

        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit

            # Print the individual if you want to inspect it
            #print(f"Generation {gen}, Individual: {ind}, Fitness: {fit}")

        population = toolbox.select(offspring + population, k=len(population))

    best_individual = tools.selBest(population, k=1)[0]
    best_function = gp.compile(expr=best_individual, pset=pset)

    print(f"Best individual fitness: {best_individual.fitness.values[0]}")
    print(f"Best individual: {best_individual}")
    print("Best function:")
    print(best_function)

    # Evaluate the best individual on the test set
    test_fitness = evaluate_training(best_individual, test_timestamps, test_values)
    print(f"Test set fitness for the best individual: {test_fitness}")

    # Apply the compiled function to the new data (test set)
    test_predictions = [best_function(x_i) for x_i in test_timestamps]

    # Print or use the predictions as needed
    print("Predictions for test set:")
    print(test_predictions)

if __name__ == "__main__":
    main()
