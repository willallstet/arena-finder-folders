DocumentationAWS Research and Engineering StudioUser GuideArchitecture diagramAWS services in this productArchitecture overviewThis section provides an architecture diagram for the components deployed with this
product.
Architecture diagram
Deploying this product with the default parameters deploys the following components in
your AWS account.
Figure 1: Research and Engineering Studio on AWS architecture
NoteAWS CloudFormation resources are created from AWS Cloud Development Kit (AWS CDK) constructs.
The high-level process flow for the product components deployed with the AWS CloudFormation
template is as follows:
RES installs components for the web portal as well as:
Engineering Virtual Desktop (eVDI) component for interactive workloads
Metrics component
Amazon CloudWatch receives metrics from the eVDI components.
Bastion Host component
Administrators may use SSH to connect to the bastion host component to manage the
underlying infrastructure.
RES installs components in private subnets behind a NAT gateway.
Administrators access the private subnets via the Application Load Balancer (ALB) or the
Bastion Host component.
Amazon DynamoDB stores the environment configuration.
AWS Certificate Manager (ACM) generates and stores a public certificate for the
Application Load Balancer (ALB).
NoteWe recommend using AWS Certificate Manager to generate a trusted certificate for your domain.
Amazon Elastic File System (EFS) hosts the default /home file system mounted on
all applicable infrastructure hosts and eVDI Linux sessions.
RES uses Amazon Cognito to create an initial bootstrap user called 'clusteradmin' within and
sends temporary credentials to the email address provided during installation. The
'clusteradmin' must change the password the first time they login.
Amazon Cognito integrates with your organization's Active Directory and user identities for
permissions management.
Security zones allow administrators to restrict access to specific components within
the product based on permissions.
AWS services in this product
AWS service
Type
Description
Amazon Elastic Compute Cloud
Core
Provides the underlying compute services to create virtual desktops with
their chosen operating system and software stack.
Elastic Load Balancing
Core
Bastion, cluster-manager, and VDI hosts are created in Auto Scaling groups
behind the load balancer. ELB balances traffic from the web portal across RES
hosts.
Amazon Virtual Private Cloud
Core
All core product components are created within your VPC.
Amazon Cognito
Core
Manages user identities and authentication. Active Directory users are mapped
to Amazon Cognito users and groups to authenticate access levels.
Amazon Elastic File System
Core
Provides the /home file system for the file browser and
VDI hosts, as well as shared external file systems.
Amazon DynamoDB
Core
Stores configuration data such as users, groups, projects, file systems,
and component settings.
AWS Systems Manager
Core
Stores documents for performing commands for VDI session management.
AWS Lambda
Core
Supports product functionalities such as updating settings within the DynamoDB
table, starting Active Directory sync workflows, and updating the prefix list.
Amazon CloudWatch
Supporting
Provides metrics and activity logs for all Amazon EC2 hosts and Lambda functions.
Amazon Simple Storage Service
Supporting
Stores application binaries for host bootstrapping and configuration.
AWS Key Management Service
Supporting
Used for encryption at rest with Amazon SQS queues, DynamoDB tables, and Amazon SNS
topics.
AWS Secrets Manager
Supporting
Stores service account credentials in Active Directory and self-signed
certificates for VDIs.
AWS CloudFormation
Supporting
Provides a deployment mechanism for the product.
AWS Identity and Access Management
Supporting
Restricts the access level for hosts.
Amazon Route 53
Supporting
Creates private hosted zone for resolving the internal load balancer and
the bastion host domain name.
Amazon Simple Queue Service
Supporting
Creates task queues to support asynchronous executions.
Amazon Simple Notification Service
Supporting
Supports the publication-subscriber model between VDI components such
as the controller and hosts.
AWS Fargate
Supporting
Installs, updates, and deletes environments using Fargate tasks.
Amazon FSx File Gateway
Optional
Provides external shared file system.
Amazon FSx for NetApp ONTAP
Optional
Provides external shared file system.
AWS Certificate Manager
Optional
Generates a trusted certificate for your custom domain.
AWS Backup
Optional
Offers backup capabilities for Amazon EC2 hosts, file systems, and DynamoDB.
Javascript is disabled or is unavailable in your browser.To use the Amazon Web Services Documentation, Javascript must be enabled. Please refer to your browser's Help pages for instructions.Document ConventionsConcepts and definitionsDemo environment Did this page help you? - YesThanks for letting us know we're doing a good job!If you've got a moment, please tell us what we did right so we can do more of it.Did this page help you? - NoThanks for letting us know this page needs work. We're sorry we let you down.If you've got a moment, please tell us how we can make the documentation better.