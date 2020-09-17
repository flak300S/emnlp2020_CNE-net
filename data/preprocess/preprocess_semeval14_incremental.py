from xml.dom import minidom
import json
import random

random.seed(2019)

cold_start_category = "service"
cold_start_ratio = 0.0
train_input_file = "../resources/data/semeval14/Restaurants_Train.xml"
train_output_file = "../resources/data/semeval14/train-{}-{}.json".format(cold_start_category, cold_start_ratio)
test_input_file = "../resources/data/semeval14/Restaurants_Test_Gold.xml"
test_output_file1 = "../resources/data/semeval14/test-{}.json".format(cold_start_category)
test_output_file2 = "../resources/data/semeval14/test-others.json"
train_output_file_origin = "../resources/data/semeval14/train-without_{}.json".format(cold_start_category)

category_list = ["food", "service", "price", "ambience", "anecdotes/miscellaneous"]
category2id = {"food": 0, "service": 1, "price": 2, "ambience": 3, "anecdotes/miscellaneous":4}


def parse_file(path):
    dom_ = minidom.parse(path)
    sentences = dom_.getElementsByTagName('sentence')
    results = []
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
        if len(labels) > 0:
            results.append({
                "text": text,
                "opinions": labels
            })
    return results


def output(data, path):
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.writelines("{}\n".format(json.dumps(item, ensure_ascii=False)))


def split_by_category(train_data, test_data, category):
    origin_train_data = []
    new_train_data = []
    new_test_data1 = []
    new_test_data2 = []
    positive = 0
    neutual = 0
    negative = 0
    conflict = 0

    for i, data in enumerate(train_data):
        current_train_data = {"text": data["text"], "opinions": []}
        current_origin_train_data = {"text": data["text"], "opinions": []}
        for opinion in data["opinions"]:
            if opinion["aspect"] not in category_list:
                continue
            if opinion["aspect"] != category:
                current_origin_train_data["opinions"].append(opinion)
            else:
                current_train_data["opinions"].append(opinion)
        new_train_data.append(current_train_data)
        origin_train_data.append(current_origin_train_data)

    random.shuffle(new_train_data)
    new_train_data = new_train_data[:int(len(new_train_data) * cold_start_ratio)]

    for data in test_data:
        current_test_data1 = {"text": data["text"], "opinions": []}
        current_test_data2 = {"text": data["text"], "opinions": []}
        for opinion in data["opinions"]:
            if opinion["aspect"] in category_list and opinion["aspect"] != category:
                current_test_data2["opinions"].append(opinion)
                if opinion["sentiment"] == "positive":
                    positive += 1
                elif opinion["sentiment"] == "neutral":
                    neutual += 1
                elif opinion["sentiment"] == "negative":
                    negative += 1
                else:
                    conflict += 1
            if opinion["aspect"] == category:
                current_test_data1["opinions"].append(opinion)
                if opinion["sentiment"] == "positive":
                    positive += 1
                elif opinion["sentiment"] == "neutral":
                    neutual += 1
                elif opinion["sentiment"] == "negative":
                    negative += 1
                else:
                    conflict += 1
        new_test_data1.append(current_test_data1)
        new_test_data2.append(current_test_data2)
    print(positive)
    print(neutual)
    print(negative)
    print(conflict)
    return origin_train_data, new_train_data, new_test_data1, new_test_data2


train_data = parse_file(train_input_file)
test_data = parse_file(test_input_file)
origin_train_data, new_train_data, test_data1, test_data2 = split_by_category(train_data, test_data, cold_start_category)

output(origin_train_data, train_output_file_origin)
output(test_data1, test_output_file1)
output(test_data2, test_output_file2)
output(new_train_data, train_output_file)
