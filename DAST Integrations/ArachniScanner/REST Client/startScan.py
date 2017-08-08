import argparse

import arachni


def main():
    parser = argparse.ArgumentParser(description="Arachni Scanner")
    parser.add_argument('-u', "--url", required=True, help="URL to scan")
    parser.add_argument('-c', "--checks",
                        default='*', help="checks (use '*' to rule them all)")
    args = parser.parse_args()
    response = arachni.create_scan(args.url, args.checks)
    result = response.json()

    print(result)

if __name__ == "__main__":
    main()
