# aws-cli cheatsheet

## Stage Invoke Permissions

When you use alias and \${stageVariables.env} in your APIGateway+Lambda, you need to manually add permissions to all of your stages.

```bash
$ aws lambda add-permission    \
     --function-name "{function_arn}:{stage}" \
     --source-arn "{api_method_arn}" \
     --principal apigateway.amazonaws.com    \
     --statement-id da5dbfa5-e0cb-45a2-baf9-e619041f3243    \
     --action lambda:InvokeFunction
```
