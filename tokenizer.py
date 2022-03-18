#!/usr/bin/env python
'''
Key Terms and Ideas:

Token - integer that corresponds to a bytes sequence (string)
Bytes - the sequence of bytes that correspond to a token

Encode - convert a sequence of bytes to a sequence of tokens
Decode - convert a sequence of tokens to a sequence of bytes

'''
# %%
import matplotlib.pyplot as plt
from collections import defaultdict

kjv = open('/tmp/kjv.txt', 'rb').read()


# %%
class Tokenizer:
    def __init__(self):  # constructor
        self.token_to_bytes = {}  # map from int to bytes
        self.bytes_to_token = {}  # map from bytes to int

        # Add starting bytes - single byte tokens
        for token in range(256):
            bytes_ = bytes([token])
            self.token_to_bytes[token] = bytes_
            self.bytes_to_token[bytes_] = token

    def encode(self, source_bytes):
        assert isinstance(source_bytes, bytes), 'source_bytes must be bytes'
        longest_bytes = max(len(b) for b in self.bytes_to_token)
        tokens = []
        idx = 0
        while idx < len(source_bytes):
            chunk = source_bytes[idx:idx + longest_bytes]
            assert isinstance(chunk, bytes), 'chunk is not bytes'
            while len(chunk):
                if chunk in self.bytes_to_token:
                    tokens.append(self.bytes_to_token[chunk])
                    idx += len(chunk)
                    break
                if len(chunk) == 1:
                    raise ValueError('No token for byte', chunk)
                chunk = chunk[:-1]
        return tokens

    def decode(self, tokens):
        assert isinstance(tokens, list), 'tokens must be list'
        result = b''
        for token in tokens:
            result += self.token_to_bytes[token]
        return result

    def byte_pair_encoding(self, source_bytes, N=1):
        # Step 1: Encode the source bytes
        # Step 2: Find the most frequent pair of tokens
        # Step 3: Add that token to the tokenizer
        for _ in range(N):
            tokens = self.encode(source_bytes)
            counts = defaultdict(int)
            for i in range(len(tokens) - 1):
                counts[tuple(tokens[i:i + 2])] += 1
            most_frequent = max(counts, key=counts.get)
            new_token = max(self.token_to_bytes.keys()) + 1
            new_bytes = self.token_to_bytes[most_frequent[0]] + self.token_to_bytes[most_frequent[1]]
            self.token_to_bytes[new_token] = new_bytes
            self.bytes_to_token[new_bytes] = new_token
            print('Added', new_bytes, 'to the tokenizer', new_token)

            
        

tokenizer = Tokenizer()
tokenizer.byte_pair_encoding(b"Mary had a little lamb", 5)

# %%
tokenizer = Tokenizer()
tokenizer.byte_pair_encoding(kjv, 100)


# %%
import time
start = time.time()
kjv_tokens = tokenizer.encode(kjv)
print(time.time() - start)


# %%


counts = defaultdict(int)
for b in kjv:
    counts[b] += 1

# %%
plt.plot(sorted(counts.values())[::-1])
# set x to log scale
# plt.xscale('log')
# set y to log scale
plt.yscale('log')

# %% get the most frequent byte
max_byte = max(counts, key=counts.get)
bytes([max_byte])