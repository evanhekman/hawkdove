import unittest

import numpy as np

import hawkdove.core as hawkdove

UNIFORM = np.array([0.25, 0.25, 0.25, 0.25])
MORE_HAWK = np.array([0.70, 0.10, 0.10, 0.10])
MORE_DOVE = np.array([0.10, 0.70, 0.10, 0.10])
MORE_BULLY = np.array([0.10, 0.10, 0.70, 0.10])
MORE_RETALIATOR = np.array([0.10, 0.10, 0.10, 0.70])


# might as well test all of it
class TestLogic(unittest.TestCase):
    def test_hawk(self):
        assert hawkdove.interaction(hawkdove.HAWK, hawkdove.HAWK) == -25
        assert hawkdove.interaction(hawkdove.HAWK, hawkdove.DOVE) == 50
        assert hawkdove.interaction(hawkdove.HAWK, hawkdove.BULL) == 50
        assert hawkdove.interaction(hawkdove.HAWK, hawkdove.RETA) == -25

    def test_dove(self):
        assert hawkdove.interaction(hawkdove.DOVE, hawkdove.HAWK) == 0
        assert hawkdove.interaction(hawkdove.DOVE, hawkdove.DOVE) == 15
        assert hawkdove.interaction(hawkdove.DOVE, hawkdove.BULL) == 0
        assert hawkdove.interaction(hawkdove.DOVE, hawkdove.RETA) == 15

    def test_bully(self):
        assert hawkdove.interaction(hawkdove.BULL, hawkdove.HAWK) == 0
        assert hawkdove.interaction(hawkdove.BULL, hawkdove.DOVE) == 50
        assert hawkdove.interaction(hawkdove.BULL, hawkdove.BULL) == 25
        assert hawkdove.interaction(hawkdove.BULL, hawkdove.RETA) == 0

    def test_retaliator(self):
        assert hawkdove.interaction(hawkdove.RETA, hawkdove.HAWK) == -25
        assert hawkdove.interaction(hawkdove.RETA, hawkdove.DOVE) == 15
        assert hawkdove.interaction(hawkdove.RETA, hawkdove.BULL) == 50
        assert hawkdove.interaction(hawkdove.RETA, hawkdove.RETA) == 15


