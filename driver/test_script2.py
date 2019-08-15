
import pickle
favorite_color = { "lion": "yellow", "kitty": "red" }

pickle.dump( favorite_color, open( "./save.p", "wb" ) )
print("it good b")
