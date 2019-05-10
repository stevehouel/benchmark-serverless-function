import argparse
import csv
import datetime as datetime
import boto3
import json

# create boto clients
cw = boto3.client('cloudwatch', region_name='us-east-1')
lb = boto3.client('lambda', region_name='us-east-1')


# extract parameters
filename = 'output.csv'

# process and write to csv
with open(filename, 'w') as csvfile:
    # initialize csv writer
    csvwriter = csv.writer(
        csvfile,
        delimiter=';',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL)

    functions = lb.list_functions(
        MaxItems=50
    )
    initial_time = datetime.datetime(2019, 4, 17, 6, 45, tzinfo=datetime.timezone.utc)
    for f in functions['Functions']:
        if 'aws-coldstart' in f['FunctionName']:
            print(json.dumps(f['FunctionName']))
            result = cw.get_metric_statistics(
                MetricName= 'Duration',
                Namespace= 'AWS/Lambda',
                Period= 60,
                Dimensions= [ { 'Name': 'FunctionName', 'Value': f['FunctionName'] } ],
                Statistics= [ 'Maximum'],
                Unit= 'Milliseconds',
                StartTime=initial_time,
                EndTime=initial_time + datetime.timedelta(days=1))
            if 'Datapoints' in result:
                avg = 0
                count = 0
                for point in sorted(result['Datapoints'], key=lambda d: d['Timestamp']):
                    avg += point['Maximum']
                    count = count + 1
                csvwriter.writerow([f['Runtime'], f['MemorySize'], avg / count])


    print('CSV file %s created.' % filename)
