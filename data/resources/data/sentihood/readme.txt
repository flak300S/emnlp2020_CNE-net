1. Origin training, validation and testing data
sentihood-train.json
sentihood-dev.json
sentihood-test.json

2. Processed training, validation and testing data (by preprocess_sentihood.py)
train.json
valid.json
test.json

3. Processed training, validation and testing data for incremental learning (by preprocess_sentihood_incremental.py)
training data in source categories: train-without_price.json
training data in incremental learning category: train-price-1.0.json, train-price-0.8.json, train-price-0.5.json, train-price-0.2.json, train-price-0.0.json
validation data for source categories: valid-others.json
validation data for target category: valid-price.json
testing data for source categories: test-others.json
testing data for target category: test-price.json