import boto3
import csv
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

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


#print(bcolors.OKGREEN + f"[+] List all regions for the Environment" + bcolors.ENDC)
print ("[+] Working on Route VPC's")
head="OwnerId,AssociationId,CidrBlock,InstanceTenancy,IsDefault,BlockPublicAccessStates,VpcId,State,CidrBlock,DhcpOptionsId \n"
with open("vpc_report.csv",'w') as headfile:
        headfile.write(str(head))
        headfile.close()
regions = connect.describe_regions()
combineval = []
for region in regions["Regions"]:
    regionName = region["RegionName"]
    try:
        vpcregionwise = session.client("ec2",region_name=regionName)
        fetchvpcfromregion = vpcregionwise.describe_vpcs()
        print(bcolors.OKBLUE + f"[+] Printing VPCs for Region {regionName}" + bcolors.ENDC)
        for vpcinregion in fetchvpcfromregion["Vpcs"]:
            print(vpcinregion['OwnerId'],",",vpcinregion['CidrBlockAssociationSet'],",",vpcinregion['InstanceTenancy'],",",vpcinregion['IsDefault'],",",vpcinregion['BlockPublicAccessStates'],",",vpcinregion['VpcId'],",",vpcinregion['State'],",",vpcinregion['CidrBlock'],",",vpcinregion['DhcpOptionsId'])
            print(vpcinregion['BlockPublicAccessStates']['InternetGatewayBlockMode'])
            writeCsv = str(vpcinregion['OwnerId'])+","+(vpcinregion['CidrBlockAssociationSet'][0]['AssociationId'])+","+(vpcinregion['CidrBlockAssociationSet'][0]['CidrBlock'])+","+str(vpcinregion['InstanceTenancy'])+","+str(vpcinregion['IsDefault'])+","+str(vpcinregion['BlockPublicAccessStates']['InternetGatewayBlockMode'])+","+str(vpcinregion['VpcId'])+","+str(vpcinregion['State'])+","+str(vpcinregion['CidrBlock'])+","+str(vpcinregion['DhcpOptionsId'])
            
            with open("vpc_report.csv",'a') as addfiles:
                writeval = writeCsv
                addfiles.write(writeval)
                addfiles.write('\n')
                addfiles.close()
    except:
        pass


print ("[+] Working on Subnets")
regions = connect.describe_regions()
head = "AvailabilityZoneId,OwnerId,SubnetArn,SubnetId,State,VpcId,CidrBlock,AvailableIpAddressCount,AvailabilityZone \n"
with open("subnets_report.csv",'w') as headfile:
        headfile.write(str(head))
        headfile.close()
for region in regions["Regions"]:
    regionName = region["RegionName"]
    try:
        vpcregionwisesub = session.client("ec2",region_name=regionName)
        regsubnets = vpcregionwisesub.describe_subnets()
        print(bcolors.OKGREEN + f"[+] Printing Subnets for Region {regionName}" + bcolors.ENDC)
        for subnets in regsubnets["Subnets"]:
            print(subnets['AvailabilityZoneId'] , "," , subnets['OwnerId'] , "," , subnets['SubnetArn'] , "," , subnets['SubnetId'] , "," , subnets['State'] , "," , subnets['VpcId'] , "," , subnets['CidrBlock'] , "," , subnets['AvailableIpAddressCount'] , "," , subnets['AvailabilityZone'])            
            subnetval = str(subnets['AvailabilityZoneId']) + "," + str(subnets['OwnerId']) + "," + str(subnets['SubnetArn']) + "," + str(subnets['SubnetId']) + "," + str(subnets['State']) + "," + str(subnets['VpcId']) + "," + str(subnets['CidrBlock']) + "," + str(subnets['AvailableIpAddressCount']) + "," + str(subnets['AvailabilityZone'])
            with open("subnets_report.csv",'a') as subnetsfile:
                subnetsfile.write(subnetval)
                subnetsfile.write('\n')
                subnetsfile.close()
    except:
        pass
        # print(f"No Subnets found in Region : {regionName} or Access Denied !")


print ("[+] Working on Route Tables")
print(bcolors.OKGREEN + f"[+] List all Route Tables for the Environment" + bcolors.ENDC)
headfilesubnet = "RegionName, Is Associations Main ,Associations - RouteTableAssociationId, Associations - RouteTableId,Associations - AssociationState - State,RouteTableId,Routes - DestinationCidrBlock,Routes - GatewayId,Routes - DestinationCidrBlock,Routes - GatewayId,Routes - State,VpcId,OwnerId"
with open("routetables_report.csv",'w') as headfilesub:
        headfilesub.write(str(headfilesubnet))
        headfilesub.write('\n')
        headfilesub.close()

regions = connect.describe_regions()
for region in regions["Regions"]:
    regionName = region["RegionName"]
    try:
        routetables = session.client("ec2",region_name=regionName)
        getroutes = routetables.describe_route_tables()
        print(bcolors.OKGREEN + f"[+] Printing Route Tables for Region {regionName}" + bcolors.ENDC)
        for routes in getroutes["RouteTables"]:
                for route in routes["Routes"]:
                    with open("routetables_report.csv","a") as f:
                        w = csv.writer(f)
                        w.writerow(route.items())
            '''
            print("=======================")
            print(routes['Associations'][0]['Main'],routes['Associations'][0]['RouteTableAssociationId'],routes['Associations'][0]['RouteTableId'],routes['Associations'][0]['AssociationState']['State'],routes['RouteTableId'],routes['Routes'][0]['DestinationCidrBlock'],routes['Routes'][0]['GatewayId'],routes['Routes'][1]['DestinationCidrBlock'],routes['Routes'][1]['GatewayId'],routes['Routes'][1]['State'],routes['VpcId'],routes['OwnerId'])
            routeval = str(regionName) + "," + str(routes['Associations'][0]['Main']) + "," + str(routes['Associations'][0]['RouteTableAssociationId']) + "," + str(routes['Associations'][0]['RouteTableId']) + "," + str(routes['Associations'][0]['AssociationState']['State']) + "," + str(routes['RouteTableId']) + "," + str(routes['Routes'][0]['DestinationCidrBlock']) + "," + str(routes['Routes'][0]['GatewayId']) + "," + str(routes['Routes'][1]['DestinationCidrBlock']) + "," + str(routes['Routes'][1]['GatewayId']) + "," + str(routes['Routes'][1]['State']) + "," + str(routes['VpcId']) + "," + str(routes['OwnerId'])
            with open("routetables_report.csv",'a') as writerouteval:
                print(routeval)
                writerouteval.write(routeval)
                writerouteval.write('\n')
                writerouteval.close()
            '''
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
