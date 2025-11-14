import unittest

import hawkdove


# might as well test all of it
class TestLogic(unittest.TestCase):
    def test_hawk(self):
        assert hawkdove.interaction(hawkdove.H_STRAT, hawkdove.H_STRAT) == -25
        assert hawkdove.interaction(hawkdove.H_STRAT, hawkdove.D_STRAT) == 50
        assert hawkdove.interaction(hawkdove.H_STRAT, hawkdove.B_STRAT) == 50
        assert hawkdove.interaction(hawkdove.H_STRAT, hawkdove.R_STRAT) == -25

    def test_dove(self):
        assert hawkdove.interaction(hawkdove.D_STRAT, hawkdove.H_STRAT) == 0
        assert hawkdove.interaction(hawkdove.D_STRAT, hawkdove.D_STRAT) == 15
        assert hawkdove.interaction(hawkdove.D_STRAT, hawkdove.B_STRAT) == 0
        assert hawkdove.interaction(hawkdove.D_STRAT, hawkdove.R_STRAT) == 15

    def test_bully(self):
        assert hawkdove.interaction(hawkdove.B_STRAT, hawkdove.H_STRAT) == 0
        assert hawkdove.interaction(hawkdove.B_STRAT, hawkdove.D_STRAT) == 50
        assert hawkdove.interaction(hawkdove.B_STRAT, hawkdove.B_STRAT) == 25
        assert hawkdove.interaction(hawkdove.B_STRAT, hawkdove.R_STRAT) == 0

    def test_rascal(self):
        assert hawkdove.interaction(hawkdove.R_STRAT, hawkdove.H_STRAT) == -25
        assert hawkdove.interaction(hawkdove.R_STRAT, hawkdove.D_STRAT) == 15
        assert hawkdove.interaction(hawkdove.R_STRAT, hawkdove.B_STRAT) == 50
        assert hawkdove.interaction(hawkdove.R_STRAT, hawkdove.R_STRAT) == 15
