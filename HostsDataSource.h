//
//  HostsDataSource.h
//  MacOSX-SSHMenu
//
//  Created by Marinho Brandao on 21/01/11.
//  Copyright 2011 Raminel Web. All rights reserved.
//

#import <Cocoa/Cocoa.h>


@interface HostsDataSource : NSObject {
    id delegate;
    NSMutableArray* hosts;
}

- (id) delegate;
- (void) setDelegate: (id)newDelegate;
- (NSMutableArray *) hosts;

- (void) saveToFile: (NSString *)fileName;
- (void) loadFromFile: (NSString *)fileName;
- (NSString *) defaultFileName;

@end
