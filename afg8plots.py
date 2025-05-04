import matplotlib.pyplot as plt
import numpy

x = numpy.linspace(0, 10, 200)
y = numpy.sin(x)

plt.plot(x, y)
plt.show()

a = numpy.random.rand(200)
b = numpy.random.rand(200)

plt.scatter(a, b)
plt.show()
