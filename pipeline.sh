#!/bin/sh
# Usage: $ sh ./pipeline.sh project-folder
# Stages
# 1: Get Input (project location to run commands in)
# 2: CD to project folder from provided input
# 3: Check for 'deploy.txt' file, if it does not exist then exit
# 4: If 'deploy.txt does exist, then read it to get deployment config
# 5: If language is included, then run security scan tool and linters, else fail
# 6: If method is included, then prepare for deployment
# 7: If everything is good, then deploy project

# Stage 1
echo "------------------------------------------------------------------"
echo "---------------------------- Stage 1 -----------------------------"
echo "-------- Get Input (Project Location To Run Commands In) ---------"
echo "------------------------------------------------------------------"
if [ "$1" ]; then
  PROJECT=$1
else
  echo "Usage: $ sh ./pipeline.sh project-folder"
  exit 0
fi
if [ -d "$PROJECT" ]; then
  echo "Beginning deployment of $PROJECT project . . . "
else
  echo "ERROR! $PROJECT is not a directory"
  exit 0
fi

# Stage 2
echo "------------------------------------------------------------------"
echo "---------------------------- Stage 2 -----------------------------"
echo "------------ CD To Project Folder From Provided Input ------------"
echo "------------------------------------------------------------------"
cd "$PROJECT"

# Stage 3
echo "------------------------------------------------------------------"
echo "---------------------------- Stage 3 -----------------------------"
echo "------------------ Check For 'deploy.txt' File -------------------"
echo "------------------------------------------------------------------"
if [ -f "deploy.json" ]; then
  echo "Loading deploy.txt configurations . . . "
else
  echo "ERROR! $PROJECT project is missing deploy.json file"
  exit 0
fi

# Stage 4
echo "------------------------------------------------------------------"
echo "---------------------------- Stage 4 -----------------------------"
echo "----------- Read deploy.json To Get Deployment Config ------------"
echo "------------------------------------------------------------------"
METHOD=$(jq '.method' deploy.json)
LANGUAGE=$(jq '.language' deploy.json)

# Stage 5
echo "------------------------------------------------------------------"
echo "---------------------------- Stage 5 -----------------------------"
echo "----------------- Run Security Tools And Linters -----------------"
echo "------------------------------------------------------------------"
if [ "$LANGUAGE" == 'python' ]; then
  SOURCE_FILE=$(jq '.source_file' deploy.json)
  if [ -d "$SOURCE_FILE" ]; then
    bandit -v -r "$SOURCE_FILE"
  else
    bandit -v "$SOURCE_FILE"
  fi
fi

# Stage 6
echo "------------------------------------------------------------------"
echo "---------------------------- Stage 6 -----------------------------"
echo "--------------------- Deployment Preparation ---------------------"
echo "------------------------------------------------------------------"
if "$METHOD" == "terraform"; then
  # Terraform needs the lambda package to be zipped
  python3 file-zip.py -i "$SOURCE_FILE" -d
  # Initialize Terraform
  terraform init .
  # Validate the Terraform code
  terraform validate .
elif "$METHOD" == "serverless"; then
  serverless info
fi

# Stage 7
echo "------------------------------------------------------------------"
echo "---------------------------- Stage 7 -----------------------------"
echo "----------------------- Deploy Application -----------------------"
echo "------------------------------------------------------------------"
if "$METHOD" == "terraform"; then
  # Deploy Terraform code
  terraform apply --auto-approve
elif "$METHOD" == "serverless"; then
  # Deploy Serverless code
  serverless deploy --verbose
fi

echo "------------------------------------------------------------------"
echo "------------------------------------------------------------------"
exit 0