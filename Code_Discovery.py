#Enc - rpyt
# This program scatters any file and makes it just a bit harder decode.


import random, os, sys, subprocess
alpha='abcdefghijklmnopqrstuvwxyz1234567890' # You may modify this if you wish.

args= sys.argv # Gets the arguments from the command line.
print(args)
# -- Key Settings -- 
key_length = 50 # defualt 25
random_seed = 12415 # defualt 10
# -- End Of Key Settings --

# -- QOL Settings --
save_keyToFile=True # Saves key to a file. Will also store setting below in same file.
save_SeedKitToFile=True # Saves random_seed_kit to same file as above, but different than below. save_keyToFile must also be True.
save_CryptionToFile=True # Saves encryption/decryption to a seperate isolated file.
overwriteCurrentFile=False # Overwrites the file that's either being encrypted or decrypted. save_CryptionToFile must be True. NOT RECCOMENDED!
# -- END OF QOL SETTINGS --

random_seed_kit = [] # every random seed used.
random_seed_kit.append(random_seed) # random_seed changes often. Save this with all others coming soon. Saves the intial seed.
def randomizeSeed():
    global random_seed, random_seed_kit, alpha, random
    c = random.randint(0, random_seed)
    random_seed_kit.append(c)
    random.seed(c)

key = ''
for i in range(key_length):
    key += alpha[random.randint(0, len(alpha)-1)]
    randomizeSeed()

print('Keys for non specified key -k:')
print('Your Key:', key)
print('Seed Kit: \n  ', random_seed_kit)

# -- Encryption/Decryption --
def encrypt(key, msg):
    encryped = []  # Initialize an empty list to hold the encrypted characters
    for i, c in enumerate(msg):  # Loop over each character in the message
        key_c = ord(key[i % len(key)])  # Get the ASCII value of the key character, cycling through the key if it's shorter than the message
        msg_c = ord(c)  # Get the ASCII value of the message character
        encryped.append(chr((msg_c + key_c) % 127))  # Add the encrypted character to the list. The encryption is done by adding the key and message ASCII values and taking the modulus 127 to keep it within ASCII range
    return ''.join(encryped)  # Join the list of encrypted characters into a string and return it

def decrypt(key, encryped):
    msg = []  # Initialize an empty list to hold the decrypted characters
    for i, c in enumerate(encryped):  # Loop over each character in the encrypted message
        key_c = ord(key[i % len(key)])  # Get the ASCII value of the key character, cycling through the key if it's shorter than the message
        enc_c = ord(c)  # Get the ASCII value of the encrypted character
        msg.append(chr((enc_c - key_c) % 127))  # Add the decrypted character to the list. The decryption is done by subtracting the key from the encrypted ASCII values and taking the modulus 127 to keep it within ASCII range
    return ''.join(msg)  # Join the list of decrypted characters into a string and return it

def string_to_binary(s):
    return [format(ord(c), '08b') for c in s]

