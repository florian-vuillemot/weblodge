# WebLodge

**WebLodge** is a command line aim to provide deployment and cloud management capabilities to anyone.

## What do I need?

- Installing the command line by doing `pip install weblodge`.
- A Python [Flask](https://flask.palletsprojects.com/en/2.3.x/) application.
- A `requirements.txt` with your dependencies. 
- Having an [Azure account](https://azure.microsoft.com/en-us/free).

> Note: By default, **WebLodge** uses **Free** [Azure services](https://azure.microsoft.com/en-us/pricing/free-services) and let the user specify non-free configurations.


## Deploying an application

The simple way to deploy your local application is by running the command line `weblodge deploy --build` in your application directory.

In that case, **WebLodge** will assumes that your application entrypoint is named `app.py` and your dependencies files is `requirements.txt`.

Behind the scene, **WebLodge** *build* then *deploy* your application.

## Application structure

**WebLodge** is sensible to the application structure. Applications must follow the pre-defined pattern or specify custom values.

Here an example of the standard pattern deployable without configuration:
```
$ cat app.py  # The application filename entrypoint.
from flask import Flask

app = Flask(__name__)  # The Flask application.

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```
It can be deploy with `weblodge deploy --build`.

Here a non standard example:
```
$ cat main.py  # The application filename entrypoint.
from flask import Flask

my_app = Flask(__name__)  # The Flask application.

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```
To be able to deploy that application you must first *build* it and specify:
- The entrypoint file: `main.py`.
- The **Flask** application: `my_app`.
```
# Build the application.
weblodge build --entrypoint main.py --app my_app
# Deploy the application.
weblodge deploy
```

## Build

The *build* operation collect and prepare the application for deployment on a specific platform.

The *build* operation can handle the following options:
| Option name | Description | Default value |
|-|-|-|
| src | Folder containing application sources. | '.' |
| dest | Folder containing the application built. | 'dist' |

> Note: Here the platform is implicitly [Azure App Service](https://azure.microsoft.com/en-us/products/app-service/web).


## Deploy

The *deploy* operation create necessary infrastructure and upload the built package on.

| Option name | Description | Default value |
|-|-|-|
| app-name | The unique name of the application on the Internet. Will be included in the application URL. | `<randomly generated>` |
| sku | The application [computational power](https://azure.microsoft.com/en-us/pricing/details/app-service/linux/). | 'F1' |
| location | The physical application location. | 'northeurope' |
| environment | The environment of your application. | 'development' |
| dist | Folder containing the application built. | 'dist' |


## Feedbacks

Feel free to create issues with bug, idea and any type of constructive feedbacks.
