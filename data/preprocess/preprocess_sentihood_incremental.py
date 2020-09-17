import json
import random

random.seed(2019)

category_list = ["general", "price", "safety", "transit-location"]
category2id = {"general": 0, "price": 1, "safety": 2, "transit-location": 3}


cold_start_category = "price"
cold_start_ratio = 0.0

train_data_path = "../resources/data/sentihood/sentihood-train.json"
valid_data_path = "../resources/data/sentihood/sentihood-dev.json"
test_data_path = "../resources/data/sentihood/sentihood-test.json"

train_output_file_origin = "../resources/data/sentihood/train-without_{}.json".format(cold_start_category)
train_output_file = "../resources/data/sentihood/train-{}-{}.json".format(cold_start_category, cold_start_ratio)
valid_output_file1 = "../resources/data/sentihood/valid-{}.json".format(cold_start_category)
valid_output_file2 = "../resources/data/sentihood/valid-others.json"
test_output_file1 = "../resources/data/sentihood/test-{}.json".format(cold_start_category)
test_output_file2 = "../resources/data/sentihood/test-others.json"


def parse_file(in_path):
    results = []
    with open(in_path, encoding="utf-8") as f:
        data = json.loads(f.read())
        for item in data:
            results.append({
                "text": item["text"].strip(),
                "opinions": item["opinions"]
            })
    return results


def output(data, path):
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.writelines("{}\n".format(json.dumps(item, ensure_ascii=False)))


def split_by_category(train_data, valid_data, test_data):
    origin_train_data = []
    new_train_data = []
    new_test_data1 = []
    new_test_data2 = []
    new_valid_data1 = []
    new_valid_data2 = []

    positive = 0
    negative = 0

    for i, data in enumerate(train_data):
        current_train_data = {"text": data["text"], "opinions": []}
        current_origin_train_data = {"text": data["text"], "opinions": []}
        for opinion in data["opinions"]:
            if opinion["aspect"] not in category_list:
                continue
            if opinion["aspect"] != cold_start_category:
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
            if opinion["aspect"] not in category_list:
                continue
            if opinion["aspect"] == cold_start_category:
                current_test_data1["opinions"].append(opinion)
                if opinion["sentiment"] == "Positive":
                    positive += 1
                elif opinion["sentiment"] == "Negative":
                    negative += 1
            else:
                current_test_data2["opinions"].append(opinion)
                if opinion["sentiment"] == "Positive":
                    positive += 1
                elif opinion["sentiment"] == "Negative":
                    negative += 1

        new_test_data1.append(current_test_data1)
        new_test_data2.append(current_test_data2)

    for data in valid_data:
        current_valid_data1 = {"text": data["text"], "opinions": []}
        current_valid_data2 = {"text": data["text"], "opinions": []}
        for opinion in data["opinions"]:
            if opinion["aspect"] not in category_list:
                continue
            if opinion["aspect"] == cold_start_category:
                current_valid_data1["opinions"].append(opinion)
            else:
                current_valid_data2["opinions"].append(opinion)
        new_valid_data1.append(current_valid_data1)
        new_valid_data2.append(current_valid_data2)

    print(positive)
    print(negative)
    return origin_train_data, new_train_data, new_valid_data1, new_valid_data2, new_test_data1, new_test_data2


train_data = parse_file(train_data_path)
valid_data = parse_file(valid_data_path)
test_data = parse_file(test_data_path)

origin_train_data, new_train_data, new_valid_data1, new_valid_data2, new_test_data1, new_test_data2\
    = split_by_category(train_data, valid_data, test_data)
output(origin_train_data, train_output_file_origin)
output(new_train_data, train_output_file)
output(new_valid_data1, valid_output_file1)
output(new_valid_data2, valid_output_file2)
output(new_test_data1, test_output_file1)
output(new_test_data2, test_output_file2)
