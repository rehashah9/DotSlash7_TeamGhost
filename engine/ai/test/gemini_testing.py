import google.generativeai as genai

genai.configure(api_key="AIzaSyAZzGyJ9DlHZYjmTJHR33FkmN09LU0W8-Q")

# Set up the model
generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

prompt_parts = [
  """
You are a helpful AI assistant expert in querying SQL Database to find sql query of user query in normal english.

Your Job:
1) You are expert in creating SQL Query for Postgres. Based on user query, create a SQL Query to fetch data from Postgres DB.
2) Your job is to convert TEXT to SQL Query.
3) Your job is to only give SQL Query. You don't need to execute it. We will execute it on our end. So please make sure that your SQL Query is correct. 
4) Your job is to only give one sql query. dont write any other text or information.
5) You can also add joins between two tables based for columns names. For example, if user query is "List of EC2 instances provisioned with undesired instance type", then you can add join between aws_ec2_instance and aws_ec2_instance_metric_cpu_utilization table based on column name "instance_id" and "instance_id" respectively.

About EC2 Instances in AWS:
The AWS EC2 Instance is a virtual server in Amazon's Elastic Compute Cloud (EC2) for running applications on the Amazon Web Services (AWS) infrastructure. It provides scalable computing capacity in the AWS cloud, eliminating the need to invest in hardware up front, so you can develop and deploy applications faster. With EC2, you can launch as many or as few virtual servers as you need, configure security and networking, and manage storage.

Instructions to Create SQL Query:
1) Here are the Table names based on EC2 instances and their corresponding column name, its datatype and the description about the columns.
2) Make sure you understand the column descriptions to create SQL query that is meant to solve User Query
3) You can use any SQL Query to solve the user query. You can use joins, subqueries, etc. to solve the user query.
4) Dont write any other text or information. Just write SQL Query.
5) Dont cast any column to any other datatype or use BIGNUMERIC. Use the datatype as it is.
6) Give SQL Query in lowercase.
""",
  """
  Amazon EC2 Tables:

1) Table: aws_ec2_instance - Query AWS EC2 Instances using SQL#
Table Usage Guide:
The aws_ec2_instance table in Steampipe provides you with information about EC2 Instances within AWS Elastic Compute Cloud (EC2). This table allows you, as a DevOps engineer, to query instance-specific details, including instance state, launch time, instance type, and associated metadata. You can utilize this table to gather insights on instances, such as instances with specific tags, instances in a specific state, instances of a specific type, and more. The schema outlines the various attributes of the EC2 instance for you, including the instance ID, instance state, instance type, and associated tags.


Schema for aws_ec2_instance:

Name	Type	Operators	Description
_ctx	jsonb		Steampipe context in JSON form, e.g. connection_name.
account_id	text		The AWS Account ID in which the resource is located.
akas	jsonb		Array of globally unique identifier strings (also known as) for the resource.
ami_launch_index	bigint		The AMI launch index, which can be used to find this instance in the launch group.
architecture	text		The architecture of the image.
arn	text		The Amazon Resource Name (ARN) specifying the instance.
block_device_mappings	jsonb		Block device mapping entries for the instance.
boot_mode	text		The boot mode of the instance.
capacity_reservation_id	text		The ID of the Capacity Reservation.
capacity_reservation_specification	jsonb		Information about the Capacity Reservation targeting option.
client_token	text		The idempotency token you provided when you launched the instance, if applicable.
cpu_options_core_count	bigint		The number of CPU cores for the instance.
cpu_options_threads_per_core	bigint		The number of threads per CPU core.
disable_api_termination	boolean		If the value is true, instance can't be terminated through the Amazon EC2 console, CLI, or API.
ebs_optimized	boolean		Indicates whether the instance is optimized for Amazon EBS I/O. This optimization provides dedicated throughput to Amazon EBS and an optimized configuration stack to provide optimal I/O performance. This optimization isn't available with all instance types.
elastic_gpu_associations	jsonb		The Elastic GPU associated with the instance.
elastic_inference_accelerator_associations	jsonb		The elastic inference accelerator associated with the instance.
ena_support	boolean		Specifies whether enhanced networking with ENA is enabled.
enclave_options	jsonb		Indicates whether the instance is enabled for Amazon Web Services Nitro Enclaves.
hibernation_options	jsonb		Indicates whether the instance is enabled for hibernation.
hypervisor	text	=	The hypervisor type of the instance. The value xen is used for both Xen and Nitro hypervisors.
iam_instance_profile_arn	text	=	The Amazon Resource Name (ARN) of IAM instance profile associated with the instance, if applicable.
iam_instance_profile_id	text		The ID of the instance profile associated with the instance, if applicable.
image_id	text	=	The ID of the AMI used to launch the instance.
instance_id	text	=	The ID of the instance.
instance_initiated_shutdown_behavior	text		Indicates whether an instance stops or terminates when you initiate shutdown from the instance (using the operating system command for system shutdown).
instance_lifecycle	text	=	Indicates whether this is a spot instance or a scheduled instance.
instance_state	text	=	The state of the instance (pending | running | shutting-down | terminated | stopping | stopped).
instance_status	jsonb		The status of an instance. Instance status includes scheduled events, status checks and instance state information.
instance_type	text	=	The instance type.
kernel_id	text		The kernel ID
key_name	text		The name of the key pair, if this instance was launched with an associated key pair.
launch_template_data	jsonb		The configuration data of the specified instance.
launch_time	timestamp with time zone		The time the instance was launched.
licenses	jsonb		The license configurations for the instance.
maintenance_options	jsonb		The metadata options for the instance.
metadata_options	jsonb		The metadata options for the instance.
monitoring_state	text	=	Indicates whether detailed monitoring is enabled (disabled | enabled).
network_interfaces	jsonb		The network interfaces for the instance.
outpost_arn	text	=	The Amazon Resource Name (ARN) of the Outpost, if applicable.
partition	text		The AWS partition in which the resource is located (aws, aws-cn, or aws-us-gov).
placement_affinity	text		The affinity setting for the instance on the Dedicated Host.
placement_availability_zone	text	=	The Availability Zone of the instance.
placement_group_id	text		The ID of the placement group that the instance is in.
placement_group_name	text	=	The name of the placement group the instance is in.
placement_host_id	text		The ID of the Dedicated Host on which the instance resides.
placement_host_resource_group_arn	text		The ARN of the host resource group in which to launch the instances.
placement_partition_number	bigint		The ARN of the host resource group in which to launch the instances.
placement_tenancy	text	=	The tenancy of the instance (if the instance is running in a VPC). An instance with a tenancy of dedicated runs on single-tenant hardware.
platform	text		The value is 'Windows' for Windows instances; otherwise blank.
platform_details	text		The platform details value for the instance.
private_dns_name	text		The private DNS hostname name assigned to the instance. This DNS hostname can only be used inside the Amazon EC2 network. This name is not available until the instance enters the running state.
private_dns_name_options	jsonb		The options for the instance hostname.
private_ip_address	inet		The private IPv4 address assigned to the instance.
product_codes	jsonb		The product codes attached to this instance, if applicable.
public_dns_name	text	=	The public DNS name assigned to the instance. This name is not available until the instance enters the running state.
public_ip_address	inet		The public IPv4 address, or the Carrier IP address assigned to the instance, if applicable.
ram_disk_id	text	=	The RAM disk ID.
region	text		The AWS Region in which the resource is located.
root_device_name	text	=	The device name of the root device volume (for example, /dev/sda1).
root_device_type	text	=	The root device type used by the AMI. The AMI can use an EBS volume or an instance store volume.
security_groups	jsonb		The security groups for the instance.
source_dest_check	boolean		Specifies whether to enable an instance launched in a VPC to perform NAT. This controls whether source/destination checking is enabled on the instance.
spot_instance_request_id	text		If the request is a Spot Instance request, the ID of the request.
sriov_net_support	text		Indicates whether enhanced networking with the Intel 82599 Virtual Function interface is enabled.
state_code	bigint		The reason code for the state change.
state_transition_reason	text		The reason for the most recent state transition.
state_transition_time	timestamp with time zone		The date and time, the instance state was last modified.
subnet_id	text	=	The ID of the subnet in which the instance is running.
tags	jsonb		A map of tags for the resource.
tags_src	jsonb		A list of tags assigned to the instance.
title	text		Title of the resource.
tpm_support	text		If the instance is configured for NitroTPM support, the value is v2.0.
usage_operation	text		The usage operation value for the instance.
usage_operation_update_time	text		The time that the usage operation was last updated.
user_data	text		The user data of the instance.
virtualization_type	text	=	The virtualization type of the instance.
vpc_id	text	=	The ID of the VPC in which the instance is running.
""",
"How many EC2 instances are running?"
]

response = model.generate_content(prompt_parts)
print(response.text)