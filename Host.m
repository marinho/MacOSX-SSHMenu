//
//  Host.m
//  MacOSX-SSHMenu
//
//  Created by Marinho Brandao on 21/01/11.
//  Copyright 2011 Raminel Web. All rights reserved.
//

#import "Host.h"


@implementation Host

- (id) init {
    if (self = [super init]) {
        [self setIdentifier:[self generateUUID]];
        [self setTitle:@"New Host"];
        [self setHost:@"Host params"];
        
        [self autorelease];
    }
    
    return self;
}

- (void) dealloc {
    [title release];
    [host release];
    
    [super dealloc];
}

- (NSString *) title {
    return title;
}

- (NSString *) host {
    return host;
}

- (void) setTitle: (NSString *)input {
    [title autorelease];
    title = [input retain];
}

- (void) setHost: (NSString *)input {
    [host autorelease];
    host = [input retain];
}

- (NSString *) identifier {
    return identifier;
}

- (void) setIdentifier: (NSString *)input {
    [identifier autorelease];
    identifier = [input retain];
}

- (NSString *) generateUUID {
    // create a new UUID which you own
    CFUUIDRef uuid = CFUUIDCreate(kCFAllocatorDefault);
    
    // create a new CFStringRef (toll-free bridged to NSString)
    // that you own
    NSString *uuidString = (NSString *)CFUUIDCreateString(kCFAllocatorDefault, uuid);
    
    // transfer ownership of the string
    // to the autorelease pool
    [uuidString autorelease];
    
    // release the UUID
    CFRelease(uuid);
    
    return uuidString;
}

- (BOOL) matchToString: (NSString *)input {
    NSRange rangeTitle = [title rangeOfString:input];
    NSRange rangeHost = [host rangeOfString:input];
    
    return (rangeTitle.location != NSNotFound) || (rangeHost.location != NSNotFound);
}

@end
