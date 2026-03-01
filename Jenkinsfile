pipeline {
    agent any

    environment {
        STACK_NAME = "todo-list-aws-production"
    }

    stages {

        stage('Get Code') {
            steps {
                git branch: 'master', 
                    url: 'https://github.com/mmuniz-unir/todo-list-aws.git'
            }
        }

        stage('Deploy Production') {
            steps {
                sh '''
                    echo "=== SAM Build ==="
                    sam build

                    echo "=== SAM Validate ==="
                    sam validate

                    echo "=== Deploy to Production ==="
                    sam deploy --config-env production --no-fail-on-empty-changeset
                '''
            }
        }

        stage('Rest Test (Read Only)') {
            steps {
                sh '''
                    echo "=== REST TEST PRODUCTION ==="

                    BASE_URL=$(aws cloudformation describe-stacks \
                        --stack-name $STACK_NAME \
                        --query "Stacks[0].Outputs[?OutputKey=='BaseUrlApi'].OutputValue" \
                        --output text)

                    echo "API Base URL: $BASE_URL"

                    export BASE_URL

                    python3 -m pytest test/integration/todoApiTest.py \
                        -m readonly \
                        --maxfail=1 \
                        --disable-warnings
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning workspace...'
            cleanWs()
        }
    }
}