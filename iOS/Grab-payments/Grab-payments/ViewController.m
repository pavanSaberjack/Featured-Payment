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
#import "TaxiServiceVC.h"
#import "GroceriesVC.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
}

-(IBAction)sendSMS:(id)sender {
    
//    if([MFMessageComposeViewController canSendText]) {
//        MFMessageComposeViewController *controller = [[MFMessageComposeViewController alloc] init];
//        controller.body = @"Hello";
//        controller.recipients = [NSArray arrayWithObjects:@"+1234567890", nil];
//        controller.messageComposeDelegate = self;
//        [self presentViewController:controller animated:YES completion:nil];
//    }
}

- (IBAction)useTaxiService:(id)sender {
    TaxiServiceVC *taxiVC = [[TaxiServiceVC alloc] initWithNibName:@"TaxiServiceVC" bundle:nil];
    [self.navigationController pushViewController:taxiVC animated:YES];
}

- (IBAction)goForGroceries:(id)sender {
    GroceriesVC *groceriesVC = [[GroceriesVC alloc] initWithNibName:@"GroceriesVC" bundle:nil];
    [self.navigationController pushViewController:groceriesVC animated:YES];
}


@end
