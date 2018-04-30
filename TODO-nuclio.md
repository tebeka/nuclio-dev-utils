# TODO

nuclio out-of-band todo list

- Upgrade pypy to 6
- In RPC, convert `content-type` to `content_type` (easier JSON)
- Create FFI/C runtime (see [here][721])
- Java runtime with one server and thread per connection
- See if we can use flask-lambda-python36 with nuclio (see [here][flask])
    - Using [flask_lambda][fl]
- Upgrade Java to JDK10/11
    - Graal?
- C runtime
- Upgrade Go to 1.10 (dockers)
- Other encoding (msgpack, flatbuffers, ...)
- RPC should first connect, then load to allow initial logging (see [here][580])
- Upgrade gradle to 4.7


[580]: https://github.com/nuclio/nuclio/issues/580
[721]: https://github.com/nuclio/nuclio/issues/721
[fl]: https://github.com/sivel/flask-lambda
[flask]: https://andrewgriffithsonline.com/blog/180412-deploy-flask-api-any-serverless-cloud-platform/
