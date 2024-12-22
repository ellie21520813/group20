pipeline {
  agent any

  tools {
      jdk 'jdk-17'
  }

  environment {
      SCANNER_HOME= tool 'sonarqube-t3'
      SONAR_URL= "http://3.89.57.237:9000"
  }
  stages {
    stage('Checkout') {
      steps {
        sh 'echo passed 1'
        git branch: 'main', changelog: false, poll: false, url: 'https://github.com/ellie21520813/deploywithk8s.git'
      }
    }

    stage('Static Code Analysis') {
        steps {
             sh '''
	            $SCANNER_HOME/bin/sonar-scanner -X \
            		-Dsonar.host.url=${SONAR_URL} \
            		-Dsonar.login=squ_f4cfc4ce9aab476640c53b5680a9e409468c0271 \
            		-Dsonar.projectName=task3\
            		-Dsonar.java.binaries=. \
            		-Dsonar.projectKey=task3 \

            '''
        }
    }
    stage('Docker Build for  be') {
        steps {
            script {
    			withDockerRegistry(credentialsId: '7ed71537-4773-4978-b9a0-79fada9e279d', toolName: 'docker') {
    				sh """
    				    cd backend
    					docker build -t nh6462/lab2_be:latest .
    					docker push nh6462/lab2_be:latest
    					cd .. && cd frontend
    					docker build -t nh6462/lab2_fe:latest .
    					docker push nh6462/lab2_fe:latest
    				"""
                }
            }
        }
    }
    stage('Deploy k8s') {
        steps {
            script {
    			kubeconfig(credentialsId: 'k8server', serverUrl: 'https://192.168.49.2:8443') {
                     echo 'Deploying....'
                        sh 'kubectl apply -f k8s/backend-deployment.yaml -n jenkins'
                        sh 'kubectl apply -f k8s/frontend-deployment.yaml -n jenkins'
                }
            }
        }
    }
  }
}


