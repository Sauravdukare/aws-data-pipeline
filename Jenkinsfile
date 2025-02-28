pipeline {
    agent any

    environment {
        AWS_REGION = "us-east-1"
        AWS_ACCOUNT_ID = "<your-aws-account-id>"
        ECR_REPO_NAME = "aws-data-pipeline"
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                script {
                    echo "Cloning the repository..."
                    checkout scm
                }
            }
        }

        stage('Setup Terraform') {
            steps {
                script {
                    echo "Initializing Terraform..."
                    sh '''
                        terraform init
                        terraform validate
                        terraform plan -out=tfplan
                    '''
                }
            }
        }

        stage('Apply Terraform') {
            steps {
                script {
                    echo "Applying Terraform..."
                    sh '''
                        terraform apply -auto-approve
                    '''
                }
            }
        }

        stage('Login to AWS ECR') {
            steps {
                script {
                    echo "Logging in to AWS ECR..."
                    sh '''
                        aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    sh '''
                        docker build -t $ECR_REPO_NAME:$IMAGE_TAG .
                    '''
                }
            }
        }

        stage('Tag & Push Image to ECR') {
            steps {
                script {
                    echo "Tagging and pushing Docker image..."
                    sh '''
                        docker tag $ECR_REPO_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:$IMAGE_TAG
                        docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Update Lambda Function') {
            steps {
                script {
                    echo "Deploying image to AWS Lambda..."
                    sh '''
                        aws lambda update-function-code \
                        --function-name aws-data-pipeline-lambda \
                        --image-uri $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Test Lambda Function') {
            steps {
                script {
                    echo "Testing AWS Lambda function..."
                    sh '''
                        aws lambda invoke --function-name aws-data-pipeline-lambda output.json
                        cat output.json
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                echo "Pipeline execution complete!"
            }
        }
    }
}
