import arachni


def main():
    scans = arachni.get_scans().json()
    for scan in scans:
        result = arachni.delete_scan(scan)
        if result.status_code == 200:
            print('Scan ID: ' + scan + ' is deleted.')
        else:
            print('Something went wrong while removing scan with ID: ' + scan + ". Response code is " +
                  str(result.status_code))

if __name__ == "__main__":
    main()
