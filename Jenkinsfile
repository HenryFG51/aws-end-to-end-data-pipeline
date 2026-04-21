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
                        env.STACK_NAME = 'data-platform-dev'
                        env.PARAM_FILE = 'iac/parameters/dev.json'
                    } else if (env.BRANCH_NAME == 'tst') {
                        env.AWS_CREDENTIALS_ID = 'aws-creds-tst'
                        env.STACK_NAME = 'data-platform-tst'
                        env.PARAM_FILE = 'iac/parameters/tst.json'
                    } else if (env.BRANCH_NAME == 'prd') {
                        env.AWS_CREDENTIALS_ID = 'aws-creds-prd'
                        env.STACK_NAME = 'data-platform-prd'
                        env.PARAM_FILE = 'iac/parameters/prd.json'
                    } else {
                        error("Branch no soportada para despliegue: ${env.BRANCH_NAME}")
                    }
                }
            }
        }

        stage('Validate Python Syntax') {
            steps {
                sh '''
                    find src -name "*.py" -exec python3 -m py_compile {} \\;
                '''
            }
        }

        stage('Validate AWS Identity') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${env.AWS_CREDENTIALS_ID}"
                ]]) {
                    sh '''
                        export AWS_DEFAULT_REGION=$AWS_REGION
                        aws sts get-caller-identity
                    '''
                }
            }
        }

        stage('Validate CloudFormation Template') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${env.AWS_CREDENTIALS_ID}"
                ]]) {
                    sh '''
                        export AWS_DEFAULT_REGION=$AWS_REGION
                        aws cloudformation validate-template \
                          --template-body file://iac/templates/data-platform.yaml
                    '''
                }
            }
        }

        stage('Deploy Stack') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${env.AWS_CREDENTIALS_ID}"
                ]]) {
                    sh '''
                        export AWS_DEFAULT_REGION=$AWS_REGION
                        aws cloudformation deploy \
                          --template-file iac/templates/data-platform.yaml \
                          --stack-name $STACK_NAME \
                          --capabilities CAPABILITY_NAMED_IAM
                    '''
                }
            }
        }
    }

    post {
        failure {
            echo 'Pipeline falló. Revisar logs.'
        }
        success {
            echo "Pipeline ejecutado correctamente para ${env.BRANCH_NAME}"
        }
    }
}