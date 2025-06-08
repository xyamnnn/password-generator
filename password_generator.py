#!/usr/bin/env python3
"""
Password Generator & Manager
Created by xyamnnn
"""

import random
import string
import os
import json
from datetime import datetime
from pathlib import Path

class PasswordGenerator:
    def __init__(self):
        downloads_path = Path.home() / "Downloads"
        self.notes_file = downloads_path / "passwords.txt"
        self.settings_file = downloads_path / "password_settings.json"
        downloads_path.mkdir(exist_ok=True)
        
        self.default_settings = {
            "length": 12,
            "include_symbols": True,
            "include_numbers": True,
            "include_uppercase": True,
            "include_lowercase": True
        }
        
        self.settings = self.load_settings()
        
    def generate_password(self, length=12, include_symbols=True, include_numbers=True, include_uppercase=True, include_lowercase=True):
        """Ultra-random password generation with chaos algorithms"""
        import time
        import hashlib
        
        # Seed with current time microseconds for true randomness
        random.seed(int(time.time() * 1000000) % 2147483647)
        
        symbols_basic = "!@#$%^&*"
        symbols_extended = "()_+-=[]{}|;:,.<>?~`"
        symbols_extra = "§±¿¡¢£¥€"
        
        # Create character pools
        pools = {}
        if include_lowercase:
            pools['lower'] = list(string.ascii_lowercase)
        if include_uppercase:
            pools['upper'] = list(string.ascii_uppercase)
        if include_numbers:
            pools['digits'] = list(string.digits)
        if include_symbols:
            pools['symbols1'] = list(symbols_basic)
            pools['symbols2'] = list(symbols_extended)
            pools['symbols3'] = list(symbols_extra)
        
        if not pools:
            pools['fallback'] = list(string.ascii_letters + string.digits)
        
        # Generate password with maximum chaos
        password = []
        
        # First pass: ensure at least one from each type
        for pool_name, pool_chars in pools.items():
            if len(password) < length:
                # Multiple random selections and hash-based choice
                temp_choices = [random.choice(pool_chars) for _ in range(5)]
                hash_input = str(time.time() * random.random()).encode()
                hash_val = int(hashlib.md5(hash_input).hexdigest()[:8], 16)
                chosen_char = temp_choices[hash_val % len(temp_choices)]
                password.append(chosen_char)
        
        # Second pass: fill remaining with pure chaos
        all_chars = []
        for pool_chars in pools.values():
            all_chars.extend(pool_chars)
        
        while len(password) < length:
            # Triple randomization
            method = random.randint(1, 4)
            
            if method == 1:
                # Random pool selection
                pool_name = random.choice(list(pools.keys()))
                password.append(random.choice(pools[pool_name]))
            elif method == 2:
                # Hash-based selection
                hash_input = str(random.random() * time.time()).encode()
                hash_val = int(hashlib.md5(hash_input).hexdigest()[:8], 16)
                password.append(all_chars[hash_val % len(all_chars)])
            elif method == 3:
                # Time-based selection
                time_val = int(time.time() * 1000000) % len(all_chars)
                password.append(all_chars[time_val])
            else:
                # Pure random
                password.append(random.choice(all_chars))
        
        # Chaos shuffling with multiple algorithms
        for _ in range(random.randint(5, 12)):
            # Method 1: Standard shuffle
            random.shuffle(password)
            
            # Method 2: Reverse random sections
            if len(password) > 3:
                start = random.randint(0, len(password) - 3)
                end = random.randint(start + 2, len(password))
                password[start:end] = password[start:end][::-1]
            
            # Method 3: Swap random positions
            for _ in range(random.randint(2, 6)):
                if len(password) > 1:
                    i, j = random.sample(range(len(password)), 2)
                    password[i], password[j] = password[j], password[i]
        
        # Final chaos: split and recombine randomly
        if len(password) > 4:
            split_points = sorted(random.sample(range(1, len(password)), random.randint(1, 3)))
            sections = []
            last_point = 0
            for point in split_points + [len(password)]:
                sections.append(password[last_point:point])
                last_point = point
            random.shuffle(sections)
            password = [char for section in sections for char in section]
        
        return ''.join(password)
    
    def load_settings(self):
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    saved_settings = json.load(f)
                return saved_settings
        except:
            pass
        return self.default_settings.copy()
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
        except Exception as e:
            print(f"Warning: Couldn't save settings: {e}")
    
    def auto_open_notepad(self):
        try:
            import platform
            import subprocess
            if platform.system() == "Windows":
                subprocess.run(['taskkill', '/f', '/im', 'notepad.exe'], 
                             capture_output=True, check=False)
                subprocess.Popen(['notepad.exe', str(self.notes_file)], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                print(f"File saved at: {self.notes_file}")
        except Exception:
            print(f"File saved at: {self.notes_file}")
    
    def view_passwords(self):
        if not os.path.exists(self.notes_file):
            print("No passwords saved yet!")
            return
            
        try:
            with open(self.notes_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                
            if not content:
                print("No passwords saved yet!")
                return
                
            print("\nSaved Passwords:")
            print("=" * 80)
            print(content)
            print("=" * 80)
            
        except Exception as e:
            print(f"Error reading passwords: {e}")
    
    def update_password(self, label, new_password):
        clean_label = label.strip()
        new_entry = f"Username: {clean_label} Password: {new_password}\n"
        
        if not os.path.exists(self.notes_file):
            with open(self.notes_file, "w", encoding="utf-8") as f:
                f.write(new_entry)
                f.flush()
            self.auto_open_notepad()
            return True
            
        try:
            with open(self.notes_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            while lines and lines[0].strip() == "":
                lines.pop(0)
            
            updated = False
            for i, line in enumerate(lines):
                if line.startswith("Username:"):
                    existing_label = line.split("Username:")[1].split("Password:")[0].strip()
                    if existing_label.lower() == clean_label.lower():
                        lines[i] = new_entry
                        updated = True
                        break
            
            if not updated:
                lines.append(new_entry)
            
            with open(self.notes_file, "w", encoding="utf-8") as f:
                f.writelines(lines)
                f.flush()
            
            self.auto_open_notepad()
            return True
            
        except Exception as e:
            print(f"Error updating password: {e}")
            return False

def main():
    generator = PasswordGenerator()
    
    print("Password Generator & Manager")
    print("=" * 30)
    
    try:
        while True:
            print("\nOptions:")
            print("1. Generate new password")
            print("2. View all passwords")
            print("3. Update existing password")
            print("4. Custom password settings")
            print("5. Exit")
            
            choice = input("\nChoose an option (1-5): ").strip()
            
            if choice == "1":
                label = input("Password for? ").strip()
                if not label:
                    print("Label cannot be empty!")
                    continue
                    
                password = generator.generate_password(
                    length=generator.settings["length"],
                    include_symbols=generator.settings["include_symbols"],
                    include_numbers=generator.settings["include_numbers"],
                    include_uppercase=generator.settings["include_uppercase"],
                    include_lowercase=generator.settings["include_lowercase"]
                )
                print(f"Generated: {password}")
                generator.update_password(label, password)
                generator.save_settings()
                     
            elif choice == "2":
                generator.view_passwords()
                 
            elif choice == "3":
                label = input("Update password for? ").strip()
                if not label:
                    print("Label cannot be empty!")
                    continue
                    
                password = generator.generate_password(
                    length=generator.settings["length"],
                    include_symbols=generator.settings["include_symbols"],
                    include_numbers=generator.settings["include_numbers"],
                    include_uppercase=generator.settings["include_uppercase"],
                    include_lowercase=generator.settings["include_lowercase"]
                )
                print(f"Generated: {password}")
                generator.update_password(label, password)
                generator.save_settings()
                     
            elif choice == "4":
                print(f"\nCurrent: Length={generator.settings['length']}, Symbols={generator.settings['include_symbols']}")
                try:
                    length = int(input(f"Password length ({generator.settings['length']}): ") or str(generator.settings['length']))
                    include_symbols = input(f"Include symbols? ({'y' if generator.settings['include_symbols'] else 'n'}): ").lower() != 'n'
                    include_numbers = input(f"Include numbers? ({'y' if generator.settings['include_numbers'] else 'n'}): ").lower() != 'n'
                    include_uppercase = input(f"Include uppercase? ({'y' if generator.settings['include_uppercase'] else 'n'}): ").lower() != 'n'
                    include_lowercase = input(f"Include lowercase? ({'y' if generator.settings['include_lowercase'] else 'n'}): ").lower() != 'n'
                    
                    generator.settings = {
                        "length": length,
                        "include_symbols": include_symbols,
                        "include_numbers": include_numbers,
                        "include_uppercase": include_uppercase,
                        "include_lowercase": include_lowercase
                    }
                    
                    generator.save_settings()
                    print("Settings saved!")
                    
                    label = input("Password for? ").strip()
                    if not label:
                        print("Label cannot be empty!")
                        continue
                        
                    password = generator.generate_password(
                        length=length,
                        include_symbols=include_symbols,
                        include_numbers=include_numbers,
                        include_uppercase=include_uppercase,
                        include_lowercase=include_lowercase
                    )
                    
                    print(f"Generated: {password}")
                    generator.update_password(label, password)
                        
                except ValueError:
                    print("Invalid input! Please enter valid numbers.")
                    
            elif choice == "5":
                generator.save_settings()
                break
                
            else:
                print("Invalid choice! Please choose 1-5.")
    
    except KeyboardInterrupt:
        generator.save_settings()
        print("\nGoodbye!")

if __name__ == "__main__":
    main() 
