# Detecting Money Laundering
## -- Based on analsis of network data
---

## Identity Manipulation

### Criminal behavior
- Synthetic identities
- Shell companies
- Straw men
- Identity recycling

### Features

Customer graph features:

- Shared phone numbers
- Shared addresses
- Shared devices
- Shared IPs


### ML approach

Graph analytics works extremely well.

Build:
```
Customer
 ↕
Address
 ↕
Phone
 ↕
Account
```

Graph features:

- Degree centrality
- Betweenness centrality
- Community membership

Models:

- Graph Neural Networks (GNNs)
- Node2Vec embeddings
- GraphSAGE

These often outperform tabular models.


## Layering

### Criminal behavior

Move funds repeatedly:
```
A → B → C → D → E
```
to obscure origin.

### Statistical features

Track:

- Velocity
- Path length
- Time between hops

Example:

Funds entering and leaving within hours.

### Graph methods

Represent:
```
nodes = accounts
edges = transfers
```
Then detect:

- Circular flows
- Long transfer chains
- Fan-in/fan-out structures

### ML

Graph Neural Networks

or

Graph anomaly detection:

- DeepWalk
- Node2Vec
- Graph Autoencoders

These are currently among the strongest approaches for layering detection.

## Network Fragmentation

### Criminal behavior

Spread activity across many accounts.

Example:

Instead of
```
1 account
100 suspicious transfers
```
they use
```
50 accounts
2 transfers each
```

### Statistical signal

Individual accounts look normal.

Network looks abnormal.

### Graph features

For account clusters:

- Number of connected accounts
- Cluster density
- Common beneficiaries
- Shared devices

### Models

Community detection:

- Louvain
- Leiden

Then classify communities rather than accounts.

This is a major trend in AML.


## Statistical Techniques Every AML Data Scientist Should Know

These appear repeatedly across AML scenarios:

### Outlier Detection
- Z-score
- Robust Z-score
- Isolation Forest

The basic standardized anomaly measure is: 
$$
z = \frac{x - \mu}{\sigma}
$$

TODO: Make an interactive plot of a Gaussian distribution. Sliders are data point $x$, mean $\mu$, and standard deviation $\sigma$. The plot sohuld show how width ($\sigma$) and location ($\mu$) changes, and shade the percentile given by $x$ (i.e., $\Phi(x)$). 


Useful for identifying unusual transaction amounts, frequencies, or account behaviors.

### Distribution Drift

Compare:
```
Current behavior
vs
Historical behavior
```
Methods:

- KL divergence
- PSI (Population Stability Index)
- Jensen-Shannon divergence

### Network Statistics

- Degree
- Clustering coefficient
- PageRank
- Betweenness

These are foundational for detecting layering and mule networks.

### Bayesian Risk Updating

Instead of assigning a fixed risk score, update risk as new evidence arrives.
$$
P(A \mid B) = \frac{P(B \mid A) P(A)}{P(B)}
$$

This is useful when combining signals such as:

- High-risk geography
- Structuring indicators
- Known suspicious counterparties
- Previous alerts

## What Top AML Teams Are Building Today

The most effective architecture is usually:

1. Rules layer
      - Regulatory thresholds
      - Simple structuring rules
2. Statistical anomaly layer
      - Outlier detection
      - Behavioral drift detection
3. Graph intelligence layer
      - Networks
      - Layering
      - Mule rings
      - Shared identities
4. Machine learning layer
      - XGBoost/LightGBM for account risk
      - GNNs for network risk
5. Case-ranking model
      - Predict which alerts investigators are most likely to escalate into SARs

In practice, graph analytics plus gradient-boosted trees often deliver more value in AML than deep learning alone, because most sophisticated laundering schemes are fundamentally network problems rather than purely transaction-level problems.

---


Graph methods and Bayesian statistics aren't really separate toolkits you're forcing together — they overlap directly in probabilistic graphical models, and AML is one of the cleanest domains for exploiting that overlap, because suspicion genuinely propagates through a network (layering, smurfing, mule networks) and you almost always want calibrated uncertainty rather than a hard yes/no flag for compliance review.

Transaction and KYC data (entities, transfers, risk flags)
      ↓
Graph Construction
      ↓
Graph Features
  (centrality,
   communities,
   embeddings,
   fraud proximity)
      ↓
Bayesian Risk Model (Bayes network, hierarchical Bayes, belief propagation)
      ↓
Posterior Fraud Probability (risk score - calib proba and uncertainty)
      ↓
Alert Prioritization (investigator triage - ranked alerts for human review)

## Methods 

* Bayesian networks over engineered graph features is the most direct fusion, since a BN is itself a graph plus a probability model. You take the centrality scores, community membership, and transaction-pattern flags as variables, learn or specify a DAG over them with pgmpy, and get exact or approximate posterior probability of "suspicious" given partial evidence, plus the ability to explain a flagged case as a chain of conditional probabilities rather than a black-box score, which compliance teams generally need.
* Hierarchical Bayesian models that use the detected communities as a grouping structure let you do partial pooling: every community gets its own risk parameter, but communities with few transactions borrow statistical strength from the population, which avoids overconfident scores for small or thin clusters. PyMC or NumPyro handle this naturally, something like a per-community intercept in a logistic model on top of graph and transaction features.
* Belief propagation, or loopy BP, is Bayesian inference run directly on the graph: a "suspicion" prior at known bad actors propagates through edges as messages, updating posterior beliefs at neighboring nodes. This is the natural mechanism for the actual AML phenomenon of guilt-by-association spreading through a transaction network, and it's a much better match for that intuition than a flat classifier. It's not in a single off-the-shelf package as cleanly as the others, but is straightforward to implement with networkx for graph traversal and your own message-passing update rule, or via pgmpy's belief propagation on a constructed factor graph.

Which of these four to lean on depends mostly on what decision the score feeds: pgmpy-style Bayesian networks are good when you need explainable risk factors for a regulator, hierarchical Bayes is good when you have very uneven data density across clusters, belief propagation is good when you're specifically trying to detect rings or networks of complicit accounts rather than score individuals independently, and Bayesian GNNs are good when you have enough labeled data to learn representations and need uncertainty-aware triage at scale.

For interpretability + uneven data density: The strongest fit is a hierarchical Bayesian generalized linear model rather than a full Bayesian network. Specifically: keep the model additive on the log-odds scale (logistic regression structure), put a global intercept and global coefficients on the features that apply everywhere (centrality, transaction velocity, KYC flags), and add a community-level random intercept with a hierarchical prior, so each community's risk baseline is community_effect[i] ~ Normal(mu_global, sigma_community). The hierarchy is exactly the mechanism that handles uneven clusters: a community with thousands of transactions gets an effect estimate driven mostly by its own data, while a community with five transactions gets pulled — "shrunk" — toward the global mean in proportion to how little evidence it has. You don't have to decide case by case which clusters are "too small to trust"; the model does it automatically through the posterior variance. 

The explainability payoff is that every prediction decomposes additively: predicted log-odds equals global intercept, plus that account's community effect, plus each feature's coefficient times its value. That's a native reason-code breakdown — no post-hoc approximation like SHAP needed — and because everything is a posterior distribution rather than a point estimate, each reason code comes with a credible interval, so you can show an investigator not just "transaction velocity contributed +0.8 to log-odds" but "with 90% confidence between +0.4 and +1.2." That tends to satisfy compliance/model-risk reviewers better than a plain logistic regression, since it makes the uncertainty in each contributing factor explicit rather than hiding it behind a single coefficient.