from glob import glob
import cPickle as pickle
import re
import json

def main():
    spam_class = "tpkws"
    ham_class = "fpkws"

    raw_data = {
        'spam': {},
        'ham': {}
    }

    spam_files = glob("{0}_*.nbts".format(spam_class))
    ham_files = glob("{0}_*.nbts".format(ham_class))

    raw_data = process_files(raw_data, spam_files, 'spam')
    raw_data = process_files(raw_data, ham_files, 'ham')


    print("Data dumps: cPickle@prob.nbcd JSON@prob.json")
    with open('prob.nbcd', 'w') as f:
        f.write(pickle.dumps(raw_data))


    with open('prob.json', 'w') as f:
        f.write(json.dumps(raw_data))


def process_files(raw_data, files, dtype):
    for f in files:
        attr_name = f.split('.')[0].split('_')[1]
        print("Found {2} data for attrib {0} in {1}".format(attr_name, f, dtype))
        raw_data[dtype][attr_name] = {}
        with open(f) as handle:
            string = handle.read()

        total = 0
        print("Processing word counts... This may take a while.")
        for word in re.findall(r"[\w']+", string):
            total += 1
            word = word.lower()
            if word in raw_data[dtype][attr_name]:
                raw_data[dtype][attr_name][word] += 1
            else:
                raw_data[dtype][attr_name][word] = 1

        print("Converting counts to probabilities...")
        for word, value in raw_data[dtype][attr_name].iteritems():
            word_prob = float(value) / float(total)
            if word_prob > 0:
                raw_data[dtype][attr_name][word] = word_prob

    return raw_data


if __name__ == "__main__":
    main()
