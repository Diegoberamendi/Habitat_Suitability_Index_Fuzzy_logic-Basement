from fun import *
from config import *
from time import perf_counter


def fuzzy_control(ant_1, ant_2, cons_1):
    """
    Fuzzy_control function that generates antecedent and consequent universe
    variables.
    Parameters
    ----------
    :ant_1: 1D array fuzzy universe variables, acting as the first antecedent
    :ant_2: 1D array fuzzy universe variables, acting as the second antecedent
    :cons_1: 1D array fuzzy universe variables, acting as the consequent

    :Return: aggregated hsi_value
    -------
    """
    # Generate the antecedent and consequent fuzzy universe variables
    depth = ctrl.Antecedent(ant_1, 'depth')
    velocity = ctrl.Antecedent(ant_2, 'velocity')
    hsi = ctrl.Consequent(cons_1, 'hsi')

    # Generate fuzzy membership functions
    depth['depth_low'] = fuzz.trapmf(depth.universe, [0, 0, 0.15, 0.35])
    depth['depth_medium'] = fuzz.trapmf(depth.universe, [0.15, 0.35, 0.8, 1.1])
    depth['depth_high'] = fuzz.trapmf(depth.universe, [0.8, 1.1, 1.45, 1.45])

    velocity['vel_low'] = fuzz.trapmf(velocity.universe, [0, 0, 0.4, 1])
    velocity['vel_medium'] = fuzz.trapmf(velocity.universe, [0.4, 1, 1.4, 2])
    velocity['vel_high'] = fuzz.trapmf(velocity.universe, [1.4, 2, 3.4, 3.4])

    hsi['hsi_low'] = fuzz.trapmf(hsi.universe, [0, 0, 0.1, 0.3])
    hsi['hsi_medium'] = fuzz.trapmf(hsi.universe, [0.1, 0.3, 0.7, 0.9])
    hsi['hsi_high'] = fuzz.trapmf(hsi.universe, [0.7, 0.9, 1, 1])

    # Define the fuzzy rules according to expert knowledge
    rule1 = ctrl.Rule(antecedent=(depth['depth_high'] & velocity['vel_high']),
                      consequent=hsi['hsi_low'])
    rule2 = ctrl.Rule(antecedent=(depth['depth_high'] & velocity['vel_medium']),
                      consequent=hsi['hsi_medium'])
    rule3 = ctrl.Rule(antecedent=(depth['depth_high'] & velocity['vel_low']),
                      consequent=hsi['hsi_low'])
    rule4 = ctrl.Rule(antecedent=(depth['depth_medium'] & velocity['vel_high']),
                      consequent=hsi['hsi_high'])
    rule5 = ctrl.Rule(antecedent=(depth['depth_medium'] & velocity['vel_medium']),
                      consequent=hsi['hsi_high'])
    rule6 = ctrl.Rule(antecedent=(depth['depth_medium'] & velocity['vel_low']),
                      consequent=hsi['hsi_low'])
    rule7 = ctrl.Rule(antecedent=(depth['depth_low'] & velocity['vel_high']),
                      consequent=hsi['hsi_low'])
    rule8 = ctrl.Rule(antecedent=(depth['depth_low'] & velocity['vel_medium']),
                      consequent=hsi['hsi_medium'])
    rule9 = ctrl.Rule(antecedent=(depth['depth_low'] & velocity['vel_low']),
                      consequent=hsi['hsi_low'])

    # Aggregate the output membership functions
    aggregate = ctrl.ControlSystem(rules=[rule1, rule2, rule3,
                                          rule4, rule5, rule6,
                                          rule7, rule8, rule9])

    # Calculate the qualitative hsi from the control system
    hsi_value = ctrl.ControlSystemSimulation(aggregate)

    return hsi_value


@logger
def main():
    # Load qualitative hsi values
    hsi_result = fuzzy_control(depth_univ, vel_univ, hsi_univ)

    # Load and read velocity and depth raster as arrays
    raster_depth, depth_array = ras.raster2array(depth_file)
    raster_velocity, vel_array = ras.raster2array(velocity_file)
    output_hsi = np.zeros_like(depth_array)

    # Iterate the depth and velocity values for each cell
    for i in range(975):
        for j in range(1151):
            hsi_result.input['depth'] = depth_array[i, j]
            hsi_result.input['velocity'] = vel_array[i, j]
            hsi_result.compute()
            output_hsi[i, j] = hsi_result.output['hsi']

    # Create hsi raster
    ras.create_raster(file_name, output_hsi, origins, pixel_width=1,
                      pixel_height=-1, epsg=5668)


if __name__ == '__main__':
    # Initialize universe variables
    depth_univ = np.linspace(0, 1.5, 100)
    vel_univ = np.linspace(0, 3.5, 100)
    hsi_univ = np.linspace(0, 1, 100)

    # Define variables for main function
    depth_file = r'' + os.getcwd() + '/data/water_depth.tif'
    velocity_file = r'' + os.getcwd() + '/data/flow_velocity.tif'

    # Define a raster origin in EPSG:5668
    origins = (786986.1064724320312962, 156145.3739023693779018)

    # Set the name of the output GeoTIFF raster
    file_name = r'' + os.getcwd() + '/output_raster/hsi_result.tif'

    # Run code and evaluate performance for creating hsi values
    t0 = perf_counter()
    main()
    t1 = perf_counter()
    print('running the code takes: ' + str(t1 - t0))
