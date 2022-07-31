# This script gets all vpc peering into a CSV file for mentioned projects. 
# If no project is mentioned, it fetches list of all projects and get their VPC peering.

import subprocess
import os
import time

projects = ["test-project"]
remove_sys_projects = True

VPC_LIST_COMMAND = "gcloud compute networks peerings list --flatten=\"peerings[]\" --format=\"csv(peerings.name:sort=1,peerings.source_network,peerings.source_network,peerings.network,peerings.network)\" --project {0}"
LIST_PROJECTS_COMMAND = "gcloud projects list --format=\"csv(project_id)\""

def get_all_projects():
    projects = subprocess.getoutput(LIST_PROJECTS_COMMAND).split("\n")
    projects.pop(0)
    print(len(projects))
    filtered_projects = []
    if remove_sys_projects == True:
        for project in projects:
            if not project.startswith("sys-"):
                filtered_projects.append(project)
    else:
        filtered_projects = projects
    return filtered_projects

def create_vpc_peering_csv(projects):
    if len(projects) == 0:
        projects = get_all_projects()
    vpc_info ="Peering Name, Source Network, Source Project, Destination Network, Destination Project"
    for project in projects:
        vpc_list = subprocess.getoutput(VPC_LIST_COMMAND.format(project)).split("\n")
        vpc_list.pop(0)
        for vpc_peering in vpc_list:
            row = vpc_peering.split(",")
            row[1] = row[1].split("/networks/")[1]
            row[2] = row[2].split("/projects/")[1].split("/global/networks/")[0]
            row[3] = row[3].split("/networks/")[1]
            row[4] = row[4].split("/projects/")[1].split("/global/networks/")[0]
            vpc_info =  vpc_info + "\n" + ",".join(row)
    timestr = time.strftime("%d-%m-%Y-%H-%M-%S")
    file_name = "vpc_list-{0}.csv".format(timestr)
    writer = open(file_name,"w")
    writer.write(vpc_info)
    writer.close()

create_vpc_peering_csv(projects)
