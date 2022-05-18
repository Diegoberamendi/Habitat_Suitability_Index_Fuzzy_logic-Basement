from membership.inputs_output import *


depth = InputVariable('depth', 0, 1.45, 1000)
depth.add_trapezoid('depth_low', 0, 0, 0.15, 0.35)
depth.add_trapezoid('depth_medium', 0.15, 0.35, 0.8, 1.1)
depth.add_trapezoid('depth_high', 0.8, 1.1, 1.45, 1.45)
depth.plot_variable()

velocity = InputVariable('velocity', 0, 3.1, 1000)
velocity.add_trapezoid('vel_low', 0, 0, 0.4, 1)
velocity.add_trapezoid('vel_medium', 0.4, 1, 1.4, 2)
velocity.add_trapezoid('vel_high', 1.4, 2, 3.4, 3.4)
velocity.plot_variable()

hsi = OutputVariable('hsi', 0, 1, 1000)
hsi.add_trapezoid('hsi_low', 0, 0, 0.1, 0.3)
hsi.add_trapezoid('hsi_medium', 0.1, 0.3, 0.7, 0.9)
hsi.add_trapezoid('hsi_high', 0.7, 0.9, 1, 1)
hsi.plot_variable()
