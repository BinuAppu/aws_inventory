import boto3

accesskey = 'INPUTYOURACCESSKEYHERE'
secretkey = 'INPUTYOURSECRETKEYHERETOACCESSAWSENVIRONMENT'

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


# ==========================================
#print ("[+] Working on listing VPCs")
# connect = session.client("ec2",region_name='us-east-1')
#fetechvpcs = connect.describe_vpcs()

#for vpc in fetechvpcs["Vpcs"]:
    # print(vpc["CidrBlock"])
    #print(vpc)
#print (" ")


#print(bcolors.OKGREEN + f"[+] List all regions for the Environment" + bcolors.ENDC)
print ("[+] Working on Route VPC's")
regions = connect.describe_regions()
for region in regions["Regions"]:
    regionName = region["RegionName"]
    vpcregionwise = session.client("ec2",region_name=regionName)
    fetchvpcfromregion = vpcregionwise.describe_vpcs()
    print(bcolors.OKBLUE + f"[+] Printing VPCs for Region {regionName}" + bcolors.ENDC)
    for vpcinregion in fetchvpcfromregion["Vpcs"]:
        print(vpcinregion)

print ("[+] Working on Subnets")
regions = connect.describe_regions()
for region in regions["Regions"]:
    regionName = region["RegionName"]
    try:
        vpcregionwisesub = session.client("ec2",region_name=regionName)
        regsubnets = vpcregionwisesub.describe_subnets()
        print(bcolors.OKGREEN + f"[+] Printing Subnets for Region {regionName}" + bcolors.ENDC)
        for subnets in regsubnets["Subnets"]:
            print(subnets)
    except:
        pass
        # print(f"No Subnets found in Region : {regionName} or Access Denied !")
        

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
            print(routes)
    except:
        pass
        # print(f"No Route Tables found in Region : {regionName} or Access Denied !")
        

print ("[+] Working on listing S3 Buckets")


for region in regions["Regions"]:
    buckets3 = ""
    bucket = ""
    regionName = region["RegionName"]
    try:
        connect = session.client("s3",region_name=regionName,)
        buckets3 = connect.list_buckets()
        print(bcolors.OKGREEN + f"[+] Printing Storage for Region {regionName}" + bcolors.ENDC)
        for bucket in buckets3["Buckets"]:
            eachbucket = bucket
            print(eachbucket)
    except:
        pass
        # print(f"No Storage found in Region : {regionName} or Access Denied !")
