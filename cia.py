HEX_TO_LETTER = {
    "0": "A", "1": "B", "2": "C", "3": "D",
    "4": "E", "5": "F", "6": "G", "7": "H",
    "8": "I", "9": "J", "a": "K", "b": "L",
    "c": "M", "d": "N", "e": "O", "f": "P",
}
LETTER_TO_HEX = {value: key for key, value in HEX_TO_LETTER.items()}
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PACKET_SEPARATOR = "::"


def custom_hash(input_text):
    reversed_text = input_text[::-1]
    hash_val = 68  # ASCII for D
    for ch in reversed_text:
        hash_val = (hash_val * 31 + ord(ch)) % (2 ** 64)
    return hex(hash_val)[2:]


def hex_to_letters(hex_text):
    return "".join(HEX_TO_LETTER[ch] for ch in hex_text.lower())


def letters_to_hex(letter_text):
    try:
        return "".join(LETTER_TO_HEX[ch] for ch in letter_text.upper())
    except KeyError:
        return None


def build_running_key_stream(key, required_length):
    key_stream = "".join(ch.upper() for ch in key if ch.isalpha())
    if len(key_stream) < required_length:
        raise ValueError(
            "Running key must contain at least as many letters as the encoded hash."
        )
    return key_stream[:required_length]


def running_key_encrypt(plain_text, key):
    key_stream = build_running_key_stream(key, len(plain_text))
    encrypted = []

    for plain_char, key_char in zip(plain_text, key_stream):
        plain_index = ord(plain_char) - ord("A")
        key_index = ord(key_char) - ord("A")
        encrypted.append(ALPHABET[(plain_index + key_index) % 26])

    return "".join(encrypted)


def running_key_decrypt(cipher_text, key):
    try:
        key_stream = build_running_key_stream(key, len(cipher_text))
    except ValueError:
        return None

    decrypted = []
    for cipher_char, key_char in zip(cipher_text, key_stream):
        if cipher_char not in ALPHABET:
            return None
        cipher_index = ord(cipher_char) - ord("A")
        key_index = ord(key_char) - ord("A")
        decrypted.append(ALPHABET[(cipher_index - key_index) % 26])

    return "".join(decrypted)


def create_packet(message, encrypted_hash):
    return f"{len(message)}{PACKET_SEPARATOR}{message}{encrypted_hash}"


def parse_packet(packet):
    try:
        length_text, remainder = packet.split(PACKET_SEPARATOR, 1)
        message_length = int(length_text)
    except ValueError:
        return None, None

    if message_length < 0 or message_length > len(remainder):
        return None, None

    message = remainder[:message_length]
    encrypted_hash = remainder[message_length:]
    return message, encrypted_hash


def sender(message, key):
    hash_value = custom_hash(message)
    hash_letters = hex_to_letters(hash_value)
    encrypted_hash = running_key_encrypt(hash_letters, key)
    return create_packet(message, encrypted_hash)


def receiver(packet, key):
    message, encrypted_hash = parse_packet(packet)
    if message is None or not encrypted_hash:
        print("  [!] Invalid packet format.")
        return False

    decrypted_letters = running_key_decrypt(encrypted_hash, key)
    if decrypted_letters is None:
        print("  [!] Could not decrypt hash - packet or key is invalid.")
        return False

    decrypted_hash = letters_to_hex(decrypted_letters)
    if decrypted_hash is None:
        print("  [!] Decrypted text could not be converted back to hex.")
        return False

    return decrypted_hash == custom_hash(message)


def main():
    while True:
        print("\nMENU")
        print("1. Send ")
        print("2. Verify")
        print("3. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "3":
            print("Exiting...")
            break

        if choice not in ("1", "2"):
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue

        key = input("Enter running key text: ").strip()

        if not key:
            print("[!] Key cannot be empty.")
            continue

        if choice == "1":
            message = input("Enter message: ").strip()
            try:
                packet = sender(message, key)
            except ValueError as exc:
                print(f"[!] {exc}")
                continue

            
            print("Hashed Output:", packet)

        elif choice == "2":
            packet = input("Enter received output: ").strip()
            is_valid = receiver(packet, key)
            #print("\n--- Receiver ---")
            if is_valid:
                print("Authentication SUCCESS (Message is authentic)")
            else:
                print("Authentication FAILED (Message altered)")


if __name__ == "__main__":
    main()
