from BlockSim.Models.Block import Block as BaseBlock

class Block(BaseBlock):

    """ Defines the Ethereum Block model.

    :param int depth: the index of the block in the local blockchain ledger (0 for genesis block)
    :param int id: the uinque id or the hash of the block
    :param int previous: the uinque id or the hash of the previous block
    :param int timestamp: the time when the block is created
    :param int miner: the id of the miner who created the block
    :param list transactions: a list of transactions included in the block
    :param int size: the block size in MB
    :param list uncles: a list of uncle blocks to be referenced in the block
    :param int gaslimit: the block gas limit (e.g., current block gas limit = 8,000,000 units of gas)
    :param int usedgas: the block used gas
    """

    def __init__(self,
	 depth=0,
	 id=0,
	 previous=-1,
	 timestamp=0,
	 miner=None,
	 transactions=[],
	 size=1.0,
	 uncles=[],
     gaslimit= 8000000,
     usedgas=0):

        super().__init__(depth,id,previous,timestamp,miner,transactions,size)
        self.uncles= uncles
        self.gaslimit= gaslimit
        self.usedgas= usedgas
        self.transactions_verification_time = 0.0
        self.block_artifacts_size = 0.0
    
    # Calculate the sum of the creation times of the transactions
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
    