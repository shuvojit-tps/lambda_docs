# How to map input sets into custom event objects?


## Context & Lambda Proxy
There is a feature called Lambda Proxy integration which when turned on, automatically maps the request and response according to their own preset mappings.

Their default mapping for requests looks something like this

```json
{
  "resource": "/users/single",
  "path": "/users/single",
  "httpMethod": "GET",
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Host": "vvm43aob14.execute-api.us-east-1.amazonaws.com",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "X-Amzn-Trace-Id": "Root=1-5c37139c-cf2762fe633943802dc2c7f2",
    "X-Forwarded-For": "61.12.81.34",
    "X-Forwarded-Port": "443",
    "X-Forwarded-Proto": "https"
  },
  "multiValueHeaders": {
    "accept": [
      "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    ],
    "accept-encoding": ["gzip, deflate, br"],
    "accept-language": ["en-GB,en-US;q=0.9,en;q=0.8"],
    "Host": ["vvm43aob14.execute-api.us-east-1.amazonaws.com"],
    "upgrade-insecure-requests": ["1"],
    "User-Agent": [
      "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    ],
    "X-Amzn-Trace-Id": ["Root=1-5c37139c-cf2762fe633943802dc2c7f2"],
    "X-Forwarded-For": ["61.12.81.34"],
    "X-Forwarded-Port": ["443"],
    "X-Forwarded-Proto": ["https"]
  },
  // this contains the get body
  "queryStringParameters": { "id": "2" },
  "multiValueQueryStringParameters": { "id": ["2"] },
  "pathParameters": null,
  "stageVariables": null,
  "requestContext": {
    "resourceId": "b5b15s",
    "resourcePath": "/users/single",
    "httpMethod": "GET",
    "extendedRequestId": "TSAAfHf7oAMF9Mw=",
    "requestTime": "10/Jan/2019:09:42:52 +0000",
    "path": "/dev/users/single",
    "accountId": "642495909037",
    "protocol": "HTTP/1.1",
    "stage": "dev",
    "domainPrefix": "vvm43aob14",
    "requestTimeEpoch": 1547113372715,
    "requestId": "1995907c-14bc-11e9-8342-071025d66a76",
    "identity": {
      "cognitoIdentityPoolId": null,
      "accountId": null,
      "cognitoIdentityId": null,
      "caller": null,
      "sourceIp": "61.12.81.34",
      "accessKey": null,
      "cognitoAuthenticationType": null,
      "cognitoAuthenticationProvider": null,
      "userArn": null,
      "userAgent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
      "user": null
    },
    "domainName": "vvm43aob14.execute-api.us-east-1.amazonaws.com",
    "apiId": "vvm43aob14"
  },
  "body": null, //this contains the post body
  "isBase64Encoded": false
}
```

And their default mapping for responses looks something like this

```js
{
    statusCode: Integer, 
    /* 
    * this gets mapped to the actual response status code
    * which is accessable by the requests status code method
    * eg in axios/fetch can be accessesd by response.status 
    * or response.ok which returns a true value for any 2** 
    * response code else, false */
    body: String, 
    /* 
    * This is mapped as the actual response body 
    * You're supposed to pass a stringified JSON here
    * which is parsed by the mapping template before returning
    * it as a response */
    headers: {
        "Key" : "Value"
    }
    /*
    * These key-value pairs are mapped to the response headers
    */
}
```



## Custom Mapping templates
The following is a basic template to map the 5 important keys from a request: post-body, query-parameters, headers, method, and path-parameters.

```js
{
  "post" : $input.json('$'),
  "headers": {
    #foreach($header in $input.params().header.keySet())
    "$header": "$util.escapeJavaScript($input.params().header.get($header))" #if($foreach.hasNext),#end

    #end
  },
  "method": "$context.httpMethod",
  "path": {
    #foreach($param in $input.params().path.keySet())
    "$param": "$util.escapeJavaScript($input.params().path.get($param))" #if($foreach.hasNext),#end

    #end
  },
  "get": {
    #foreach($queryParam in $input.params().querystring.keySet())
    "$queryParam": "$util.escapeJavaScript($input.params().querystring.get($queryParam))" #if($foreach.hasNext),#end

    #end
  }  
}
```