"""
Fraud Graph Explorer
====================
Run this file to:
  1. Build a synthetic fraud graph  (swap in your own data here)
  2. Extract graph features          (add/remove features here)
  3. Train a classifier              (swap model here)
  4. Launch an interactive browser explorer

Usage:
    python run.py

Requirements:
    pip install networkx scikit-learn numpy
"""

import json
import os
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import networkx as nx
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

np.random.seed(42)

# ── CONFIG ────────────────────────────────────────────────────────────────────
PORT = 8765


# =============================================================================
# STEP 1 — BUILD / LOAD YOUR GRAPH
# =============================================================================
# Replace this function with your own data loader, e.g.:
#
#   import pandas as pd
#   edges_df  = pd.read_csv("edges.csv")       # columns: src, dst
#   labels_df = pd.read_csv("labels.csv")      # columns: node_id, fraud
#   G = nx.from_pandas_edgelist(edges_df, "src", "dst")
#   nx.set_node_attributes(G, labels_df.set_index("node_id")["fraud"].to_dict(), "fraud")
#   return G

def build_graph():
    """Synthetic fraud graph: scale-free legit network + tight fraud rings."""
    print("Building graph...")
    N_LEGIT = 200

    G_legit = nx.barabasi_albert_graph(N_LEGIT, m=2, seed=42)
    G = nx.Graph()
    G.add_nodes_from(G_legit.nodes())
    G.add_edges_from(G_legit.edges())

    fraud_node_ids = []
    offset = N_LEGIT
    for i in range(3):
        ring = nx.watts_strogatz_graph(12, k=4, p=0.3, seed=i)
        mapping = {n: n + offset for n in ring.nodes()}
        G.add_nodes_from(mapping.values())
        G.add_edges_from((mapping[u], mapping[v]) for u, v in ring.edges())
        fraud_node_ids.extend(mapping.values())
        offset += ring.number_of_nodes()

    # Bridge edges: connect fraud rings to legit network
    rng = np.random.default_rng(42)
    bridge_legit = rng.choice(N_LEGIT, size=6, replace=False)
    bridge_fraud  = rng.choice(fraud_node_ids, size=6, replace=False)
    for l, f in zip(bridge_legit, bridge_fraud):
        G.add_edge(int(l), int(f))

    labels = {n: 0 for n in G.nodes()}
    for n in fraud_node_ids:
        labels[n] = 1
    nx.set_node_attributes(G, labels, "fraud")

    print(f"  {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print(f"  Fraud: {sum(labels.values())} ({100*sum(labels.values())/G.number_of_nodes():.1f}%)")
    return G


# =============================================================================
# STEP 2 — EXTRACT FEATURES
# =============================================================================
# Add your own features inside the loop — any key you add to the dict will
# appear automatically in the browser explorer.

def extract_features(G):
    """Compute node-level features from graph structure."""
    print("Extracting features...")
    nodes = list(G.nodes())
    fraud_label = nx.get_node_attributes(G, "fraud")

    # Structural features
    degree      = dict(G.degree())
    clustering  = nx.clustering(G)
    pagerank    = nx.pagerank(G, alpha=0.85)
    betweenness = nx.betweenness_centrality(G, k=min(80, len(nodes)))
    closeness   = nx.closeness_centrality(G)
    triangles   = nx.triangles(G)

    # Neighbourhood features
    nbr_fraud_frac  = {}
    nbr_degree_mean = {}
    nbr_degree_max  = {}
    nbr_clustering  = {}

    for n in nodes:
        nbrs = list(G.neighbors(n))
        if nbrs:
            nbr_fraud_frac[n]  = float(np.mean([fraud_label.get(nb, 0) for nb in nbrs]))
            degs               = [degree[nb] for nb in nbrs]
            nbr_degree_mean[n] = float(np.mean(degs))
            nbr_degree_max[n]  = float(np.max(degs))
            nbr_clustering[n]  = float(np.mean([clustering[nb] for nb in nbrs]))
        else:
            nbr_fraud_frac[n] = nbr_degree_mean[n] = nbr_degree_max[n] = nbr_clustering[n] = 0.0

    # ── ADD YOUR OWN FEATURES HERE ───────────────────────────────────────────
    # Example: 2-hop neighbourhood fraud fraction
    # nbr2_fraud = {}
    # for n in nodes:
    #     two_hop = set()
    #     for nb in G.neighbors(n):
    #         two_hop.update(G.neighbors(nb))
    #     two_hop.discard(n)
    #     nbr2_fraud[n] = float(np.mean([fraud_label.get(nb,0) for nb in two_hop])) if two_hop else 0.0
    # ─────────────────────────────────────────────────────────────────────────

    rows = []
    for n in nodes:
        rows.append({
            "node":                 n,
            "label":                fraud_label.get(n, 0),
            # Structural
            "degree":               degree[n],
            "clustering_coef":      round(clustering[n], 6),
            "pagerank":             round(pagerank[n], 6),
            "betweenness":          round(betweenness[n], 6),
            "closeness":            round(closeness[n], 6),
            "triangles":            triangles[n],
            # Neighbourhood
            "neighbor_fraud_frac":  round(nbr_fraud_frac[n], 6),
            "neighbor_degree_mean": round(nbr_degree_mean[n], 4),
            "neighbor_degree_max":  round(nbr_degree_max[n], 4),
            "neighbor_clustering":  round(nbr_clustering[n], 6),
            # Add your own features here — they appear in the explorer automatically
            # "nbr2_fraud_frac": round(nbr2_fraud[n], 6),
        })

    print(f"  {len(rows)} nodes x {len(rows[0]) - 2} features")
    return rows


# =============================================================================
# STEP 3 — TRAIN CLASSIFIER
# =============================================================================
# Swap LogisticRegression for any sklearn-compatible model, e.g.:
#   from sklearn.ensemble import RandomForestClassifier
#   clf = RandomForestClassifier(class_weight="balanced", n_estimators=100)
#
# The explorer shows coefficients for linear models and feature importances
# for tree models automatically.

def train_model(rows, feature_cols):
    """Train, evaluate, and return predictions for all nodes."""
    print("Training model...")

    X = np.array([[r[c] for c in feature_cols] for r in rows])
    y = np.array([r["label"] for r in rows])
    node_ids = [r["node"] for r in rows]

    X_tr, X_te, y_tr, y_te, idx_tr, idx_te = train_test_split(
        X, y, node_ids, test_size=0.3, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr)
    X_te_s = scaler.transform(X_te)

    # ── SWAP YOUR MODEL HERE ─────────────────────────────────────────────────
    clf = LogisticRegression(class_weight="balanced", C=0.5, max_iter=1000)
    # clf = RandomForestClassifier(class_weight="balanced", n_estimators=100)
    # ────────────────────────────────────────────────────────────────────────

    clf.fit(X_tr_s, y_tr)

    print("\n── Classification report (test set) ──")
    print(classification_report(y_te, clf.predict(X_te_s), target_names=["Legit", "Fraud"]))

    # Coefficients (linear models) or importances (tree models)
    if hasattr(clf, "coef_"):
        raw_coefs = clf.coef_[0]
        coefs = {f: round(float(raw_coefs[i]), 4) for i, f in enumerate(feature_cols)}
        coef_type = "coefficient"
    elif hasattr(clf, "feature_importances_"):
        raw_imp = clf.feature_importances_
        coefs = {f: round(float(raw_imp[i]), 4) for i, f in enumerate(feature_cols)}
        coef_type = "importance"
    else:
        coefs = {f: 0.0 for f in feature_cols}
        coef_type = "none"

    # Predictions for test nodes only
    probs_te = clf.predict_proba(X_te_s)[:, 1]
    preds_te = clf.predict(X_te_s)
    test_results = {
        nid: {"prob": round(float(probs_te[i]), 4), "pred": int(preds_te[i])}
        for i, nid in enumerate(idx_te)
    }

    return coefs, coef_type, test_results, set(idx_tr), set(idx_te)


# =============================================================================
# STEP 4 — BUILD LAYOUT AND EXPORT
# =============================================================================

def build_export(G, rows, feature_cols, coefs, coef_type, test_results, train_ids, test_ids):
    """Compute spring layout and assemble JSON payload for the browser."""
    print("Computing layout...")
    pos = nx.spring_layout(G, seed=42, k=1.2)

    nodes_out = {}
    for r in rows:
        n = r["node"]
        tr = test_results.get(n, {})
        nodes_out[str(n)] = {
            "id":       n,
            "x":        round(pos[n][0], 4),
            "y":        round(pos[n][1], 4),
            "label":    r["label"],
            "is_test":  n in test_ids,
            "features": {c: r[c] for c in feature_cols},
            "prob":     tr.get("prob"),
            "pred":     tr.get("pred"),
        }

    return {
        "nodes":        nodes_out,
        "edges":        [[int(u), int(v)] for u, v in G.edges()],
        "feature_cols": feature_cols,
        "coefs":        coefs,
        "coef_type":    coef_type,
    }


# =============================================================================
# STEP 5 — SERVE THE EXPLORER
# =============================================================================

HTML_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "explorer.html")

def make_handler(data_json):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # silence request logs

        def do_GET(self):
            if self.path == "/data.json":
                body = data_json.encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)
            elif self.path in ("/", "/index.html"):
                with open(HTML_FILE, "rb") as f:
                    body = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self.send_response(404)
                self.end_headers()
    return Handler


def main():
    G = build_graph()
    rows = extract_features(G)
    feature_cols = [k for k in rows[0].keys() if k not in ("node", "label")]
    coefs, coef_type, test_results, train_ids, test_ids = train_model(rows, feature_cols)
    export = build_export(G, rows, feature_cols, coefs, coef_type, test_results, train_ids, test_ids)
    data_json = json.dumps(export, separators=(",", ":"))

    url = f"http://localhost:{PORT}"
    server = HTTPServer(("localhost", PORT), make_handler(data_json))

    print(f"\n── Explorer ready ──────────────────────────")
    print(f"   {url}")
    print(f"   Press Ctrl+C to stop")
    print(f"────────────────────────────────────────────\n")

    threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()