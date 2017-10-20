import glob

def available_name():
    names = glob.glob('/dev/ttyACM*')
    return names[0]

def main():
    print available_name()

if __name__ == '__main__':
    main()
