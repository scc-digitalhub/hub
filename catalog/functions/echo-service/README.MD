# echoservice
echoservice is a simple Python service that demonstrates how a simple Python function can be operationalizes as a service based on serverless container runtime feature. The service is exposed as an API responding to POST message with the text input and returns the same text back — an echo.

## Definition
```
import json

def init(context):
    print("some initialization function")
    setattr(context, "value", "some value")

def serve(context, event):

    if isinstance(event.body, bytes):
        body = json.loads(event.body)
    else:
        body = event.body
    context.logger.info(f"Received event: {body}")
    text = body["text"]

    return {"result": f"hello {text} from '{context.value}'"}
```

The init(context) method is responsible for initializing the function’s execution context.

The serve(context, event) method contains the core functionality of the service, including the incoming request handling and execution logic.


## Usage

The function demonstrates:

- How to define a simple serverless python function
- How to expose the underlying function as an API
- How to initialize runtime service context
- How to generate and return output
- How to call the function

### Start the service

```
serve_run = function_echoservice.run(action='serve', wait=True)

```

### Send a request
```
import requests
SERVICE_URL = serve_run.refresh().status.to_dict()["service"]["url"]

with requests.post(f'http://{SERVICE_URL}', data='{"text": "Test caller"}') as r:
    res = r.content
print(res)
```

### Response:

```
b'{"result": "hello Test caller from \'some value\'"}'
```

Notes: For detailed usage, check the <a href='usage.ipynb'>usage notebook</a>.
