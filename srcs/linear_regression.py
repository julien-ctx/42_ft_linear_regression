import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

class LinearRegression:

	def __init__(self, alpha = 0.001, max_i = 100000):
		self.thetas = np.array([[0.], [0.]]).astype(float)
		self.alpha = alpha
		self.max_i = max_i
	
	def add_intercept(self, x):
		if not isinstance(x, (np.ndarray, np.generic)):
			return None
		if not x.size:
			return None
		if x.ndim == 1:
			x = x[:,np.newaxis]
		ones = np.ones((len(x), 1))
		return np.hstack((ones, x))

	def gradient(self, x, y, theta):
		xp = self.add_intercept(x)
		xpt = xp.T
		return np.array((xpt @ (xp @ theta - y)) / y.size)
	
	def gradient_descent(self, x, y):
		for _ in range(self.max_i):
			self.thetas = self.thetas - self.alpha * self.gradient(x, y, self.thetas)
		return self.thetas

	def plot(self, old_x, x, y):
		plt.scatter(old_x, y)
		plt.plot(old_x, x * self.thetas[1] + self.thetas[0], 'r')
		plt.xlabel("Mileage (km)")
		plt.ylabel("Price ($)")
		plt.show()

	@staticmethod
	def standardization(x):
		return (x - np.mean(x)) / np.std(x)

if __name__ == "__main__":
	dataset = pd.read_csv("../assets/data.csv")
	x = np.array(dataset['km']).reshape(-1, 1).astype(float)
	y = np.array(dataset['price']).reshape(-1, 1).astype(float)
	old_x = x
	model = LinearRegression()
	mean, std = np.mean(x), np.std(x)
	x = LinearRegression.standardization(x)
	thetas = model.gradient_descent(x, y)
	if len(sys.argv) == 1:
		print(f"{mean},{std},{int(thetas[1])},{int(thetas[0])}")
	elif (sys.argv[1] == 'plot'):
		model.plot(old_x, x, y)
