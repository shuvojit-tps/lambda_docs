## Running & Testing lambda functions without AWS Console

#### Install python-lambda-local inside a VirtualEnv 
This provides an interface to feed in an event json to replicate a request
```sh
$ pip install python-lambda-local
```

#### Create a file event.json and write your custom event code in it
A sample POST request event would look like
```json
{
    "body": "{\"name\":\"Shuvojit\", \"email\":\"shuvojit7@gmail.com\"}"
}
```
![Screenshot](https://raw.githubusercontent.com/shuvojit-tps/lambda_docs/master/assets/Screenshot%20from%202018-12-26%2011-43-57.png)


#### Using ParameterStore Locally

First add your credetials to a profile under ~/.aws/credentials
```
[staging]
aws_access_key_id = xxxxxxxxxxxxxxxxxx
aws_secret_access_key = xxxxxxxxxxxxxxxxxxx

[prod]
aws_access_key_id = xxxxxxxxxxxxxxxx
aws_secret_access_key = xxxxxxxxxxxxxx

```

Now you have to set a default profile which all of your boto3 clients would use.
Add this to your .bashrc or .zshrc
```
export AWS_PROFILE=prod
```
Now you can just switch this value to use whichever profile you prefer.

#### Choosing a profile in Py Function (not recommended)
You can however, switch to a profile in the Py file, but it's not recommended as the same code won't work on the lambda function as the env in the lambda will just have a default aws profile.
However, you can do it by creating a session 

```python
import boto3
session = boto3.Session(profile_name='prod')
client = session.client('ssm')
```