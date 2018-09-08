#!/bin/sh
#Author: BEMOSS Team

#Download the package lists from the repositories and update them
../sudo apt-get update
#Download and install the dependencies of the postgresql database
../sudo apt-get install postgresql postgresql-contrib python-yaml --assume-yes
#Create the bemossdb database
../sudo -u postgres psql -c "CREATE USER admin WITH PASSWORD 'admin';"
../sudo -u postgres psql -c "DROP DATABASE IF EXISTS hiveosdb"
../sudo -u postgres createdb hiveosdb -O admin
../sudo -u postgres psql -d hiveosdb -c "create extension hstore;"

