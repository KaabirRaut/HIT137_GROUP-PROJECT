def encrypt_char(character, multiplier_n, multiplier_m):
    if 'a' <= character <= 'z':
        if character <= 'm':
            shift = multiplier_n * multiplier_m
            new_char = ord('a') + (ord(character) + shift - ord('a')) % 26
            return chr(new_char), 'lower_first'
        else:
            shift = multiplier_n + multiplier_m
            new_char = ord('a') + (ord(character) - shift - ord('a')) % 26
            return chr(new_char), 'lower_second'
    elif 'A' <= character <= 'Z':
        if character <= 'M':
            shift = multiplier_n
            new_char = ord('A') + (ord(character) - shift - ord('A')) % 26
            return chr(new_char), 'upper_first'
        else:
            shift = multiplier_m ** 2
            new_char = ord('A') + (ord(character) + shift - ord('A')) % 26
            return chr(new_char), 'upper_second'
    else:
        return character, 'other'


def decrypt_char(character, encryption_type, multiplier_n, multiplier_m):
    if encryption_type == 'lower_first':
        shift = multiplier_n * multiplier_m
        new_char = ord('a') + (ord(character) - shift - ord('a')) % 26
        return chr(new_char)
    elif encryption_type == 'lower_second':
        shift = multiplier_n + multiplier_m
        new_char = ord('a') + (ord(character) + shift - ord('a')) % 26
        return chr(new_char)
    elif encryption_type == 'upper_first':
        shift = multiplier_n
        new_char = ord('A') + (ord(character) + shift - ord('A')) % 26
        return chr(new_char)
    elif encryption_type == 'upper_second':
        shift = multiplier_m ** 2
        new_char = ord('A') + (ord(character) - shift - ord('A')) % 26
        return chr(new_char)
    else:
        return character


def encrypt_file(input_file_path, output_file_path, multiplier_n, multiplier_m):
    try:
        with open(input_file_path, 'r') as file:
            file_content = file.read()

        encrypted_data = [encrypt_char(char, multiplier_n, multiplier_m) for char in file_content]
        encrypted_text = ''.join([char for char, _ in encrypted_data])
        encryption_types = ','.join([enc_type for _, enc_type in encrypted_data])

        with open(output_file_path, 'w') as file:
            file.write(encrypted_text)

        with open(output_file_path + '.types', 'w') as file:
            file.write(encryption_types)

        print(f"File encrypted and saved to {output_file_path}")
    except Exception as error:
        print(f"Error: {error}")


def decrypt_file(input_file_path, output_file_path, multiplier_n, multiplier_m):
    try:
        with open(input_file_path, 'r') as file:
            encrypted_text = file.read()

        with open(input_file_path + '.types', 'r') as file:
            encryption_types = file.read().split(',')

        decrypted_text = ''.join(
            decrypt_char(char, enc_type, multiplier_n, multiplier_m) for char, enc_type in zip(encrypted_text, encryption_types)
        )

        with open(output_file_path, 'w') as file:
            file.write(decrypted_text)

        print(f"File decrypted and saved to {output_file_path}")
        return decrypted_text
    except Exception as error:
        print(f"Error: {error}")
        return None


def verify_decryption(original_file_path, decrypted_text):
    try:
        with open(original_file_path, 'r') as file:
            original_text = file.read()

        if original_text == decrypted_text:
            print("Decryption verified successfully")
            return True
        else:
            print("Decryption verification failed")
            return False
    except Exception as error:
        print(f"Error: {error}")
        return False


def main():
    try:
        multiplier_n = int(input("Enter multiplier n: "))
        multiplier_m = int(input("Enter multiplier m: "))
    except ValueError:
        print("Invalid input. Enter integers only.")
        return

    input_file_path = "raw_text.txt"
    encrypted_file_path = "encrypted_text.txt"
    decrypted_file_path = "decrypted_text.txt"

    encrypt_file(input_file_path, encrypted_file_path, multiplier_n, multiplier_m)
    decrypted_text = decrypt_file(encrypted_file_path, decrypted_file_path, multiplier_n, multiplier_m)

    if decrypted_text is not None:
        verify_decryption(input_file_path, decrypted_text)


if __name__ == "__main__":
    main()
