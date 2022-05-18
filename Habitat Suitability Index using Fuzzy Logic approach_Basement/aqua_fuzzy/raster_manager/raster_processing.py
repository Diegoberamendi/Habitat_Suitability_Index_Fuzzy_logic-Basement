from osgeo import gdal
import osr
import sys
import numpy as np


def open_raster(file):
    """
    Open the raster file according to given band number.
    Parameters
    ----------
    :file: STR, raster file name
    :band_number: INT, raster band number, as default: 1

    :Return: objects of gdal dataset and band objects
    ----------
    """
    gdal.UseExceptions()

    # Open raster file or return None if not accessible
    try:
        raster = gdal.Open(file)
    except RuntimeError as e:
        print('Error. Unable to open file.tif')
        print(e)
        sys.exit(1)

    # Open raster band or return None if corrupted
    try:
        raster_band = raster.GetRasterBand(1)
    except RuntimeError as e:
        print('ERROR: Cannot access raster band 1.')
        print(e)
        return None

    return raster, raster_band


def raster2array(file, band_number=1):
    """
    Converts the raster.TIFF to arrays
    Parameters
    ----------
    :file_name: STR, raster file to convert in np.array"
    :band_number: INT, raster band, default: 1

    :Return: (1) raster file to be converted in array
             (2) np array(), raster band (nan values are now np.nan values)
    ----------
    """
    # Open the raster and band
    raster, band = open_raster(file)

    # Get geotransformation
    try:
        geot = raster.GetGeoTransform()
    except RuntimeError as e:
        print('No band %i found' % band_number)
        print(e)
        sys.exit(1)

    # Read Projection
    try:
        prj = raster.GetProjection()
    except RuntimeError as e:
        print('Cannot access Projection.')
        print(e)

    # Read array data from band
    array = band.ReadAsArray()

    # Overwrite NoDataValues with np.nan
    array = np.where(array == band.GetNoDataValue(),
                     np.nan, array)

    return raster, array


def create_raster(file_name, raster_array, origin=None,
                  epsg=None, pixel_width=None, pixel_height=None,
                  nan_value=-9999.0, geo_info=False):
    """
    Creates a raster file from numpy arrays
    Parameters
    ----------
    :file_name: STR, file name to be created
    :raster_array: np. array values to convert in raster format
    :origin: TUPLE of coordinates
    :epsg: INT, projection to be used in the output file
    :pixel_width: INT, pixel width
    :pixel_height: INT, pixel height
    :nan_value: INT/FLOAT not a number value to use in the raster
    :geo_info: TUPLE of geotransform
    -------
    """
    gdal.UseExceptions()

    # Check out driver
    driver = gdal.GetDriverByName('GTiff')
    driver.Register()

    # Create raster dataset with number of columns and rows of the input array
    cols = raster_array.shape[1]
    rows = raster_array.shape[0]
    new_raster = driver.Create(file_name, cols, rows,
                               bands=1, eType=gdal.GDT_Float32)

    # Geotransform
    if not geo_info:
        origin_x = origin[0]
        origin_y = origin[1]
        new_raster.SetGeoTransform((origin_x, pixel_width, 0,
                                    origin_y, 0, pixel_height))
    else:
        new_raster.SetGeoTransform(geo_info)

    # Retrieve band number 1
    band = new_raster.GetRasterBand(1)
    band.SetNoDataValue(nan_value)
    band.WriteArray(raster_array)
    band.SetScale(1.0)

    # Create projection and assign to raster
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg)
    new_raster.SetProjection(srs.ExportToWkt())

    # Release raster band
    band.FlushCache()

