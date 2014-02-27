#!/usr/bin/env python

import ConfigParser
import os.path

class Config:

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        if not os.path.isfile("americano.ini"):
            cfgfile = open("americano.ini",'w')
            self.config.add_section('MySQL')
            self.config.add_section("Preferences")
            self.config.add_section("Info")
            self.config.set("Preferences", "ExtraHeaderEnabled", "False")
            self.config.set("Preferences", "Colors", "Default")
            self.config.set("Info", "Installed", "1")
            self.config.write(cfgfile)
            cfgfile.close()
        else:
            self.config.read("americano.ini")

    def setMySQLUsername(self, username):
        cfgfile = open("americano.ini",'w')
        self.config.set('MySQL','username',username)
        self.config.write(cfgfile)
        cfgfile.close()

    def setMySQLPassword(self, password):
        cfgfile = open("americano.ini",'w')
        self.config.set('MySQL','password',password)
        self.config.write(cfgfile)
        cfgfile.close()

    def setMySQLDatabase(self, database):
        cfgfile = open("americano.ini",'w')
        self.config.set('MySQL','database',database)
        self.config.write(cfgfile)
        cfgfile.close()

    def setName(self, name):
        cfgfile = open("americano.ini",'w')
        self.config.set('Info','name',name)
        self.config.write(cfgfile)
        cfgfile.close()

    def setInstalled(self, val):
        cfgfile = open("americano.ini",'w')
        self.config.set('Info','installed',val)
        self.config.write(cfgfile)
        cfgfile.close()

    def ConfigSectionMap(self, section):
        dict1 = {}
        self.config.read('americano.ini')
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
                if dict1[option] == -1:
                    print "skip: %s" % option
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

if __name__ == '__main__':
    con = Config()
    con.setMySQLUsername("admin")
    con.setMySQLPassword("andre")
    con.setMySQLDatabase("blog")
    print con.ConfigSectionMap("MySQL")["database"]
