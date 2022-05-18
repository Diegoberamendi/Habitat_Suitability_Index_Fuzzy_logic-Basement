try:
    import os
    import logging
    import sys
    import osr
except ImportError:
    print('ERROR: Cannot import basic Python libraries.')

try:
    import numpy as np
    import pandas as pd
    from matplotlib import pyplot as plt
except ImportError:
    print('ERROR: Cannot import SciPy libraries.')
    
try:
    from osgeo import gdal
except ImportError:
    print('ERROR: Cannot import geoprocessing libraries.')
    
try:
    import skfuzzy as fuzz
    from skfuzzy import control as ctrl
except ImportError:
    print('ERROR: Cannot import fuzzy libraries.')

try:
    import raster_manager.raster_processing as ras
except ImportError:
    print('ERROR: Cannot import raster_manager.')

    
    

