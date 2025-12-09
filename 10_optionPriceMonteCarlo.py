import numpy as np


class OptionPriceMonteCarlo:
    def __init__(self, S0, E, T, rf, sigma, iterations=5):
        self.S0 = S0
        self.E = E
        self.T = T
        self.rf = rf
        self.sigma = sigma
        self.iterations = iterations

    def call_option_price(self):
        option_data = np.zeros([self.iterations, 2])

        # Wiener Process
        rand = np.random.normal(0, 1, [1, self.iterations])

        # Stock Price
        stock_price = self.S0 * np.exp(
            (self.rf - 0.5 * self.sigma**2) * self.T
            + self.sigma * np.sqrt(self.T) * rand
        )

        #  S-E : max(0, S-E)
        option_data[:, 1] = stock_price - self.E

        average_option_price = np.sum(np.amax(option_data, axis=1)) / float(
            self.iterations
        )

        present_value = average_option_price * np.exp(-self.rf * self.T)

        return present_value

    def put_option_price(self):
        option_data = np.zeros([self.iterations, 2])

        # Wiener Process
        rand = np.random.normal(0, 1, [1, self.iterations])

        # Stock Price
        stock_price = self.S0 * np.exp(
            (self.rf - 0.5 * self.sigma**2) * self.T
            + self.sigma * np.sqrt(self.T) * rand
        )

        #  E-S : max(0, E-S)
        option_data[:, 1] = self.E - stock_price

        average_option_price = np.sum(np.amax(option_data, axis=1)) / float(
            self.iterations
        )

        present_value = average_option_price * np.exp(-self.rf * self.T)

        return present_value


if __name__ == "__main__":
    S = 100
    E = 100
    T = 1
    rf = 0.05
    sigma = 0.2
    model = OptionPriceMonteCarlo(S, E, T, rf, sigma, 10000)

    print(f"The call option price is {model.call_option_price()}")
    print(f"The put option price is {model.put_option_price()}")
