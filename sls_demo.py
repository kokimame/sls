from heuristics import *

def main():
    episode(50)
    [desk.set_tlx(500) for desk in desks]
    episode(50)

if __name__ == "__main__":
    main()