import time
from sympy.solvers.diophantine.diophantine import diop_linear
import random
from sympy import *
import os


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_menu():
    print("================")
    print("1. Caesar cipher")
    print("2. ROT13")
    print("3. Rövarspråket")
    print("4. Encrypt RSA")
    print("5. Decrypt RSA")
    print("6. Encrypt Vigenère")
    print("7. Decrypt Vigenère")
    # print("5. ChaCha")
    # print("6. DES")
    # print("7. Blowfish")
    # print("8. Enigma simulator")  # substitution cipher with multiple rotors
    print("0. Quit")
    print("================")


def fetch_msg(choice, encryption=True):
    print("=========================================================")
    print("Every message will be stripped, i.e., no whitespaces \n "
          "or special characters are allowed. This does not apply to Rövarspråket.")
    print("The encrypted message will only contain lowercase letters.")
    print("Special characters 'Å, Ä, Ö' will be replaced automatically with 'a, a, o'")
    print("=========================================================")

    if not encryption:
        msg = input("Enter message to decrypt: ")
    else:
        msg = input("Enter message to encrypt: ")
    stripped_msg = ''.join(c.lower() for c in msg if c.isalpha())
    strip = [1, 2, 6, 7]
    if choice in strip:  # cant have åäö
        if 'å' in stripped_msg or 'ä' in stripped_msg:
            stripped_msg = stripped_msg.replace("å", "ä")
        if 'ö' in stripped_msg:
            stripped_msg = stripped_msg.replace("ö", "o")
    return stripped_msg, msg


def caesar(msg, n):
    return ''.join(chr((ord(c) - 97 + n) % 26 + 97) for c in msg)


def r_lang(msg):
    enc_msg = ""
    consonants = "bcdfghjklmnpqrstvwxz"
    for c in msg:
        enc_msg += c
        if c in consonants:
            enc_msg += "o" + c
    return enc_msg


