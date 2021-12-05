from wave_prevention import *

if __name__ == "__main__":
    X = [i/100 for i in range(1, 50)]
    Y = [x + 10*x**5 - 0.5*x**6 + log(2*x) - exp(0.002*x) + 10 for x in X]
    plt.plot(X, Y)
    #plt.plot(X, [linear_approximation(X, Y)(x) for x in X])
    #plt.plot(X, [exponential_approximation(X, Y)(x) for x in X])
    plt.plot(X, [polynomial_approximation(X, Y, 4)(x) for x in X])
    plt.show()
    print(best_approximation(X, Y))
