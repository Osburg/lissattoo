import argparse
import os

import matplotlib.pyplot as plt
import numpy as np

params = np.array([[1, 0, 1, 0], [1, 2 / 3 * np.pi, 1, 0], [1, 4 / 3 * np.pi, 1, 0]])


def R(theta):
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])


def v(theta):
    return R(theta) @ np.array([[1], [0]])


def lissajous(params: np.ndarray):
    def f(t):
        return np.sum(
            [
                params[i, 0]
                * v(params[i, 1])
                * np.sin(params[i, 2] * t + 2 * np.pi / 360 * params[i, 3])
                for i in range(params.shape[0])
            ],
            axis=0,
        )

    coords = np.array([f(t) for t in np.linspace(0, 2 * np.pi, 1000)])
    return coords


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Lissattoo",
        description="This program creates your custom Lissajous-Figure tattoo",
    )
    parser.add_argument(
        "--theta", nargs="+", type=float, help="Angles for the Sine wave in radians"
    )
    parser.add_argument(
        "--a", nargs="+", type=float, help="Amplitudes for the Sine wave"
    )
    parser.add_argument(
        "--omega", nargs="+", type=float, help="Frequencies for the Sine wave"
    )
    parser.add_argument("--phi", nargs="+", type=float, help="Phases for the Sine wave")
    parser.add_argument(
        "--output",
        type=str,
        help="Output file name",
        default=os.path.dirname(os.path.realpath(__file__)) + "/lissattoo.png",
    )

    args = parser.parse_args()
    params = []
    assert (
        len(args.theta)
        == len(args.a)
        == len(args.omega)
        == len(args.phi)
    ), "The number of arguments for each parameter must be the same"
    assert len(args.theta) > 0, "At least one sine wave must be provided"
    for i in range(len(args.omega)):
        params.append(
            [args.a[i], args.theta[i], args.omega[i], args.phi[i]]
        )
    params = np.array(params)

    coords = lissajous(params)
    plt.figure(figsize=(5, 5))
    plt.plot(coords[:, 0], coords[:, 1], linewidth=3, color="black")
    plt.axis("off")
    plt.savefig(args.output)
    print("Parameters for your Lissattoo:" + "\n")
    for i in range(params.shape[0]):
        print(
            f"Component {i+1}: Amplitude = {params[i, 0]}, Theta = {params[i, 1]}, Omega = {params[i, 2]}, Phi = {params[i, 3]}")
    print("Lissattoo saved as", args.output)
