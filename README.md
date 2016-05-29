
# Twitters reaction to EPL

Collecting Tweets using the Twitter streaming API for analyzing the reaction and support for Leicester during its match against Manchester United (1st May, 2016) in the English Premier League. 

Look at a visualization of the tweets [here](https://mickeykedia.github.io/epl-twitter-viz/).

The repo for the visualization is at [https://github.com/mickeykedia/epl-twitter-viz](https://github.com/mickeykedia/epl-twitter-viz).

Edit: Also collecting Tweets during Chelsea vs Tottenham match (2nd May, 2016) as a draw for Tottenham means that Leicester would win the premier league

Edit 2: Tottenham drew ! Leicester has won the leage. Twitter has gone nuts. Thankfully my stream is working !! Woohoo

Edit 3: Used the same setup to collect tweets for the Champions League final (Real Madrid vs Atletico Madrid), and Game 6 in the Western Conference playoffs (Warriors vs OKC) 


## Motivation

- Play with the Twitter Streaming API
- Map EPL supporters during the epic championship bid by Leicester
- Make a cool visualization for my data visualization project

## Method 

I ended up using a node.js app with AWS Kinesis Firehose which writes the tweets as JSON blobs to files in S3. 

## Steps for set up

I used parts of a tutorial by AWS [here](https://blogs.aws.amazon.com/bigdata/post/Tx1Z6IF7NA8ELQ9/Building-a-Near-Real-Time-Discovery-Platform-with-AWS). This tutorial tells you how to use the Twitter streaming API to stream data using Kinesis Firehose into S3 and then into an Elastic Search cluster which can be queried real time by Kibana. 

I only used a part of the tutorial and only setup a Twitter to Firehose to S3 thing. There were certain things which did not go smoothly though and I want to address those steps


### Overview
- Create an S3 bucket
- Setup an IAM user which grants access to AWS Kinesis Firehose to write data into S3
- Setup EC2 to run an application which accesses the Twitter streaming API
- Clone a node.js application onto EC2 (referenced in the AWS blog, also available in this repo as `twitter-streaming-firehose-nodejs` folder)
- Acquire credentials for the Twitter APP (consumer_key, consumer_secret_key, api_key, api_secret_key)
- Change config in the application 
- Change some simple code to filter the Twitter stream according to words rather than locations (original example)
- Install node dependencies
- Run application
- Monitor Kinesis Firehose and S3 

#### Create an S3 bucket

Create an S3 bucket for the data

#### Setup IAM user for Kinesis Firehose

This is the trickiest part of the entire process. But I think I've got it figured out now. 

- Read [this](http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-service.html#roles-creatingrole-service-cli) and [this](http://docs.aws.amazon.com/firehose/latest/dev/controlling-access.html#using-iam-s3)
- Make sure you have AWS CLI 
- Make sure the `~/.aws/credentials` file has your credentials
- Get AWS ID from your account in AWS
- update `firehose_trust_policy.json` (in the repo) with the AWS ID
- update `firehose_deliver_role.json` (in the repo) with S3 bucket name 
- In the commandline with the AWS CLI installed and the json files in the path, run: 

    `aws iam create-role --role-name firehose_delivery_role --assume-role-policy-document file://firehose_trust_policy.json`
    
    `aws iam put-role-policy --role-name firehose_delivery_role --policy-name Permissions-For-S3 --policy-document file://firehose_deliver_role.json`

#### Setup EC2

Setup a tiny EC2 instance

#### Install node.js on EC2

`sudo yum -y install nodejs npm --enablerepo=epel`

#### Clone node.js application on EC2

Clone this repo on EC2 and use the `twitter-streaming-firehose-nodejs` folder

#### Acquire Config for Twitter

Go to [https://apps.twitter.com/](https://apps.twitter.com/) and register your app. Get credentials (Refer AWS blog if neccessary).

#### Change config in the node.js app

Update the `config_template.json` file with the relevant details and rename it to `config.js`

#### Update settings to what you need

The `config_template.js` file has two fields `track` and `locations` these can be used to filter the stream as you want. Go to the file `twitter_stream_producer.js` file to understand what's happening. 

Note that the node.js application is using a library called [Twit](https://github.com/ttezel/twit). Please read documentation from there to change the app as you need it

#### Install application dependencies on EC2

- install aws-sdk: `npm install aws-sdk`
- install twit: `npm install twit`
- install log4js: `npm install log4js`

#### Run app

Use `screen` and run the app from a screen session by calling `node twitter_stream_producer_app` from the app folder. This should start the firehose using the aws-sdk and then log the tweets on to the screen. 

In a few minutes you should be able to see the files being stored to S3. The files are stored in a Year/Month/Day/Hour folder format. One file of json tweets is stored every 5 minutes. 

#### That's it

Monitor your stream by navigating to Kinesis Firehose on AWS and monitoring your `Firehose`

Woohooo!  


### Note

I also tried out this fine [tutorial](http://socialmedia-class.org/twittertutorial.html) to get started. That attempt is in the `streaming_trial.py` file.

## TODO

- Read data in AWS RDS
- Query data 
- Map it !
- Plot it !
- 

## Data setup
- S3 bucket epl-twitter/raw-data2016/05/28 - UCL Finals
- S3 buckec epl-twitter/raw-data2016/05/29 - Game 6 warriors vs okc 

