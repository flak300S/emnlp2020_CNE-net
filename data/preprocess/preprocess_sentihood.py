import json


train_data_path = "../resources/data/sentihood/sentihood-train.json"
valid_data_path = "../resources/data/sentihood/sentihood-dev.json"
test_data_path = "../resources/data/sentihood/sentihood-test.json"
train_output_path = "../resources/data/sentihood/train.json"
valid_output_path = "../resources/data/sentihood/valid.json"
test_output_path = "../resources/data/sentihood/test.json"

def transfer(in_path, out_path):
    results = []
    with open(in_path, encoding="utf-8") as f:
        data = json.loads(f.read())
        for item in data:
            results.append({
                "text": item["text"].strip(),
                "opinions": item["opinions"]
            })
    with open(out_path, "w", encoding="utf-8") as f:
        for result in results:
            f.writelines("{}\n".format(json.dumps(result, ensure_ascii=False)))

transfer(train_data_path, train_output_path)
transfer(valid_data_path, valid_output_path)
transfer(test_data_path, test_output_path)