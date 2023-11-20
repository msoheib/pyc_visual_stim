#%%
import sys
sys.path.insert(0,'G:\\My Drive\\0-Main\pycontrol_api_v181') # Add pyControl dir to path.
from api.api import Api
import random

orientations = ['degrees_0', 'degrees_45','degrees_90','degrees_135','degrees_180','degrees_225','degrees_270','degrees_315']
orientations = ['degrees_135','degrees_180','degrees_225','degrees_270','degrees_315','degrees_0', 'degrees_45','degrees_90']
random.shuffle(orientations)
Api.set_variable('foo','orientations', orientations)
print('orientations: ' + str(orientations))
