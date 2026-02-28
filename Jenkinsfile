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
                
                flake8 --format=pylint --exit-zero src > flake8.out
                
                '''

                }
        }

            stage ('Bandit') {
            
                steps {
                
                unstash name:'code'
                
                sh '''
                
                bandit -r src -f html -o reports/bandit.html || true
                
                '''
                    
                }
        }        
        
        }
    }
        stage('Deploy') {
            
            steps {

            sh'''
            echo 'Hola'
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