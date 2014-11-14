Toa
===

Toa is a web based NetFlow data network monitoring system (NMS). Toa consists of a collection of scripts that automatically parse NetFlow data, store this information in a database system, and generate interactive line charts for network visualization analytics. The system is pseudo real time, meaning that it continuously updates the interactive charts from NetFlow data that is generated every five minutes. Toa also provides an interface to generate customized charts from the data stored in the database, and plugins that connect the visualization charts with the NetFlow data file for more in depth visualizations and analysis.


---

# Installation 

Following this installation instructions you will install Toa in user account toa.

### Create user toa

```
useradd toa
```

You may assign a password to the user toa

```
passwd toa
```

Finally login as user toa.

### Change directory to user toa folder and download the toa code

Normally the users home is under /home
```
cd /home/toa/
```

Download the compressed files from github at: https://github.com/cslab-uprrp/toa

or with wget:

```
wget https://github.com/cslab-uprrp/toa/archive/master.zip
```

or git:

```
git clone https://github.com/cslab-uprrp/toa.git
```

If you downloaded the compressed file master.zip, uncompress with:

```
unzip master.zip
```

When you unzip the master.zip file or clone the **toa** repository there will be a directory toa/ that contains the following folders inside:

* public_html/
* bin/
* etc/
* db/

Move each of the directories to you home directory.

For example to move public_html to your home directory:

```
mv toa/public_html/ ~/
mv toa/bin/ ~/
mv toa/etc/ ~/
mv toa/db/ ~/
```

You must have the following directory structure:
```
/home/toa/public_html/
/home/toa/bin/
/home/toa/etc/
/home/toa/db/
```

### Create toa database

Login as a priviledge user to your mysql database.

```
mysql -u root -p
```

Create database for toa:

```
create database toa;
```

Create a user that can access the toa database: (please make sure to change the password in the command bellow)
```
grant all privileges on toa.* to ‘toa’@’localhost’ identified by 'yourpassword';
```
Before quiting the database run the following command to make sure you can use the new user.
```
flush privileges ;
```

Exit mysql and in the terminal run the following command to create all the toa tables.

```
mysql -u toa -p toa < ~/db/flowsschema.sql
```




---

Main developers

Jose R. Ortiz-Ubarri

Albert Maldonado

Eric Santos

Jhensen Grullon


