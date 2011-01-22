//
//  HostsDataSource.m
//  MacOSX-SSHMenu
//
//  Created by Marinho Brandao on 21/01/11.
//  Copyright 2011 Raminel Web. All rights reserved.
//

#import "HostsDataSource.h"
#import "Host.h"

@implementation HostsDataSource

- (id) init {
    if (self = [super init]) {
        hosts = [[NSMutableArray alloc] init];
        [self loadFromFile:[self defaultFileName]];
    }
    return self;
}

- (void) dealloc {
    [hosts release];
    [super dealloc];
}

- (id) delegate {
    return delegate;
}

- (void) setDelegate: (id)newDelegate {
    delegate = newDelegate;
}

- (NSMutableArray *) hosts {
    return hosts;
}

- (NSInteger) numberOfRowsInTableView: (NSTableView *)tableView {
    return [hosts count];
}

- (id) tableView:(NSTableView *)tableView objectValueForTableColumn: (NSTableColumn *)tableColumn row:(NSInteger)index {
    if ([[tableColumn identifier] isEqualToString:@"display"]) {
        NSString* title = [[hosts objectAtIndex:index] title];
        NSString* host = [[hosts objectAtIndex:index] host];
        NSString* str = [NSString stringWithFormat:@"<font face='Lucida Grande' size='4'><big><b>%@</b></big><br/>&nbsp;&nbsp;<small style='color:gray'>%@</small></font>", title, host];
        NSData* html = [str dataUsingEncoding:NSUTF8StringEncoding];
    
        NSAttributedString* ret = [[NSAttributedString alloc] initWithHTML:html documentAttributes:nil];
    
        return ret;
    } else {
        return [[hosts objectAtIndex:index] identifier];
    }
}

- (void) saveToFile: (NSString *)fileName {
    id plist = [[NSMutableArray alloc] init];
    for (int index=0;index<[hosts count]; index++) {
        id dict = [[NSMutableDictionary alloc] init];
        [dict setValue:[[hosts objectAtIndex:index] identifier] forKey:@"identifier"];
        [dict setValue:[[hosts objectAtIndex:index] title] forKey:@"title"];
        [dict setValue:[[hosts objectAtIndex:index] host] forKey:@"host"];
        [plist addObject:dict];
    }
    
    NSString *error;
    NSData *xmlData = [NSPropertyListSerialization
        dataFromPropertyList:plist
        format:NSPropertyListXMLFormat_v1_0
        errorDescription:&error];

    if (xmlData) {
        [xmlData writeToFile:fileName atomically:YES];
    } else {
        NSLog(error);
        [error release];
    }
}

- (void) loadFromFile: (NSString *)fileName {
    NSData *xmlData = [NSData dataWithContentsOfFile:fileName];
    NSString *error;
    NSPropertyListFormat format;
    id plist;
    
    plist = [NSPropertyListSerialization
             propertyListFromData:xmlData
             mutabilityOption:NSPropertyListImmutable
             format:&format
             errorDescription:&error];
    
    if (!plist) {
        NSLog(error);
        [error release];
    } else {
        for (int index=0; index<[plist count]; index++) {
            Host *host = [[Host alloc] init];
            [host setIdentifier:[[plist objectAtIndex:index] valueForKey:@"identifier"]];
            [host setTitle:[[plist objectAtIndex:index] valueForKey:@"title"]];
            [host setHost:[[plist objectAtIndex:index] valueForKey:@"host"]];
            
            [hosts addObject:host];
        }
    }
}

- (NSString *) defaultFileName {
    NSString *path = [[NSBundle mainBundle] pathForResource:@"Hosts" ofType:@"plist"];
    return path;
}

@end
