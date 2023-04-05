# serverless-leaps-screener

Serverless automation that scrapes finviz.com for potential LEAPS options opportunities among growing large cap, optionable companies who have recently had corrections. Results will be send to the recipients email 3 times a day.

###### Resources Created

Lambda

Lambda Layer

EventBridge Scheduling Rule

SNS Topic

SNS Subscription

###### Requires

1. AWS CLI

2. SAM CLI

3. Python3

4. BeautifulSoup Python Library exported to .zip file

```shell
# mkdir -p bs4 && cd bs4
# mkdir -p python && cd python
# pip3 install bs4 -t .
# cd ..
# zip -r ./bs4.zip .
```

###### Parameters

1. Recipient Email

2. Finviz URL (Default URL provided)
