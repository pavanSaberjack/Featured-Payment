//
//  PaymentVC.m
//  Grab-payments
//
//  Created by Pavan on 07/12/19.
//  Copyright © 2019 Pavan. All rights reserved.
//

#import "PaymentVC.h"

@interface PaymentVC ()
@property (weak, nonatomic) IBOutlet UIButton *homeButton;

@end

@implementation PaymentVC

- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    [self.navigationController setNavigationBarHidden:YES];
}

- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.homeButton.layer.cornerRadius = 5.0;
    // Do any additional setup after loading the view from its nib.
}

- (IBAction)buttonPressed:(id)sender {
    [self.navigationController setNavigationBarHidden:NO];
    [self.navigationController popToRootViewControllerAnimated:YES];
}

@end
