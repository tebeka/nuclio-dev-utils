# TODO

nuclio out-of-band todo list

- Have make rebuild images when sources change
- Upgrade pypy to 6
- In RPC, convert `content-type` to `content_type` (easier JSON)
- Create FFI/C runtime (see [here][721])
- Java runtime with one server and thread per connection
- See if we can use flask-lambda-python36 with nuclio (see [here][flask])
    - Using [flask_lambda][fl]
- Upgrade Java to JDK10/11
    - Graal?
- RPC should first connect, then load to allow initial logging (see [here][580])
- Upgrade gradle to 4.8
- Faster RPC (msgpack? flatbuffers?)
- RPC via shared memory
- Generate SDKs from common interface definition
- Nuke alpine
- Triggers as plugins
- Runtimes as plugins
- On timeout, restart from last checkpoint
- Python stdout of invocation as log
- Jupyter to nuclio function
    - !pip install -> build command
    - return response with exception
    - Jupyter extension?
- Dask with nuclio


[580]: https://github.com/nuclio/nuclio/issues/580
[721]: https://github.com/nuclio/nuclio/issues/721
[fl]: https://github.com/sivel/flask-lambda
[flask]: https://andrewgriffithsonline.com/blog/180412-deploy-flask-api-any-serverless-cloud-platform/
