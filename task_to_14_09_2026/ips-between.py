import sys
import ipaddress

# python ips-between.py 192.168.0.100 192.168.0.0 # 100
# python ips-between.py 192.168.1.0 192.168.0.5 # 251

def print_help():
    print("Usage: ips-between.py <ip1> <ip2>")
    print("[Usage: ips-between.py <ip1> <ip2>]")
    print("\n")
    print("Calculate the number of IP addresses between two given IPs (inclusive start, exclusive end).")
    print("[Calculate the number of IP addresses between two given IPs (inclusive start, exclusive end).]")
    print("\n")
    print("Example: ips-between.py 192.168.0.1 192.168.0.100")
    print("[Example: ips-between.py 192.168.0.1 192.168.0.100]")



def tonum(adress):
    parts = list(map(int, adress.split('.'))) 
    
    for part in parts:
        if part < 0 or part > 255:
            raise ValueError(f"IP octet out of range: {part}")

    return (parts[0] >> 24) + (parts[1] >> 16) + (parts[2] >> 8) + parts[3]

def main():

    if '-h' in sys.argv:
        print_help()
        return
    
    try:

        fadress = sys.argv[1]
        sadress = sys.argv[2]

        fst = tonum(fadress)
        snd = tonum(fadress)

        print(abs(fst - snd))

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()