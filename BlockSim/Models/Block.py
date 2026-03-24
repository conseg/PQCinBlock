class Block(object):
    
    """ Defines the base Block model.

    :param int depth: the index of the block in the local blockchain ledger (0 for genesis block)
    :param int id: the uinque id or the hash of the block
    :param int previous: the uinque id or the hash of the previous block
    :param int timestamp: the time when the block is created
    :param int miner: the id of the miner who created the block
    :param list transactions: a list of transactions included in the block
    :param int size: the block size in MB
    """

    def __init__(self,
	 depth=0,
	 id=0,
	 previous=-1,
	 timestamp=0,
	 miner=None,
	 transactions=[],
	 size=1.0):

        self.depth = depth
        self.id = id
        self.previous = previous
        self.timestamp = timestamp
        self.miner = miner
        self.transactions = transactions or []
        self.size = size
        self.transactions_verification_time = 0.0
        self.block_artifacts_size = 0.0
        self.transactions_creation_time = 0.0

    def calculate_transactions_verification_time(self):
        acc =0
        for t in self.transactions:
            acc += t.verification_time
        self.transactions_verification_time = acc
    
    # def calculate_transactions_creation_time(self):
    #     acc =0
    #     for t in self.transactions:
    #         acc += t.creation_time
    #     self.transactions_creation_time = acc
    
    def calculate_block_artifacts_size(self, mean_publicKeySize=0.0):
        acc = 0
        for t in self.transactions:
            acc += t.artifacts_size
        # Scenario 3: signature * n + 1 * public key size
        acc += mean_publicKeySize
        self.block_artifacts_size = acc
