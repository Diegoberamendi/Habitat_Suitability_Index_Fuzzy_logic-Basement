import pathlib


def path_in_files():
    """
    Delete paths from the .xdmf files in the working directory
    Parameters
    ----------
    :path_base_folders: gets the current working directory
    :content: Read the lines of the .xdmf files in the working directory

    Returns
    --------
    :ouput_remp: replace the paths in the .xdmf files in the working directory

    """
    # Get current directory
    path_base_folders = pathlib.Path().absolute()

    # Find the .xdmf files in the current directory and delete the paths
    for item in path_base_folders.glob('**/*'):
        if item.suffix == '.xdmf':
            with open(item, 'r') as output:
                print(item)
                content = output.readlines()

            with open(item, 'w') as output_remp:
                for line in content:
                    output_remp.write(line.replace(str(item.parent) + '\\', ''))

    return print('The paths from .xdmf files were deleted')


if __name__ == '__main__':
    path_in_files()
