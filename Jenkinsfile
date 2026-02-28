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
                
                unstash name:'code'
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
            
            sh'''
            echo 'Hola'
            '''

            }
        }

        stage('Promote') {
            
            steps {

            sh'''
            echo 'Hola'
            '''

            }
        }
    }    
}    