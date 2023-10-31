
# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

If you do not have CDK installed, you can install it by running;

```
$ npm install -g aws-cdk
```

Then bootstrap CDK in your AWS account (if you have not done so).

```
$ cdk bootstrap
```

Deploy the stack to setup ths S3 buckets and presigned url API gateways:

```
$ cdk deploy -O output.json
```

The stack will deploy:
 * 3 x S3 buckets with CORS rule (allow all origin, allow origin https://test.com and allow origin http://localhost:5173 respectively)
 * API Gateways backed with Lambda functions to generate presigned post url
 * _output.json_ is needed by the frontend code to get presigned post url from the API 

## Front End

Based off Vue.js scaffolding codes, run the following to build and run the test front end.

```
$ cd frontend/s3cors
$ npm install
$ npm run dev
```

Enjoy!
