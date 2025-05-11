import hashlib
import json
from time import time
from typing import List, Dict, Any

class Block:
    def __init__(self, index: int, transactions: List[Dict], timestamp: float, previous_hash: str, nonce: int = 0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self) -> str:
        """
        Возвращает хеш блока, вычисляя его из содержимого блока
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    # Сложность майнинга (количество ведущих нулей)
    difficulty = 2
    
    def __init__(self):
        self.chain: List[Block] = []
        self.unconfirmed_transactions: List[Dict] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Создает начальный блок (genesis block) и добавляет его в цепочку
        """
        genesis_block = Block(0, [], time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def proof_of_work(self, block: Block) -> str:
        """
        Алгоритм Proof of Work - ищет nonce, который делает хеш блока соответствовать сложности
        """
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block: Block, proof: str) -> bool:
        """
        Добавляет блок в цепочку после проверки
        """
        previous_hash = self.last_block.hash
        
        if previous_hash != block.previous_hash:
            return False
        
        if not self.is_valid_proof(block, proof):
            return False
        
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block: Block, block_hash: str) -> bool:
        """
        Проверяет, соответствует ли proof сложности и является ли правильным хешем блока
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and (block_hash == block.compute_hash())

    def add_new_transaction(self, transaction: Dict) -> None:
        self.unconfirmed_transactions.append(transaction)

    def mine(self) -> int:
        """
        Майнит новые блоки, добавляя ожидающие транзакции в блокчейн
        """
        if not self.unconfirmed_transactions:
            return -1
        
        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

    def check_chain_validity(cls, chain: List[Block]) -> bool:
        """
        Проверяет валидность всей цепочки
        """
        result = True
        previous_hash = "0"

        for block in chain:
            block_hash = block.hash
            # Удаляем поле hash для пересчета хеша
            delattr(block, "hash")
            
            if not cls.is_valid_proof(block, block_hash) or previous_hash != block.previous_hash:
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash

        return result

# Пример использования
if __name__ == "__main__":
    blockchain = Blockchain()
    
    # Добавляем несколько транзакций
    blockchain.add_new_transaction({
        "sender": "Alice",
        "recipient": "Bob",
        "amount": 5
    })
    blockchain.add_new_transaction({
        "sender": "Bob",
        "recipient": "Charlie",
        "amount": 2
    })
    
    # Майним блок с транзакциями
    blockchain.mine()
    
    # Выводим информацию о блокчейне
    print("Блокчейн:")
    for block in blockchain.chain:
        print(f"Block {block.index}:")
        print(f"  Hash: {block.hash}")
        print(f"  Previous hash: {block.previous_hash}")
        print(f"  Transactions: {block.transactions}")
        print(f"  Nonce: {block.nonce}")
        print()
    
    # Проверяем валидность цепочки
    print(f"Цепочка валидна: {blockchain.check_chain_validity(blockchain.chain)}")
