# WebLodge

**WebLodge** is a command line aiming to provide anyone with deployment and cloud management capabilities.

## What do I need?

- Install the command line with `pip install weblodge`.
- A Python [Flask](https://flask.palletsprojects.com/en/2.3.x/) application.
- A `requirements.txt` with your dependencies. 
- Have an [Azure account](https://azure.microsoft.com/en-us/free).

> Note: By default, **WebLodge** uses **Free** [Azure services](https://azure.microsoft.com/en-us/pricing/free-services) and lets the user specify non-free configurations.


## Deploying an application

The simple way to deploy your local application is by running the command line `weblodge deploy --build` in your application directory.

In that case, **WebLodge** will assume that your application entry point is named `app.py` and your dependencies file is `requirements.txt`.

Behind the scene, **WebLodge** *build* then *deploy* your application.

## Application structure

**WebLodge** is sensible to the application structure. Applications must follow the pre-defined pattern or specify custom values.

Here is an example of the standard pattern deployable without configuration:
```
$ cat app.py  # The application filename entry point.
from flask import Flask

app = Flask(__name__)  # The Flask application.

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```
It can be deployed with `weblodge deploy --build`.

Here is a non-standard example:
```
$ cat main.py  # The application filename entry point.
from flask import Flask

my_app = Flask(__name__)  # The Flask application.

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```
To be able to deploy the application, you must first *build* it and specify:
- The entry point file: `main.py`.
- The **Flask** application: `my_app`.
```
# Build the application.
weblodge build --entry-point main.py --app my_app
# Deploy the application.
weblodge deploy
```

## Build

The *build* operation collects and prepares the application for deployment on a specific platform.

The *build* operation can handle the following options:
| Option name | Description | Default value |
|-|-|-|
| src | Folder containing application sources. | '.' |
| dist | Folder containing the application built. | 'dist' |

> Note: Here, the platform is implicitly [Azure App Service](https://azure.microsoft.com/en-us/products/app-service/web).


## Deploy

The *deploy* operation creates the necessary infrastructure and uploads the build package - i.e. your code - on the infrastructure.

| Option name | Description | Default value |
|-|-|-|
| app-name | The unique name of the application on the Internet. It will be included in the application URL. | `<randomly generated>` |
| sku | The application [computational power](https://azure.microsoft.com/en-us/pricing/details/app-service/linux/). | 'F1' |
| location | The physical application location. | 'northeurope' |
| environment | The environment of your application. | 'development' |
| dist | Folder containing the application built. | 'dist' |


## Delete

The *delete* operation deletes the infrastructure deployed but keeps the build.

| Option name | Description | Default value |
|-|-|-|
| app-name | The name of the application to be deployed. | `<my-app>` |
| yes | Do not prompt a validation message before deletion. | 'false' |


## Feedbacks

Feel free to create issues with bugs, ideas and any constructive feedback.
