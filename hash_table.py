
"""CSC 225 - Hash table starter. Complete the TODO sections."""

SIZES = [11, 23, 47, 97, 197, 397]


class HashTable:
    def __init__(self, method="linear", hash_method="mod"):
        self.method = method
        self.hash_method = hash_method
        self.capacity = 11
        self.count = 0

        if method == "chaining":
            self.table = [[] for i in range(self.capacity)]
        else:
            self.table = [None] * self.capacity

    def hash_key(self, key):
        if self.hash_method == "mod":
            return key % self.capacity

        total = 0
        for digit in str(abs(key)):
            total += int(digit)

        return total % self.capacity

    def insert(self, key):
        if self.search(key):
            return

        threshold = 0.70

        if self.method == "quadratic":
            threshold = 0.50
        elif self.method == "chaining":
            threshold = 0.75

        if (self.count / self.capacity) >= threshold:
            self.resize()

        start = self.hash_key(key)

        if self.method == "chaining":
            self.table[start].append(key)
        else:
            i = 0
            while i < self.capacity:
                if self.method == "linear":
                    pos = (start + i) % self.capacity
                else:
                    pos = (start + (i * i)) % self.capacity

                if self.table[pos] is None:
                    self.table[pos] = key
                    break

                i += 1

        self.count += 1

    def search(self, key):
        start = self.hash_key(key)

        if self.method == "chaining":
            return key in self.table[start]

        for i in range(self.capacity):
            if self.method == "linear":
                pos = (start + i) % self.capacity
            else:
                pos = (start + (i * i)) % self.capacity

            slot = self.table[pos]

            if slot is None:
                return False

            if slot == key:
                return True

        return False

    def resize(self):
        old_table = self.table

        index = SIZES.index(self.capacity)

        if index + 1 >= len(SIZES):
            return

        self.capacity = SIZES[index + 1]

        if self.method == "chaining":
            self.table = [[] for _ in range(self.capacity)]
        else:
            self.table = [None] * self.capacity

        self.count = 0

        if self.method == "chaining":
            for bucket in old_table:
                for key in bucket:
                    self.insert(key)
        else:
            for slot in old_table:
                if slot is not None:
                    self.insert(slot)

    def show(self):
        print("\nMethod:", self.method, "| Hash:", self.hash_method)
        print("Size:", self.capacity, "| Values:", self.count)
        print("Load factor:", round(self.count / self.capacity, 2))

        for i in range(self.capacity):
            print(i, ":", self.table[i])
