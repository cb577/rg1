class Tile:
    """
    A tile on a map. It may be blocked, or may block sight.
    """
    def __init__(self, blocked, block_sight=None, parent=None):
        self.blocked = blocked
        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        self.explored = False

        self.parent = parent

