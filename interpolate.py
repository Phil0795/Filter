import numpy as np
from scipy.interpolate import interp1d
from sklearn.metrics import mean_absolute_error as mae


# get my list of x and y values
x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([2, 2, 3, 4, 5, 7, 7, 8, 9, 9])

x2 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y2 = np.array([3, 3, 4, 5, 6, 7, 8, 8, 9, 9])

# create a function that will interpolate the data
f = interp1d(x, y, kind='cubic')
f2 = interp1d(x2, y2, kind='cubic')

# create a new set of x values to interpolate to
xnew = np.arange(1, 10, 0.1)

# interpolate to find the y values
ynew = f(xnew)
ynew2 = f2(xnew)

# calculate the mean absolute error
#mae = np.mean(np.abs(ynew - ynew2))
error = mae(ynew, ynew2)

# print the result
print(error)
