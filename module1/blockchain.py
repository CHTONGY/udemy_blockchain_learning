# 1. building a blockchain
from block import Block


class Blockchain:

    def __init__(self) -> None:
        self.chain = []
        self.create_block(data={}, prev_hash='0'*64)

    def create_block(self, data: map, prev_hash: str = None) -> Block:
        if prev_hash is None:
            prev_hash = self.get_last_block().do_hash()
        new_block = Block(block_index=len(self.chain)+1,
                          data=data, prev_hash=prev_hash)
        self.proof_of_work(new_block)
        self.chain.append(new_block)
        return new_block

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def proof_of_work(self, block: Block) -> int:
        nounce = 1
        valid_proof = False

        while not valid_proof:
            block.nounce = nounce
            hash_str = block.do_hash()
            if hash_str[:4] != '0000':
                nounce += 1
            else:
                valid_proof = True

        return nounce

    def is_chain_valid(self) -> bool:
        prev_block = self.chain[0]

        for i in range(1, len(self.chain)):
            cur_block = self.chain[i]
            # check whether cur_block.prev_hash == prev_block.do_hash()
            if cur_block.prev_hash != prev_block.do_hash():
                return False
            # check whether prev_block.do_hash() start with '0000'
            if prev_block.do_hash()[:4] != '0000':
                return False

            prev_block = cur_block

        return True
