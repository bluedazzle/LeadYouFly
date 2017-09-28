# coding: utf-8
import time
import datetime
from fabric.api import run, env, local
from fabric.context_managers import cd

env.hosts = ['182.92.187.203']
env.user = 'root'
env.password = 'Aiwe2015'


def deploy():
    remote_dir = "/var/www/site/sy/"
    with cd(remote_dir):
        run("git add .")
        try:
            run("git commit -m 'server commit {0}'".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        except:
            pass
        run("git pull origin sy")
        run("python manage.py makemigrations")
        run("python manage.py migrate")
    remote_dir = "/var/www/site/"
    with cd(remote_dir):
        run("uwsgi --reload uwsgi_sy.pid")


def up():
    commit = 'fix {0}'.format(time.time())
    mail = "rapospectre@gmail.com"
    commit_message = '{0}\r\n\r\nAuthor:{1}'.format(commit, mail)
    local("git add .")
    local("git commit -m '{0}'".format(commit_message))
    local("git push origin sy")

    remote_dir = "/var/www/site/sy/"
    with cd(remote_dir):
        run("git add .")
        try:
            run("git commit -m 'server commit {0}'".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        except:
            pass
        run("git pull origin sy")
        run("python manage.py makemigrations")
        run("python manage.py migrate")
    remote_dir = "/var/www/site/"
    with cd(remote_dir):
        run("uwsgi --reload uwsgi_sy.pid")
