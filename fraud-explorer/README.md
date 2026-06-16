# fraud_explorer

An interactive browser-based tool for exploring fraud detection on graph data. Run one Python script — it builds the graph, extracts features, trains a model, and opens a visual explorer in your browser where you can click any node to inspect its features and model prediction.

![Explorer screenshot showing the graph canvas on the left and the node inspector panel on the right](screenshot.png)

## What it does

- Builds a transaction graph (synthetic by default, swappable for real data)
- Extracts interpretable node-level features: degree, clustering coefficient, PageRank, betweenness, closeness, triangle count, and neighbourhood fraud fraction
- Trains a logistic regression classifier on a held-out test split
- Launches a local web server and opens an interactive explorer where you can:
  - See every node coloured by its fraud probability (blue = safe, red = high risk)
  - Click any node to see its raw features, model coefficients, and per-feature contribution to the prediction
  - Toggle training nodes on/off to see the full graph context
  - Hover any node for a quick tooltip with its ID and fraud probability

## File structure

## Requirements

Python 3.8 or later, plus:

```bash
pip install networkx scikit-learn numpy
```

No frontend build step — the browser UI is plain HTML and JavaScript.

## Usage

```bash
python run.py
```

The script runs the full pipeline, prints a classification report to the terminal, and opens `http://localhost:8765` in your default browser. Press `Ctrl+C` to stop the server.

## How to customise

All four customisation points are in `run.py`, each clearly marked with a comment block.

### Swap in your own dataset

Replace the body of `build_graph()`. The only requirement is that the function returns a NetworkX `Graph` with a `"fraud"` node attribute set to `0` or `1`:

```python
import pandas as pd

def build_graph():
    edges_df  = pd.read_csv("edges.csv")       # columns: src, dst
    labels_df = pd.read_csv("labels.csv")      # columns: node_id, fraud
    G = nx.from_pandas_edgelist(edges_df, "src", "dst")
    nx.set_node_attributes(
        G,
        labels_df.set_index("node_id")["fraud"].to_dict(),
        "fraud"
    )
    return G
```

For the [Elliptic Bitcoin dataset](https://www.kaggle.com/datasets/ellipticco/elliptic-data-set) or the [FraudAmazon DGL dataset](https://docs.dgl.ai/en/latest/generated/dgl.data.FraudAmazonDataset.html), load the edge list and label columns the same way.

### Add or remove features

Inside `extract_features()`, add any key to the dict inside the `rows.append({...})` call. New features appear automatically in the browser explorer with no other changes needed:

```python
rows.append({
    ...
    "my_new_feature": round(my_values[n], 4),
})
```

A commented example of a 2-hop neighbourhood fraud fraction is already included as a starting point.

### Swap the model

One line inside `train_model()`. Any scikit-learn compatible classifier works:

```python
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(class_weight="balanced", n_estimators=100)
```

The explorer automatically shows coefficients for linear models (`coef_`) and feature importances for tree models (`feature_importances_`).

### Change the port

At the top of `run.py`:

```python
PORT = 8765
```

## How the explorer works

`run.py` runs a lightweight HTTP server on `localhost` with two routes:

- `GET /` — serves `explorer.html`
- `GET /data.json` — serves the graph, features, layout coordinates, and model outputs as JSON

`explorer.html` fetches `/data.json` on load and renders everything client-side using the Canvas API. No data is hardcoded in the HTML file — rerunning `run.py` with a different dataset or model immediately updates the explorer.

## Understanding the inspector panel

When you click a node, the right panel shows three things:

**Fraud probability** — the model's predicted probability that this node is fraudulent, with a true/false positive/negative badge showing whether the prediction was correct.

**Feature contributions** — for each feature: its model coefficient (or importance for tree models), the node's raw value, and its contribution to the log-odds score, calculated as `coef × (value − mean) / std`. Blue bars push the prediction toward fraud; amber bars push it away. This shows you *why* the model scored this node the way it did.

**Raw features** — the exact values used as model input.

## Background

This tool was built to accompany a tutorial on interpretable fraud detection using graph data and logistic regression. For the full explanation of the approach — including feature extraction rationale, why graph neighbourhood features (especially `neighbor_fraud_frac`) dominate the signal, and how this pipeline compares to Graph Attention Networks and Graph Transformers — see the conversation that produced it.