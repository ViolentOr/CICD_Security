import argparse

import arachni


def main():
    parser = argparse.ArgumentParser(description="Arachni Scanner")
    parser.add_argument('-i', "--id", required=True, help="Scan ID that should be deleted")
    args = parser.parse_args()
    result = arachni.delete_scan(args.id)
    print(result.status_code)

if __name__ == "__main__":
    main()
