//
//  MacOSX_SSHMenuAppDelegate.h
//  MacOSX-SSHMenu
//
//  Created by Marinho Brandao on 21/01/11.
//  Copyright 2011 Raminel Web. All rights reserved.
//

#import <Cocoa/Cocoa.h>

@interface MacOSX_SSHMenuAppDelegate : NSObject <NSApplicationDelegate> {
    NSWindow *window;
}

@property (assign) IBOutlet NSWindow *window;

@end