# -- Main Proccess--
if __name__ == '__main__':
    argPrompts=False
    if ('-e' in args or '-E' in args) and ('-d' in args or '-D' in args):
        print('Invalid Arguments: Cannot Encrypt and Decrypt at the same time.')
        sys.exit()
    if '-e' in args or '-E' in args:
        if '-E' in args: 
            id = args.index('-E')
            args[id] = '-e'
        argPrompts=True
        prompt='1'  
    if '-d' in args or '-D' in args:
        if '-D' in args: 
            id = args.index('-D')
            args[id] = '-d'
        argPrompts=True
        prompt='2'
    if argPrompts==True:
        # Removes the file name and changes directory to the file's location.
        try:
            drChange = os.path.dirname(args[args.index('-e')+1])
            file_nameArg = os.path.basename(args[args.index('-e')+1])
        except:
            drChange = os.path.dirname(args[args.index('-d')+1])
            file_nameArg = os.path.basename(args[args.index('-d')+1])
        os.chdir(drChange)
        print('Changed Directory to:', os.getcwd())
        try:
            if os.path.exists('tax_returns.txt'):
                with open('tax_returns.txt', 'r') as file:
                    exec(file.read())
                    print(taxHash)
        except:
            key=args.index('-e')+1
            if key != str:
                raise Exception('Key not specified. And tax_returns.txt not found. Please specify a key.')     
    if argPrompts==False:
        while True:
            # List all files in current directory
            x = subprocess.check_output(['ls'])
            x = x.decode()
            xlist=[]
            a, b = 0, 0
            for i in range(len(x)):
                if x[i] == '\n':
                    xlist.append(x[a:b]) # Adds everything between a and b to the list right before the '\n'
                    a = b; b = a+1 
                else:
                    b+=1
            xlist[0]='\n'+xlist[0] # Fixes the first entry not being a valid file/folder
            for i in range(len(xlist)):
                print(('('+str(i)+') - '+str((xlist[i])[1:len(xlist[i])])))
            totalEntryC=len(xlist) # Total amount of files/folders
            # Display Options
            file_name = input('\n\nTo change directory or open discovery type -( dir )-\nPlease enter file # to crypt: ')
            if file_name not in ['dir', 'ls', 'directory', 'path']:
                if int(file_name) <= totalEntryC-1:
                    if int(file_name) > -1:
                        choice = int(file_name); changedir = (str((xlist[choice])[1:len(xlist[choice])]))
                        if os.path.isdir(changedir) == True:
                            print(' -- Selection not a file, instead a directory. Changing directory to:', changedir, ' --')
                            os.chdir(changedir)
                        else:
                            print('File Exists:', os.path.exists(changedir))
                            if os.path.exists(changedir):
                                break
            else:
                finished=False
                clearScreen=True
                while finished==False:
                    if clearScreen == True:
                        os.system('clear')
                    clearScreen=True # Resets back to True, just incase it's still false.
                    current_directory = os.getcwd()
                    print('Current Directory:',current_directory)
                    print('ls - lists all in current dir',
                            '\nback - Goes back 1 folder',
                            '\nreturn - Go back to file selection')
                    output=input('Input new directory: ')
                    if output=='back':
                        c=len(current_directory)
                        a = c
                        for i in range(c):
                            if current_directory[a-1] == "/":
                                try:
                                    os.chdir(str(current_directory[0:a-1]))
                                except:
                                    os.system('clear')
                                    print('Not recommended to go beyond users.')
                                    clearScreen=False
                            else:
                                a-=1
                    elif output=='ls':
                        #os.system('clear')
                        x = subprocess.check_output(['ls'])
                        x = x.decode()
                        xlist=[]
                        a, b = 0, 0
                        for i in range(len(x)):
                            if x[i] == '\n':
                                xlist.append(x[a:b])
                                a = b; b = a+1
                            else:
                                b+=1
                        xlist[0]='\n'+xlist[0] # Fixes the first entry not being a valid file/folder
                        for i in range(len(xlist)):
                            print(('('+str(i)+') - '+str((xlist[i])[1:len(xlist[i])])))
                        totalEntryC=len(xlist) # Total amount of files/folders
                        output = input('Enter Number to select: ')
                        if int(output) <= totalEntryC-1:
                            if int(output) > -1:
                                choice = int(output); changedir = (str((xlist[choice])[1:len(xlist[choice])])); os.chdir(changedir)
                            else:
                                print('Invalid Number: Less than expected.')
                        else:
                            print('Invalid Number: Bigger than expected.')
                    elif output=='return':
                        break
                    else:
                        try: os.chdir(output)
                        except: print('Invalid Change!')
        # Beggin encryption/decryption.
        prompt = input('-( 1 )- Encrypt\n-( 2 )- Decrypt\nYour choice: ')
    if prompt == "1": # Encrypt
        try:
            changedir=file_nameArg
        except: # For args only
            pass
        text_c = open(changedir, 'r').read()
        text_x = encrypt(key, text_c)
        if save_CryptionToFile:
            if overwriteCurrentFile==False:
                new_name = ('encr'+changedir)
            else:
                os.remove(changedir)
                new_name = (changedir)
            if os.path.exists(new_name):
                os.remove(new_name)
            print('New File:', new_name)
            new_file = open(new_name, 'w')
            new_file.write(text_x)
            new_file.close()
        else:
            print(text_x)
        # Saves our tax returns
        if save_keyToFile:
            print("Tax Returns Saved!")
            new_file = open('tax_returns.txt', 'w')
            new_file.write("taxHash='"+str(key)+"'")
            if save_SeedKitToFile:
                new_file.write("\ntaxList="+str(random_seed_kit)+"")
    elif prompt == "2": # Decrypt
        try:
            changedir=file_nameArg
        except: # For args only
            pass
        if argPrompts==False:
            if os.path.exists('tax_returns.txt'):
                print('Tax Returns Found!')
                exec(open('tax_returns.txt').read())
                key = taxHash
                #random_seed_kit = taxList
                text_c = open(changedir, 'r').read()
                text_x = decrypt(key, text_c)
            else:
                text_c = open(changedir, 'r').read()
                text_x = decrypt(input('Key: '), text_c)
        else:
            text_c = open(changedir, 'r').read()
            text_x = decrypt(key, text_c)
        if save_CryptionToFile:
            if overwriteCurrentFile==False:
                new_name = ('decr'+changedir)
            else:
                os.remove(changedir)
                new_name = (changedir)
            print('Removing old files...')
            if os.path.exists(new_name):
                os.remove(new_name)
            os.remove(changedir)
            try: os.remove('tax_returns.txt')
            except: pass
            new_file = open(new_name, 'x')
            new_file.write(text_x)
            new_file.close()
            print('New File:', new_name)
            print('Complete!')
        else:
            print(text_x)
    else: # Invalid
        print('Invalid Choice.')
    #encrypted = encrypt(key, msg) 
    #decrypted = decrypt(key, encrypted)
