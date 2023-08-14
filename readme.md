# FHIR Server

The FHIR Server is a RESTful web service that uses the HL7 FHIR standard to provide a FHIR interface for data stored in the database.


## Clone Project
Using GitHub, clone the project. 
```bash
Git clone https://github.com/kryonknowledgeworks/kryon-fire.git

```
## Project setup
Download and install PyCharm.

```bash
https://www.jetbrains.com/pycharm/download/#section=windows
```
Go to the project directory
```bash
cd kryon-fire
```
## Install dependencies
Install required libraries
```bash
pip install -r requirements.txt
```
## Environment  variables

#### Required items

| Parameter             | Type      | Description                         |
|:----------------------|:----------|:------------------------------------|
| `database`            | `string`  | **Required**. MongoDB Database Name |
| `host`                | `string`  | **Required**. MongoDB host name     |
| `username`            | `string`  | **Required**. MongoDB username      |
| `password`            | `string`  | **Required**. MongoDB password      |
| `port`                | `integer` | **Required**. MongoDB port          |

## Run locally

Run command
```bash
python app.py
```