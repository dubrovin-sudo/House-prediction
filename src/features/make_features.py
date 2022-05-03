import os

if __name__ == "__main__":

    for dirname, _, filenames in os.walk("/data/interim"):
        for filename in filenames:
            print(os.path.join(dirname, filename))
