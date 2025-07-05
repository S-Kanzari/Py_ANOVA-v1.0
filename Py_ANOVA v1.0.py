import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import MultiComparison
from scipy.stats import kruskal
import scikit_posthocs as sp
import itertools

# ----- Settings -----
plt.rcParams.update({'font.family': 'Times New Roman', 'font.size': 16})
file_path = 'Climat_DATA_Example.xlsx'         # Replace with your Excel file path
group_col = 'Region'                  # Replace with your group column name
value_col = 'T'                  # Replace with your value column name

# ----- Load Data -----
df = pd.read_excel(file_path)
df = df[[group_col, value_col]].dropna()

# ----- ANOVA + Tukey HSD -----
anova_model = ols(f'{value_col} ~ C({group_col})', data=df).fit()
anova_table = sm.stats.anova_lm(anova_model, typ=2)
print("ANOVA Table:\n", anova_table)

mc = MultiComparison(df[value_col], df[group_col])
tukey = mc.tukeyhsd()
print("\nTukey HSD:\n", tukey)

# ----- Significance Letters (Tukey) -----
def get_significance_letters(mc, reject):
    groups = list(mc.groupsunique)
    comparisons = list(itertools.combinations(groups, 2))
    letters_dict = {g: set([g]) for g in groups}
    for (g1, g2), sig in zip(comparisons, reject):
        if not sig:
            merged = letters_dict[g1].union(letters_dict[g2])
            for g in merged:
                letters_dict[g] = merged
    unique_sets = {}
    letters = {}
    current_letter = ord('a')
    for g in sorted(groups):
        key = tuple(sorted(letters_dict[g]))
        if key not in unique_sets:
            unique_sets[key] = chr(current_letter)
            current_letter += 1
        letters[g] = unique_sets[key]
    return letters

tukey_letters = get_significance_letters(mc, tukey.reject)

# ----- Plot 1: Tukey HSD Horizontal Boxplot -----
plt.figure(figsize=(10, 6))
sns.boxplot(y=group_col, x=value_col, data=df, palette="pastel", orient='h')
for i, group in enumerate(sorted(df[group_col].unique())):
    x_max = df[df[group_col] == group][value_col].max()
    plt.text(x_max * 1.01, i, tukey_letters[group], va='center', ha='left')
plt.title('Horizontal Boxplot with Tukey Significance Letters')
plt.ylabel(group_col)
plt.xlabel(value_col)
plt.tight_layout()
plt.show()

# ----- Kruskal-Wallis -----
grouped = [g[value_col].values for _, g in df.groupby(group_col)]
h_stat, p_val = kruskal(*grouped)
print(f"\nKruskal-Wallis H = {h_stat:.4f}, p = {p_val:.4f}")

# ----- Dunn’s Test -----
dunn = sp.posthoc_dunn(df, val_col=value_col, group_col=group_col, p_adjust='bonferroni')
print("\nDunn’s Test:\n", dunn)

# ----- Significance Letters (Dunn) -----
def get_dunn_letters(dunn_df, alpha=0.05):
    groups = dunn_df.columns.tolist()
    letters_dict = {g: set([g]) for g in groups}
    for g1 in groups:
        for g2 in groups:
            if g1 != g2 and dunn_df.loc[g1, g2] > alpha:
                merged = letters_dict[g1].union(letters_dict[g2])
                for g in merged:
                    letters_dict[g] = merged
    unique_sets = {}
    letters = {}
    current_letter = ord('a')
    for g in sorted(groups):
        key = tuple(sorted(letters_dict[g]))
        if key not in unique_sets:
            unique_sets[key] = chr(current_letter)
            current_letter += 1
        letters[g] = unique_sets[key]
    return letters

dunn_letters = get_dunn_letters(dunn)

# ----- Plot 2: Dunn’s Test Horizontal Boxplot -----
plt.figure(figsize=(10, 6))
sns.boxplot(y=group_col, x=value_col, data=df, palette="pastel", orient='h')
for i, group in enumerate(sorted(df[group_col].unique())):
    x_max = df[df[group_col] == group][value_col].max()
    plt.text(x_max * 1.01, i, dunn_letters[group], va='center', ha='left')
plt.title('Horizontal Boxplot with Dunn Significance Letters')
plt.ylabel(group_col)
plt.xlabel(value_col)
plt.tight_layout()
plt.show()
