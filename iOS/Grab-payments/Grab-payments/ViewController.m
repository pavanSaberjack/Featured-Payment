//
//  ViewController.m
//  Grab-payments
//
//  Created by Pavan on 07/12/19.
//  Copyright © 2019 Pavan. All rights reserved.
//

#import "ViewController.h"
#import <MessageUI/MessageUI.h>
#import <MessageUI/MFMessageComposeViewController.h>

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
}

-(IBAction)sendSMS:(id)sender {
    
    if([MFMessageComposeViewController canSendText]) {
        MFMessageComposeViewController *controller = [[MFMessageComposeViewController alloc] init];
        controller.body = @"Hello";
        controller.recipients = [NSArray arrayWithObjects:@"+1234567890", nil];
        controller.messageComposeDelegate = self;
        [self presentViewController:controller animated:YES completion:nil];
    }
}


@end
