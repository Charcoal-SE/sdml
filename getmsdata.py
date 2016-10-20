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
        data[type_name] = []
        for page in range(1, max_pages + 1):
            api_result = requests.get('https://metasmoke.erwaysoftware.com{}&key={}&page={}'.format(api_route, metasmoke_api_key, page))
            if api_result.status() == 200:
                json_data = api_result.json()
                for item in json_data['items']:
                    data[type_name].append(item)

                if json_data['has_more'] == False:
                    break

    for type_name, type_data in data.iteritems():
        with open("{}.nbts.json".format(type_name), "w") as f:
            f.write(json.dumps(type_data))


if __name__ == "__main__":
    main()
