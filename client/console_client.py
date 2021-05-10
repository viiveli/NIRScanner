import socket, json, pickle, os
from sklearn.neural_network import MLPClassifier
import pandas as pd

mlmodel = pickle.load(open("mlmodel.mdl", "rb"))
spectrum_db = pd.read_csv("spectrum_db.csv", skipinitialspace=True)

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    else:
        print('Unknown operating system. Unable to clear screen.')

def poll_scanner(device_id='c44f330a102d', port=65432):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket.gethostbyname(device_id), port))

        data = s.recv(1024)

        if not data:
            pass
        else:
            s.close()
            return json.loads(data)
    
    except Exception as e:
        print(e)
        return None

def main_menu():
    clear_screen()

    print("# Menu\n")
    print("i)".rjust(10) + " Identify materials")
    print("r)".rjust(10) + " Retrieve & save spectrum data from scanner\n")
    print("q)".rjust(10) + " Quit\n")
    
    mode = input("\ninput: ")

    if mode == "i":
        identify_materials()
    elif mode == "r":
        retrieve_spectrum_data()
    elif mode == "q":
        quit()
    else:
        pass

def identify_materials():
    clear_screen()
    print("# Identify materials\n")
    print("enter)".rjust(10) + " Poll scanner")
    print("m)".rjust(10) + " Return to main menu\n")

    while True:
        mode = input("\ninput: ")

        if mode == "":
            print("Polling scanner...")
            data = poll_scanner()

            if not data:
                print('error while polling scanner...')
                input('press any kay to return to main menu...')
                break

            print("Retrieved spectrum:", data["spectrum"])

            df = pd.DataFrame(data["spectrum"])
            prediction = mlmodel.predict(df.T)

            print("identified as:", spectrum_db.type.unique()[prediction])
            
        elif mode == "m":
            break

def retrieve_spectrum_data():
    clear_screen()
    materials_in_db = pd.unique(spectrum_db['type'])
    
    print("# Retrieve & save spectrum data from scanner\n")
    print("choose material type...\n")

    while True:
        for idx, material in enumerate(materials_in_db):
            print(f'{ str(idx) })'.rjust(10), material)

        print('\n' + 'n)'.rjust(10) + ' add new material')

        material = input('\ninput: ')

        if material.isnumeric() and int(material) in range(len(materials_in_db)):
            material = materials_in_db[int(material)]
            break
        elif material == 'n':
            material = input('Enter new material type: ').lower()
            break
        else:
            continue

    print(f'\nRetrieving { material } spectrum data...\n')

    print("enter)".rjust(10) + " Poll scanner")
    print("m)".rjust(10) + " Return to main menu\n")
    
    while True:
        mode = input("\ninput: ")

        if mode == "":
            print("Polling scanner...")
            data = poll_scanner()

            if not data:
                print('error while polling scanner...')
                input('press any kay to return to main menu...')
                break

            print("Retrieved spectrum:", data["spectrum"])

            new_db_entry = data["spectrum"]
            new_db_entry.append(material)

            with open("spectrum_db.csv", "a") as f:
                f.write("\n" + str(new_db_entry).strip("[]").replace("'", ""))

            print("saved to db as " + material)

        elif mode == "m":
            break

try:
    while True:
        main_menu()

except Exception as e:
    print(e)
    input()
    main_menu()
