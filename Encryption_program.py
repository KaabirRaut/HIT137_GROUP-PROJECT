# Question 1 solution:
def encrypt_char(c, n, m):
    if 'a' <= c <= 'z':
        if c <= 'm':
            # First half of lowercase: shift forward by n*m
            shift = n * m
            new_ord = ord(c) + shift
            # Handle wrap-around
            new_ord = ord('a') + (new_ord - ord('a')) % 26
            return (chr(new_ord), 'lower_first')
        else:
            # Second half of lowercase: shift backward by n+m
            shift = n + m
            new_ord = ord(c) - shift
            # Handle wrap-around
            new_ord = ord('a') + (new_ord - ord('a')) % 26
            return (chr(new_ord), 'lower_second')
    elif 'A' <= c <= 'Z':
        if c <= 'M':
            # First half of uppercase: shift backward by n
            shift = n
            new_ord = ord(c) - shift
            # Handle wrap-around
            new_ord = ord('A') + (new_ord - ord('A')) % 26
            return (chr(new_ord), 'upper_first')
        else:
            # Second half of uppercase: shift forward by m^2
            shift = m ** 2
            new_ord = ord(c) + shift
            # Handle wrap-around
            new_ord = ord('A') + (new_ord - ord('A')) % 26
            return (chr(new_ord), 'upper_second')
    else:
        # Special characters and numbers remain unchanged
        return (c, 'other')

def decrypt_char(c, encryption_type, n, m):
    if encryption_type == 'lower_first':
        # Reverse first half lowercase encryption
        shift = n * m
        new_ord = ord(c) - shift
        new_ord = ord('a') + (new_ord - ord('a')) % 26
        return chr(new_ord)
    elif encryption_type == 'lower_second':
        # Reverse second half lowercase encryption
        shift = n + m
        new_ord = ord(c) + shift
        new_ord = ord('a') + (new_ord - ord('a')) % 26
        return chr(new_ord)
    elif encryption_type == 'upper_first':
        # Reverse first half uppercase encryption
        shift = n
        new_ord = ord(c) + shift
        new_ord = ord('A') + (new_ord - ord('A')) % 26
        return chr(new_ord)
    elif encryption_type == 'upper_second':
        # Reverse second half uppercase encryption
        shift = m ** 2
        new_ord = ord(c) - shift
        new_ord = ord('A') + (new_ord - ord('A')) % 26
        return chr(new_ord)
    else:
        # Special characters and numbers remain unchanged
        return c

def encrypt_file(input_file, output_file, n, m):
    try:
        with open(input_file, 'r') as f:
            content = f.read()
        
        encrypted_chars = [encrypt_char(c, n, m) for c in content]
        encrypted_content = ''.join([char for char, _ in encrypted_chars])
        
        # Save both the encrypted content and the encryption types
        with open(output_file, 'w') as f:
            f.write(encrypted_content)
        
        # Save encryption types to a separate file for decryption
        with open(output_file + '.types', 'w') as f:
            f.write(','.join([etype for _, etype in encrypted_chars]))
            
        print(f"✅ File encrypted successfully and saved to {output_file}")
    except Exception as e:
        print(f"❌ Error during encryption: {e}")

def decrypt_file(input_file, output_file, n, m):
    try:
        with open(input_file, 'r') as f:
            content = f.read()
        
        # Read the encryption types
        with open(input_file + '.types', 'r') as f:
            encryption_types = f.read().split(',')
        
        decrypted_content = ''.join([
            decrypt_char(c, etype, n, m) 
            for c, etype in zip(content, encryption_types)
        ])
        
        with open(output_file, 'w') as f:
            f.write(decrypted_content)
            
        print(f"✅ File decrypted successfully and saved to {output_file}")
        return decrypted_content
    except Exception as e:
        print(f"❌ Error during decryption: {e}")
        return None

def verify_decryption(original_file, decrypted_content):
    try:
        with open(original_file, 'r') as f:
            original_content = f.read()
        
        if original_content == decrypted_content:
            print("✅ Verification successful: Decrypted content matches original")
            return True
        else:
            print("❌ Verification failed: Decrypted content does NOT match original")
            # Print first 10 differing characters for debugging
            print("\nDebugging info (first 10 differences):")
            for i, (orig, dec) in enumerate(zip(original_content, decrypted_content)):
                if orig != dec:
                    print(f"Position {i}: Original '{orig}' (ord={ord(orig)}), Decrypted '{dec}' (ord={ord(dec)})")
                    if len([x for x in original_content if x != decrypted_content[original_content.index(x)]]) >= 10:
                        break
            return False
    except Exception as e:
        print(f"❌Error during verification: {e}")
        return False

def main():
    # Get user inputs for n and m
    try:
        n = int(input("Enter value for n (integer): "))
        m = int(input("Enter value for m (integer): "))
    except ValueError:
        print("Please enter valid integers for n and m")
        return
    
    input_file = "raw_text.txt"
    encrypted_file = "encrypted_text.txt"
    decrypted_file = "decrypted_text.txt"
    
    # Encrypt the file
    encrypt_file(input_file, encrypted_file, n, m)
    
    # Decrypt the file
    decrypted_content = decrypt_file(encrypted_file, decrypted_file, n, m)
    
    # Verify the decryption
    if decrypted_content is not None:
        verify_decryption(input_file, decrypted_content)

if __name__ == "__main__":
    main()