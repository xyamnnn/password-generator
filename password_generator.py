"""
Password Generator & Manager
Created by xyamnnn
"""

import secrets
import string
import os
import json
import math
from pathlib import Path

class PasswordGenerator:
    def __init__(self):
        downloads_path = Path.home() / "Downloads"
        self.notes_file = downloads_path / "passwords.txt"
        self.settings_file = downloads_path / "password_settings.json"
        downloads_path.mkdir(exist_ok=True)
        
        self.default_settings = {
            "length": 18, "include_symbols": True, "include_numbers": True,
            "include_uppercase": True, "include_lowercase": True,
            "include_extended_symbols": True
        }
        self.settings = self.load_settings()
        
        self.basic_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?~`"
        self.extended_chars = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    
    def format_crack_time(self, years):
        if years < 1e12: return f"{years/1e9:.1f} billion years"
        elif years < 1e15: return f"{years/1e12:.1f} trillion years"
        elif years < 1e18: return f"{years/1e15:.1f} quadrillion years"
        elif years < 1e21: return f"{years/1e18:.1f} quintillion years"
        else: return f"{years:.2e} years"
    
    def generate_password(self, length=18, **options):
        length = max(12, length)
        
        chars = ""
        required = []
        
        if options.get('include_lowercase', True):
            chars += string.ascii_lowercase
            required.append(secrets.choice(string.ascii_lowercase))
        if options.get('include_uppercase', True):
            chars += string.ascii_uppercase
            required.append(secrets.choice(string.ascii_uppercase))
        if options.get('include_numbers', True):
            chars += string.digits
            required.append(secrets.choice(string.digits))
        if options.get('include_symbols', True):
            symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?~`"
            chars += symbols
            required.append(secrets.choice(symbols))
        if options.get('include_extended_symbols', True):
            chars += self.extended_chars
            required.append(secrets.choice(self.extended_chars))
        
        if not chars: chars = self.basic_chars
        
        remaining = length - len(required)
        if remaining > 0:
            password_list = required + [secrets.choice(chars) for _ in range(remaining)]
        else:
            password_list = required[:length]
        
        for i in range(len(password_list) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            password_list[i], password_list[j] = password_list[j], password_list[i]
        
        password = ''.join(password_list)
        
        return password
    
    def load_settings(self):
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    saved = json.load(f)
                for key, value in self.default_settings.items():
                    if key not in saved: saved[key] = value
                return saved
        except: pass
        return self.default_settings.copy()
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
                f.flush()
        except Exception as e:
            print(f"Warning: {e}")
    
    def auto_open_notepad(self):
        try:
            import platform, subprocess
            if platform.system() == "Windows":
                subprocess.run(['taskkill', '/f', '/im', 'notepad.exe'], capture_output=True, check=False)
                subprocess.Popen(['notepad.exe', str(self.notes_file)], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                print(f"File: {self.notes_file}")
        except: print(f"File: {self.notes_file}")
    
    def view_passwords(self):
        if not os.path.exists(self.notes_file):
            print("No passwords saved yet!")
            return
        try:
            with open(self.notes_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                print("\n" + "="*80)
                print(content)
                print("="*80)
            else:
                print("No passwords saved yet!")
        except Exception as e:
            print(f"Error: {e}")
    
    def update_password(self, label, password):
        entry = f"Username: {label.strip()} Password: {password}\n"
        
        if not os.path.exists(self.notes_file):
            with open(self.notes_file, "w", encoding="utf-8") as f:
                f.write(entry)
            self.auto_open_notepad()
            return
            
        try:
            with open(self.notes_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            updated = False
            for i, line in enumerate(lines):
                if line.startswith("Username:"):
                    existing = line.split("Username:")[1].split("Password:")[0].strip()
                    if existing.lower() == label.strip().lower():
                        lines[i] = entry
                        updated = True
                        break
            
            if not updated: lines.append(entry)
            
            with open(self.notes_file, "w", encoding="utf-8") as f:
                f.writelines(lines)
            self.auto_open_notepad()
        except Exception as e:
            print(f"Error: {e}")

def main():
    gen = PasswordGenerator()
    
    print("Password Generator & Manager")
    print("="*30)
    
    try:
        while True:
            print("\n1. Generate password")
            print("2. View passwords")
            print("3. Update password")
            print("4. Settings")
            print("5. Exit")
            
            choice = input("\nChoice (1-5): ").strip()
            
            if choice in ["1", "3"]:
                label = input("Password for: ").strip()
                if not label:
                    print("Label required!")
                    continue
                
                password = gen.generate_password(
                    length=gen.settings["length"],
                    include_symbols=gen.settings["include_symbols"],
                    include_numbers=gen.settings["include_numbers"],
                    include_uppercase=gen.settings["include_uppercase"],
                    include_lowercase=gen.settings["include_lowercase"],
                    include_extended_symbols=gen.settings["include_extended_symbols"]
                )
                print(f"\nPassword: {password}")
                gen.update_password(label, password)
                gen.save_settings()
                
            elif choice == "2":
                gen.view_passwords()
                
            elif choice == "4":
                print(f"\nCurrent length: {gen.settings['length']}")
                try:
                    length = int(input(f"Length (min 12): ") or gen.settings['length'])
                    symbols = input("Basic symbols (y/n): ").lower() != 'n'
                    numbers = input("Numbers (y/n): ").lower() != 'n'
                    upper = input("Uppercase (y/n): ").lower() != 'n'
                    lower = input("Lowercase (y/n): ").lower() != 'n'
                    extended = input("Extended symbols (y/n): ").lower() != 'n'
                    
                    gen.settings.update({
                        "length": max(12, length), "include_symbols": symbols,
                        "include_numbers": numbers, "include_uppercase": upper,
                        "include_lowercase": lower, "include_extended_symbols": extended
                    })
                    
                    gen.save_settings()
                    print("Settings saved!")
                    
                    label = input("Generate password for: ").strip()
                    if label:
                        password = gen.generate_password(**gen.settings)
                        print(f"\nPassword: {password}")
                        gen.update_password(label, password)
                        
                except ValueError:
                    print("Invalid input!")
                    
            elif choice == "5":
                gen.save_settings()
                break
            else:
                print("Invalid choice!")
                
    except KeyboardInterrupt:
        gen.save_settings()
        print("\nGoodbye!")

if __name__ == "__main__":
    main() 
