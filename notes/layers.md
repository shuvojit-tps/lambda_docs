# 1. Using Layers to seperate code and dependencies

Usual use case would be to reduce function size and reusablity for libraries and custom modules.

#### Create a directory for dependencies and replicate a python lib directory structure

```bash
$ mkdir -p build/python/lib/python3.6/site-packages
```

#### Install pip packages inside site-packages

```bash
$ cd build/python/lib/python3.6/site-packages/
$ pip install pymysql -t .
```

#### Zip from build directory

```bash
$ zip -r  package.zip *
```

#### Create new layer

You'll find layers in the left panel in lambda console

![layer_screenshot](https://github.com/shuvojit-tps/lambda_docs/blob/master/assets/Screenshot%20from%202018-12-26%2011-58-22.png)

#### Attach Layer to function

![layer-to-function](https://github.com/shuvojit-tps/lambda_docs/blob/master/assets/Screenshot%20from%202018-12-26%2012-02-08.png?raw=true)

#### Run without dependencies in Function folder

![run-without-dependencies](https://github.com/shuvojit-tps/lambda_docs/blob/master/assets/Screenshot%20from%202018-12-26%2012-03-16.png?raw=true)

# 2. Using lambda to create DataLayer

Usual use case would be to save secret key-value pairs and fetch them from json file at runtime.

#### Create a directory for the layer and create another directory called data inside

```bash
$ mkdir layer_name/data -p
```

### Inside layer/data create json files to fetch data from, in this case we'll create two files for different enviournments

```bash
$ touch dev.json prod.json
```

#### Sample dev.json file
```json
{
  "host": "myhostname",
  "user": "username",
  "passwd": "$3c12ET",
  "db": "mydatabase"
}

```

### Now add data as json in both the documents and zip recursively with layer folder as root and upload on AWS as a layer

```bash
$ zip -r data_layer.zip .
```

### The data folder is mounted under /opt/ whenever a new lambda instance is fired up, so the files will be accessable from /opt/data/
#### Attach the data layer to the lambda function, then you  can acccess the credentials

```python
import json
import sys
import logging
import pymysql

def lambda_handler(event, context):
    # TODO implement
    db_config = {}
    with open('/opt/data/dev.json') as db_json:
        db_config = json.load(db_json)
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    try:
        # unpack dict as parameters
        conn = pymysql.connect(**db_config)
    except:
        logger.error(
            "ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()
    
    logger.info("SUCCESS: Connection to RDS mysql instance succeeded")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

```