class TestDirection(unittest.TestCase):
    def test_hawk_wins(self):
        assert hawkdove.interaction(hawkdove.HAWK, MORE_HAWK) < hawkdove.interaction(
            hawkdove.HAWK, UNIFORM
        )
        assert hawkdove.interaction(hawkdove.HAWK, MORE_DOVE) > hawkdove.interaction(
            hawkdove.HAWK, UNIFORM
        )
        assert hawkdove.interaction(hawkdove.HAWK, MORE_BULLY) > hawkdove.interaction(
            hawkdove.HAWK, UNIFORM
        )
        assert hawkdove.interaction(
            hawkdove.HAWK, MORE_RETALIATOR
        ) < hawkdove.interaction(hawkdove.HAWK, UNIFORM)

    def test_dove_wins(self):
        assert hawkdove.interaction(hawkdove.DOVE, MORE_HAWK) < hawkdove.interaction(
            hawkdove.DOVE, UNIFORM
        )
        assert hawkdove.interaction(hawkdove.DOVE, MORE_DOVE) > hawkdove.interaction(
            hawkdove.DOVE, UNIFORM
        )
        assert hawkdove.interaction(hawkdove.DOVE, MORE_BULLY) < hawkdove.interaction(
            hawkdove.DOVE, UNIFORM
        )
        assert hawkdove.interaction(
            hawkdove.DOVE, MORE_RETALIATOR
        ) > hawkdove.interaction(hawkdove.DOVE, UNIFORM)

    def test_bully_wins(self):
        assert hawkdove.interaction(hawkdove.BULL, MORE_HAWK) < hawkdove.interaction(
            hawkdove.BULL, UNIFORM
        )
        assert hawkdove.interaction(hawkdove.BULL, MORE_DOVE) > hawkdove.interaction(
            hawkdove.BULL, UNIFORM
        )
        assert hawkdove.interaction(hawkdove.BULL, MORE_BULLY) > hawkdove.interaction(
            hawkdove.BULL, UNIFORM
        )
        assert hawkdove.interaction(
            hawkdove.BULL, MORE_RETALIATOR
        ) < hawkdove.interaction(hawkdove.BULL, UNIFORM)

    def test_retaliator_wins(self):
        # retaliator seems to be the best strategy because it wins unless there are more hawks than average...
        assert hawkdove.interaction(hawkdove.RETA, MORE_HAWK) < hawkdove.interaction(
            hawkdove.RETA, UNIFORM
        )
        assert hawkdove.interaction(hawkdove.RETA, MORE_DOVE) > hawkdove.interaction(
            hawkdove.RETA, UNIFORM
        )
        assert hawkdove.interaction(hawkdove.RETA, MORE_BULLY) > hawkdove.interaction(
            hawkdove.RETA, UNIFORM
        )
        assert hawkdove.interaction(
            hawkdove.RETA, MORE_RETALIATOR
        ) > hawkdove.interaction(hawkdove.RETA, UNIFORM)

    def test_hawk_complex(self):
        """
        Make sure that hawk outcompetes in favorable populations.
        """
        # hawk should beat dove if there are lots of doves
        assert hawkdove.interaction(hawkdove.HAWK, MORE_DOVE) > hawkdove.interaction(
            hawkdove.DOVE, MORE_DOVE
        )
        # dove should beat hawk if there are lots of retaliators
        assert hawkdove.interaction(
            hawkdove.DOVE, MORE_RETALIATOR
        ) > hawkdove.interaction(hawkdove.HAWK, MORE_RETALIATOR)
        # hawk should beat bully if there are lots of bullies
        assert hawkdove.interaction(hawkdove.HAWK, MORE_BULLY) > hawkdove.interaction(
            hawkdove.BULL, MORE_BULLY
        )
        # bully should beat hawk if there are lots of retaliators
        assert hawkdove.interaction(
            hawkdove.BULL, MORE_RETALIATOR
        ) > hawkdove.interaction(hawkdove.HAWK, MORE_RETALIATOR)
        # hawk should beat retaliator if there are lots of doves
        assert hawkdove.interaction(hawkdove.HAWK, MORE_DOVE) > hawkdove.interaction(
            hawkdove.RETA, MORE_DOVE
        )
        # retaliator should beat hawk if there are lots of retaliators
        assert hawkdove.interaction(
            hawkdove.RETA, MORE_RETALIATOR
        ) > hawkdove.interaction(hawkdove.HAWK, MORE_RETALIATOR)

    def test_dove_complex(self):
        """
        Make sure that dove outcompetes in favorable populations.
        """
        # dove should beat bully if there are lots of retaliators
        assert hawkdove.interaction(
            hawkdove.DOVE, MORE_RETALIATOR
        ) > hawkdove.interaction(hawkdove.BULL, MORE_RETALIATOR)
        # bully should beat dove if there are lots of bullies
        assert hawkdove.interaction(hawkdove.BULL, MORE_BULLY) > hawkdove.interaction(
            hawkdove.DOVE, MORE_BULLY
        )
        # dove should beat retaliator if there are lots of hawks
        assert hawkdove.interaction(hawkdove.DOVE, MORE_HAWK) > hawkdove.interaction(
            hawkdove.RETA, MORE_HAWK
        )
        # retaliator should beat dove if there are lots of bullies
        assert hawkdove.interaction(hawkdove.RETA, MORE_BULLY) > hawkdove.interaction(
            hawkdove.DOVE, MORE_BULLY
        )

    def test_bully_complex(self):
        """
        Make sure that bully outcompetes in favorable populations.
        """
        # bully should beat retaliator if there are lots of doves
        assert hawkdove.interaction(hawkdove.BULL, MORE_DOVE) > hawkdove.interaction(
            hawkdove.RETA, MORE_DOVE
        )
        # retaliator should beat bully if there are lots of bullies
        assert hawkdove.interaction(hawkdove.RETA, MORE_BULLY) > hawkdove.interaction(
            hawkdove.BULL, MORE_BULLY
        )

    def test_retaliator_complex(self):
        """
        Make sure that retaliator outcompetes in favorable populations.
        """
        ...


if __name__ == "__main__":
    unittest.main()
