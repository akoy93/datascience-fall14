#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
import re
import collections
import logging
import optparse
from numpy import nan

import dedupe
from unidecode import unidecode

# ## Logging

# Dedupe uses Python logging to show or suppress verbose output. Added for convenience.
# To enable verbose logging, run `python examples/csv_example/csv_example.py -v`
optp = optparse.OptionParser()
optp.add_option('-v', '--verbose', dest='verbose', action='count',
                help='Increase verbosity (specify multiple times for more)'
                )
(opts, args) = optp.parse_args()
log_level = logging.WARNING 
if opts.verbose == 1:
    log_level = logging.INFO
elif opts.verbose >= 2:
    log_level = logging.DEBUG
logging.getLogger().setLevel(log_level)


# ## Setup

# Switch to our working directory and set up our input and out put paths,
# as well as our settings and training file locations
input_file = 'products.csv'
output_file = 'products_out.csv'
settings_file = 'products_learned_settings'
training_file = 'products_training.json'


# Dedupe can take custom field comparison functions
# Here you need to define any custom comparison functions you may use for different fields

def priceComparator(price1, price2):
    if price1 and price2:
    	price1 = parsePrice(price1)
        price2 = parsePrice(price2)

        if price1 == 0 or price2 == 0:
            return nan 

        max_price = max(price1, price2)
        min_price = min(price1, price2)

        percentage = min_price / max_price

        if percentage < .75:
            return 0

        return percentage
    else:
        return nan

def parsePrice(price):
    if price[-3:] == "gbp":
        return float(price[0:-3]) * 1.61
    else:
        return float(price)

def preProcess(column):
    """
    Do a little bit of data cleaning with the help of Unidecode and Regex.
    Things like casing, extra spaces, quotes and new lines can be ignored.
    """

    column = unidecode(column)
    column = re.sub('  +', ' ', column)
    column = re.sub('\n', ' ', column)
    column = column.strip().strip('"').strip("'").lower().strip()
    return column

def strip(word):
    pattern = re.compile('[\W_]+')
    return re.sub(pattern, '', word)

def readData(filename):
    """
    Read in our data from a CSV file and create a dictionary of records, 
    where the key is a unique record ID and each value is dict
    """

    data_d = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # clean_row = [(k, preProcess(v)) for (k, v) in row.items()]
            clean_row = []
            for (k, v) in row.items():
                v = preProcess(v)
                if k == 'description':
                    #print 'description'
                    v = ' '.join([strip(w) for w in v.split(' ')[0:10]])
                clean_row.append((k, v))

            #joined_row = [clean_row[0], ('manufacturer_title', preProcess(clean_row[5][1] + " " + clean_row[1][1])), clean_row[2], clean_row[3], clean_row[4]]
            row_id = row['id']
            data_d[row_id] = dict(clean_row)

    return data_d


print 'importing data ...'
data_d = readData(input_file)

# ## Training

if os.path.exists(settings_file):
    print 'reading from', settings_file
    with open(settings_file, 'rb') as f:
        deduper = dedupe.StaticDedupe(f)

else:
    # Here you will need to define the fields dedupe will pay attention to. You also need to define the comparator
    # to be used and specify any customComparators. Please read the dedupe manual for details
    fields = [
        {'field' : 'manufacturer', 'type': 'String'},
 	    {'field' : 'title', 'type': 'String'},
        {'field' : 'price', 'type': 'Custom', 'has missing':True, 'comparator' : priceComparator},
        {'field' : 'description', 'type': 'Text', 'has missing': True}
        ]

    # Create a new deduper object and pass our data model to it.
    deduper = dedupe.Dedupe(fields)

    # To train dedupe, we feed it a random sample of records.
    deduper.sample(data_d, 150000)


    # If we have training data saved from a previous run of dedupe,
    # look for it an load it in.
    # __Note:__ if you want to train from scratch, delete the training_file
    if os.path.exists(training_file):
        print 'reading labeled examples from ', training_file
        with open(training_file, 'rb') as f:
            deduper.readTraining(f)

    # ## Active learning
    # Dedupe will find the next pair of records
    # it is least certain about and ask you to label them as duplicates
    # or not.
    # use 'y', 'n' and 'u' keys to flag duplicates
    # press 'f' when you are finished
    print 'starting active labeling...'

    dedupe.consoleLabel(deduper)

    deduper.train()

    # When finished, save our training away to disk
    with open(training_file, 'w') as tf :
        deduper.writeTraining(tf)

    # Save our weights and predicates to disk.  If the settings file
    # exists, we will skip all the training and learning next time we run
    # this file.
    with open(settings_file, 'w') as sf :
        deduper.writeSettings(sf)


# ## Blocking

print 'blocking...'

# ## Clustering

# Find the threshold that will maximize a weighted average of our precision and recall. 
# When we set the recall weight to 2, we are saying we care twice as much
# about recall as we do precision.
#
# If we had more data, we would not pass in all the blocked data into
# this function but a representative sample.

threshold = deduper.threshold(data_d, recall_weight=2.0)

# `match` will return sets of record IDs that dedupe
# believes are all referring to the same entity.

print 'clustering...'
clustered_dupes = deduper.match(data_d, threshold)

print '# duplicate sets', len(clustered_dupes)

# ## Writing Results

# Write our original data back out to a CSV with a new column called 
# 'Cluster ID' which indicates which records refer to each other.

cluster_membership = {}
cluster_id = 0
for (cluster_id, cluster) in enumerate(clustered_dupes):
    id_set, conf_score = cluster
    cluster_d = [data_d[c] for c in id_set]
    for record_id in id_set:
        cluster_membership[record_id] = {
            "cluster id" : cluster_id,
            "confidence": conf_score
        }

singleton_id = cluster_id + 1

with open(output_file, 'w') as f_output:
    writer = csv.writer(f_output)

    with open(input_file) as f_input :
        reader = csv.reader(f_input)

        heading_row = reader.next()
        heading_row.insert(0, 'Cluster ID')
        heading_row.append('confidence_score')
        
        writer.writerow(heading_row)

        for row in reader:
            row_id = row[1]
            if row_id in cluster_membership:
                cluster_id = cluster_membership[row_id]["cluster id"]
                row.insert(0, cluster_id)
                row.append(cluster_membership[row_id]['confidence'])
            else:
                row.insert(0, singleton_id)
                singleton_id += 1
                row.append(None)
            writer.writerow(row)
