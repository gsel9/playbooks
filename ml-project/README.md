# ML Project

- Implement a baseline model. E.g., rule-based heuristics
- Test feature information: compare model performance with only random data in input features
- Sensitivity analysis: Model performance over range of hyperparameters
- Ablation study: Sequential removal of features
- Bayesian hierarchical models for handling categorical features
- Can establish causal models using subset of features to create meta features for final model?
- Uncertainty quantification (epistemic and aleoteric)
  - Uncertainty in input features
  - Uncertainty in labels
  - Uncertainty in model parameters
- Check unique values per variable relative to number of samples
- Check if det(X.T @ X) = 0 => dummy variable trap/multicolinearity (solve by dropping one variable)
- Drop high cardinality or no variance features. Drops these features from training and validation sets. Applies to features with all values missing, with the same value across all rows, or with high cardinality (for example, hashes, IDs, or GUIDs).
- Impute missing values* For numeric features, imputes with the average of values in the column. For categorical features, imputes with the most frequent value.
- Transforms numeric features that have few unique values into categorical features. One-hot encoding is used for low-cardinality categorical features. One-hot-hash encoding is used for high-cardinality categorical features.
- Cluster distance. Trains a k-means clustering model on all numeric columns. Produces k new features (one new numeric feature per cluster) that contain the distance of each sample to the centroid of each cluster.


AML:
> Bayesian statistics for uncertainty and prior knowledge, and when labels are scarce 
> Semi-supervised Learning for large unlabelled datasets
> Graph/network Methods (Bayesian Networks)
> Optimization and decision theory
> Anomaly detection (Gaussian models/density estimation)
> Graph-based + anomaly detection + domain rules + tabular ML

Plotting
--------
It's always the same tricks that make your chart better - and AI won't apply them if you don't ask:
- no 8px font
- is accessible?
- z index matters
- tell a story in the title
- inset graphs are powerful
- prefer direct labelling over legend
- reveal a chart step by step to tell a story
- if you cannot explain it in less than 25 seconds, no one will understand it
- don't build unintuitive/misleading axes
- is everything aligned with something?
- use interactivity only if it matters
- play with bin size of histograms
- use the right chart type
- boxplot hides truth
- respect color rules
- annotation is key
- declutter it

