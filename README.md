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
