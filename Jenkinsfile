#!groovy

def tryStep(String message, Closure block, Closure tearDown = null) {
    try {
        block();
    }
    catch (Throwable t) {
        slackSend message: "${env.JOB_NAME}: ${message} failure ${env.BUILD_URL}", channel: '#ci-channel', color: 'danger'

        throw t;
    }
    finally {
        if (tearDown) {
            tearDown();
        }
    }
}


node {

    stage("Checkout") {
        checkout scm
    }


    stage("Build base image") {
        tryStep "build", {
            sh "docker-compose build"
        }
    }


    stage('Test') {
        tryStep "test", {
            sh "docker-compose run --rm -u root web ./docker-test.sh"
        }, {
            step([$class: "JUnitResultArchiver", testResults: "reports/junit.xml"])

            sh "docker-compose down"
        }
    }

    stage("Build develop image") {
        tryStep "build", {
            def image = docker.build("admin.datapunt.amsterdam.nl:5000/datapunt/nap:${env.BUILD_NUMBER}", "web")
            image.push()
            image.push("develop")
        }
    }
}

node {
    stage(name: "Deploy to ACC") {
        tryStep "deployment", {
            build job: 'Subtask_Openstack_Playbook',
                    parameters: [
                            [$class: 'StringParameterValue', name: 'INVENTORY', value: 'acceptance'],
                            [$class: 'StringParameterValue', name: 'PLAYBOOK', value: 'deploy-nap.yml'],
                            [$class: 'StringParameterValue', name: 'BRANCH', value: 'master'],
                    ]
        }
    }
}


stage('Waiting for approval') {
    input "Deploy to Production?"
//    nog geen milestone available
//    milestone
}


node {
    stage('Push production image') {
        tryStep "image tagging", {
            def image = docker.image("admin.datapunt.amsterdam.nl:5000/datapunt/nap:${env.BUILD_NUMBER}")
            image.pull()

            image.push("master")
            image.push("latest")
        }
    }
}

node {
    stage(name: "Deploy to PROD") {
        tryStep "deployment", {
            build job: 'Subtask_Openstack_Playbook',
                    parameters: [
                            [$class: 'StringParameterValue', name: 'INVENTORY', value: 'production'],
                            [$class: 'StringParameterValue', name: 'PLAYBOOK', value: 'deploy-nap.yml'],
                            [$class: 'StringParameterValue', name: 'BRANCH', value: 'master'],
                    ]
        }
    }
}