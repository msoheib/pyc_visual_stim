#%%
from api.api import Api
import random

class orientation_listener(Api):

    def __init__(self):
        self.i = 0

    def update(self):
        if self.i == 0:
            self.i = self.i + 1
            self.orientations = ['degrees_135','degrees_180','degrees_225','degrees_270','degrees_315','degrees_0', 'degrees_45','degrees_90']
            random.shuffle(self.orientations)
            self.set_variable('orientations', self.orientations)
