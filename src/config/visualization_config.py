import matplotlib.pyplot as plt
import seaborn as sns

# TODO: Change the default settings for the visualization!

# set default matplotlib parameters
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['lines.linewidth'] = 2

# set Seaborn style
sns.set_theme(style="whitegrid", palette="muted", rc=plt.rcParams)

# shared color palettes
COLOR_PALETTE = sns.color_palette("muted")
CUSTOM_PALETTE = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F", "#EDC948"]
sns.set_palette(CUSTOM_PALETTE)

def initialize_viz():
    """Initialize the visualization settings."""
    plt.rcParams.update(plt.rcParams) 
