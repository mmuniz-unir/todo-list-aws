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
                set -e  # Abortar en el primer error
                echo "=== Rest Test Stage ==="
        
                # Obtener URL del API desde CloudFormation
                API_URL=$(aws cloudformation describe-stacks \
                    --stack-name staging-todo-list-aws \
                    --query "Stacks[0].Outputs[?OutputKey=='CreateTodoApi'].OutputValue" \
                    --output text)
                echo "API URL: $API_URL"
        
                # 1️⃣ Crear un nuevo To-Do
                RESPONSE=$(curl -s -w "%{http_code}" -o create.json -X POST \
                    -H "Content-Type: application/json" \
                    -d '{ "text": "Learn Serverless" }' \
                    $API_URL)
                HTTP_CODE=${RESPONSE: -3}
                if [ "$HTTP_CODE" != "200" ]; then
                    echo "POST /todos failed with HTTP $HTTP_CODE"
                    exit 1
                fi
        
                TODO_ID=$(jq -r '.id' create.json)
                echo "Created To-Do ID: $TODO_ID"
        
                # 2️⃣ Listar todos los To-Do
                RESPONSE=$(curl -s -o list.json -w "%{http_code}" $API_URL)
                HTTP_CODE=${RESPONSE: -3}
                if [ "$HTTP_CODE" != "200" ]; then
                    echo "GET /todos failed with HTTP $HTTP_CODE"
                    exit 1
                fi
        
                # 3️⃣ Obtener el To-Do por ID
                RESPONSE=$(curl -s -o get.json -w "%{http_code}" "$API_URL$TODO_ID")
                HTTP_CODE=${RESPONSE: -3}
                if [ "$HTTP_CODE" != "200" ]; then
                    echo "GET /todos/$TODO_ID failed with HTTP $HTTP_CODE"
                    exit 1
                fi
        
                # 4️⃣ Actualizar el To-Do
                RESPONSE=$(curl -s -o update.json -w "%{http_code}" -X PUT \
                    -H "Content-Type: application/json" \
                    -d '{ "text": "Learn Python and more", "checked": true }' \
                    "$API_URL$TODO_ID")
                HTTP_CODE=${RESPONSE: -3}
                if [ "$HTTP_CODE" != "200" ]; then
                    echo "PUT /todos/$TODO_ID failed with HTTP $HTTP_CODE"
                    exit 1
                fi
        
                # 5️⃣ Borrar el To-Do
                RESPONSE=$(curl -s -o delete.json -w "%{http_code}" -X DELETE "$API_URL$TODO_ID")
                HTTP_CODE=${RESPONSE: -3}
                if [ "$HTTP_CODE" != "200" ]; then
                    echo "DELETE /todos/$TODO_ID failed with HTTP $HTTP_CODE"
                    exit 1
                fi
        
                echo "All REST tests passed ✅"
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