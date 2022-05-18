import os
import shutil
import subprocess
import tkinter as tk
from decorators import time_func
from decorators import change_name_file
from tkinter.messagebox import showinfo
from tkinter import filedialog
from os.path import dirname
from os.path import abspath
import replace_path


class BasementApplication(tk.Frame):

    def __init__(self, parent=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Set of canvas
        self.parent = parent
        self.config(width=1000, height=1000)
        self.parent.title('Basegem Beta 1')

        # Input of discharges
        self.input_string = tk.StringVar()
        self.a_label = tk.Label(parent, text='Discharge values (m\u00B3/s):',
                                fg='dark blue')
        self.a_label.grid(sticky=tk.W, row=1, column=0, padx=10)

        self.v_input_string = tk.Entry(parent, bg='alice blue', width=15,
                                       textvariable=self.input_string)
        self.v_input_string.grid(stick=tk.EW, row=1, column=1, padx=5)

        # Input of initial discharge
        self.q_ini = tk.StringVar()
        self.b_label = tk.Label(parent, text='First discharge (m\u00B3/s):',
                                fg='dark blue')
        self.b_label.grid(sticky=tk.W, row=2, column=0, padx=10)
        self.v_q_ini = tk.Entry(parent, bg='alice blue', width=15,
                                textvariable=self.q_ini)
        self.v_q_ini.grid(stick=tk.EW, row=2, column=1, padx=5)

        # Input of default_friction coefficient
        self.friction_ini = tk.StringVar()
        self.c_label = tk.Label(parent, text='Default_friction:',
                                fg='dark blue')
        self.c_label.grid(sticky=tk.W, row=3, column=0, padx=10)
        self.v_friction_ini = tk.Entry(parent, bg='alice blue', width=15,
                                       textvariable=self.friction_ini)
        self.v_friction_ini.grid(stick=tk.EW, row=3, column=1, padx=5)

        # Input of default_friction coefficients
        self.input_friction = tk.StringVar()
        self.c_label = tk.Label(parent, text='Default_friction values:',
                                fg='dark blue')
        self.c_label.grid(sticky=tk.W, row=4, column=0, padx=10)
        self.v_input_friction = tk.Entry(parent, bg='alice blue', width=15,
                                         textvariable=self.input_friction)
        self.v_input_friction.grid(stick=tk.EW, row=4, column=1, padx=5)

        # Check button for the default_friction coefficients
        self.friction = tk.BooleanVar()
        self.c_button_friction = tk.Checkbutton(parent,
                                                text='Default_friction values',
                                                fg='dark blue',
                                                variable=self.friction)
        self.c_button_friction.grid(stick=tk.W, row=5, column=1)
        self.friction.set(False)

        # Check button for the running of Basement in batch mode
        self.batch = tk.BooleanVar()
        self.c_button_batch = tk.Checkbutton(parent,
                                             text='Run the files',
                                             fg='dark blue',
                                             variable=self.batch)
        self.c_button_batch.grid(stick=tk.W, row=6, column=1)
        self.batch.set(False)

        # Button for executing the function Basement_generator
        self.run_button = tk.Button(parent, text='Run',
                                    command=lambda: self.basement_generator(),
                                    fg='dark blue', padx=8, pady=8)
        self.run_button.grid(stick=tk.EW, row=7, column=0)

        # Button for erasing .xdmf paths
        self.help_button = tk.Button(parent, text='Erase paths from .xdmf '
                                                  'files',
                                     fg='dark blue',
                                     padx=8, pady=8,
                                     command=lambda: replace_path.path_in_files())
        self.help_button.grid(stick=tk.EW, row=7, column=1)

        # Button for erasing the contents of the simulation.batch file
        self.erase_simulation = tk.Button(parent, text='Clean batch file',
                                          command=lambda: self.erase_batch_file(),
                                          fg='dark blue', padx=8, pady=8)
        self.erase_simulation.grid(stick=tk.EW, row=7, column=2)

        # Menu bar
        self.menu_bar = tk.Menu(self)
        self.parent.config(menu=self.menu_bar)

        # Drop down menu, 'about'
        self.drop_about = tk.Menu(self, tearoff=0)
        self.menu_bar.add_cascade(label='About', menu=self.drop_about)
        self.drop_about.add_command(label='About',
                                    command=lambda: self.about_message())

        # Drop down menu, 'select working directory'
        self.folderPath = tk.StringVar()
        self.drop_wdirectory = tk.Menu(self, tearoff=0)
        self.menu_bar.add_cascade(label='Working directory',
                                  menu=self.drop_wdirectory)
        self.drop_wdirectory.add_command(label='Working directory',
                                         command=lambda: [
                                             self.get_working_path(),
                                             self.copy_q_files()])

        # Drop down menu, 'select Basement installation  directory'
        self.folderPath_base = tk.StringVar()
        self.drop_bdirectory = tk.Menu(self, tearoff=0)
        self.menu_bar.add_cascade(label='Basement directory',
                                  menu=self.drop_bdirectory)
        self.drop_bdirectory.add_command(label='Basement directory',
                                         command=lambda: [
                                             self.get_basement_directory(),
                                             self.writing_paths()])

        # Drop down menu, 'Help'
        self.drop_help = tk.Menu(self, tearoff=0)
        self.menu_bar.add_cascade(label='Help', menu=self.drop_help)
        self.drop_help.add_command(label='Help',
                                   command=lambda: self.help_func())

    @classmethod
    def about_message(cls):

        message_text = '''
                        Basegem Beta 1
                        Diego Beramendi Ortega  
                        Yomer Cisneros Aguirre
                        WAREM 2021 - University of Stuttgart '''
        return showinfo('Python Programming for Water Resources ', message_text)

    def get_working_path(self):
        """
        Change the working directory to the one  indicated by the user
        """
        working_folder = filedialog.askdirectory()
        self.folderPath.set(working_folder)
        os.chdir(working_folder)

    def get_basement_directory(self):
        """
        Get the installation directory of the software Basement
        """
        basement_folder = filedialog.askdirectory()
        self.folderPath_base.set(basement_folder)

    @classmethod
    def help_func(cls):
        """
        Opens the 'Basegembeta1_Tutorial.pdf' file
        """

        os.startfile(str(dirname(dirname(abspath(__file__))))
                     + '\\basegembeta1\\Basegembeta1_Tutorial.pdf')

    def writing_paths(self):
        """
        Write the installation directory of Basement in the 'backup.txt' file
        The mentioned directory is indicated only  once by the user
        """
        with open('backup.txt', mode='w') as f:
            f.write(self.folderPath_base.get())

    @classmethod
    def erase_batch_file(cls):
        """
        The content of the Simulation_base.bat is erased when the user press
        the button 'Clean batch file'
        """
        try:
            with open('Simulation_base.bat', mode='r+') as f:
                f.truncate(0)
                print('Simulation_base.bat was cleaned')
        except Exception:
            print('File not found')

    def copy_q_files(self):
        """
        Copy the 'results.json' and 'simulation.json' files from the
        directory of the App to the indicated working directory
        """

        if os.path.isfile('results.json') and os.path.isfile('simulation.json'):
            print(
                'results.json and simulation.json are already in the selected '
                'working directory')
            pass
        else:
            # get the parent directory of the python file regardless of the
            # current working directory
            parent_directory = dirname(dirname(abspath(__file__)))
            # Copy the results.json and simulation.json files to current
            # working directory
            shutil.copy(parent_directory + '\\basegembeta1\\results.json',
                        self.folderPath.get())
            shutil.copy(parent_directory + '\\basegembeta1\\simulation.json',
                        self.folderPath.get())

    @time_func
    def basement_generator(self):
        """
        Generation of json files with different discharge and
        default_friction values.
        Create folders to storage the created files
        together with the simulation and results filesCreates a '.bat' file
        with the instructions to run Basement in Batch mode.

        Parameters
        ----------
        :input_string: STR from  entry box
        :q_ini: STR form tkinter entry box
        :friction_ini: STR from tkinter entry box
        :friction: Boolean, checkbox, if Yes takes into account different
            default_friction-values
        :input_friction: STR from tkinter entry box
        :batch: Boolean, if Yes execute the batch file that contains the running
            instructions of the created files
        """

        # The values must be provided with a space between them
        input_string = self.input_string.get()
        q_ini = self.q_ini.get()
        friction_ini = self.friction_ini.get()
        friction = self.friction.get()

        # The values are converted into a list
        flows = input_string.split()

        # rename the initial model.json to model_coy.json  file in order to
        # get files model.json in the created folders
        os.rename('model.json', 'model_copy.json')

        if friction is True:
            input_dif_friction = self.input_friction.get()
            list_input_friction = input_dif_friction.split()
            pass
        else:
            list_input_friction = []
            for element in range(len(flows)):
                list_input_friction.append(friction_ini)
            pass

        with open('backup.txt', mode='r') as f:
            base_path_intxt = f.readline()

        for i, j in zip(flows, list_input_friction):
            # The gson file originally created is opened
            first_json = 'model_copy.json'

            with open(first_json, 'r') as infile, \
                    open("model.json", 'w') as outfile:
                model_json = infile.read()

                # The variable 'json_flows' receives the flow values of the
                # list
                json_flows = '"discharge": {0}'.format(i)

                # The variable 'json_default_friction' receives the values of
                # friction coefficients of the list
                json_default_friction = '"default_friction": {0}'.format(j)

                # The original discharge is replaced by the values of the
                # provided list
                model_json = model_json.replace(
                    '"discharge": {0}'.format(q_ini), json_flows). \
                    replace('"default_friction": {0}'.format(friction_ini),
                            json_default_friction)

                # The outfile is written
                outfile.write(model_json)
            infile.close()
            outfile.close()

            # The points are replaced by '_' since Basement does not recognize
            # points in folder names
            new_folder = 'Q' + str(i.replace('.', '_'))

            # The new folder is created
            os.makedirs(new_folder)

            # The model.json file modified is moved to the created New folder
            destination = new_folder
            source = 'model.json'
            shutil.move(source, destination)

            # The simulation and the results file are copied into the
            # respective folders
            shutil.copy('results.json', destination)
            shutil.copy('simulation.json', destination)

            new_folder_path = os.path.abspath(new_folder)

            with open("Simulation_base.bat", 'a') as file:
                string1 = str(
                    '"{0}/BMv3_BASEplane_setup.exe" ^\n-f ' + new_folder_path
                    + '\\model.json ^\n-o ' + new_folder_path
                    + '\\mySim_run.h5\n').format(str(base_path_intxt))
                string2 = str(
                    '"{0}/BMv3_BASEplane_omp.exe" ^\n-f ' + new_folder_path
                    + '\\simulation.json ^\n-r ' + new_folder_path
                    + '\\mySim_run.h5 ^\n-o ' + new_folder_path
                    + '\\mySim_run_results.h5 -p -n 4\n'). \
                    format(str(base_path_intxt))
                string3 = str(
                    '"{0}/BMv3_BASEplane_results.exe" ^\n-f ' + new_folder_path
                    + '\\results.json ^\n-r ' + new_folder_path
                    + '\\mySim_run_results.h5 ^\n-o ' + new_folder_path
                    + '\\mySim_output\nPAUSE\n').format(str(base_path_intxt))

                file.write("%s\n%s\n%s\n" % (string1, string2, string3))

        batch = self.batch.get()

        if batch is True:
            subprocess.call([os.path.abspath('Simulation_base.bat')])
            replace_path.path_in_files()
            pass

        @change_name_file
        def change_json_name(a, b):
            return print('model_copy.json has changed to model.json')

        change_json_name('model_copy.json', 'model.json')

    print(basement_generator.__doc__)


if __name__ == '__main__':
    root = tk.Tk()
    BasementApplication(root)
    root.mainloop()
