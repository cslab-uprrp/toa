Toa
===

Toa is a web based NetFlow data network monitoring system (NMS). Toa consists of a collection of scripts that automatically parse NetFlow data, store this information in a database system, and generate interactive line charts for network visualization analytics. The system is pseudo real time, meaning that it continuously updates the interactive charts from NetFlow data that is generated every five minutes. Toa also provides an interface to generate customized charts from the data stored in the database, and plugins that connect the visualization charts with the NetFlow data file for more in depth visualizations and analysis.


---

#Installation

Following are two installation instructions to get Toa working in your linux server: 

* [Automatic installation](#automatic-installation)
* [Manual installation](#manual-installation)

You may try the automatic installation first and if something fails then follow the manual installation. 

In order to get Toa working you need to create an user for the installation, say user toa.  If you don't know how to create an user skip to the step [Create user toa](#create-user-toa) in the manual installation.

The following are prerequisites must be installed to have toa working in your server:

* flowtools ([link](https://code.google.com/p/flow-tools/))
* py-flowtools ([link](https://code.google.com/p/pyflowtools/))
* MySQL
* python
* python-MySQL

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
* graphs/

Move each of these directories to you home directory.

For example to move public_html to your home directory:

```
mv toa/public_html/ ~/
mv toa/bin/ ~/
mv toa/etc/ ~/
mv toa/db/ ~/
mv toa/graphs/ ~/
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
create user 'toa'@'localhost' identified by 'yourpassword';
grant all on toa.* to 'toa'@'localhost' ;
```
Before quiting the database run the following command to make sure you can use the new user.
```
flush privileges ;
```

## Automatic installation

Move to the bin directory:

```
cd bin
```

and run the installation script, then follow the instructions.

```
python install.py
```

Your installation session will look like the following:
```
Enter MySQL User to be use with Toa: toa
Your selection was toa ok?(y/n)y
Enter the password: aottoor
Your selection was aottoor ok?(y/n)y
Enter the database to be used: toa
Your selection was toa ok?(y/n)y
Testing connection to database using toadb...
Succesfully Connected
Loading Database Schema...
Database loaded

Now enter the following information to create the configuration file

Enter path where the Flow files are stored: /path/to/flows/
Your selection was /path/to/flows/ ok?(y/n)y
Enter for how many years will Toa keep data in the database before deleting it
min 1 year,  max 5 years (only int): 1
Your selection was 1 ok?(y/n)y
..Done, a file named config.xml was created in directory ../etc/

Generating crontab commands
..Done, a file named crontab  was created in the ../etc directory.
Please copy its contents to the crontab (remember to update crontab if any path changes)

Creating user for the web interface.
Enter your email to be used as user account: user@user.com
Insert password for user user@user.com
(at least 8 characters and at least one number, one letter and one unique character)
Enter a password 
mypass
Please confirm password
mypass
Done, you are now able to log in as admin using the toa user
```

There is an important message that you might have skipped and is the part to add the crontab lines that execute the heart of toa.  

```
Generating crontab commands
..Done, a file named crontab  was created in the ../etc directory.
Please copy its contents to the crontab (remember to update crontab if any path changes)
```
Click [here](#the-crontab) for instructions on how to copy the contents to the crontab.

## Manual Installation 

Following this installation instructions you will install Toa in user account toa.

### Add database tables to the MySQL database

In the terminal run the following command to create all the toa tables.

```
mysql -u toa -p toa < ~/db/flowsschema.sql
```

### The crontab

You need to add two lines to your crontab to run the parser and grapher.

To enter the crontab run the following command:

``` 
crontab -e
```

Add the following lines:
```
*/5 * * * * $HOME/bin/flowdbu.sh
0 22 * * * python $HOME/bin/flowsgrapherdaily_pool.py
0 22 * * * python /home/jortiz/bin/flowsdbcleaner.py
```

To exit type the Esc key, then the : key, then type wq, and enter.

### Edit configuration file

Open the configuration file:
```vi etc/config.xml```

Edit the document such that it looks similar to the configuration but with 
your database access information, and correct paths (if you changed them during the installation instructions)
```
<config>
        <!-- database information -->
        <database>
            <name>toa</name>
            <auth>
                <user>toa</user>
                <passwd>toa</passwd>
            </auth>
        </database>

        <!-- paths information (replace /home/toa with apropiate home dir) -->
        <logs><path>/tmp</path></logs>
        <flows><path>/home/toa/flows</path></flows>
        <graphs><path>/home/toa/graphs/</path></graphs>
        <crontime><time>300</time></crontime>
        <oldesttime><time>1</time></oldesttime>
        <toapath><path>/home/toa</path></toapath>
</config>
```

### Apache configuration 

Make sure that User directories are enable by commenting the line in your apache configuration file:

```UserDir disabled```

and uncomment the line:

```UserDir public_html```

Then in the user dir configuration make sure the ExecCGI Options is added.  Your user directory configuration should look like the following:
```
<Directory /home/*/public_html>
    AllowOverride FileInfo AuthConfig Limit
    Options MultiViews Indexes SymLinksIfOwnerMatch IncludesNoExec ExecCGI
    <Limit GET POST OPTIONS>
        Order allow,deny
        Allow from all
    </Limit>
    <LimitExcept GET POST OPTIONS>
        Order deny,allow
        Deny from all
    </LimitExcept>
</Directory>
```


---

##### Main developers:

Jose R. Ortiz-Ubarri<br>
Albert Maldonado<br>
Eric Santos<br>
Jhensen Grullon<br>


