import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from itertools import groupby

def clift_approximation(pe):
    # mod_sh = sh
    return (1 / 2) * (1 + (1 + 2 * pe) ** (1 / 3))

def our_approx(pe, r_particle):
    return clift_approximation(pe) + (pe/4)*(r_particle**2)*((3-r_particle)/2)

parent_dir = Path(__file__).parent
fem_path = parent_dir / "fem_pe_vs_sh.csv"
fem = np.loadtxt(fem_path, delimiter=",", skiprows=1)
# we have to split into listst wiht different r_syf
fem_sorted = fem[fem[:, 1].argsort()]
fem_grouped = groupby(fem_sorted, key=lambda x: x[1])
fem_plt = {k: np.array([[x, y, z/(clift_approximation(x) + x*((2 + y)*(1 - y)**2)/8)] for x, y, z in g]) for k, g in fem_grouped}
# fem_plt = {k: np.array([[x, y, z/(1 + x*((2 + y)*(1 - y)**2)/8)] for x, y, z in g]) for k, g in fem_grouped}


py_path = parent_dir / "py_pe_vs_sh.csv"
py = np.loadtxt(py_path, delimiter=",", skiprows=1)
# we have to split into listst wiht different r_syf
py_sorted = py[py[:, 1].argsort()]
py_grouped = groupby(py_sorted, key=lambda x: x[1])
# py_plt = {k: np.array([[x, y, z/(1 + x*((2 + y)*(1 - y)**2)/8)] for x, y, z in g]) for k, g in py_grouped}
py_plt = {k: np.array([[x, y, z/(clift_approximation(x) + x*((2 + y)*(1 - y)**2)/8)] for x, y, z in g]) for k, g in py_grouped}


peclet_values = np.logspace(-1, 13, 300)
analytic_clift = clift_approximation(peclet_values)


# Plot all data

fontsize=27
plt.figure(figsize=(12, 7))
plt.rcParams.update({"text.usetex": True, "font.family": "Cambria"})

# # Plot Clift data
# plt.plot(
#     peclet_values,
#     analytic_clift,
#     label="Clift et al. (analytic)",
#     color="k",
#     linestyle="-",
#     linewidth=2,
#     zorder = 0
# )

num = 0
for data in fem_plt.values():
    # Plot our data
    plt.scatter(
        data[:, 0],
        data[:, 2],
        label=f"$\\beta = {round(10000*(1-data[1,1]))/10000}$",
        color=f"C{num}"
    )
    num +=1

num = 0
for data in py_plt.values():
    # Plot our data
    plt.scatter(
        data[:, 0],
        data[:, 2],
        color=f"C{num}",
        facecolors='none'
    )
    num +=1

# for limits, modified sherwood should be 1
plt.plot(
    peclet_values,
    [1 for x in peclet_values],
    color="k",
    linestyle="--",
    linewidth=2,
    zorder = 0
)


#add dummy plt to make legend

plt.scatter(
    [0],
    [0],
    label="FEM",
    color="k"
)

plt.scatter(
    [0],
    [0],
    label=r"pychastic",
    color="k",
    facecolors='none'
)

# Logarithmic scale
plt.xscale("log")
plt.xlim(0.1, 10**12)
plt.ylim(0.9, 1.4)
plt.xticks(fontsize=fontsize)
plt.yticks(fontsize=fontsize)

# Labels and Title
plt.xlabel(r"Peclet Number $\left(Pe\right)$", fontsize=fontsize)
plt.ylabel(r"Proposed approach $\Phi/\left(\Phi_{\textrm{D}} Sh_{\textrm{Cl}}+\Phi_{\textrm{A}}\right)$", fontsize=fontsize)

# Legend
plt.legend(fontsize=fontsize, frameon=False, loc = 1)
plt.tight_layout()
tosave = parent_dir.parent / "ignore/mod_better_sh_vs_pe.pdf"
plt.savefig(tosave)

# Show plot
plt.show()