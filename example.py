import pandas as pd
from mapmatch import Matcher

# step1: read trajectory file
traj = pd.read_csv("sample_preprocessed.csv")

# step2: initialize a matcher object
matcher = Matcher(engine='pytrack')  # only pytrack engine is supported currently

# step3: perform map-matching
"""
the algorithm will automatically extract road network of the trajectory region
so there is no need to download a network mannually
a new column named [osmid] will be generated, which represents the matched road section index in OSM
"""
traj = matcher.match(
    traj=traj,
    lonCol='lon',  # longitude column name
    latCol='lat',  # latitude column name
    tripIDCol=None,  # if assign tripIDCol, the matching process will be executed for each trip seperately 
    dropCoord=True,  # if False, the matched coordinates will be kept
)

# step4: merge road type information
"""
this procedure will assign road type, geometry and length to each trajectory point according to osmid
"""
roadnet = pd.read_csv('roadnet_chengdu.csv')
traj_matched = pd.merge(traj, roadnet, on='osmid', how='left')

# step5: save
traj_matched.to_csv('traj_matched.csv', index=False)