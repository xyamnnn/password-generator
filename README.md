# 🔐 Password Generator & Manager

I got tired of using weak passwords and forgetting them, so I built this simple tool that generates secure passwords and saves them automatically to a text file.

## What it does

- Generates random, secure passwords 
- Saves them to `Downloads/passwords.txt` with labels
- Opens the file in Notepad automatically so you can see your passwords
- Updates existing passwords if you use the same label twice
- Works on Windows, Mac, and Linux

## How to use

### Step 1: Download the file
- Download `password_generator.py` to any folder (like Downloads or Desktop)

### Step 2: Open your terminal/command prompt
**Windows:**
- Press `Windows + R`, type `cmd`, press Enter
- OR search "Command Prompt" in start menu
- OR search "PowerShell" in start menu

**Mac:**
- Press `Cmd + Space`, type "Terminal", press Enter
- OR go to Applications > Utilities > Terminal

**Linux:**
- Press `Ctrl + Alt + T`
- OR search "Terminal" in your applications

### Step 3: Navigate to where you saved the file
```bash
# If you saved it to Downloads:
cd Downloads

# If you saved it to Desktop:
cd Desktop

# If you saved it somewhere else, replace with your path:
cd path/to/your/folder
```

### Step 4: Run the script
```bash
python password_generator.py
```

**If that doesn't work, try:**
```bash
python3 password_generator.py
```

### Step 5: Use it
- Pick option 1 from the menu
- Type what the password is for (like "facebook" or "work email")  
- Done! It creates a secure password and saves it to your Downloads folder

## What the output looks like

Your `passwords.txt` file will look like this:
```
Username: facebook Password: Xy9#mK2$pL4!
Username: gmail Password: Bz8&nQ5@rT3%
Username: work laptop Password: Qw7!mN3$kL9@
```

## Menu options

1. **Generate new password** - Make a new password and save it
2. **View all passwords** - See everything you've saved
3. **Update existing password** - Change an existing password
4. **Custom password settings** - Pick length and what characters to use
5. **Exit** - Quit

## Password settings

- Length: 4-128 characters (default is 12)
- Can include/exclude: lowercase, uppercase, numbers, symbols

## Where it saves

Passwords go to your Downloads folder:
- Windows: `C:\Users\YourName\Downloads\passwords.txt`
- Mac: `/Users/YourName/Downloads/passwords.txt`
- Linux: `/home/YourName/Downloads/passwords.txt`

## Requirements

- Python 3.6 or newer (most computers have this already)
- That's it - no extra packages needed

### Don't have Python?
**Windows:** Download from [python.org](https://www.python.org/downloads/) and check "Add to PATH" during installation

**Mac:** Usually comes pre-installed, but you can get the latest from [python.org](https://www.python.org/downloads/)

**Linux:** Usually pre-installed, if not: `sudo apt install python3` (Ubuntu/Debian) or `sudo yum install python3` (CentOS/RHEL)

## Notes

- Passwords are saved in plain text, so don't use this for super sensitive stuff
- For high-security accounts, use a proper password manager like Bitwarden
- The file auto-opens in Notepad on Windows so you can copy your passwords easily

## License

MIT License - feel free to use and modify however you want. 
