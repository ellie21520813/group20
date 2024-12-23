pipeline {
  agent any

  tools {
      jdk 'jdk-17'
  }

  environment {
      HARBOR_REGISTRY = 'harbor.example.com'
      SCANNER_HOME= tool 'sonarqube-t3'
      SONAR_URL= ""
      DOCKER_COMPOSE_FILE = 'docker-compose.yml'
      SERVICES = ['auth-service', 'camera-service', 'device-service', 'file-service', 'task-service', 'user-service', 'ui']
      HARBOR_USERNAME =
      HARBOR_PASSWORD =

  }
  stages {
    stage('Checkout') {
      steps {
        sh 'echo passed checkout'
        git branch: 'main', changelog: false, poll: false, url: 'https://github.com/ellie21520813/group20'
      }
    }

    stage('login harbor') {
        steps {
            echo 'Login to Harbor registry'
            sh" docker login ${HARBOR_REGISTRY} -u ${HARBOR_USERNAME} -p ${HARBOR_PASSWORD}"
        }
    }

    stage('Static Code Analysis') {
        steps {
            script {
                for (service in SERVICES) {
                    echo "Running SonarQube analysis for ${service}"
                    def sourceDir = (service == 'ui') ? 'src' : 'app'
                        dir("${service}") {
                            withSonarQubeEnv('SonarQube') {
                                sh 'sonar-scanner
                                    -Dsonar.projectKey=${service}
                                    -Dsonar.sources= ${sourceDir}
                                    -Dsonar.host.url=${SONAR_URL}'
                            }
                        }
                    }
                }
            }
        }
    }

    stage('Build and Push Docker Images') {
        steps {
            script {
                for (service in SERVICES) {
                    echo "Building and pushing Docker image for ${service}"
                    sh "docker-compose build ${service}"
                    sh "docker tag ${service}:latest ${HARBOR_REGISTRY}/${service}:${IMAGE_TAG}"
                    sh "docker push ${HARBOR_REGISTRY}/${service}:${IMAGE_TAG}"
                }
            }
        }
    }

    stage('scan with trivy') {
        steps {
            script {
                for (service in SERVICES) {
                    echo "Trivy Security Scan for ${service}"
                    sh "trivy --severity HIGH,CRITICAL --no-progress image --format json -o ${service}-trivy-report.json ${HARBOR_REGISTRY}/${service}:${IMAGE_TAG}"
                }
            }
        }
    }
  }
}


