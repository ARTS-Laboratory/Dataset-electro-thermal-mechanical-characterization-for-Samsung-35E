# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 11:49:10 2026
Modified last on Tues August 11 16:32:21 2026

Creates the Bode and Nyquist Plots Automatically
Only needed file. 
        
@author: Charlie Buren
"""

#%% Setup
import os
import gamry_parser as parser
import matplotlib.pyplot as plt
from pathlib import Path

# =============================================================================
# User Inputs
# =============================================================================
# Paths
DTA_FOLDER = Path("data")           # Path to where .DTA files are stored
GRAPH_FOLDER = Path("media")        # Path to where graphs are created/stored
MD_PATH = Path('Display_Graphs.md') # Path to the .md file

# Saving
SAVE_TYPE = '.png'                  # What to save the plots as
SAVE_TOGGLE = True                  # Do you want to save the plots
SAVE_GENERIC_NAME = False           # Leave as False unless you want to have save as Test#                    
SHOW_GRAPHS = False                 # Do you want the graphs to pop open in new window

# Graphing 
FIGSIZE = (6.5, 6)


#%% Defs
def load_dta_files(
        path: Path,
        extension: str | None = '.DTA'
    ) -> tuple [dict, list, int]:
    """
    Takes .DTA files and builds a dict of all the dataset from all tests

    Args:
        path (Path): path to the folder with test data
        extension (str, optional): str of file extension. Defaults to .DTA

    Returns:
        data (dict): all data in tests
        test_names (list): all the names of the tests
        file_count (int): number of files in data folder
    """
    gp = parser.GamryParser()

    # Count DTA files
    file_count = int(len([
        file for file in os.listdir(path)   # Find all files in DTA path
        if file.endswith(extension)]))      # Count only .DTA files

    # Get all file paths
    path = list(path.glob(f'*{extension}'))

    # Convert paths to str
    test_names = [(file.name).replace(extension, '') for file in path]

    ''' Create Data Dict '''
    data = {}
    for i in range(file_count):
        # Load the file
        gp.load(filename=path[i])

        # Append the data
        df_name = test_names[i]             # Get name of test for dict
        data[df_name] = gp.get_curve_data() # Add data to dict

    return data, test_names, file_count


def create_plots(
        data: dict,
        output_folder: Path,
        colors: list | None = plt.rcParams['axes.prop_cycle'].by_key()['color'],
        save_type: str | None = '.png',
        save_toggle: bool | None = False,
        save_to_md: bool | None = False,
        show_graphs: bool | None = False,
        ylabel_mag: str | None = 'Zmod (Ω)',
        ylabel_phase: str | None = 'Zphz (°)',
        ylabel_nyquist: str | None = '-Zimag (Ω)',
        xlabel_nyquist: str | None = 'Zreal (Ω)',
        xlabel_phase: str | None = 'Frequency (Hz)'
    ):
    """
    Plots a bode & nyquist chart based off of loaded impedance files.

    Args:
        data (dict): dataset off all impedance tests
        out_folder (Path): path to folder where graphs will be saved
        colors (list, optional): list of colors plotted. Defaults to axes.prop_cycle list from matplotlib
        save_type (str, optional): str for graph saving file extension. Defaults to .png
        save_toggle (bool, optional): bool for saving graphs. Defaults to False.
        save_to_md (bool, optional): bool for if you want to export the files to .MD. Defaults to False.
        show_graphs (bool, optional): bool for if you want to see graphs. Defaults to False.
        ylabel_mag (str, optional): str for labeling top y-axis bode plot. Defaults to 'Zmod (Ω)'.
        ylabel_phase (str, optional): str for labeling bot y-axis bode plt. Defaults to 'Zphz (°)'.
        ylabel_nyquist (str, optional): str for labeling y-axis of nyquist plot. Defaults to '-Zimag (Ω)'.
        xlabel_nyquist (str, optional): str for labeling x-axis nyquist plot. Defaults to 'Zreal (Ω)'.
        xlabel_phase (str, optional): str for labeling x-axis bode plot. Defaults to 'Frequency (Hz)'.
    Graphs:
        Bode plots are a log plot that shows a systems resistance to AC across frequency spectrums
            - Axis's:
                - X-axis: Frequency tested at
                - Top y-axis: Zmod (Ω) or abs value of impedance
                - Bot y-axis: Zphz (°) or lag between current & voltage signals
            - One for each file in folder
            - Overlay plot of each file
        Nyquist plots is a plot where each point is a response at a specific AC frequency
            - Axis's 
                - X-axis: Zreal (Ω) or real resistance of system
                - Y-axis: -Zimag (Ω) or imaginary reactance of system
            - One for each file in folder
            - Overlay plot of each file
    """
    ''' Initialize Overlay Plots '''
    # Bode 
    Bode_Overlay = plt.figure(layout="constrained")
    Plot_Overlay = Bode_Overlay.subplots(2,1, squeeze = False)

    Overlay_Mag = Plot_Overlay[0,0]
    Overlay_Phase = Plot_Overlay[1,0]

    # Nyquist
    Nyquist_Over_Fig, Nyquist_Over_Ax = plt.subplots()

    loop_count = 0 # Count loops

    ''' Plotting '''
    for (key, df), colors in zip(data.items(), colors):
        loop_count = loop_count + 1 # Add 1 for each loop

        ''' Variables '''
        Freq = df['Freq'].values
        Zmod = df['Zmod'].values
        Zphz = df['Zphz'].values
        Zreal = df['Zreal'].values
        Zimag = df['Zimag'].values

        ''' Bode Plot '''
        Bode_Plot = plt.figure(layout="constrained")
        Plot_Array = Bode_Plot.subplots(2,1, squeeze = False)

        # Title
        bode_title = f'{key} Bode Plot'
        Bode_Plot.suptitle(bode_title)

        # Mag Graph (Top)
        Bode_Mag = Plot_Array[0,0]
        Bode_Mag.semilogx(Freq, Zmod, color = colors, linestyle = '-', label = f'{key} Mag')
        Bode_Mag.set_ylabel(ylabel_mag)
        Bode_Mag.legend()

        # Phase Graph (Bot)
        Bode_Phase = Plot_Array[1,0]
        Bode_Phase.semilogx(Freq, Zphz, color = colors, linestyle = '-', label = f'{key} Phase')
        Bode_Phase.set_ylabel(ylabel_phase)
        Bode_Phase.set_xlabel(xlabel_phase)
        Bode_Phase.legend()

        # Overlay
        Overlay_Mag.semilogx(Freq, Zmod, color = colors, linestyle = '-', label = f'{key}')
        Overlay_Phase.semilogx(Freq, Zphz, color = colors, linestyle = '-', label = f'{key}')

        ''' Nyquist Plot '''
        # Create Nyquist Plot
        Nyquist_Fig, Nyquist_Ax = plt.subplots()

        # Title
        nyquist_title = f'{key} Nyquist Plot'
        Nyquist_Fig.suptitle(nyquist_title)

        # Nyquist Plot
        Nyquist_Ax.plot(Zreal, Zimag, color = colors, linestyle = '-', label = key)
        Nyquist_Ax.set_ylabel(ylabel_nyquist)
        Nyquist_Ax.set_xlabel(xlabel_nyquist)
        Nyquist_Ax.grid(True, alpha = .3)
        Nyquist_Ax.invert_yaxis()
        Nyquist_Ax.legend()

        # Overlay
        Nyquist_Over_Ax.plot(Zreal, Zimag, color = colors, linestyle = '-', label = key)

        ''' Saving & Showing '''
        if output_folder.exists():
            if save_toggle:
                if save_to_md:
                    bode_save = output_folder / f'Test{loop_count}_Bode{save_type}'
                    Bode_Plot.savefig(bode_save)

                    nyquist_save = output_folder / f'Test{loop_count}_Nyquist{save_type}'
                    Nyquist_Fig.savefig(nyquist_save)

                    # Printing
                    print(f'Test {loop_count} bode & nyquist plots were created.')
                    print(f' - Saved at {os.path.abspath(output_folder)}')

                if not save_to_md:
                    bode_save = output_folder / f'{key}_Bode{save_type}'
                    Bode_Plot.savefig(bode_save)

                    nyquist_save = output_folder / f'{key}_Nyquist{save_type}'
                    Nyquist_Fig.savefig(nyquist_save)

                    # Printing
                    print(f'{key} bode & nyquist plots were created.')
                    print(f' - Saved at {os.path.abspath(output_folder)}')
        if not output_folder.exists():
            raise FileNotFoundError(f"The path {os.path.abspath(output_folder)} doesn't exist.")

    ''' Overlays '''
    # Titles
    Bode_Overlay.suptitle('Overlay Bode Plot')
    Nyquist_Over_Fig.suptitle('Overlay Nyquist Plot')

    # Labels
    Overlay_Mag.set_ylabel(ylabel_mag)
    Overlay_Phase.set_ylabel(ylabel_phase)
    Overlay_Phase.set_xlabel(xlabel_phase)

    Nyquist_Over_Ax.set_ylabel(ylabel_nyquist)
    Nyquist_Over_Ax.set_xlabel(xlabel_nyquist)
    Nyquist_Over_Ax.grid(True, alpha = .3)
    Nyquist_Over_Ax.invert_yaxis()

    Overlay_Phase.legend()
    Nyquist_Over_Ax.legend()

    if output_folder.exists():
        if save_toggle:
            bode_save = output_folder / f'Overlay_Bode{save_type}'
            Bode_Overlay.savefig(bode_save)
    
            nyquist_save = output_folder / f'Overlay_Nyquist{save_type}'
            Nyquist_Over_Fig.savefig(nyquist_save)
    
            # Printing
            print(f'Overlay bode & nyquist plots were created.')
            print(f' - Saved at {os.path.abspath(output_folder)}')

        if not save_toggle:
            print('Saving of the graphs has been turned off.')
            print(' - To save use:\n\t- save_toggle = True')

    if not output_folder.exists():
        raise FileNotFoundError(f"The path {os.path.abspath(output_folder)} doesn't exist.")
    
    if show_graphs:
        plt.show()
    else:
        print('\nPlots have been hidden.')
        print(' - To show graphs: \n\t- show_graphs = True\n')


def graphs_to_md(
        md_path: Path, 
        graph_folder: Path,
        test_names: list,
    ):
    """
    Write the created graphs to the markdown file.

    Args:
        md_path (Path): path to .md file. Leave in the same directory as the file.
        graph_folder (Path): path to where the graphs are saved.
        test_names (list): list of names of cells or files tested.
    """
    if md_path.exists():
        print('File exists creating markdown file.')
        with open(md_path, 'w') as f:
            # Title
            f.write('# Potentiostatic EIS Plots\n')
            f.write('## Cells Tested: \n\t - ')
            f.write('\n\t - '.join(test_names))

            # Single Cell Show
            for i in test_names:
                f.write(f'\n\n## Cell {i} Graphs:\n')
                f.write(f'<img src="{graph_folder}/{i}_Bode.png" width="500" height="333.33" alt="{i} Bode Plot">\n')
                f.write(f'<img src="{graph_folder}/{i}_Nyquist.png" width="500" height="333.33" alt="{i} Nyquist Plot">\n\n')
            
            # Overlay
            f.write(f'\n## Overlay Graphs:\n')
            f.write(f'<img src="{graph_folder}/Overlay_Bode.png" width="500" height="333.33" alt="Overlay Bode Plot">\n')
            f.write(f'<img src="{graph_folder}/Overlay_Nyquist.png" width="500" height="333.33" alt="Overlay Nyquist Plot">\n\n')
        print('Display_Graph.md has been created.')
    if not md_path.exists():
        raise FileExistsError("Markdown file doesn't exist. Please try again.")
    

#%% Loading
data, test_names, file_count = load_dta_files(path=DTA_FOLDER)

create_plots(
    data=data,
    output_folder=GRAPH_FOLDER,
    save_type=SAVE_TYPE,
    save_toggle=SAVE_TOGGLE,
    show_graphs=SHOW_GRAPHS,
)

graphs_to_md(
    md_path=MD_PATH,
    graph_folder=GRAPH_FOLDER,
    test_names=test_names,
)