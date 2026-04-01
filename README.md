# The Hash Function

The hash function is a simple function that manipulates the ASCII value of the message using repeated multiplication.

For each character:
- Start with initial value of 68 (ASCII of 'D', my initial)
- Multiply by 31 (common prime no. choice)
- Add the ASCII of current character
- Apply modulo 2^64 to keep the value within 64-bit range.

General Operation:

<p align="center">
  <b><code>hash = (hash * 31 + ASCII(character)) mod 2^64</code></b>
</p>

# The Encryption- Running Cipher

Each character is combined with the corresponding character from the key. I have done this using ASCII addition for encryption and subtraction for decryption.

Combination
First the input is passed through the hash function to give a fixed-size hash
The output hash is passed through the cipher with a key.

# Instructions to run:

- In the initial menu, choose 1 to encrypt.
- Enter Key for cipher.
- Enter message to be hashed
- You will receive the message with encrypted hash, and a menu.
- In this menu, choose 2 to verify.
- Enter same running key.
- Enter the received message(copy-paste to prevent error).

# Example 1:

Running Key: ElliotSimpsons

Message: HelloWorld


Hashed Output: HelloWorldQYMOCICOAETBRW

# Example 2:

Running Key: LockAndKey

Message: abort


Hashed Output: 5::abortSXKYKAJW
