## Using Layers to seperate code and dependencies
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

### Zip from build directory
```bash
$ zip -r  package.zip *
```

### Create new layer 
You'll find layers in the left panel in lambda console

![layer_screenshot](https://github.com/shuvojit-tps/lambda_docs/blob/master/assets/Screenshot%20from%202018-12-26%2011-58-22.png)


### Attach Layer to function
![layer-to-function](https://github.com/shuvojit-tps/lambda_docs/blob/master/assets/Screenshot%20from%202018-12-26%2012-02-08.png?raw=true)


### Run without dependencies in Function folder
![run-without-dependencies](https://github.com/shuvojit-tps/lambda_docs/blob/master/assets/Screenshot%20from%202018-12-26%2012-03-16.png?raw=true)
