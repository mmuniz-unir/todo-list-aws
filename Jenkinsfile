pipeline {
    agent any

    options { skipDefaultCheckout() }

     stages {
     
        stage('Get Code') {
            
            steps {
                // Obtener código del repo
                
                git branch: 'develop',
                url: 'https://github.com/mmuniz-unir/todo-list-aws.git'
                stash name:'code', includes:'**'
            }
        }
        
        stage('Static Test') {
        
        
            parallel {
            
            stage ('Flake8') {
            
                steps {
                
                unstash 'code'
                sh '''
                
                flake8 --format=pylint --exit-zero src | tee flake8.out
                
                '''

                }
        }

            stage ('Bandit') {
            
                steps {
                
                unstash name:'code'
                
                sh '''
                
                bandit --exit-zero -r src -f txt | tee bandit.out
                
                '''
                    
                }
        }        
        
        }
    }
        stage('Deploy') {
        
            steps {
                unstash 'code'
                sh '''
                echo "=== SAM Build ==="
                sam build
        
                echo "=== SAM Validate ==="
                sam validate
        
                echo "=== Deploy to Staging ==="
                sam deploy --config-env staging --no-fail-on-empty-changeset
                '''
            }
        }
        
            
        stage('Rest Test') {
            steps {
                unstash 'code'
                sh '''
                echo "=== Rest Test Stage (Pytest) ==="
        
                # Obtener URL de la API desde CloudFormation
                BASE_URL=$(aws cloudformation describe-stacks \
                    --stack-name staging-todo-list-aws \
                    --query "Stacks[0].Outputs[?OutputKey=='BaseUrlApi'].OutputValue" \
                    --output text)
                echo "API Base URL: $BASE_URL"
        
                # Exportamos la variable para Pytest
                export BASE_URL
        
                # Ejecutamos las pruebas de integración con Pytest
                python3 -m pytest test/integration/todoApiTest.py --maxfail=1 --disable-warnings
                '''
            }
        }

        stage('Promote') {
            
            steps {

                echo "=== Promote Stage ==="
        
                withCredentials([usernamePassword(
                    credentialsId: 'github-token', 
                    usernameVariable: 'GIT_USER', 
                    passwordVariable: 'GIT_TOKEN'
                )]) {
                    sh '''
                        git config --global user.name "Marc Muñiz"
                        git config --global user.email "marcmusuau@gmail.com"
        
                        git checkout master
        
                        # Mantener Jenkinsfile de master
                        git checkout master -- Jenkinsfile
        
                        git merge develop --no-ff -m "Promote to master"
        
                        # Restaurar Jenkinsfile de master por si el merge lo tocó
                        git checkout HEAD -- Jenkinsfile
        
                        git remote set-url origin https://${GIT_TOKEN}@github.com/mmuniz-unir/todo-list-aws.git
                        git push origin master
                    '''
            
            }
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