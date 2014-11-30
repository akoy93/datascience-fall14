from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import csv

KEYSPACE = "lab7_python"


def main():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()

    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
        """ % KEYSPACE)

    session.set_keyspace(KEYSPACE)

    session.execute("""
        CREATE TABLE IF NOT EXISTS data (
            type text,
            owner_id int,
            ad_id int,
            num_clicks int,
            num_impressions int,
            PRIMARY KEY ((owner_id,ad_id),type)
        )
        """)

    query = SimpleStatement("""
        INSERT INTO data (type, owner_id, ad_id, num_clicks, num_impressions)
        VALUES (%(type)s, %(owner_id)s, %(ad_id)s, %(num_clicks)s, %(num_impressions)s)
        """, consistency_level=ConsistencyLevel.ONE)

    prepared = session.prepare("""
        INSERT INTO data (type, owner_id, ad_id, num_clicks, num_impressions)
        VALUES (?, ?, ?, ?, ?)
        """)

    with open('data.csv', 'rb') as datafile:
        reader = csv.reader(datafile)
        i = 0
        for row in reader:
            i += 1
            session.execute(query, dict(type=row[0], owner_id=int(row[1]), ad_id=int(row[2]), num_clicks=int(row[3]), num_impressions=int(row[4])))
            session.execute(prepared, (row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4])))

    # find ctr for each OwnerId, AdId pair
    owner_ids = {}
    keys = {}
    clicks = {}
    impressions = {}

    future = session.execute_async("SELECT * FROM data")

    try:
        rows = future.result()
    except Exception:
        print "exception"

    for row in rows:
        owner_ids[row[0]] = True
        keys[(row[0], row[1])] = True

    for key in keys:
        clicks_future = session.execute_async("SELECT * FROM data WHERE owner_id = %s AND ad_id = %s AND type='clicks'" % (key[0], key[1]))
        clicks_rows = clicks_future.result()
        impressions_future = session.execute_async("SELECT * FROM data WHERE owner_id = %s AND ad_id = %s AND type='impressions'" % (key[0], key[1]))
        impressions_rows = impressions_future.result()
        for click in clicks_rows:
            if key[0] in clicks:
                clicks[key[0]] += click[3]
            else:
                clicks[key[0]] = click[3]
            clicks[key] = click[3]
        for impression in impressions_rows:
            if key[0] in impressions:
                impressions[key[0]] += impression[4]
            else:
                impressions[key[0]] = impression[4]
            impressions[key] = impression[4]

    # Data:
    print "owner_id, ad_id, ctr"
    for key in keys:
        print "%s, %s, %f" % (key[0], key[1], float(clicks[key]) / float(impressions[key]))
    print
    print "owner_id, ctr"
    for owner_id in owner_ids:
        print "%s, %f" % (owner_id, float(clicks[owner_id]) / float(impressions[owner_id]))
    print
    print "owner_id, ad_id, ctr (for owner_id=1, ad_id=3)"
    print "%s, %s, %f" % (1, 3, float(clicks[(1, 3)]) / float(impressions[(1, 3)]))
    print
    print "owner_id, ctr (for owner_id=2)"
    print "%s, %f" % (2, float(clicks[2]) / float(impressions[2]))


    session.execute("DROP KEYSPACE " + KEYSPACE)

if __name__ == "__main__":
    main()