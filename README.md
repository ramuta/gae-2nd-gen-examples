# GAE (2nd Gen) Python 3 Examples

This repository holds examples of Python 3 web apps that run on the Google App Engine (GAE) 2nd Generation environment.

## Prerequisites

- [Python 3](https://www.python.org/)
- Java JDK (I recommend **OpenJDK 11** from [AdoptOpenJDK](https://adoptopenjdk.net/)) - this is needed to run the Datastore 
or Firestore emulator (via Cloud SDK)
- [Cloud SDK](https://cloud.google.com/sdk/docs/quickstarts)

## Examples

- **[simple-gae-app](https://github.com/smartninja/gae-2nd-gen-examples/tree/master/simple-gae-app)**: A simple Flask app with all the basic GAE settings needed. No database included here.
- **[simple-app-datastore](https://github.com/smartninja/gae-2nd-gen-examples/tree/master/simple-app-datastore)**: A simple Flask app that allows you to store items in Datastore (Datastore Emulator is used).
- **[simple-app-datastore-tests](https://github.com/smartninja/gae-2nd-gen-examples/tree/master/simple-app-datastore-tests)**: Flask app with Datastore and tests (pytest).
- **simple-app-sql**
- **simple-app-sql-tests**
- **simple-app-firestore**
- **simple-app-firestore-tests**
- **structured-app-firestore**
- **app-firestore-custom-auth**
- **app-firestore-firebase-auth**

## Improvement proposals or issues found?

Please [create a new issue](https://github.com/smartninja/gae-2nd-gen-examples/issues/new) in case there's some bug or 
something should be improved.

Happy to receive pull requests, too! :)
