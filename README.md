# **Tsukyomi**. A Volatility 3 GUI by Cassiopeia
<br/>
<br/>
volatility3 stable: https://github.com/volatilityfoundation/volatility3/tree/stable



## Description
<br/>
Tsukiyomi is a python program that uses Tkinter to give Volatility3 a graphical user interface. <br/>
The intent of the GUI is to make the work of an experienced user faster, while also lowering the <br/>
necessary skill level required to operate Volatility3.
<br/>
<br/>

**external packages**
required: pillow (PIL)


## Instructions for setting up volatility3 dependencies
<br/>
This is not required for volatility3 to function, but if its ignored some plugins might not work correctly.

Volatility 3 requires Python 3.7.0 or later. To install the most minimal set of dependencies (some plugins will not work) use a command such as:

pip3 install -r volatility3/requirements-minimal.txt

Alternately, the minimal packages will be installed automatically when Volatility 3 is installed using setup.py.

python3 volatility3/setup.py build 
python3 volatility3/setup.py install

To enable the full range of Volatility 3 functionality, use a command like the one below.

pip3 install -r requirements.txt

Source: https://pypi.org/project/volatility3/
more info in volatility3/README.MD
<br/>


**How to run a psscan:**

1. After starting the program, choose the OS relevant to the memory dump you wish to work on.
2. Choose memory dump file with the `Browse` button.
3. Choose `Psscan` with `no flags` in the Commands menu located in the upper center of the GUI.
4. Click the `Run` button located in the center bar of the GUI.
5. Wait for the program to complete; the result will be displayed in the text field on the lower half of the display.
6. The result of the scan can be saved by clicking the `File` menu and choosing `Save as` in the dropdown menu.

