#!/bin/python3
from genericpath import exists
import os
import os.path
import subprocess
import pipes
import sys

option = ""
try:
    option = sys.argv[1]
except:
    pass

help = """
This is wpup 1.1 written by koyu

--help or -h    :   Show this help
--sysup or -s   :   Upgrade all host systems
--puppyup -p    :   Upgrades to the latest version of wpup
"""

def exists_remote(host, path):
    status = subprocess.call(
        ['ssh', host, 'test -f {}'.format(pipes.quote(path))])
    if status == 0:
        return True
    if status == 1:
        return False
    raise Exception('SSH failed')

class tcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if option == "":
    if not os.path.exists(os.path.expanduser("~/.wpuprc")):
        print(tcolors.FAIL+"File .wuprc doesn't exist. Please create this file and add your WordPress hosts and the path to your WordPress installation without /var/www/ delimited with a colon line-by-line."+tcolors.ENDC)
    else:
        f = open(os.path.expanduser("~/.wpuprc"), "r")
        lines = f.readlines()
        f.close()
        lcount = len(lines)
        currl = 0
        for el in lines:
            currl = currl+1
            sleft = lcount-currl
            host = el.split(":")[0]
            wppath = el.split(":")[1].replace("\n", "")
            if host.startswith("#"):
                print(tcolors.WARNING+"("+str(currl)+"/"+str(lcount)+") Site "+wppath.replace("#", "")+" on host "+host.replace("#", "")+" ignored."+tcolors.ENDC)
            else:
                print(tcolors.OKCYAN+"("+str(currl)+"/"+str(lcount)+") Upgrading host "+host+" with site "+wppath+tcolors.ENDC)
                if exists_remote(host, "/var/www/"+wppath+"/wp-config.php"):
                    if not exists_remote(host, "/var/www/"+wppath+"/wp-content/plugins/woocommerce/"):
                        command = """
                        cd /var/www/%%path%%
                        wp --allow-root plugin update --all
                        wp --allow-root theme update --all
                        wp --allow-root core update
                        wp --allow-root core update-db
                        wp --allow-root language core update
                        wp --allow-root language theme update --all
                        wp --allow-root language plugin update --all
                        chown -R www-data:www-data /var/www/%%path%%
                        """
                    else:
                        command = """
                        cd /var/www/%%path%%
                        wp --allow-root plugin update --all
                        wp --allow-root wc update
                        wp --allow-root theme update --all
                        wp --allow-root core update
                        wp --allow-root core update-db
                        wp --allow-root language core update
                        wp --allow-root language theme update --all
                        wp --allow-root language plugin update --all
                        chown -R www-data:www-data /var/www/%%path%%
                        """
                    f = open("/tmp/updscript", "w+")
                    f.write(command.replace("%%path%%", wppath))
                    f.close()
                    os.system("cat /tmp/updscript | ssh "+host)
                    os.remove("/tmp/updscript")
                    print(tcolors.OKGREEN+"Successfully upgraded host "+host+" with site "+wppath+tcolors.ENDC+" 🎉️")
                else:
                    print(tcolors.WARNING+"Warning: Site "+wppath+" on host "+host+" is not a valid WordPress instllation."+tcolors.ENDC)
            if sleft != 0:
                print()
            else:
                print()
                print(tcolors.OKGREEN+"All sites have been upgraded! Happy blogging 🎉️"+tcolors.ENDC)
else:
    arg2 = ""
    try:
        arg2 = sys.argv[2]
    except:
        pass
    if option == "-h" or option == "--help" or option == "-v" or option == "--version":
        if arg2 == "":
            print(help)
        else:
            if "s" in sys.argv[2].replace("--", "").lower():
                print("--sysup or -s upgrades all hosts in your .wpuprc file. It doesn't require any further arguments.")
            elif "h" in sys.argv[2].replace("--", "").lower():
                print("--help or -h shows the help. It doesn't require any further arguments.")
            elif "p" in sys.argv[2].replace("--", "").lower():
                print("--puppyup or -p upgrades your version of wpup. It doesn't require any further arguments.")
            else:
                print(tcolors.FAIL+"Error: Couldn't find help entry. 😢"+tcolors.ENDC)
    elif option == "-s" or option == "--sysup":
        f = open(os.path.expanduser("~/.wpuprc"), "r")
        lines = f.readlines()
        f.close()
        hosts = []
        for e in lines:
            hosts.append(e.split(":")[0])
        hosts = list(dict.fromkeys(hosts))
        for host in hosts:
            command = """
            apt update -y
            apt dist-upgrade -y
            """
            f = open("/tmp/updscript", "w+")
            f.write(command)
            f.close()
            os.system("cat /tmp/updscript | ssh "+host)
            os.remove("/tmp/updscript")
            print(tcolors.OKGREEN+"Successfully upgraded host "+host+" "+tcolors.ENDC+" 🎉️")
    elif option == "-p" or option == "--puppyup":
        os.system("sudo rm /usr/bin/wpup")
        os.system("sudo wget -O /usr/bin/wpup https://raw.githubusercontent.com/koyuspace/wpup/main/wpup.py")
        os.system("sudo chmod +x /usr/bin/wpup")
    else:
        print(tcolors.FAIL+"Error: Unrecognized argument. 😢"+tcolors.ENDC)