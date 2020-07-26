from basicModule import boot
from sys import argv

if __name__ == "__main__":
    print(argv)
    if len(argv) > 1:
        boot.run(argv[1])
    else:
        boot.run('yc')
