import sys
import ipaddress

# python ips-between.py 192.168.0.100 192.168.0.0 # 100
# python ips-between.py 192.168.1.0 192.168.0.5 # 251


def tonum(adress):
    splitted = adress.split('.')
    return (splitted[0] >> 24) + (splitted[1] >> 16) + (splitted[2] >> 8) + (splitted[3])

def main():
    fadress = sys.argv[1]
    sadress = sys.argv[2]

    fst = tonum(fadress)
    snd = tonum(fadress)

    print(abs(fst - snd))

if __name__ == "__main__":
    main()