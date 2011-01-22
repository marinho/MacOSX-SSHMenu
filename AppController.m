//
//  AppController.m
//  MacOSX-SSHMenu
//
//  Created by Marinho Brandao on 21/01/11.
//  Copyright 2011 Raminel Web. All rights reserved.
//

#import "AppController.h"


@implementation AppController

- (IBAction) doOpenTerminal: (id)pId {
    NSInteger index = [hostsTableView selectedRow];
    
    if (index >= 0) {
        id ds = [hostsTableView dataSource];
        id host = [[ds hosts] objectAtIndex:index];

        // Launchs the task on Terminal
        NSString* cmd = [@"/usr/bin/ssh " stringByAppendingString:[host host]];

        id script1 = [[NSAppleScript alloc] initWithSource:[NSString stringWithFormat:@"tell application \"Terminal\" to do script \"%@\"",cmd]];
        [script1 executeAndReturnError:nil];
    
        // Brings the Terminal window to front
        id script2 = [[NSAppleScript alloc] initWithSource:@"tell application \"Terminal\" to activate"];
        [script2 executeAndReturnError:nil];
    }
}

- (IBAction) doConfirmEditHost: (id)pId {
    id ds = [hostsTableView dataSource];
    
    if (editHostState == @"editing") {
        NSInteger index = [hostsTableView selectedRow];
        
        id found_host = [[ds hosts] objectAtIndex:index];
        id host = [self hostByIdentifier:[found_host identifier]];
                
        [host setTitle:[panelInputTitle stringValue]];
        [host setHost:[panelInputHost stringValue]];
    } else {
        id host = [[Host alloc] init];
    
        [host setTitle:[panelInputTitle stringValue]];
        [host setHost:[panelInputHost stringValue]];
    
        [[ds hosts] addObject:host];
    }
    
    [self updateTableView];
    
    [panelInputTitle setStringValue:@""];
    [panelInputHost setStringValue:@""];
    [NSApp endSheet:panelSheet];
    
    [ds saveToFile:[ds defaultFileName]];
}

- (IBAction) doCancelEditHost: (id)pId {
    [panelInputTitle setStringValue:@""];
    [panelInputHost setStringValue:@""];
    [NSApp endSheet:panelSheet];
}

- (IBAction) doAddHost: (id)pId {    
    [panelInputTitle selectText:nil];
    editHostState = @"adding";
    
    [NSApp beginSheet: panelSheet
       modalForWindow: [NSApp mainWindow]
        modalDelegate: self
       didEndSelector: @selector(didEndSheet:returnCode:contextInfo:)
          contextInfo: nil];
}

- (IBAction) doEditHost: (id)pId {
    NSInteger index = [hostsTableView selectedRow];
    
    if (index >= 0) {
        id host = [[[hostsTableView dataSource] hosts] objectAtIndex:index];
        editHostState = @"editing";
        
        [panelInputTitle selectText:nil];

        [panelInputTitle setStringValue:[host title]];
        [panelInputHost setStringValue:[host host]];
    
        [NSApp beginSheet: panelSheet
           modalForWindow: [NSApp mainWindow]
            modalDelegate: self
           didEndSelector: @selector(didEndSheet:returnCode:contextInfo:)
              contextInfo: nil];
    }
}

- (IBAction) doDeleteHost: (id)pId {
    NSInteger index = [hostsTableView selectedRow];
    
    if (index >= 0) {
        id ds = [hostsTableView dataSource];
        id host = [[ds hosts] objectAtIndex:index];
    
        [[ds hosts] removeObject:[self hostByIdentifier:[host identifier]]];
        [ds saveToFile:[ds defaultFileName]];
        
        [self updateTableView];
    }
}

- (id)hostByIdentifier: (NSString *)identifier {
    id ds = [hostsTableView dataSource];
    id host = nil;
    
    for (int index=0; index<[[ds hosts] count]; index++ ) {
        id temp_host = [[ds hosts] objectAtIndex:index];
        
        if ([temp_host identifier] == identifier) {
            host = temp_host;
            break;
        }
    }
    
    return host;
}

- (void)didEndSheet:(NSWindow *)sheet returnCode:(int)returnCode contextInfo:(void *)contextInfo{
    [panelSheet orderOut:self];
}

- (void) updateTableView {
    [hostsTableView reloadData];
}

@end
