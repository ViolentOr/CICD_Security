import arachni


def main():
    scans = arachni.get_scans().json()
    for scan in scans:
        print("Scans in memory:")
        print(scan)

if __name__ == "__main__":
    main()
