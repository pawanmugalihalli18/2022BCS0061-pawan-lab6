pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "2022bcs0061_pawan/model"
        DOCKERHUB_CREDENTIALS = "dockerhub-creds"
    }

    stages {

        // stage('Clone Repo') {
        //     steps {
        //         git 'https://github.com/pawanmugalihalli18/2022BCS0061-pawan-lab6.git'
        //     }
        // }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
    steps {
        sh '''
        . venv/bin/activate
        python scripts/train.py
        '''
    }
}

        stage('Print Info') {
            steps {
                echo "Name: Pawan"
                echo "Roll No: 2022bcs0061"
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t 2022bcs0061pawan/2022bcs0061-pawan-lab5-model .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'USERNAME',
                    passwordVariable: 'PASSWORD'
                )]) {
                    sh '''
                    echo $PASSWORD | docker login -u $USERNAME --password-stdin
                    docker push 2022bcs0061pawan/2022bcs0061-pawan-lab5-model
                    '''
                }
            }
        }
    }
}