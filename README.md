# sdml - Smoke Detector (Machine Learning)

So here's a bit of a half-assed attempt at a self-written Bayesian classifier. Just to see what it can do.

### Requirements
You can use `pip` to install all the required packages for this thing:

    python2 -m pip install requests websocket-client termcolor

You will also need a working implementation of `cPickle`. You've *probably* got one, but not *all* Py2 installs came with it.

### Using it
Once you've `git clone`d the repo, you need to run the `analyze` and `prepare` scripts:

    python2 analyze.py title body
    python2 prepare.py

When those two scripts complete, you have the data set up that the classifier needs to run from. You can run the live
classifier now (which takes data from the Stack Exchange websocket, like Smokey does):

    python2 ws.py
