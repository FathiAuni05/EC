# ackley multimodal function
from numpy import arange
from numpy import exp
from numpy import sqrt
from numpy import cos
from numpy import e
from numpy import pi
from numpy import meshgrid
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import streamlit as st

st.title("Evalution Strategies")
st.write('the surface plot of the ackley function showing the vast number of local optima')
# objective function
def objective(x, y):
	return -20.0 * exp(-0.2 * sqrt(0.5 * (x**2 + y**2))) - exp(0.5 * (cos(2 * pi * x) + cos(2 * pi * y))) + e + 20

# define range for input
r_min, r_max = -5.0, 15.0
# sample input range uniformly at 0.1 increments
xaxis = arange(r_min, r_max, 0.1)
yaxis = arange(r_min, r_max, 0.1)
# create a mesh from the axis
x, y = meshgrid(xaxis, yaxis)
# compute targets
results = objective(x, y)
# create a surface plot with the jet color scheme
figure = pyplot.figure()
axis = figure.add_subplot(projection='3d')
axis.plot_surface(x, y, results, cmap='jet')
# show the plot
st.pyplot(figure)


# evolution strategy (mu, lambda) of the ackley objective function
from numpy import asarray
from numpy import exp
from numpy import sqrt
from numpy import cos
from numpy import e
from numpy import pi
from numpy import argsort
from numpy.random import randn
from numpy.random import rand
from numpy.random import seed

st.write('Develop a (mu, λ)-ES')
# objective function
def objective(v):
	x, y = v
	return -20.0 * exp(-0.2 * sqrt(0.5 * (x**2 + y**2))) - exp(0.5 * (cos(2 * pi * x) + cos(2 * pi * y))) + e + 20

# check if a point is within the bounds of the search
def in_bounds(point, bounds):
	# enumerate all dimensions of the point
	for d in range(len(bounds)):
		# check if out of bounds for this dimension
		if point[d] < bounds[d, 0] or point[d] > bounds[d, 1]:
			return False
	return True

# evolution strategy (mu, lambda) algorithm
def es_comma(objective, bounds, n_iter, step_size, mu, lam):
	best, best_eval = None, 1e+10
	# calculate the number of children per parent
	n_children = int(lam / mu)
	# initial population
	population = list()
	for _ in range(lam):
		candidate = None
		while candidate is None or not in_bounds(candidate, bounds):
			candidate = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
		population.append(candidate)
	# perform the search
	for epoch in range(n_iter):
		# evaluate fitness for the population
		scores = [objective(c) for c in population]
		# rank scores in ascending order
		ranks = argsort(argsort(scores))
		# select the indexes for the top mu ranked solutions
		selected = [i for i,_ in enumerate(ranks) if ranks[i] < mu]
		# create children from parents
		children = list()
		for i in selected:
			# check if this parent is the best solution ever seen
			if scores[i] < best_eval:
				best, best_eval = population[i], scores[i]
				st.write('%d, Best: f(%s) = %.5f' % (epoch, best, best_eval))
			# create children for parent
			for _ in range(n_children):
				child = None
				while child is None or not in_bounds(child, bounds):
					child = population[i] + randn(len(bounds)) * step_size
				children.append(child)
		# replace population with children
		population = children
	return [best, best_eval]


# seed the pseudorandom number generator
seed(1)
# define range for input
bounds = asarray([[-15.0, 5.0], [-15.0, 5.0]])
# define the total iterations
n_iter = 5000
# define the maximum step size
step_size = 0.15
# number of parents selected
mu = 20
# the number of children generated by parents
lam = 100
# perform the evolution strategy (mu, lambda) search
best, score = es_comma(objective, bounds, n_iter, step_size, mu, lam)
st.write('Done!')
st.write('f(%s) = %f' % (best, score))


# evolution strategy (mu + lambda) of the ackley objective function
from numpy import asarray
from numpy import exp
from numpy import sqrt
from numpy import cos
from numpy import e
from numpy import pi
from numpy import argsort
from numpy.random import randn
from numpy.random import rand
from numpy.random import seed

st.text('')
st.write('Develop a (mu + λ)-ES')
# objective function
def objective(v):
	x, y = v
	return -20.0 * exp(-0.2 * sqrt(0.5 * (x**2 + y**2))) - exp(0.5 * (cos(2 * pi * x) + cos(2 * pi * y))) + e + 20

# check if a point is within the bounds of the search
def in_bounds(point, bounds):
	# enumerate all dimensions of the point
	for d in range(len(bounds)):
		# check if out of bounds for this dimension
		if point[d] < bounds[d, 0] or point[d] > bounds[d, 1]:
			return False
	return True

# evolution strategy (mu + lambda) algorithm
def es_plus(objective, bounds, n_iter, step_size, mu, lam):
	best, best_eval = None, 1e+10
	# calculate the number of children per parent
	n_children = int(lam / mu)
	# initial population
	population = list()
	for _ in range(lam):
		candidate = None
		while candidate is None or not in_bounds(candidate, bounds):
			candidate = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])
		population.append(candidate)
	# perform the search
	for epoch in range(n_iter):
		# evaluate fitness for the population
		scores = [objective(c) for c in population]
		# rank scores in ascending order
		ranks = argsort(argsort(scores))
		# select the indexes for the top mu ranked solutions
		selected = [i for i,_ in enumerate(ranks) if ranks[i] < mu]
		# create children from parents
		children = list()
		for i in selected:
			# check if this parent is the best solution ever seen
			if scores[i] < best_eval:
				best, best_eval = population[i], scores[i]
				st.write('%d, Best: f(%s) = %.5f' % (epoch, best, best_eval))
			# keep the parent
			children.append(population[i])
			# create children for parent
			for _ in range(n_children):
				child = None
				while child is None or not in_bounds(child, bounds):
					child = population[i] + randn(len(bounds)) * step_size
				children.append(child)
		# replace population with children
		population = children
	return [best, best_eval]

# seed the pseudorandom number generator
seed(1)
# define range for input
bounds = asarray([[-10.0, 5.0], [-10.0, 5.0]])
# define the total iterations
n_iter = 5000
# define the maximum step size
step_size = 0.15
# number of parents selected
mu = 20
# the number of children generated by parents
lam = 100
# perform the evolution strategy (mu + lambda) search
best, score = es_plus(objective, bounds, n_iter, step_size, mu, lam)
st.write('Done!')
st.write('f(%s) = %f' % (best, score))
