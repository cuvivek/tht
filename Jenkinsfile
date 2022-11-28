pipeline {
  agent any
  stages {
    stage('Checkout code') {
      steps {
        git(url: 'https://github.com/cuvivek/tht', branch: 'master', changelog: true)
      }
    }

    stage('test') {
      steps {
        mail(subject: 'test jenkins', body: 'test', to: 'vivekcu81@gmail.com')
      }
    }

  }
}