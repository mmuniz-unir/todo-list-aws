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
                
                flake8 src || true
                
                '''

                }
        }

            stage ('Bandit') {
            
                steps {
                
                unstash 'code'
                
                sh '''
                
                bandit -r src -f txt || true
                
                '''
                    
                }
        }        
        
        }
    }
        stage('Deploy') {
            
            steps {



            }
        }
            
        stage('Rest Test') {
            
            steps {



            }
        }

        stage('Promote') {
            
            steps {



            }
        }
    }    
}    