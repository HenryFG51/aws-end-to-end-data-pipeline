pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Running branch: ${env.BRANCH_NAME}"
            }
        }

        stage('Set Environment Config') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'dev') {
                        env.AWS_CREDENTIALS_ID = 'aws-creds-dev'
                        env.STACK_NAME = 'data-platform-dev-stack'
                        env.PARAM_FILE = 'iac/parameters/dev.json'
                        env.S3_BUCKET = 'data-platform-dev-main-570435244160'
                        env.SKIP_DEPLOY = 'false'
                    } else if (env.BRANCH_NAME == 'tst') {
                        env.AWS_CREDENTIALS_ID = 'aws-creds-tst'
                        env.STACK_NAME = 'data-platform-tst-stack'
                        env.PARAM_FILE = 'iac/parameters/tst.json'
                        env.S3_BUCKET = 'data-platform-tst-main-614399201520'
                        env.SKIP_DEPLOY = 'false'
                    } else if (env.BRANCH_NAME == 'prd') {
                        env.AWS_CREDENTIALS_ID = 'aws-creds-prd'
                        env.STACK_NAME = 'data-platform-prd-stack'
                        env.PARAM_FILE = 'iac/parameters/prd.json'
                        env.S3_BUCKET = 'data-platform-prd-main-805981941599'
                        env.SKIP_DEPLOY = 'false'
                    } else if (env.BRANCH_NAME == 'main') {
                        env.SKIP_DEPLOY = 'true'
                        echo 'Main branch detected. Validation only, no deployment.'
                    } else {
                        error("Branch no soportada para despliegue: ${env.BRANCH_NAME}")
                    }
                }
            }
        }

        stage('Validate Python Syntax') {
            steps {
                sh '''
                    if [ -d "src" ]; then
                      find src -name "*.py" -exec python3 -m py_compile {} \\;
                    else
                      echo "No src directory found. Skipping Python syntax validation."
                    fi
                '''
            }
        }

        stage('Validate CloudFormation Template') {
            when {
                expression { env.SKIP_DEPLOY != 'true' }
            }
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${env.AWS_CREDENTIALS_ID}"
                ]]) {
                    sh '''
                        export AWS_DEFAULT_REGION=$AWS_REGION
                        aws sts get-caller-identity
                        aws cloudformation validate-template \
                          --template-body file://iac/templates/data-platform.yaml
                    '''
                }
            }
        }

        stage('Deploy Stack') {
            when {
                expression { env.SKIP_DEPLOY != 'true' }
            }
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${env.AWS_CREDENTIALS_ID}"
                ]]) {
                    sh """
                        export AWS_DEFAULT_REGION=$AWS_REGION
                        aws cloudformation deploy \
                          --template-file iac/templates/data-platform.yaml \
                          --stack-name ${env.STACK_NAME} \
                          --parameter-overrides file://${env.PARAM_FILE} \
                          --capabilities CAPABILITY_NAMED_IAM
                    """
                }
            }
        }

        stage('Upload ETL Scripts to S3') {
            when {
                expression { env.SKIP_DEPLOY != 'true' }
            }
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${env.AWS_CREDENTIALS_ID}"
                ]]) {
                    sh """
                        export AWS_DEFAULT_REGION=$AWS_REGION

                        aws s3 cp src/etl/ s3://${env.S3_BUCKET}/data-platform-lab/glue/data-platform-lab-etl/src/etl/ \
                          --recursive \
                          --exclude "*" \
                          --include "*.py"

                        aws s3 cp src/packages/ s3://${env.S3_BUCKET}/data-platform-lab/glue/data-platform-lab-etl/src/packages/ \
                          --recursive 
                          --exclude "__pycache__/*" \
                          --exclude "*.pyc"
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline ejecutado correctamente para la rama ${env.BRANCH_NAME}"
        }
        failure {
            echo 'Pipeline falló. Revisar logs.'
        }
        always {
            cleanWs()
        }
    }
}