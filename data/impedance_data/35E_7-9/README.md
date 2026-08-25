Test Run: Potentiostatic EIS
Test Date: (Enter Date)

How to use:
 1) Open Impedance_From_DTA
 2) Folders
     - data: where .DTA files should be
     - media:
          - Where code saves graphs
          - Display_Graphs.md reads the graphs
 3) Change the graph settings as desired
     - Read the parameters if you want to change any settings
 4) Run the code.


What this code does:
 1) Creates Nyquist & Bode plots
     - Creates variable amount of graphs
          - Depends on the amount of .DTA files
 2) Saves the plots
 3) Updates the Display_Graphs.md to show the created graphs

This is an impedance test using a Gamry Reference 3000.

R-V Data was collected using the BK Analyzer BA6010

Test Settings
 - DC Voltage (V): 0 vs. EOC
 - AC Voltage (mV rms): 10
 - Initial Freq (Hz): 10000
 - Final Freq (Hz): .01
 - Points/decade: 10
 - Area (cm^2): 2.54
 - Conditioning: Off
 - Init. Delay: 600s
 - Drift Correction: On
 - THD: Off
 - Estimated Z (Ohms): .1
 - Open Circuit (V): 

 - Test Notes: (Copy and Paste if needed)
    - Potentiostatic EIS Data Test performed on (Cell Type) battery.
    - 10 AC mV rms performed on 3/30/26
    - Battery # (Cell Type)
    - Tested Samsung (Cell Type) battery
    - Custom Battery Holder Tray. Wood Base w/ reference alligator clips connected to the center of the banana plug.
    - No Floating Ground
    - No Faraday Cage
