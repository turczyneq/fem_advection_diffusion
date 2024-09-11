import pychast.generate_trajectories as gen_traj
import pychast.process_trajectories as proc_traj
import pychast.simpson_integration as simpson
import udajki as loc
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Arc
import numpy as np
import time


def visualise_trajectories(
    peclet,
    ball_radius,
    floor_r = 0.3,
    floor_h = 5,
    r_mesh = 0.01,
    trials = 10,
    display_traj = 10):

    if display_traj == 'all':
        display_traj = int(trials*floor_r/r_mesh)
    else:
        pass

    initial = gen_traj.construct_initial_condition(
        floor_r=floor_r, floor_h=floor_h, r_mesh=r_mesh, trials=trials
    )
    
    def drift(q):
        return gen_traj.stokes_around_sphere(q, ball_radius)

    collision_data = gen_traj.simulate_with_trajectories(
        drift=drift,
        noise=gen_traj.diffusion_function(peclet=peclet),
        initial=initial,
        floor_h=floor_h,        
    )

    cmap = mpl.colormaps['viridis']

    plt.figure(figsize=(12, 10))

    trajectories = collision_data["trajectories"]
    for i in range(display_traj):

        r = (trajectories[i, :, 0] ** 2 + trajectories[i, :, 1] ** 2) ** 0.5
        z = trajectories[i, :, -1]
        when_hit = np.concatenate((np.where(r**2 + z**2 < 1)[0],[-1]))[0]

        r = r[:when_hit]
        z = z[:when_hit]

        if collision_data["ball_hit"][i]:
            color = "#2a2"
        elif collision_data["something_hit"][i]:
            color = "#2a2"
        else:
            color = "#a22"

        if i%2:
            plt.plot(r, z, color=color)
        else:
            plt.plot(-r, z, color=color)
        # plt.scatter(r[-1], z[-1], s=8, color="k", zorder=5)
        # plt.scatter(r[0], z[0], s=8, color="k", zorder=5)

    plt.gca().add_artist(plt.Circle((0, 0), ball_radius, edgecolor = 'k', facecolor="#fff" , hatch = "///"))
    plt.gca().add_artist(Arc((0, 0), 2, 2, color='k', linestyle = '--', theta1=0, theta2=360))

    # plt.text(1,-1, f"Pe = 10^{int(np.log10(peclet))}")

    plt.gca().set_aspect('equal', 'box')  # 'equal' ensures that one unit in x is equal to one unit in y
    plt.tight_layout()
    plt.xlim(-3, 3)
    plt.ylim(-2.5, 5.5)

    # plt.savefig("traj_visualize.svg", format='svg')
    plt.show()

visualise_trajectories(500, 0.7, floor_r = 1, r_mesh = 0.01, trials = 1, display_traj = 'all')