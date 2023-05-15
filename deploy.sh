#!/bin/bash

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "|     CSSE6440 CLOUD INFRA ASSIGNMENT     |"
echo "|          Shaoming Teng, 44660145        |"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "> Before begin to depoly, please make sure the following requirements are met:"
echo -e "> Please make sure \033[1m\033[31mPython3.10\033[0m, Python library \033[1m\033[31mpsycopg2\033[0m and \033[1m\033[31mDocker\033[0m are installed on local machine, they are used to upload init data to database."
echo ""
#read -p "Press any key to continue... " -n1 -s
echo ""
echo "Continuing..."
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "> Zip lambda function"
cd ./lambda_hamilton || exit
# zip folder bin and psycopg2 and file lambda_function to lambda_function.zip
zip -r lambda_function_payload.zip bin/ psycopg2/ lambda_function.py
cd ..
echo "> Generated lambda_hamilton/lambda_function_payload.zip"
echo "Copying credential file to terraform"
cp ./credentials ./terraform/credentials || exit
echo "chdir to terraform folder"
cd ./terraform || exit
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "> Begin deploying..."
terraform apply -var-file="secret.tfvars" -auto-approve
echo "Deploying Done."
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "Fetching API URL..."
API_URL=$(terraform output -raw api_url)
echo "API URL: $API_URL"
# Build a file called api.txt which the URL in it
echo "$API_URL" > ../api.txt
cd ..
# sleep 30 seconds
echo "Sleeping for 30 seconds... wait for everything is set up on cloud"
sleep 30
echo "Deploying Done."
