pipeline {
    agent any

    environment {
        IMAGE_NAME = "2022bcs0064/surabhi_2022bcs0064"
    }

    stages {

        stage('Checkout') {
            steps {
                git credentialsId: 'git-creds', url: 'https://github.com/ThisIsSurabhiSinha/Surabhi_2022BCS0064-Lab6.git'
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                python3 -m venv .venv
                . .venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                sh '''
                . .venv/bin/activate
                python scripts/train.py
                '''
            }
        }

        stage('Read Accuracy') {
            steps {
                script {
                    def acc = sh(script: "jq .accuracy app/artifacts/metrics.json", returnStdout: true).trim()
                    env.CURRENT_ACCURACY = acc
                    echo "Accuracy: ${acc}"
                }
            }
        }

        stage('Compare Accuracy') {
            steps {
                script {
                    def best = credentials('best-accuracy')
                    def isBetter = sh(
                        script: "echo ${env.CURRENT_ACCURACY} ${best} | awk '{print (\\$1 > \\$2)}'",
                        returnStdout: true
                    ).trim()
                    env.IS_BETTER = isBetter
                    echo "Is better: ${isBetter}"
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression { env.IS_BETTER == '1' }
            }
            steps {
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
                sh "docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
            }
        }

        stage('Push Docker Image') {
            when {
                expression { env.IS_BETTER == '1' }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh "echo $PASS | docker login -u $USER --password-stdin"
                }
                sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'app/artifacts/**', fingerprint: true
        }
    }
}