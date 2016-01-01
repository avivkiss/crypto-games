
from crypto.simulator.base_sim import BaseSim


class UFCMASim(BaseSim):
    """
    This simulator was written to be used with GameUFCMA. It simulates the
    game with an Adversary and allows you to compute an approximate advantage.
    """

    def run(self):
        """
        Runs the game with the adversary provided to the constructor.

        :return: 1 for success and 0 for failure.
        """
        self.game.initialize()
        self.adversary(self.game.tag, self.game.verify)
        return self.game.finalize()

    def compute_success_ratio(self):
        """
        Runs the game 1000 times and computes the ratio of successful runs
        over total runs.

        :return: successes / total_runs
        """
        results = []
        for i in xrange(0, 1000):
            results += [self.run()]

        successes = float(results.count(1))
        failures = float(results.count(0))

        return successes / (successes + failures)

    def compute_advantage(self):
        """
        Adv = Pr[UFCMA => True]

        :return: Approximate advantage computed using the above equation.
        """

        return self.compute_success_ratio()
