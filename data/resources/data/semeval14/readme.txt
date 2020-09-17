1. Origin training and testing data
Restaurants_Train.xml
Restaurants_Test_Gold.xml

2. Processed training and testing data (by preprocess_semeval14.py)
train.json
test.json

3. Processed training and testing data for incremental learning (by preprocess_semeval14_incremental.py)
training data in source categories: train-without_service.json
training data in incremental learning category: train-service-1.0.json, train-service-0.8.json, train-service-0.5.json, train-service-0.2.json, train-service-0.0.json
testing data for source categories: test-others.json
testing data for target category: test-service.json