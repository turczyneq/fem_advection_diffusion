import pychast.generate_trajectories as gen_traj
import pychast.process_trajectories as proc_traj
import pychast.simpson_integration as simpson
import udajki as loc
import matplotlib.pyplot as plt
import numpy as np
import time


def sherwood_from_simpson(peclet,
    ball_radius,
    trials=100,
    floor_h=5,):

    def fun(x):
        value = gen_traj.hitting_propability_at_x(x, peclet, ball_radius, trials = trials)
        ver, vez = loc.velocities(x, floor_h, ball_radius)
        return 2 * np.pi * x * value * vez

    start = time.time()
    '''
    find the radius where propability is around 0.01
    bin search works only for increasing function so search is for -fun and we are looking for -0.01
    '''
    def to_search(x):
        value = gen_traj.hitting_propability_at_x(x, peclet, ball_radius, trials = 400)
        return -value
    edge = loc.binary_search(to_search, -0.01, 0, 0.5, tol = 10**(-3) )
    end = time.time()
    print(f"edge {end - start}, equal {edge}")


    absolute_tolerance = 1e-5

    start = time.time()

    internal = simpson.integrate_with_adaptive_simpson(fun, 0, edge , absolute_tolerance)

    end = time.time()
    print(f"internal {end - start}, equal {internal}")
    
    start = time.time()

    external = simpson.integrate_with_adaptive_simpson(fun, edge, 0.5 , absolute_tolerance)

    effective_area = internal + external
    end = time.time()
    print(f"external {end - start}, equal {external}")


    r_eff = (effective_area / np.pi) ** 0.5

    sherwood = (peclet / 4) * ((r_eff) ** 2)
    return sherwood

def sherwood_from_peclet(
    peclet,
    ball_radius,
    trials=100,
    r_mesh=0.1,
    floor_r=5,
    floor_h=5,):
        
    single_pe_trajectories = gen_traj.generate_trajectories_multiply(
    peclet,
    ball_radius,
    trials=trials,
    r_mesh=r_mesh,
    floor_r=floor_r,
    floor_h=floor_h,)

    sh_number = proc_traj.sherwood(single_pe_trajectories,peclet,ball_radius,floor_h = floor_h)

    return sh_number

def visualise_trajectories(
    peclet,
    ball_radius,
    floor_r = 0.3,
    floor_h = 5,
    r_mesh = 0.01,
    trials = 10,
    display_traj = 10):

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

    #plt.figure(figsize=(12, 10))

    trajectories = collision_data["trajectories"]
    for i in range(display_traj):
        r = (trajectories[i, :, 0] ** 2 + trajectories[i, :, 1] ** 2) ** 0.5
        z = trajectories[i, :, -1]

        if collision_data["ball_hit"][i]:
            color = "#2a2"
        elif collision_data["something_hit"][i]:
            color = "#aa2"
        else:
            color = "#a22"

        plt.plot(r, z, color=color)
        plt.scatter(r[-1], z[-1], s=8, color="k", zorder=5)
        plt.scatter(r[0], z[0], s=8, color="k", zorder=5)

    circle = plt.Circle((0, 0), 1, color="#222", fill=False)
    plt.gca().add_artist(circle)
    circle = plt.Circle((0, 0), ball_radius, color="#666", fill=False)
    plt.gca().add_artist(circle)

    plt.text(1,-1, f"Pe = 10^{int(np.log10(peclet))}")

    plt.gca().set_aspect("equal")
    plt.axis([0, 2, -2, 0])

    # plt.savefig("traj_visualize.svg", format='svg')
    plt.show()

visualise_trajectories(10**6, 0.995, floor_r = 0.002, r_mesh = 0.0005)

visualise_trajectories(10**9, 0.995, floor_r = 0.002, r_mesh = 0.0005)

# print(gen_traj.hitting_propability_at_x(0.0005, 10**9, 0.999, trials = 400))

# pe_list = [10**i for i in range(5,10)]

# ball_list = []
# for i in range(-3,0):
#     ball_list = ball_list + [(10**i)*ball for ball in [1, 2, 5]]
# ball_list = ball_list[:-1]


# output_file = f"numerical_results/sim_vs_pych_test.txt"
# with open(output_file, 'w') as f:
#     f.write("Peclet\tr_syf\tSherwood_simpson\tSherwood_pychast\n")

# for j in range(len(ball_list)):
#     for n in range(len(pe_list)):
#         peclet = pe_list[n]
#         ball_radius = 1 - ball_list[j]
#         print(f"radius = {ball_radius}, peclet = {peclet}")
#         femsol = sherwood_from_simpson(peclet, ball_radius, trials = 400)
#         # trajsol = sherwood_from_peclet(peclet, ball_radius, trials = 400, floor_r = ball_list[j]*2, r_mesh = ball_list[j]*2/100)
#         # with open(output_file, 'a') as f:
#         #     f.write(f"{peclet}\t{ball_list[j]}\t{femsol}\t{trajsol}\n")


# print(f"{sherwood_from_simpson(100000, 0.999, trials = 400)}, {sherwood_from_peclet(100000, 0.999, trials = 400, floor_r = 0.001*50, r_mesh = 0.001*50/50)}")