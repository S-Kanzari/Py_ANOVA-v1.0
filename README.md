# Py_ANOVA-v1.0
Boxplots with ANOVA Statistical Significance (Tukey &amp; Dunn)


DESCRIPTION
-----------
This script reads a dataset from an Excel (.xlsx) file containing group labels
and numerical values. It performs the following:

1. ANOVA followed by Tukey's HSD post hoc test (parametric)
2. Kruskal-Wallis test followed by Dunn's test (non-parametric)
3. Generates two horizontal boxplots:
   - One with significance letters based on Tukey HSD
   - One with significance letters based on Dunn's test

All significance letters are shown on the plot next to each box.
Fonts are set to Times New Roman, size 16.

REQUIREMENTS
------------
Install the following Python packages (if not already installed):

pip install pandas openpyxl seaborn matplotlib scipy statsmodels scikit-posthocs

DATA FORMAT
-----------
Your Excel file must have at least two columns:
- Column 1: Group labels (e.g., Treatment names)
- Column 2: Numeric values (e.g., Measurements)

Example:
+--------+--------+
| Group  | Value  |
+--------+--------+
| A      | 12.5   |
| A      | 13.1   |
| B      | 10.2   |
| C      | 15.3   |
| ...    | ...    |
+--------+--------+

Make sure the column names in the Excel file match those defined in the script:
- group_col = 'Group'
- value_col = 'Value'

HOW TO USE
----------
1. Place your Excel file in the same directory as the script.
2. Open the script in Spyder (or any Python IDE).
3. Replace the file name in this line:
      file_path = 'your_file.xlsx'
4. Run the script.

OUTPUT
------
- Two horizontal boxplots will be shown:
   1. With Tukey HSD significance letters
   2. With Dunn’s test significance letters
- Statistical results are printed to the console:
   - ANOVA table
   - Tukey HSD results
   - Kruskal-Wallis test result
   - Dunn’s test p-value matrix

AUTHOR
------


[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15815362.svg)](https://doi.org/10.5281/zenodo.15815362)


Date: 2025
