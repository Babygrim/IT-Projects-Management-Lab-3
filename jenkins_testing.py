
import jenkins
import json
import os

host = "http://localhost:8090"
username = "pogkopi" #jenkins username here
password = "119396f5f26a03f93f6f5c242db941caac"
server = jenkins.Jenkins(host, username=username, password=password) #automation_user_password

# user = server.get_whoami()
# version = server.get_version()
# print('Hello %s from Jenkins %s' % (user['fullName'], version))



# #Create deployment jobs
# #create a blank job
# server.create_job("job1", jenkins.EMPTY_CONFIG_XML)

#create pre-configured-job
try:
    server.delete_job('job1')
    server.delete_job('job2')
    server.delete_job('lab 3 job')
except jenkins.NotFoundException:
    pass

job1_xml = open("./job_1.xml", mode='r', encoding='utf-8').read()
server.create_job("job1", job1_xml)

# job3_xml = open("job3.xml", mode='r', encoding='utf-8').read()
# server.create_job("job3", job3_xml)

#view jobs
# jobs = server.get_jobs()
# print(jobs)

#copy job
# server.copy_job('job2', 'job4')

#update job
# updated_job_3 = open("job_3_updated.xml", mode='r', encoding='utf-8').read()
# server.reconfig_job('job3', updated_job_3)

#disable job
# server.disable_job('sample_job')

# Run a build and get build number and more info
# server.build_job('job3')
# last_build_number = server.get_job_info('job3')['lastCompletedBuild']['number']
# print("Build Number", last_build_number)
# build_info = server.get_build_info('job3', last_build_number)
# print("build info", build_info)

#delete job
# server.delete_job('sample_job')


# Create View
# view_config = open("jobs_view.xml", mode='r', encoding='utf-8').read()
# server.create_view("Job List", view_config)

#get list of view
# views = server.get_views()
# print(views)

# Update View
# updated_view_config = open("jobs_view_updated.xml", mode='r', encoding='utf-8').read()
# server.reconfig_view("Job List", updated_view_config)

#Delete View
# server.delete_view("Job List")