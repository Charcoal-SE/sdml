import requests
import json
import sys


metasmoke_api_key = ""
types_routes = {
    'tpkws': '/api/posts/feedback?type=tpu-',
    'fpkws': '/api/posts/feedback?type=fp-'
}
max_pages = 10
data = {}


def main():
    if len(sys.argv) >= 2:
        metasmoke_api_key = sys.argv[1]

    for type_name, api_route in types_routes.iteritems():
        print("Fetching data for data_type={}".format(type_name))
        data[type_name] = []
        for page in range(1, max_pages + 1):
            api_result = requests.get('https://metasmoke.erwaysoftware.com{}&key={}&page={}'.format(api_route, metasmoke_api_key, page))
            status = api_result.status_code
            print("Page {}: HTTP/1.1 {}".format(page, status))
            if status == 200:
                json_data = api_result.json()
                for item in json_data['items']:
                    data[type_name].append(item)

                if json_data['has_more'] == False:
                    break
            else:
                print("Request errored out, breaking.")
                break

    for type_name, type_data in data.iteritems():
        print("Writing data file {}.nbts.json".format(type_name))
        with open("{}.nbts.json".format(type_name), "w") as f:
            f.write(json.dumps(type_data))


if __name__ == "__main__":
    main()
