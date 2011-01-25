//
//  AppController.h
//  MacOSX-SSHMenu
//
//  Created by Marinho Brandao on 21/01/11.
//  Copyright 2011 Raminel Web. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import "Host.h"

@interface AppController : NSObject {
    IBOutlet id hostsTableView;
    IBOutlet id panelSheet;
    IBOutlet id panelInputTitle;
    IBOutlet id panelInputHost;
    NSString *editHostState;
}

- (IBAction) doOpenTerminal: (id)pId;
- (IBAction) doAddHost: (id)pId;
- (IBAction) doEditHost: (id)pId;
- (IBAction) doDeleteHost: (id)pId;
- (IBAction) doConfirmEditHost: (id)pId;
- (IBAction) doCancelEditHost: (id)pId;
- (IBAction) doImport: (id)pId;
- (IBAction) doExport: (id)pId;

- (void) updateTableView;

- (void)didEndSheet:(NSWindow *)sheet returnCode:(int)returnCode contextInfo:(void *)contextInfo;

@end
