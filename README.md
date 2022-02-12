# resal-assessment

# Introduction
This project is for Resal's interview assessment.  
I have implemented an API that takes a list of products (csv format) and returns the top rated product.  
You will find to branches other that __main__:
* feature-1 -> for the first requirement.
* feature-2 -> for the second requirement.

main will have the lates code, in this case feature-2's code.

# How to start the service?
I have created a docker-compose file so that you can start up the stack easily.
just run:
```console
docker-compose up -d
```
__NOTE:__ not sure why, but app container's logs for the message exchange between the client & server doesn't appear unless you consume the REST Api at least once. However, works instantly when ran locally.

you will see 2 containers running:
* message.broker -> rabbitmq
* app -> our application proccessing product csv through API or messages

you can see the logs of the messages between the CLIENT & SERVER by running:
```console
docker logs app 
```
# How to to run tests?
I have create a script inside __scripts__ file that will run tests, run:
```console
sh ./scripts/test.sh
```
# How to consume the service?
## 1: Through REST API
You can use the postman collection in this repo to test all cases that the api handles, or send your correctly formated CSV on:
```console
curl --location --request POST 'http://YOUR_HOST:YOUR_PORT/product/top' \
--form 'file=@"path/to/file.csv"'
```

## 2: Through message broker
On the start of the application i created a simple client/server communication that you will see happening on the console.
you can see the logs of the messages between the CLIENT & SERVER by running:
```console
docker logs app 
```  
* [SERVER] for server.
* [CLIENT] for client.



However, if you want to test it yourself there are 2 queues generate when the application starts:
* TO_BE_PROCESSED:
  * Push requests to this queue in this format:
    ```json
    {
        "request_id": "YOUR_REQUEST_UNIQE_ID", // So that you can identify the response after processing
        "file_path": "path/to/your/file.csv" // because it is not perfarable to send pure files to the queue, i chose to send the file path only
    }
    ```
* PROCESSED:
  * Listen to payloads coming from this queue in this format:
    ```json
    {
        "request_id": "YOUR_REQUEST_UNIQE_ID", // So that you can match the response after processing
        "response": "{\"top_product\": \"STRING\",\"product_rating\": NUMBER,\"is_successful\": BOOLEAN,\"error\": STRING}"
    }
    ```
## Things I would do better next time
* Write more comprehensive README.md
* Generalize error handling
* Allow multiple errors in the same response
* Cover more code with testing

## Resources I used
* .gitignore files are copied from [https://github.com/github/gitignore](https://github.com/github/gitignore)
* .dockerignore file is copied from [https://github.com/GoogleCloudPlatform/getting-started-python/blob/main/optional-kubernetes-engine/.dockerignore](https://github.com/GoogleCloudPlatform/getting-started-python/blob/main/optional-kubernetes-engine/.dockerignore)
* Implemented message broker based on [RabbitMQ's tutorial](https://www.rabbitmq.com/tutorials/tutorial-one-python.html)
  