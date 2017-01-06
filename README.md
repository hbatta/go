# Go

[![build status](https://git.gmu.edu/srct/go/badges/master/build.svg)](https://git.gmu.edu/srct/go/commits/master) [![coverage report](https://git.gmu.edu/srct/go/badges/master/coverage.svg)](https://git.gmu.edu/srct/go/commits/master) [![python version](https://img.shields.io/badge/python-2.7-blue.svg)]() [![Django version](https://img.shields.io/badge/Django-1.10-brightgreen.svg)]()

#### A project of [GMU SRCT](http://srct.gmu.edu).

Go is a drop-in URL shortening service. This project aims to provide an easy to use
URL branding service for institutions that wish to widely disseminate information
without unnecessarily outsourcing branding.

Go is currently a `Python 2.7` project written in the `Django` web framework, with
`MySQL` as our backend database.

# Setup instructions for local development

Go currently supports developers on Linux, macOS and Windows platforms through
both the Docker and Vagrant virtualization platforms. You may use either one
though we have included instructions for manual setup as well. Here's our walk-through
of steps we will take:

1. Install `git` on your system.
2. Clone the Go codebase.
3. Get Go up and running with the method of your choice.

## 1) Install `git` on your system.

`git` is the version control system used for SRCT projects.

### On Linux Based Systems

**with apt:**

Open a terminal and run the following command:

    sudo apt update

This retrieves links to the most up-to-date and secure versions of your packages.

Next, with:

    sudo apt install git

you install `git` onto your system.

**with yum (now something else??):**

**with rpm:**

**with other package manager???:**

### On macOS

We recommend that you use the third party Homebrew package manager for macOS,
which allows you to install packages from your terminal just as easily as you
could on a Linux based system. You could use another package manager (or not
use one at all), but Homebrew is highly reccomended.

To get homebrew, run the following command in a terminal:

    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)

**Note**: You do NOT need to use `sudo` when running any Homebrew commands, and
it likely won't work if you do.

Next, to make sure Homebrew is up to date, run:

    brew update

Finally we can install git with:

    brew install git

### On Windows

Instructions on how to setup git on Windows goes here.

## 2) Clone the Go codebase.

Now, we're going to clone down a copy of the Go codebase from [git.gmu.edu](http://git.gmu.edu/srct/go),
the SRCT code respository with SSH.

**a)** Configure your ssh keys by following the directions at:

[git.gmu.edu/help/ssh/README](http://git.gmu.edu/help/ssh/README).

**b)** Now, on your computer, navigate to the directory in which you want to download the project (ie. perhaps one called `development/SRCT`), and run

    git clone git@git.gmu.edu:srct/go.git

## 3) Get Go up and running with the method of your choice.

Now that we have `git` setup and cloned down the code you can

    cd go/

and get to working on setting up a development environment!

### Docker

Docker is an emerging containerization platform written in Google's Go
language.
Instead of running a full VM that runs Go, we package up all the
various bits that make up Go and run that as a container (two
containers: one for Go and the other for mysql) that act as normal
processes to the OS.   

Pros:

 - Lightweight
    - Can be run on most machines without needing significant resources.
    - SRCT members report minimal battery impact on laptops.
 - Fast
    - Compared to other methods, Docker is comparatively faster than
    Vagrant or manual setup.
 - Minimal setup
    - You run one command. Really easy to get up and running once you install
    Docker.
 - Good cross platform support
    - Runs smoothly on macOS, Linux, and Windows
    - Great docs to help if you get stuck.
 - Can easily destroy and rebuild the docker images
 - Loads in changes to code on the fly

Cons:

 - Challenging to debug problems
    - Cannot interact with attached images and as a result, you cannot really
    interact with the database.

There are instructions on how to setup/develop with Docker at the [docker-configuration page in the Go project wiki](https://git.gmu.edu/srct/go/wikis/docker-configuration).

### Vagrant + Ansible

Vagrant boots up a full virtual machine (VM) through VirtualBox that then runs Go. A
script written with Ansible will then run on that VM to automate the setup process
for you. It is similar in a way to running Go on a legitimate server.

Pros:

  - Very similar to a production environment
  - Can use `vagrant ssh` to "ssh" into the VM to debug things such as the
    database.
  - Relatively straightforward and easy setup.
    - One Command.
  - Can easily destroy and rebuild the VM.
  - Loads in changes to code on the fly.
  - Fast-ish (Initial provision takes a bit).

Cons:

  - Heavier on resources.
    - It's literally a full VM.
  - Occasional issues/hiccups.
    - Documented fixes are in the wiki.

There are instructions on how to setup with Vagrant at the [vagrant-configuration
page in the Go project wiki](https://git.gmu.edu/srct/go/wikis/vagrant-configuration).

Additionally, there is documentation about developing with Vagrant at
the [vagrant-usage page in the Go project wiki](https://git.gmu.edu/srct/go/wikis/vagrant-usage).

### Manual Setup

Manual setup (or: the old fashioned way) is where you install all dependecies on
your system and run Go as a local server with Django. Granted you are technically
doing that with Vagrant and Docker except those platforms automate the steps that
are laid out in this section.

Pros:
  - Experience setting up a Django project for local development

Cons:
  - Greater potential for things to go wrong
  - Way more steps

Link to wiki page goes here.

# Some words about contributing to Go.

Words about contributing.md go here.

I encourage you to join the [#go channel](https://srct.slack.com/messages/go/details/) in SRCT's [Slack Group](https://srct.slack.com)
if you have any questions on setup or would like to contribute.


# Some words about deploying Go.

someone @sysadmin writes up about how to deploy Go or just links to the wiki.

In order to expire links, you need to set up a cron job to run the manage.py
expirelinks command regularly. A sample cron script is available in the
repository and is named go-cleanlinks.cron. Drop this in cron.hourly and
change the paths so that they point to the virtualenv activate script and
manage.py.

---
**Note:**

Link by Viktor Vorobyev from the Noun Project.
