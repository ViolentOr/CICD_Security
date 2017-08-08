import json
import argparse


def get_scans():
    response_url = request_url + "/scans"
    response = session.get(response_url, headers=headers)
    return response


def create_scan(scan_url, checks=None):
    if checks is None:
        payload = {"url": scan_url}
    else:
        payload = {"url": scan_url, "checks": checks}

    response_url = request_url + "/scans"
    response = session.post(response_url, data=json.dumps(payload), headers=headers)
    return response


def get_scan(scan_id):
    response_url = request_url + "/scans/" + scan_id
    response = session.get(response_url)
    return response


def get_report(scan_id, report_format):
    extender = '.json'
    if report_format == 'json':
        extender = ".json"
    elif report_format == 'xml':
        extender = ".xml"
    if report_format == 'yaml':
        extender = ".yaml"
    if report_format == 'html':
        extender = ".html.zip"
    response_url = request_url + "/scans/" + scan_id + "/report" + extender
    response = session.get(response_url)
    response.headers = headers
    return response


def pause_scan(scan_id):
    response_url = request_url + "/scans/" + scan_id + "/pause"
    response = session.put(response_url, headers=headers)
    return response


def resume_scan(scan_id):
    response_url = request_url + "/scans/" + scan_id + "/resume"
    response = session.put(response_url, headers=headers)
    return response


def delete_scan(scan_id):
    response_url = request_url + "/scans/" + scan_id
    response = session.delete(response_url, headers=headers)
    return response


def get_status(scan_id):
    scan_status = get_scan(scan_id)
    status_json = scan_status.json()
    return status_json['busy']


# noinspection PyTypeChecker
def main():
    parser = argparse.ArgumentParser(description="Arachni Scanner")
    parser.add_argument('-u', "--url", required=True, help="URL to be scanned")
    parser.add_argument('-c', "--checks",
                        default='*', help="checks (use '*' to rule them all)")
    parser.add_argument('-f', "--fail",
                        default=0, help="should we fail if smth found (set 1 fail)")
    args = parser.parse_args()

    scan = create_scan(args.url, args.checks)
    scan_json = scan.json()
    scan_id = scan_json['id']
    print("Scan ID: " + scan_id)
    print('Scanning in Progress...')

    scan_status = get_status(scan_id)

    while scan_status is True:
        scan_status = get_status(scan_id)

    result = get_report(scan_id, 'html')
    # Write data to file
    filename = "report.zip"
    file_ = open(filename, 'wb')
    file_.write(result.content)
    file_.close()

    scan_issues = get_report(scan_id, "json").json()["issues"]
    delete_scan(scan_id)
    print('Scan ID: ' + scan_id + ' finished.')

    if args.fail == "1" and len(scan_issues) > 0:
        exit(1)


if __name__ == "__main__":
    main()
