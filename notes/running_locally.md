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
