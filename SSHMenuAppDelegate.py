#
#  SSHMenuAppDelegate.py
#  SSHMenu
#
#  Created by Marinho Brandao on 20/10/09.
#  Copyright __MyCompanyName__ 2009. All rights reserved.
#

from Foundation import *
from AppKit import *

class SSHConnection(object):
    host = str()
    title = str()
    
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

class SSHMenuAppDelegate(NSObject):
    ssh_connections = [
        SSHConnection(host='marinho@sistema.amigosdoolair.com.br', title='Agittus - Amigos do Olair'),
        SSHConnection(host='marinho@www.euprecisode.com.br', title='EuPrecisoDe'),
    ]
    
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")

        self.statusItem = NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)
        self.statusItem.setTitle_(u'SSH')
        self.statusItem.setHighlightMode_(TRUE)
        self.statusItem.setEnabled_(TRUE)
        self.statusItem.retain()
        
        # Sub menu
        self.statusSub = NSMenu.alloc().init()
        
        for ssh_conn in self.ssh_connections:
            menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(ssh_conn.title, 'terminate:', '')
            self.statusSub.addItem_(menuitem)
        
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
        self.statusSub.addItem_(menuitem)
        
        self.statusItem.setMenu_(self.statusSub)
