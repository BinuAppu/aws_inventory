import boto3
import os
import pandas as pd

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

# Enter the Access key or Secret Key here
accesskey = ''
secretkey = ''

logo = """
======================================
This script collects Inventory for AWS
======================================
Script by Binu Balan
"""
print(logo)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

session = boto3.Session(
    aws_access_key_id=accesskey,
    aws_secret_access_key=secretkey
)

if accesskey and secretkey:
    print("[+] Connecting using Access and Secret Key")
    connect = session.client("ec2",region_name='us-east-1')
else:
    print("[+] Connecting using base authentication.")
    connect = boto3.client("ec2",region_name='us-east-1')

#print(bcolors.OKGREEN + f"[+] List all regions for the Environment" + bcolors.ENDC)
print ("[+] Working on Route VPC's")
regions = connect.describe_regions()
combineval = []
for region in regions["Regions"]:
    regionName = region["RegionName"]
    try:
        vpcregionwise = session.client("ec2",region_name=regionName)
        fetchvpcfromregion = vpcregionwise.describe_vpcs()
        print(bcolors.OKBLUE + f"[+] Printing VPCs for Region {regionName}" + bcolors.ENDC)
        for vpcinregion in fetchvpcfromregion["Vpcs"]:
            # pandas dict to csv
            pd.DataFrame([vpcinregion]).to_csv("vpc_report_panda.csv", mode='a', header=True, index=False)
    except:
        pass

print ("[+] Working on Subnets")
regions = connect.describe_regions()
for region in regions["Regions"]:
    regionName = region["RegionName"]
    try:
        vpcregionwisesub = session.client("ec2",region_name=regionName)
        regsubnets = vpcregionwisesub.describe_subnets()
        print(bcolors.OKGREEN + f"[+] Printing Subnets for Region {regionName}" + bcolors.ENDC)
        for subnets in regsubnets["Subnets"]:
            pd.DataFrame([subnets]).to_csv("subnets_report_panda.csv", mode='a', header=True, index=False)
    except:
        pass
        

print ("[+] Working on Route Tables")
print(bcolors.OKGREEN + f"[+] List all Route Tables for the Environment" + bcolors.ENDC)
regions = connect.describe_regions()
for region in regions["Regions"]:
    regionName = region["RegionName"]
    try:
        routetables = session.client("ec2",region_name=regionName)
        getroutes = routetables.describe_route_tables()
        print(bcolors.OKGREEN + f"[+] Printing Route Tables for Region {regionName}" + bcolors.ENDC)
        for routes in getroutes["RouteTables"]:
                for route in routes["Routes"]:
                    print(route)
                    pd.DataFrame([route]).to_csv("route_report_panda.csv", mode='a', header=True, index=False)
    except:
        pass
        

print ("[+] Working on listing S3 Buckets")
#for region in regions["Regions"]:
buckets3 = ""
bucket = ""

connect = session.client("s3")
buckets3 = connect.list_buckets()
print(bcolors.OKGREEN + f"[+] Printing Storage for Region {regionName}" + bcolors.ENDC)
for bucket in buckets3["Buckets"]:
    eachbucket = bucket
    print(eachbucket)
    pd.DataFrame([eachbucket]).to_csv("storage_report_panda.csv", mode='a', header=True, index=False)


print ("[+] Working on Public IPs")
for region in regions["Regions"]:
    regionName = region["RegionName"]
    try:
        regionpubips = session.client("ec2",region_name=regionName)
        allpubips = regionpubips.describe_addresses()
        print(bcolors.OKGREEN + f"[+] Printing Public IPs for Region {regionName}" + bcolors.ENDC)
        for pubips in allpubips["Addresses"]:
            print(pubips)
            pd.DataFrame([pubips]).to_csv("public_ip_report_panda.csv", mode='a', header=True, index=False)
    except:
        pass
 

# export Ec2 Instances
print ("[+] Working on EC2 Instances")
for region in regions["Regions"]:
    regionName = region["RegionName"]
    try:
        ec2region = session.client("ec2",region_name=regionName)
        allinstances = ec2region.describe_instances()
        print(bcolors.OKGREEN + f"[+] Printing EC2 Instances for Region {regionName}" + bcolors.ENDC)
        for reservation in allinstances["Reservations"]:
            for instance in reservation["Instances"]:
                print("Working on Instance: ", instance.get("InstanceId"))
                pd.DataFrame([instance]).to_csv("ec2_report_panda.csv", mode='a', header=True, index=False)
    except:
        pass


# Export volume details
print ("[+] Working on EC2 Volumes")
for region in regions["Regions"]:
    regionName = region["RegionName"]
    try:
        ec2regionvol = session.client("ec2",region_name=regionName)
        allvolumes = ec2regionvol.describe_volumes()
        print(bcolors.OKGREEN + f"[+] Printing EC2 Volumes for Region {regionName}" + bcolors.ENDC)
        for volume in allvolumes["Volumes"]:
            print(volume)
            pd.DataFrame([volume]).to_csv("ec2_volume_report_panda.csv", mode='a', header=True, index=False)
    except:
        pass

# Export following to Text File - EBS Encryption by Default, AMI Block Public Access, EBS Snapshot Block Public Access, IMDS defaults
print ("[+] Working on EBS Encryption by Default")
secconfig = session.client("ec2")
ebsdefault = secconfig.get_ebs_encryption_by_default()
print(bcolors.OKGREEN + f"[+] EBS Encryption by Default: {ebsdefault}" + bcolors.ENDC)
with open("ebs_configs.txt", "a") as file:
    file.write(str("EBS Encryption by Default:"))
    file.write(str(ebsdefault))
    file.write(str("\n"))
    file.close()
print ("[+] Working on AMI Block Public Access")
amiblock = secconfig.get_image_block_public_access_state()
print(bcolors.OKGREEN + f"[+] AMI Block Public Access: {amiblock}" + bcolors.ENDC)
with open("ebs_configs.txt", "a") as file:
    file.write(str("AMI Block Public Access:"))
    file.write(str(amiblock))
    file.write(str("\n"))
    file.close()
print ("[+] Working on EBS Snapshot Block Public Access")
ebssnapshotblock = secconfig.get_image_block_public_access_state()
print(bcolors.OKGREEN + f"[+] EBS Snapshot Block Public Access: {ebssnapshotblock}" + bcolors.ENDC)
with open("ebs_configs.txt", "a") as file:
    file.write(str("EBS Snapshot Block Public Access:"))
    file.write(str(ebssnapshotblock))
    file.write(str("\n"))
    file.close()
print ("[+] Working on IMDS defaults")
imdsdefaults = secconfig.get_instance_metadata_defaults()
print(bcolors.OKGREEN + f"[+] IMDS Defaults: {imdsdefaults}" + bcolors.ENDC)
with open("ebs_configs.txt", "a") as file:
    file.write(str("IMDS Defaults:"))
    file.write(str(imdsdefaults))
    file.write(str("\n"))
    file.close()