def is_prime(n):
    for i in range(2, n//2+1):
        if n % i == 0:
            return False
    return True


def is_relative_prime(a, b):
    for i in range(2, min(a, b)//2+1):
        if a % i == 0 and a % i == 0:
            return False
    return True


def rsa_decrypt(d, n, enc_msg, enc_len_seq, clean_len_seq):
    clean = ""
    for i in enc_len_seq:
        enc_n = int(enc_msg[:int(i)])
        clean_n = enc_n**d % n
        clean += str(clean_n)
        enc_msg = enc_msg[int(i):]

    readable = ""
    for i in clean_len_seq:
        clean_n = int(clean[:int(i)])
        readable += chr(clean_n+96)
        clean = clean[int(i):]
    return readable


def rsa_encrypt(e, n, rsa_msg, clean_len_seq):
    enc_msg = ""
    enc_len_seq = ""

    for s in rsa_msg:  # encrypt every number individually
        new_s = s**e % n
        enc_msg += str(new_s)
        enc_len_seq += str(len(str(new_s)))

    return enc_msg, enc_len_seq, clean_len_seq


def make_rsa_compatible(msg):
    rsa_msg = []
    clean_len_seq = ""
    for c in msg:
        rsa_msg += [ord(c) - 96]  # makes a=1 etc.
        clean_len_seq += str(len(str(ord(c) - 96)))
    return rsa_msg, clean_len_seq


def rsa_generate(msg):
    """
    Generates two random prime numbers between 10 and 400
    (my computer can't handle higher than 400)
    """
    print("Generating keys... (might take a while)")
    primes = [n for n in range(100, 500) if is_prime(n)]

    p, q = random.choice(primes), random.choice(primes)
    n = p * q
    r = (p-1)*(q-1)

    e_candidates = [e for e in range(2, r) if is_relative_prime(e, r)]
    e = random.choice(e_candidates)
    x, y, t_0 = symbols("x, y, t_0", integer=True)
    d = diop_linear(e * x - r * y - 1)
    d = d[0].subs(t_0, 2)

    print("=======================================")
    print("Here are your RSA keys: ")
    print("n: ", n)
    print("e: ", e)
    print("d: ", d)
    print("* public key pair: (" + str(e) + ", " + str(n) + ")")
    print("* private key pair: (" + str(d) + ", " + str(n) + ")")
    print("=======================================")
    encrypt_or_quit = input("Encrypt message with your new keys? (y/n): ")
    if encrypt_or_quit == 'y':
        rsa_msg, clean_len_seq = make_rsa_compatible(msg)
        return rsa_encrypt(e, n, rsa_msg, clean_len_seq)
    elif encrypt_or_quit == 'n':
        exit(0)


def rsa_main(msg):
    while True:
        choice = input("(g)enerate keys or (e)ncrypt message? ")
        if choice == "e":
            while True:
                try:
                    e = int(input("Enter e-value: "))
                except ValueError:
                    print("Must be an integer.")
                else:
                    break
            while True:
                try:
                    n = int(input("Enter n-value: "))
                except ValueError:
                    print("Must be an integer.")
                else:
                    break
            rsa_msg, clean_len_seq = make_rsa_compatible(msg)
            return rsa_encrypt(e, n, rsa_msg, clean_len_seq)
        if choice == "g":
            return rsa_generate(msg)


def rsa_decrypt_handler():

    while True:
        try:
            d = int(input("Enter your d-value: "))
        except ValueError:
            print("Needs to be an integer.")
        else:
            break
    while True:
        try:
            n = int(input("Enter your n-value: "))
        except ValueError:
            print("Needs to be an integer.")
        else:
            break
    while True:
        try:
            enc_msg = input("Enter the encrypted message: ")
        except ValueError:
            print("The encrypted message should only be digits.")
        else:
            break
    while True:
        try:
            # need eval() to confirm that its actually a valid length sequence
            enc_len_seq = eval(input("Enter the encrypted length sequence: "))
        except SyntaxError:
            print("Should look like 23456 but with your own digits, try again!")
        else:
            break
    while True:
        try:
            # need eval() to confirm that its actually a valid length sequence
            clean_len_seq = eval(input("Enter the clean length sequence: "))
        except SyntaxError:
            print("Should look like 23456 but with your own digits, try again!")
        else:
            break
    return rsa_decrypt(d, n, enc_msg, str(enc_len_seq), str(clean_len_seq))


def extend(key, msg):  # repeat key until it matches length of msg
    a = len(msg)//len(key)
    b = len(msg) % len(key)
    return key * a + key[:b]


def vig_cipher(msg, encrypt=True):
    cont = True
    keyword = ""
    enc_msg = ""
    while cont:
        cont = False
        keyword = input("Enter keyword: ")
        for letter in keyword:
            if not letter.isalpha():
                print("Keyword can only contain letters!")
                cont = True
    adj_key = extend(keyword, msg)
    for i in range(len(msg)):
        a, b = ord(msg[i]) - 97, ord(adj_key[i]) - 97  # get their positions in the english alphabet
        c = (a - b) % 26
        if encrypt:
            c = (a + b) % 26
        enc_msg += chr(c + 97)
    return enc_msg, keyword


def main():
    last_choice = 0  # needed to check if clearing console is a good idea or not, used in testing
    while True:
        decryption = False
        clean_msg = ""
        show_menu()
        choice = 0
        n = 3
        enc_msg = ""
        while True:
            try:
                choice = int(input("Choose an option from the menu (0-7): "))
            except ValueError:
                print("Please enter an integer between 0 and 7.")
                continue
            else:
                break

        if choice == 0:
            exit(0)

        if choice == 1:
            cls()
            print("[CURRENT METHOD: CAESAR ENCRYPTION]")
            msg, orig_msg = fetch_msg(choice, True)
            while True:
                try:
                    n = int(input("Choose n (displacement to the right): ")) % 26
                except ValueError:
                    print("Please enter an integer.")
                    continue
                else:
                    break
            enc_msg = caesar(msg, n)

        elif choice == 2:
            cls()
            print("[CURRENT METHOD: ROT13 ENCRYPTION]")
            msg, orig_msg = fetch_msg(choice, True)
            enc_msg = caesar(msg, 13)

        elif choice == 3:
            print("[CURRENT METHOD: RÖVARSPRÅKET]")
            cls()
            msg, orig_msg = fetch_msg(choice, True)
            enc_msg = r_lang(orig_msg)

        elif choice == 4:
            cls()
            print("[CURRENT METHOD: RSA ENCRYPTION]")
            msg, orig_msg = fetch_msg(choice, True)
            enc_msg, enc_len_list, clean_len_list = rsa_main(msg)
            print("Encrypted length sequence: ", enc_len_list)
            print("Clean length sequence: ", clean_len_list)

        elif choice == 5:
            if last_choice != 4:
                cls()
            print("[CURRENT METHOD: RSA DECRYPTION]")
            decryption = True
            clean_msg = rsa_decrypt_handler()

        elif choice == 6:
            cls()
            print("[CURRENT METHOD: VIGENÈRE ENCRYPTION]")
            msg, orig_msg = fetch_msg(choice, True)
            enc_msg, key = vig_cipher(msg)
            print("Encryption made with key: ", key)

        elif choice == 7:
            if last_choice != 6:
                cls()
            print("[CURRENT METHOD: VIGENÈRE DECRYPTION]")
            decryption = True
            msg, orig_msg = fetch_msg(choice, False)
            clean_msg, key = vig_cipher(msg, False)

        else:
            print("Not implemented yet!")

        if decryption:
            print("Your decrypted message is: ", clean_msg)
        else:
            print("Your encrypted message is: ", enc_msg)
        last_choice = choice
        time.sleep(2)


if __name__ == "__main__":
    main()
