import json
from glob import glob
import sys

def main():
    attribs = sys.argv[1:]
    files = glob("*.nbts.json")
    filedata = {}

    for f in files:
        print("Found data file {0}".format(f))
        with open(f) as handle:
            filedata[f] = json.load(handle)

    for name, data in filedata.iteritems():
        print("Processing data from {0}".format(name))
        data_strings = {}
        for attrib in attribs:
            print("Creating data string for attrib {0}".format(attrib))
            data_strings[attrib] = ""

        for item in data:
            for attrib in attribs:
                if attrib in item and item[attrib] is not None:
                    data_strings[attrib] += item[attrib] + " "

        for key, string in data_strings.iteritems():
            fn = name.split('.')[0]
            with open("{0}_{1}.nbts".format(fn, key), "w") as handle:
                print("Saving data string for attrib {0}, data file {1} in {1}_{0}.nbts".format(key, fn))
                handle.write(string.encode('utf8'))


if __name__ == "__main__":
    main()
