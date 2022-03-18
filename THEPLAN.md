# The Plan

Today is Mar 17, keep this to 90 min or so.

Software mentoring / pair working / pair coding / twitch streaming / broadcasting.

Goal is to build engineering capacity for AI safety work.

Me: Aray.  I've done professional software > 10 years, professional AI > 5.

Pair: Eli.  

I'm a guy. I do stuff. Sometimes. I am not a programmer. I have ever written a script or made an app for myself. 

Setup for today: mostly me driving, little bit of Eli driving, mostly asking questions and trying to following along.

Expectation is overwhelmed pretty quickly -- slow down until things can be followed.

## Specific thing to build: Tokenizer

Turn strings into chunks.  This is a first step before something like transformers, LSTMs, RNNs.

"Mary had a little lamb." -> ["Mary", " had", " a", " little", " lamb", "."]  So here are the chunks.

Each chunk has a unique mapping -> integer.  So in our example maybe it converts to [234, 353, 567, 890, 987, 654]

What if do if we run into a word that is not in our dictionary?  We can tokenize in parts ["Ma", "ry"] -- as a backup, we have tokens for all the letters "a", "b", etc.

*Tokenization* is a mapping from these strings to integers.  GPT-2, GPT-3 use same tokenization.

We are going to make our own tokenization.

### What tokens to add: Byte Pair Encoding

Algorithm:
* start with a token for every byte "a", "b", "c", etc
* then we search over some dataset, for the most common pair of tokens.
    e.g. "abcabdabe" then the pair "ab" occurs a bunch, add "ab" to the token list.
* then we go back to searching over the dataset


### How to do encoding

Tokens_to_bytes = {
    1: 'a',
    2: 'b',
    3: 'c',
    4: 'ab',
    5: 'abc,
    6: 'bc',
}

Encode the bytes sequence: "abcabcabc"
Byte by byte:
start with "a", which does exist, but we prefer a longer one.
Longest first:
know the longest token is length 3
start with candidate of length 3 -> "abc"
if its not in our dictionary, then remove the last byte and try again.
eventually we'll have a 1-byte sequence, so we'll always find a match

