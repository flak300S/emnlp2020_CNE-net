from xml.dom import minidom
import json

train_input_file = "../resources/data/semeval14/Restaurants_Train.xml"
train_output_file = "../resources/data/semeval14/train.json"
test_input_file = "../resources/data/semeval14/Restaurants_Test_Gold.xml"
test_output_file = "../resources/data/semeval14/test.json"


def parse_file(path):
    dom_ = minidom.parse(path)
    sentences = dom_.getElementsByTagName('sentence')
    results = []
    count = {"food": 0, "service": 0, "price": 0, "ambience": 0, "anecdotes/miscellaneous": 0}
    for sentence in sentences:
        text = sentence.getElementsByTagName("text")[0].childNodes[0].data
        opinions = sentence.getElementsByTagName("aspectCategory")
        labels = []
        for opinion in opinions:
            polarity = opinion.getAttribute("polarity")
            category = opinion.getAttribute("category")
            if category in ["food", "service", "price", "ambience", "anecdotes/miscellaneous"]:
                labels.append({
                    "sentiment": polarity,
                    "aspect": category,
                })
                count[category] += 1
        if len(labels) > 0:
            results.append({
                "text": text,
                "opinions": labels
            })
    print(count)
    return results


def output(data, path):
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.writelines("{}\n".format(json.dumps(item, ensure_ascii=False)))


train_data = parse_file(train_input_file)
test_data = parse_file(test_input_file)
output(test_data, test_output_file)
output(train_data, train_output_file)
