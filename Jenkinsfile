pipeline {
  agent any

  tools {
      jdk 'jdk-17'
  }

  environment {
      HARBOR_REGISTRY = 'harbor.example.com'
      SCANNER_HOME= tool 'sonarqube-t3'
      SONAR_URL= ""
      SONAR_TOKEN=""
      DOCKER_COMPOSE_FILE = 'docker-compose.yml'
      SERVICES = ['auth-service', 'camera-service', 'device-service', 'file-service', 'task-service', 'user-service', 'ui']
      HARBOR_USERNAME =
      HARBOR_PASSWORD =
      K8S_MANIFESTS = ['userdb-deployment.yml', 'uiapp-deployment.yml']

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
                    dir("${service}") {
                        sh """
                            ${SCANNER_HOME}/bin/sonar-scanner -X \
                            -Dsonar.host.url=${SONAR_URL} \
                            -Dsonar.login= ${SONAR_TOKEN}\
                            -Dsonar.projectName=${service} \
                            -Dsonar.java.binaries=. \
                            -Dsonar.projectKey=${service}
                        """
                    }
                }
            }
        }
    }


    /*stage('Static Code Analysis') {
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
    */
    stage('Build and Push Docker Images') {
        steps {
            script {
                for (service in SERVICES) {
                    echo "Building and pushing Docker image for ${service}"
                    sh "docker-compose build ${service}"
                    sh "docker tag ${service}:latest ${HARBOR_REGISTRY}/${service}:${BUILD_NUMBER}"
                    sh "docker push ${HARBOR_REGISTRY}/${service}:${BUILD_NUMBER}"
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

     stage('Update Deployment File') {
        environment {
            GIT_REPO_NAME = "group20"
            GIT_USER_NAME = "ellie21520813"
        }
        steps {
            withCredentials([string(credentialsId: 'github', variable: 'GITHUB_TOKEN')]) {
                dir("k8s") {
                    for (k8s_manifest in K8S_MANIFESTS) {
                        def mnf_service = (k8s_manifest == 'userdb-deployment.yaml') ? 'user-service' : 'ui-app'
                        echo "Updating image tag for ${mnf_service} in ${k8s_manifest}"
                        sh '''
                            git config user.email "215220813@gm.uit.edu.vn"
                            git config user.name "${GIT_USER_NAME}"
                            BUILD_NUMBER=${BUILD_NUMBER}
                            sed -i "s|${HARBOR_REGISTRY}/${mnf_service}:.*|${HARBOR_REGISTRY}/${mnf_service}:${BUILD_NUMBER}|g" ${k8s_manifest}
                        '''
                        // sed -i "s+${HARBOR_REGISTRY}/${mnf_service}.*+${HARBOR_REGISTRY}/${mnf_service}:${BUILD_NUMBER}+g" ${k8s_manifest}
                    }
                    sh '''
                        git add .
                        git commit -m "Update deployment image to version ${BUILD_NUMBER}"
                        git push https://${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/${GIT_REPO_NAME} HEAD:main
                    '''
                }
            }
        }
     }
  }
}


