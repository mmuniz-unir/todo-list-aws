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
                
                flake8 src --format=html --htmldir=reports/flake8 || true
                
                '''

                }
        }

            stage ('Bandit') {
            
                steps {
                
                unstash 'code'
                
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