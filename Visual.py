import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mp

plt.rcParams["figure.dpi"] = 200


class Visual:
    def __init__(self, sample_point, sample_label, mu_set, cov_set):
        self.K = len(mu_set)
        self.D = len(sample_point[0])

        self.sample_point = sample_point
        self.sample_label = sample_label
        self.mu_set = mu_set
        self.cov_set = cov_set

        self.color = ("gray",    "red",    "blue",   "seagreen", "cyan",
                      "magenta", "orange", "purple", "pink")

        self.legend = [mp.Patch(color=self.color[i],
                                label="Gaussian_{}".format(i))
                       for i in range(self.K)]
        self.legend[0] = mp.Patch(color=self.color[0], label="Background")
        self.x_max = 6
        self.x_min = -6
        self.y_max = 6
        self.y_min = -6

    def plot_sample(self):
        ax, fig = None, None

        if self.D == 2:
            fig, ax = plt.subplots()
        elif self.D == 3:
            ax = plt.subplot(111, projection='3d')

        if ax is None: return
        plot_scatter(self.sample_point, self.sample_label, ax, self.color)

        plt.legend(handles=self.legend, fontsize=8)
        plt.axis([self.x_min, self.x_max, self.y_min, self.y_max])
        plt.grid()

        return plt

    def plot_DB(self, method):
        if self.D != 2: return

        fig, ax = plt.subplots()

        plot_decision_boundary(self.K, method.predict, ax, self.color,
                               self.x_min, self.x_max, self.y_min, self.y_max)
        plt.legend(handles=self.legend, fontsize=10)
        plt.axis([self.x_min, self.x_max, self.y_min, self.y_max])
        plt.grid()

        return plt


""" Help function for class 'Visual' """


def plot_scatter(sample_point, sample_label, ax, color):
    """
    Plot scatter diagram of the sample. The color of a point is match with its
    label.

    :param sample_point: [ sample_size * D ], np.array
    :param sample_label: [ sample_size * K ], np.array
    :param ax: axes object of the 'fig'
    :param color: color set. each Gaussian has one corresponding color.
    """
    color_set = []
    for n in sample_label:
        color_set.append(color[np.argmax(n)])

    if len(sample_point[0]) == 2:
        ax.scatter(sample_point[:, 0], sample_point[:, 1], s=2, color=color_set)
    elif len(sample_point[0]) == 3:
        ax.scatter(sample_point[:, 0], sample_point[:, 1], sample_point[:, 2],
                   s=2, color=color_set)


def plot_decision_boundary(K, predict, ax, color, x_min, x_max, y_min, y_max):
    """
    Plot the decision boundary according to the input variable "predict"

    :param K: number of classification
    :param predict: a function that use to predict the classification
    :param ax: axes object of the "fig"
    :param color: color set. each Gaussian has one corresponding color.
    :param x_min: minimum x value in the "fig"
    :param x_max: maximum x value in the "fig"
    :param y_min: minimum y value in the "fig"
    :param y_max: maximum y value in the "fig"
    :return:
    """
    x, y = np.meshgrid(np.linspace(x_min, x_max, 1000),
                       np.linspace(y_min, y_max, 1000))

    z = predict(np.c_[np.ravel(x), np.ravel(y)])
    z = np.argmax(z, axis=1).reshape(x.shape)
    ax.contourf(x, y, z, K - 1, alpha=0.15, colors=color)
