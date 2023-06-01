import tkinter as tk

def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = gcd_extended(b % a, a)
        return gcd, y - (b // a) * x, x

def affine_encrypt(text, a, b):
    encrypted_text = ""
    for char in text:
        if char.isalnum():
            if char.isalpha():
                char_value = ord(char)
                if char.isupper():
                    encrypted_char = chr(((a * (char_value - 65) + b) % 26) + 65)
                else:
                    encrypted_char = chr(((a * (char_value - 97) + b) % 26) + 97)
            else:
                char_value = ord(char)
                if char.isdigit():
                    encrypted_char = chr(((a * (char_value - 48) + b) % 10) + 48)
                else:
                    encrypted_char = char
        else:
            encrypted_char = char
        encrypted_text += encrypted_char
    return encrypted_text


def affine_decrypt(cipher, a, b):
    decrypted_text = ""
    gcd, a_inverse, _ = gcd_extended(a, 26)  # Check if multiplicative inverse exists
    if gcd != 1:
        return "Invalid 'a' value. Multiplicative inverse does not exist."
    for char in cipher:
        if char.isalnum():
            if char.isalpha():
                char_value = ord(char)
                if char.isupper():
                    decrypted_char = chr(((a_inverse * (char_value - 65 - b)) % 26) + 65)
                else:
                    decrypted_char = chr(((a_inverse * (char_value - 97 - b)) % 26) + 97)
            else:
                char_value = ord(char)
                if char.isdigit():
                    decrypted_char = chr(((a_inverse * (char_value - 48 - b)) % 10) + 48)
                else:
                    decrypted_char = char
        else:
            decrypted_char = char
        decrypted_text += decrypted_char
    return decrypted_text


def affine_encrypt_text():
    text = plaintext_entry.get()
    a = int(a_entry.get())
    b = int(b_entry.get())
    encrypted_text = affine_encrypt(text, a, b)
    ciphertext_entry.delete(0, tk.END)
    ciphertext_entry.insert(tk.END, encrypted_text)


def affine_decrypt_text():
    text = ciphertext_entry.get()
    a = int(a_entry.get())
    b = int(b_entry.get())
    decrypted_text = affine_decrypt(text, a, b)
    decrypted_entry.delete(0, tk.END)
    decrypted_entry.insert(tk.END, decrypted_text)


def crypto_analysis():
    cipher = ciphertext_entry.get()
    for a in range(1, 26):
        gcd, a_inverse, _ = gcd_extended(a, 26)  # Check if multiplicative inverse exists
        if gcd != 1:
            continue
        for b in range(26):
            decrypted_text = affine_decrypt(cipher, a, b)
            if decrypted_text.startswith("Invalid 'a' value."):
                continue
            print(f"a = {a}, b = {b}: {decrypted_text}")


# Create the main window
window = tk.Tk()
window.title("Encryption & Decryption Using Affine")
window.geometry("600x600")
# Customize the color scheme
window.configure(bg="#e6f2ff")  # Set the background color
label_color = "#336699"  # Define a color for labels
button_color = "#00cc66"  # Define a green color for buttons
# Create the input labels and entry fields
plaintext_label = tk.Label(window, text="Plaintext:", bg=window['bg'], fg=label_color)
plaintext_label.pack()
plaintext_entry = tk.Entry(window, width=50, font=("Arial", 12))
plaintext_entry.pack(pady=5)

a_label = tk.Label(window, text="Value of 'a':", bg=window['bg'], fg=label_color)
a_label.pack()
a_entry = tk.Entry(window, width=50, font=("Arial", 12))
a_entry.pack(pady=5)

b_label = tk.Label(window, text="Value of 'b':", bg=window['bg'], fg=label_color)
b_label.pack()
b_entry = tk.Entry(window, width=50, font=("Arial", 12))
b_entry.pack(pady=5)

# Create a frame for the buttons
button_frame = tk.Frame(window, bg=window['bg'])
button_frame.pack(pady=10)

# Create the buttons for encryption, decryption, and cryptoanalysis
encrypt_button = tk.Button(button_frame, text="Encrypt", command=affine_encrypt_text, bg=button_color, relief=tk.RAISED)
encrypt_button.pack(side=tk.LEFT, padx=10)

decrypt_button = tk.Button(button_frame, text="Decrypt", command=affine_decrypt_text, bg=button_color, relief=tk.RAISED)
decrypt_button.pack(side=tk.LEFT, padx=10)

crypto_button = tk.Button(button_frame, text="Cryptoanalysis", command=crypto_analysis, bg=button_color, relief=tk.RAISED)
crypto_button.pack(side=tk.LEFT, padx=10)

# Create the output labels and entry fields
ciphertext_label = tk.Label(window, text="Cipher text:", bg=window['bg'], fg=label_color)
ciphertext_label.pack()
ciphertext_entry = tk.Entry(window, width=50, font=("Arial", 12))
ciphertext_entry.pack(pady=5)

decrypted_label = tk.Label(window, text="Decrypted Text:", bg=window['bg'], fg=label_color)
decrypted_label.pack()
decrypted_entry = tk.Entry(window, width=50, font=("Arial", 12))
decrypted_entry.pack(pady=5)

# Start the GUI event loop
window.mainloop()
