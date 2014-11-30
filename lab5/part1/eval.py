#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import itertools

dupe_file = 'products_out.csv'
ground_truth_file = 'product_mapping.csv'

# (amazon id, google id) -> boolean
ground_truth = set()

with open(ground_truth_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        ground_truth.add((row["idAmazon"], row["idGoogleBase"]))

# cluster id -> { source -> [] }
dupes_clusters = {}

with open(dupe_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        cluster_id = int(row['Cluster ID'])

        if not cluster_id in dupes_clusters:
            dupes_clusters[cluster_id] = {'amazon': [], 'google': []}

        dupes_clusters[cluster_id][row['source']].append(row['id'])

# get dupe mapping
dupe_pairs = []

for v in dupes_clusters.itervalues():
    for i in itertools.product(v['amazon'], v['google']):
        dupe_pairs.append(i)

# compute statistics
tp = 0
fp = 0
fn = len(ground_truth - set(dupe_pairs))

for p in dupe_pairs:
    if p in ground_truth:
        tp += 1
    else:
        fp += 1

precision = float(tp) / (tp + fp)
recall = float(tp) / (tp + fn)

print 'Duplicates Found: ', len(dupe_pairs)
print
print 'True Positives: ', tp
print 'False Positives: ', fp
print 'False Negatives: ', fn
print
print 'Precision: ', precision
print 'Recall: ', recall
print 'F-measure: ', 2 * (precision * recall) / (precision + recall)
