#Enc - rpyt
# This program scatters any file and makes it just a bit harder decode.


import random, os, sys, subprocess
alpha='abcdefghijklmnopqrstuvwxyz1234567890' # You may modify this if you wish.

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

print('Please Save All of this!!')
print('Your Key:', key)
print('Seed Kit: \n  ', random_seed_kit)

# -- Encryption/Decryption --
def encrypt(key, msg):
    encryped = []
    for i, c in enumerate(msg):
        key_c = ord(key[i % len(key)])
        msg_c = ord(c)
        encryped.append(chr((msg_c + key_c) % 127))
    return ''.join(encryped)

def decrypt(key, encryped):
    msg = []
    for i, c in enumerate(encryped):
        key_c = ord(key[i % len(key)])
        enc_c = ord(c)
        msg.append(chr((enc_c - key_c) % 127))
    return ''.join(msg)

# -- Main Proccess--
if __name__ == '__main__':
    while True:
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
            new_file = open(new_name, 'x')
            new_file.write(text_x)
            new_file.close()
        else:
            print(text_x)
        # Saves our tax returns
        if save_keyToFile:
            print("Tax Returns Saved!")
            new_file = open('tax_returns.txt', 'x')
            new_file.write("taxHash='"+str(key)+"'")
            if save_SeedKitToFile:
                new_file.write("\ntaxList="+str(random_seed_kit)+"")
    elif prompt == "2": # Decrypt
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
            os.remove('tax_returns.txt')
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
