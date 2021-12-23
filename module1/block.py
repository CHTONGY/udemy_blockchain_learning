import json
import hashlib
import jsonpickle

class Block:
    def __init__(self, block_index: int, data: map, prev_hash: str, nounce: int = 0) -> None:
        self.block_index = block_index
        self.nounce = 0
        self.data = {}
        self.prev_hash = ""
        if nounce != 0:
            self.nounce = nounce
        if data is not None:
            self.data = data
        if prev_hash is not None:
            self.prev_hash = prev_hash

    def do_hash(self) -> str:
        # encode_block = json.dumps(self, sort_keys=True).encode()
        encode_block = json.dumps(jsonpickle.encode(value=self, unpicklable=False), sort_keys=True).encode()
        return hashlib.sha256(encode_block).hexdigest()

    
