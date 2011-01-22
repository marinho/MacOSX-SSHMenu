//
//  Host.h
//  MacOSX-SSHMenu
//
//  Created by Marinho Brandao on 21/01/11.
//  Copyright 2011 Raminel Web. All rights reserved.
//

#import <Cocoa/Cocoa.h>


@interface Host : NSObject {
    NSString* identifier;
    NSString* title;
    NSString* host;
}

- (NSString *) identifier;
- (NSString *) title;
- (NSString *) host;

- (void) setIdentifier: (NSString *)input;
- (void) setTitle: (NSString *)input;
- (void) setHost: (NSString *)input;

- (NSString *) generateUUID;
- (BOOL) matchToString: (NSString *)input;

@end
