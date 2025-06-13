# VOC Analyzer - Pig Behavior Prediction System

## Project Objectives
1. To automate renaming, sorting, and restructuring raw data files from the VOC analysers ready to be imported into the software.
2. Create backend software that extracts sensor data from a large amount of text files and stores the data efficiently to the hard disk to eliminate the need to import the data every time the software is executed.
3. Pre-process data by normalisation and standardization and detect and eliminate corrupt data points and abnormal data spikes.
4. Create frontend software with a user-friendly GUI framework to visually plot the data display test information allowing a user to recognize and spot visual trends.
5. Use dimensionality reduction techniques such as PCA and t-SNE to effectively visualize clusters or groups of data points and their relative proximities and display results.
6. Recognize data patterns using this software and pair them with conditions altered in each pen.

## Project Structure
The project consists of several key components:

### Core Python Files
- `main.py` - Main application entry point
- `gui.py` - GUI implementation and user interface
- `datahandler.py` - Data processing and management
- `plot.py` - Data visualization and plotting functionality
- `PCA.py` - Principal Component Analysis implementation
- `openfile.py` - File handling and data import functionality
- `train.py` - Training module for the prediction system

### Resource Files
- `main.ui` - Qt Designer UI file
- `resource.qrc` - Qt resource file
- `logo.png` - Application logo
- `icon.ico` - Application icon

### Build and Distribution
- `build/` - Build directory
- `dist/` - Distribution directory
- `main.spec` - PyInstaller specification file
- `gui.spec` - GUI PyInstaller specification file
- `VOC Tool.spec` - Main application specification file
- `build.bat` - Build script

### Documentation
- `README.md` - Project documentation

## Installation
1. Ensure Python 3.x is installed on your system
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage
1. Run the main application:
```bash
python main.py
```

## Dependencies
The project dependencies are listed in `requirements.txt`. Key dependencies include:
- PyQt6 for the GUI
- NumPy for numerical computations
- Pandas for data manipulation
- Matplotlib for plotting
- scikit-learn for machine learning algorithms

## Contributing
This project is part of an undergraduate Bachelor of Engineering project. For any questions or contributions, please contact the author.

## License
This project is proprietary and confidential. All rights reserved.
