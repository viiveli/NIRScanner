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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostbyname(device_id), port))

    data = s.recv(1024)

    if not data:
        pass
    else:
        return json.loads(data)
        s.close()

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
            print("Retrieved spectrum:", data["spectrum"])

            df = pd.DataFrame(data["spectrum"])
            prediction = mlmodel.predict(df.T)

            print("identified as:", spectrum_db.type.unique()[prediction])
            
        elif mode == "m":
            break

def retrieve_spectrum_data():
    clear_screen()
    material_type = "cotton" # change material type accordingly
    
    print("# Retrieve & save spectrum data from scanner\n")

    print("enter)".rjust(10) + " Poll scanner")
    print("m)".rjust(10) + " Return to main menu\n")
    
    while True:
        mode = input("\ninput: ")

        if mode == "":
            print("Polling scanner...")
            data = poll_scanner()
            print("Retrieved spectrum:", data["spectrum"])

            new_db_entry = data["spectrum"]
            new_db_entry.append(material_type)

            with open("spectrum_db.csv", "a") as f:
                f.write("\n" + str(new_db_entry).strip("[]").replace("'", ""))

            print("saved to db as " + material_type)

        elif mode == "m":
            break

try:
    while True:
        main_menu()

except Exception as e:
    print(e)
    input()
    main_menu()
