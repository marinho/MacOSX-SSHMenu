#
#  SSHMenuAppDelegate.py
#  SSHMenu
#
#  Created by Marinho Brandao on 20/10/09.
#  Copyright __MyCompanyName__ 2009. All rights reserved.
#

import os, sys

import webbrowser
from objc import IBAction, IBOutlet
from Foundation import *
from AppKit import *

class SSHMenuAppDelegate(NSObject):
    menu_connections = None
    aboutWindow = IBOutlet()
    prefsWindow = IBOutlet()
    prefsTable = IBOutlet()
    prefsArray = IBOutlet()
    
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")

        # Icon on SystemMenuBar (clock's tray icon)
        self.statusItem = NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)
        self.statusItem.setTitle_(u'SSH')
        self.statusItem.setHighlightMode_(TRUE)
        self.statusItem.setEnabled_(TRUE)
        self.statusItem.retain()
        
        # Sub menu
        self.statusSub = NSMenu.alloc().init()
        
        self.make_menu_items()
        
    def clear_menu_items(self):
        #for item in self.menu_connections.keys():
        for item in self.statusSub.itemArray():
            self.statusSub.removeItem_(item)
            
        self.menu_connections = {}

    def make_menu_items(self):
        self.load_menu_connections()
        
        self.statusSub.addItem_(NSMenuItem.separatorItem())
        self.statusSub.addItem_(
            NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Preferences', 'showPreferencesWindow:', '')
            )
        self.statusSub.addItem_(
            NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('About', 'showAboutWindow:', '')
            )
        self.statusSub.addItem_(
            NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
            )
        
        self.statusItem.setMenu_(self.statusSub)
    
    def load_conf_file(self):
        """Loads configuration from .sshmenu file"""
        if getattr(self, '_ssh_connections', []):
            return self._ssh_connections
        
        conf_path = os.path.join(NSHomeDirectory(), '.sshmenu')

        # Try the official way (just saving unicode of the dictionary)
        try:
            fp = file(conf_path)
            cont = fp.read()
            fp.close()

            # Parses the file content
            conf = eval(cont)
            
            self._ssh_connections = conf.get('items', [])
                
        # If get no success, try using PyYAML
        except SyntaxError:
            try:
                import yaml
            except ImportError: # FIXME
                sys.path.append('/Library/Python/2.5/site-packages/')
                
                try:
                    import yaml
                except ImportError:
                    raise Exception('Invalid file "~/.sshmenu" format (must be JSON or YAML)')
            
            fp = file(conf_path)
            self._ssh_connections = yaml.load(fp).get('items', [])
            fp.close()

        # If an error ocurred when loading the file
        except IOError:
            self._ssh_connections = []
        
        return self._ssh_connections
        
    def save_conf_file(self):
        """Saves the SSH connections to file ~/.sshmenu"""
        conf_path = os.path.join(NSHomeDirectory(), '.sshmenu')
            
        conf = {'items': self._ssh_connections}
        
        try:
            fp = file(conf_path, 'wb')
        except IOError:
            return

        fp.write(unicode(conf))
        fp.close()
        
        return self._ssh_connections

    def load_menu_connections(self):
        """Creates the menu itens from the configuration data"""
        self.load_conf_file()
        
        self.menu_connections = self.menu_connections or {}
        
        for item in self._ssh_connections:
            menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                item['title'], 'executeSSHConnection:', '',
                )
            self.menu_connections[menuitem] = item
            self.statusSub.addItem_(menuitem)

    @IBAction
    def executeSSHConnection_(self, sender):
        NSLog('Executing executeSSHConnection method')
        NSLog(self.menu_connections[sender]['sshparams'])
        
        # Launchs the task on Terminal
        cmd = '/usr/bin/ssh '+self.menu_connections[sender]['sshparams']
        script = NSAppleScript.alloc().initWithSource_("tell application \"Terminal\" to do script \"%s\""%cmd)
        script.executeAndReturnError_(None)
        
        # Brings the Terminal window to front
        script = NSAppleScript.alloc().initWithSource_("tell application \"Terminal\" to activate")
        script.executeAndReturnError_(None)

    @IBAction
    def showAboutWindow_(self, sender):
        NSLog('Executing showAboutWindow method')
        self.aboutWindow.makeKeyAndOrderFront_(sender)
        NSApplication.sharedApplication().activateIgnoringOtherApps_(YES)

    @IBAction
    def loadWebSite_(self, sender):
        NSLog('loadWebSite')
        webbrowser.open('http://www.marinhobrandao.com/sshmenu/')

    @IBAction
    def showPreferencesWindow_(self, sender):
        NSLog('Executing showPreferencesWindow method')
        self.prefsWindow.makeKeyAndOrderFront_(sender)
        NSApplication.sharedApplication().activateIgnoringOtherApps_(YES)

    @IBAction
    def savePreferences_(self, sender):
        NSLog('Executing savePreferences method')
        
        # Stores the SSH connections in internal variable
        self._ssh_connections = list(self.prefsArray.arrangedObjects())
        
        self.save_conf_file()
        self.clear_menu_items()
        self.make_menu_items()
        
        # Hides the window
        self.prefsWindow.orderOut_(sender)
        
    @IBAction
    def removeSSHConnection_(self, sender):
        NSLog('Executing removeSSHConnection method')
        self.prefsArray.removeObjects_(self.prefsArray.selectedObjects())
        
    @IBAction
    def addSSHConnection_(self, sender):
        NSLog('Executing addSSHConnection method')
        self.prefsArray.addObject_({'title': 'new title', 'sshparams': 'user@host params'})

    def ssh_connections(self):
        self.load_conf_file()
        return self._ssh_connections
