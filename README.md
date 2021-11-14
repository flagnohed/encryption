A program with different encryption/decryption methods

Current methods:
* Caesar cipher
* ROT13 
* Rövarspråket
* RSA encryption/decryption
* Vigenère encryption/decryption

Note:
In the implementation of RSA encryption/decryption, "length sequences" are used. 
These keep track of how many digits the integer representation of each letter in the message has.
For example, the string "fix" will (since int representation is based of their position in the english alphabet (1-indexed)) be written as
6924, with the length sequence of 112, since 'f' == 6, 'i' == 9 and 'x' == 24.
