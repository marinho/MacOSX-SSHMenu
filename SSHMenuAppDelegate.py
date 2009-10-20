#
#  SSHMenuAppDelegate.py
#  SSHMenu
#
#  Created by Marinho Brandao on 20/10/09.
#  Copyright __MyCompanyName__ 2009. All rights reserved.
#

import os

try:
    import yaml
except ImportError: # FIXME
    import sys
    sys.path.append('/Library/Python/2.5/site-packages/')
    import yaml

from objc import IBAction
from Foundation import *
from AppKit import *

class SSHMenuAppDelegate(NSObject):
    menu_connections = {}
    
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")

        self.statusItem = NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)
        self.statusItem.setTitle_(u'SSH')
        self.statusItem.setHighlightMode_(TRUE)
        self.statusItem.setEnabled_(TRUE)
        self.statusItem.retain()
        
        # Sub menu
        self.statusSub = NSMenu.alloc().init()

        self.load_menu_items()
        
        self.statusSub.addItem_(NSMenuItem.separatorItem())
        #self.statusSub.addItem_(
        #    NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Preferences', 'terminate:', '')
        #    )
        self.statusSub.addItem_(
            NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
            )
        
        self.statusItem.setMenu_(self.statusSub)

    def load_menu_items(self):
        """Creates the menu itens from the configuration file"""
        conf_path = os.path.join(NSHomeDirectory(), '.sshmenu')
            
        try:
            fp = file(conf_path)
        except IOError:
            return
        
        data = yaml.load(fp)
        
        for item in data['items']:
            menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                item['title'], self.executeSSHConnection, '',
                )
            self.menu_connections[menuitem] = item
            self.statusSub.addItem_(menuitem)
            
        fp.close()

    @IBAction
    def executeSSHConnection(self, sender):
        NSLog('Executing executeSSHConnection method')
        NSLog(self.menu_connections[sender]['sshparams'])
        
        # Launchs the task on Terminal
        cmd = '/usr/bin/ssh '+self.menu_connections[sender]['sshparams']
        script = NSAppleScript.alloc().initWithSource_("tell application \"Terminal\" to do script \"%s\""%cmd)
        script.executeAndReturnError_(None)
        
        # Brings the Terminal window to front
        script = NSAppleScript.alloc().initWithSource_("tell application \"Terminal\" to activate")
        script.executeAndReturnError_(None)
