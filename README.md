# GAE (2nd Gen) Python 3 Examples

This repository holds examples of Python 3 web apps that run on the Google App Engine (GAE) 2nd Generation environment.

> If you find this repository useful, please **star** it ;) 

## Prerequisites

- [Python 3](https://www.python.org/)
- Java JDK (I recommend **OpenJDK 11** from [AdoptOpenJDK](https://adoptopenjdk.net/)) - this is needed to run the Datastore 
or Firestore emulator (via Cloud SDK)
- [Cloud SDK](https://cloud.google.com/sdk/docs/quickstarts)

In order to deploy the web app on Google Cloud, you will probably need to connect your credit card to it. But this 
doesn't mean Google will start charging you right away - the free quota is pretty generous and you can also set a 
daily spending limit to 0 USD (see step 4 below in the "Deployment to GAE" section).

### Cloud SDK components

Make sure you have the following Cloud SDK components installed ([instructions](https://cloud.google.com/sdk/docs/components)):

- Cloud SDK Core Libraries (core)
- gcloud app Python Extensions (app-engine-python)
- gcloud app Python Extensions - Extra Libraries (app-engine-python-extras)
- gcloud Beta Commands (beta)

If you'll use Datastore or Firestore, you'll need to install one of these (or both) components too:

- Cloud Datastore Emulator (cloud-datastore-emulator)
- Cloud Firestore Emulator (cloud-firestore-emulator)

## Examples

- **[simple-gae-app](https://github.com/smartninja/gae-2nd-gen-examples/tree/master/simple-gae-app)**: A simple Flask app with all the basic GAE settings needed. No database included here.
- **[simple-app-datastore](https://github.com/smartninja/gae-2nd-gen-examples/tree/master/simple-app-datastore)**: A simple Flask app that allows you to store items in Datastore (Datastore Emulator is used).
- **[simple-app-datastore-tests](https://github.com/smartninja/gae-2nd-gen-examples/tree/master/simple-app-datastore-tests)**: Flask app with Datastore and tests (pytest).
- **[simple-app-firestore](https://github.com/smartninja/gae-2nd-gen-examples/tree/master/simple-app-firestore)**: Flask app with the Firestore database.
- **[simple-app-firestore-tests](https://github.com/smartninja/gae-2nd-gen-examples/tree/master/simple-app-firestore-tests)**: Flask app with Firestore + tests.
- **simple-app-sql**
- **simple-app-sql-tests**
- **[structured-app-firestore](https://github.com/smartninja/gae-2nd-gen-examples/tree/master/structured-app-firestore)**: A structured Flask app with Firestore + tests. Gives you an idea how to structure your web app.
- **[structured-app-ndb](https://github.com/smartninja/gae-2nd-gen-examples/tree/master/structured-app-ndb)**: An example using the new ndb library for Python 3 GAE runtime.
- **[env-var-example](https://github.com/smartninja/gae-2nd-gen-examples/tree/master/env-var-example)**: GAE does not support environment variables, so the alternative is to write them in the database instead. Here's an example how.
- **app-firestore-custom-auth**
- **app-firestore-firebase-auth**

### How to run the examples?

Click on each example and check the README.md there - it has all the instructions you need.

## Deployment to Google App Engine

### 1) gcloud init

Open the Terminal in the root of the project and type in:

    gcloud init

If this is a new project, select the choice no.2: **Create a new configuration.** Then enter a name for this 
configuration (it needs to be unique only on your computer, not globally).

If this is an already existing project with an existing configuration, select it and skip some of the next steps.

After this step you'll need to log in with your Google account.

### 2) Select the cloud project or create a new one

If you already have a Google Cloud project for this repository, select it. If not, create a new one.

### 3) Create the App Engine instance

Now it's time to create a Google App Engine instance and select the region where it will run (See the 
[list of possible regions here](https://cloud.google.com/appengine/docs/locations)).

> Important: The region cannot be changed later.

Once you've chosen the region, enter the following command:

    gcloud app create --region=europe-west

In this case we chose the "europe-west" region, but replace it with some other if you want.

### 4) Enable Cloud Build API

Go to Google Cloud Console, open your project and type this in the Search box: **Cloud Build API**. Then enable it.

You will probably need to enable billing for your project, but don't worry - this does not mean Google will start 
charging you. Google has a very generous **free quota** and you will very likely stay within that quote.

But it doesn't hurt to set up the daily limit for your GAE app on Google Cloud Console (type "App Engine settings" in 
the Search box and then enter the daily spending limit (it can be 0).

### 5) Deploy your code to GAE

The next step is to deploy your code to Google Cloud:

    gcloud app deploy --version production

You could do it without the version flag, but it's a good practice so that GAE does not create a new version for each of 
your deployments. You can also name versions after your Git branches (for example: master, develop).

### 6) Check if either Datastore or Firestore is enabled

If you'll use Datastore or Firestore as a database, you have to make sure the database is enabled on Google Cloud 
Platform.

**Important:** Only one of these two can be enabled in the same project! Either Datastore, or Firestore. Both cannot 
be enabled and you cannot switch from one to another once you have data in the database!

> What's the difference between the two? Firestore is the newer version of Datastore. All Datastores will eventually 
be converted into Firestore, but they will continue working via the, so called, "Datastore Mode", which has less 
features than native Firestore. So if you're creating a new project with an empty database, choose Firestore.

**How to enable Datastore/Firestore?**

If it's not enabled automatically, just type either "Datastore" or "Firestore" in the Search box on Google Cloud 
Platform. Once you click on the selection, the Datastore/Firestore will be automatically enabled.

## Troubleshooting

Note that `google-cloud-datastore` requires a `google-cloud-core` library version less than 0.30.0 (currently 0.28.1), while 
`google-cloud-firestore` requires a version bigger than 1.0.0. (currently 1.0.3). That's why you might need to use two 
separate virtual environments (one with the datastore lib and the other with the firestore lib).

Or to run `pip install google-cloud-datastore` or `google-cloud-firestore` each time you would want to switch the 
project.

But in my experience this wasn't needed. Try it out and you'll see.

## Improvement proposals or issues found?

Please [create a new issue](https://github.com/smartninja/gae-2nd-gen-examples/issues/new) in case there's some bug or 
something should be improved.

Happy to receive pull requests, too! :)
