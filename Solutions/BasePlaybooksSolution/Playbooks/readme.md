# Vendor Product Logic Apps connector and playbook templates

<img src="./logo.png" alt="drawing" width="20%"/><br>

## Table of Contents

1. [Overview](#overview)
1. [Custom Connectors + 3 Playbook templates deployment](#deployall)
1. [Authentication](#importantnotes)
1. [Prerequisites](#prerequisites)
1. [Deployment](#deployment)
1. [Post-Deployment Steps](#postdeployment)
1. [References](#references)
1. [Known issues and limitations](#limitations)

<a name="overview">

# Overview

Vendor Product is ...

<a name="deployall">

## Custom Connectors + 4 Playbook templates deployment

This package includes:

* [Logic Apps custom connector for Vendor Product API](./VendorProductAPIConnector)


* These three playbook templates leverage Vendor Product custom connector:
  * [playbook name](./Playbooks/VendorProduct-playbookname) - short description.

You can choose to deploy the whole package: connectors + all three playbook templates, or each one seperately from its specific folder.

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2FAzure-Sentinel%2Fmaster%2FSolutions%2FBasePlaybooksSolution%2FPlaybooks%2Fazuredeploy.json) [![Deploy to Azure](https://aka.ms/deploytoazuregovbutton)](https://portal.azure.us/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FAzure%2FAzure-Sentinel%2Fmaster%2FSolutions%2FBasePlaybooksSolution%2FPlaybooks%2Fazuredeploy.json)

# Vendor Product connectors documentation 

<a name="authentication">

## Authentication

* API Key authentication

<a name="prerequisites">

### Prerequisites in Vendor Product

To get Vendor Product API credentials, follow the instructions:

1. 1.
2. 2.
3. 3.

<a name="deployment">

### Deployment instructions 

1. To deploy Custom Connectors and Playbooks, click the Deploy to Azure button. This will launch the ARM Template deployment wizard.
2. Fill in the required parameters for deploying Custom Connectors and Playbooks

| Parameters | Description |
|----------------|--------------|
|**For Connector**|
|**parameter name** | short description |
|**For Playbooks**|
|**parameter name** | short description |

<br>
<a name="postdeployment">

### Post-Deployment instructions

#### a. Authorize connections

Once deployment is complete, authorize each connection.

1. Click the Azure Sentinel connection resource
2. Click edit API connection
3. Click Authorize
4. Sign in
5. Click Save
6. Repeat steps for other connections

#### b. Configurations in Sentinel

Each Playbook requires a different type of configuration. Check documentation for each Playbook.

<a name="limitations">

## Known Issues and Limitations
