import pickle
import matplotlib.pyplot as plt

angles = pickle.load( open( "free_run.p", "rb" ) )

plt.plot(angles)

plt.show()