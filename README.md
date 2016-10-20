# sdml - Smoke Detector (Machine Learning)

So here's a bit of a half-assed attempt at a self-written Bayesian classifier. Just to see what it can do.

### Requirements
You can use `pip` to install all the required packages for this thing:

    python2 -m pip install requests websocket-client termcolor

You will also need a working implementation of `cPickle`. You've *probably* got one, but not *all* Py2 installs came with it.

### Using it
Once you've `git clone`d the repo, you can do one of two things:

- update the data set, or
- just run the thing already

To update the data set, you need to run a few scripts. The first gets new data, the second analyzes it for specific
attributes, and the third converts the analyzed data to a format that the classifier can load.

To successfully run the first script, you need a valid [API key](https://github.com/Charcoal-SE/metasmoke/wiki/API-Documentation)
for [metasmoke](https://github.com/Charcoal-SE/metasmoke). Read the [API docs](https://github.com/Charcoal-SE/metasmoke/wiki/API-Documentation)
to learn how to get one.

    python2 getmsdata.py INSERT_MS_API_KEY_HERE
    python2 analyze.py title body
    python2 prepare.py

When those scripts complete, you have the data set up that the classifier needs to run from. You can run the live
classifier now (which takes data from the Stack Exchange websocket, like Smokey does):

    python2 ws.py

### Naive Bayes formula
*This section is a shortened explanation of the classification algorithm and its math. If you don't care about how it works,
 feel free to skip this section entirely.*

This project uses a simplified version of the Naive Bayes algorithm to classify posts. NB is, essentially, basic math operations.
The algorithm used here works like this:

- We have a *prior probability* of a post being S (spam) or H (ham). If 95% of all posts are legitimate, and 5% are spam, then our prior
  probability for Ham is 0.95, and for Spam is 0.05. We represent this as `p(S) = 0.05` and `p(H) = 0.95`.
- We also have a list of probabilities that a given word will appear in a spam post, and a ham post. Taking the word "muscle" as an example,
  we might see that it occurs in ham posts 0.00217% of the time, and in spam posts it comes up 5% of the time. As probabilities, those are
  0.0000217 and 0.05. We work that probability out for *every* word that we've ever seen in any post.
- When we get a post to classify, we split it up into words. For each word, we look up the probability that it occurs in spam and ham. We
  call the first word `w0`, and the probabilities that it occurs in spam or ham are respectively `Ps(w0)` and `Ph(w0)`.
- Once we've got the probabilities for every word, we multiply them together to come up with a probability that the entire text would occur
  as spam or as ham. We call those, respectively, `PS(w0..wn)` and `PH(w0..wn)` - these are the *text probabilities*.
- We work out an *initial probability* that the post is spam or ham by multiplying our text probabilities by their respective prior
  probabilities. The initial probability of a post being spam is therefore `p(S) * PS(w0..wn)`. We can represent both of these calculations
  as formulae: `IP(S) = p(S) * PS(w0..wn)` and `IP(H) = p(h) * PH(w0..wn)`
- Probabilities should add up to 1. In most cases, our initial probability figures *don't*, so we need to *normalize* them so they do. We
  calculate a *normalization factor*, represented as `Fn`, by adding both initial probabilities together: `Fn = IP(S) + IP(H)`
- To normalize, we need to divide our initial probabilities by this normalization factor, to come up with final probabilities.
  `P(S) = IP(S) / Fn` and `P(H) = IP(H) / Fn`.
- Now classification is simple: if `P(S) > P(H)`, the post is spam.
