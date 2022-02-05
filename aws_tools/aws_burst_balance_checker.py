#!usr/bin/python3.7
"""Usage: python3 aws_burst_balance_checker.py -h """
import argparse
import boto3
import pprint
from datetime import datetime, timezone, timedelta
from botocore.exceptions import ClientError

# Parser for command line arguments
parser = argparse.ArgumentParser(prog="python3 aws_burst_balance_checker.py",
                                 description="This is a script to show the details of EBS Volume burst balance. Tips: "
                                             "Keep the start and end times close together (ie don't try to get metrics"
                                             "that span a few hours).")
# Add parser arguments
parser.add_argument("-p",
                    "--profile",
                    dest="profile",
                    required=True,
                    help="REQUIRED. The AWS profile name to use")
parser.add_argument("-r",
                    "--region",
                    dest="region",
                    required=False,
                    default="us-east-1",
                    help="The AWS region to check. Default is us-east-1")
parser.add_argument("-i",
                    "--instance",
                    dest="instance_id",
                    required=True,
                    help="The Instances EBS Volumes to search for")
parser.add_argument("-d",
                    "--debug",
                    dest="debug",
                    action="store_true",
                    default=False,
                    help="Turn on debugging, Default is False")
parser.add_argument("-s",
                    "--start",
                    dest="start",
                    required=False,
                    help="The metric start time in ISO 8601 UTC format. Ex: 2020-03-09T07:00:00Z")
parser.add_argument("-e",
                    "--end",
                    dest="end",
                    required=False,
                    help="The metric end time in ISO 8601 UTC format. Ex: 2020-03-09T07:05:00Z")
# Parse the arguments
args = parser.parse_args()

# Set the Boto3 session
session = boto3.Session(profile_name=args.profile)
if args.debug:
    # Use a pretty printer for printing list of lists
    pp = pprint.PrettyPrinter()


def ebs_describer():
    """This function handles describing EBS volumes for an EC2 instance provided."""
    try:
        # The EC2 boto3 client
        ec2_client = session.client('ec2', region_name=args.region)
        # The CloudWatch boto3 client
        cw_client = session.client('cloudwatch', region_name=args.region)
        # List the EBS volumes attached to the Ec2 Instance provided
        ec2_volumes = ec2_client.describe_volumes(Filters=[{'Name': 'attachment.instance-id',
                                                            'Values': [args.instance_id]}])
        # Set the Start and End times based on input. Default is 5 to 4 minutes ago
        start_time = args.start if args.start \
            else (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat().split('.')[0]
        end_time = args.end if args.end \
            else (datetime.now(timezone.utc) - timedelta(minutes=4)).isoformat().split('.')[0]
        if args.debug:
            print(f"start_time: {start_time}\nend_time: {end_time}")
        # The EBS Volume types that can use burst IOPS
        burstable_list = ["gp2", "st1", "sc1"]

        if args.debug:
            pp.pprint(ec2_volumes)
        for volumes in ec2_volumes['Volumes']:
            # General Volume Information
            volume_id = volumes['VolumeId']
            volume_iops = volumes['Iops']
            volume_size = volumes['Size']
            volume_type = volumes['VolumeType']
            volume_status = "N/A"
            burst_avg = "N/A"
            burst_min = "N/A"
            ebs_read_ops = "N/A"
            ebs_write_ops = "N/A"
            # EBS Volume Status
            ebs_status = ec2_client.describe_volume_status(VolumeIds=[volume_id])
            if ebs_status:
                volume_status = ebs_status['VolumeStatuses'][0]['VolumeStatus']['Status']
            # If the volume is less than a terabyte, then it will use burst IOPS
            if volume_size < 1000 and volume_type in burstable_list:
                if args.debug:
                    print("(if volume_size < 1000 and volume_type in burstable_list)")
                ebs_metrics = cw_client.get_metric_statistics(Namespace='AWS/EBS',
                                                              MetricName='BurstBalance',
                                                              Dimensions=[{
                                                                  "Name": 'VolumeId',
                                                                  "Value": volume_id
                                                              }],
                                                              StartTime=start_time,
                                                              EndTime=end_time,
                                                              Period=1,
                                                              Statistics=['Minimum'],
                                                              Unit='Percent')
                if ebs_metrics:
                    if args.debug:
                        print(f"(if ebs_metrics) VolumeID: {volume_id} "
                              f"metric count: {len(ebs_metrics['Datapoints'])}")
                    if len(ebs_metrics['Datapoints']) > 0:
                        burst_min = min(metric['Minimum'] for metric in ebs_metrics['Datapoints'])
                        burst_avg = float(sum(metric['Average'] for metric in ebs_metrics['Datapoints'])) / len(ebs_metrics['Datapoints'])
                    elif args.debug:
                        print(f"(!len(ebs_metrics['Datapoints']) > 0) ebs_metrics: {pp.pformat(ebs_metrics)}")

            if args.debug:
                print("(else IOPS Reads/Writes) . . . ")
            ebs_reads = cw_client.get_metric_statistics(Namespace='AWS/EBS',
                                                        MetricName='VolumeReadOps',
                                                        Dimensions=[{
                                                              'Name': 'VolumeId',
                                                              'Value': volume_id
                                                        }],
                                                        StartTime=start_time,
                                                        EndTime=end_time,
                                                        Period=1,
                                                        Statistics=['Sum'],
                                                        Unit='Count')
            ebs_writes = cw_client.get_metric_statistics(Namespace='AWS/EBS',
                                                         MetricName='VolumeWriteOps',
                                                         Dimensions=[{
                                                              'Name': 'VolumeId',
                                                              'Value': volume_id
                                                         }],
                                                         StartTime=start_time,
                                                         EndTime=end_time,
                                                         Period=1,
                                                         Statistics=['Sum'],
                                                         Unit='Count')
            if ebs_reads:
                if args.debug:
                    print(f"(if ebs_reads) VolumeID: {volume_id}"
                          f"metric count: {len(ebs_reads['Datapoints'])}")
                if len(ebs_reads['Datapoints']) > 0:
                    ebs_read_ops = sum(metric['Sum'] for metric in ebs_reads['Datapoints'])
                elif args.debug:
                    print(f"(!len(ebs_reads['Datapoints']) > 0) ebs_metrics: {pp.pformat(ebs_reads)}")
            if ebs_writes:
                if args.debug:
                    print(f"(if ebs_writes) VolumeID: {volume_id}"
                          f"metric count: {len(ebs_writes['Datapoints'])}")
                if len(ebs_writes['Datapoints']) > 0:
                    ebs_write_ops = sum(metric['Sum'] for metric in ebs_writes['Datapoints'])
                elif args.debug:
                    print(f"(!len(ebs_writes['Datapoints']) > 0) ebs_metrics: {pp.pformat(ebs_writes)}")
            # Print the details of each volume.
            print(f"***************************************************************")
            print(f"\tVolumeID: {volume_id} \n\tType: {volume_type} \n\tIOPS: {volume_iops}"
                  f"\n\tSize: {volume_size}\n\tStatus: {volume_status}\n\tBurst Avg: {burst_avg}"
                  f"\n\tBurst Min: {burst_min}\n\tRead Ops: {ebs_read_ops}\n\tWrite Ops: {ebs_write_ops}")
            print(f"***************************************************************")

    except ClientError as ce:
        print(f"ERROR! ClientError: {ce}")


if __name__ == '__main__':
    """The Main function"""
    if args.debug:
        print(f"Checking The AWS Account For {args.profile} In Region {args.region} . . . ")
    ebs_describer()
