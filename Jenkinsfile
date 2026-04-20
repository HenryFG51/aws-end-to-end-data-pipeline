stage('Validate CloudFormation Template') {
    steps {
        withCredentials([[
            $class: 'AmazonWebServicesCredentialsBinding',
            credentialsId: 'aws-creds-dev'
        ]]) {
            sh '''
                export AWS_DEFAULT_REGION=$AWS_REGION
                aws sts get-caller-identity
                aws cloudformation validate-template --template-body file://iac/templates/data-platform.yaml
            '''
        }
    }
}