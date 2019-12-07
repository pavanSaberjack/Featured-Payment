//
//  GroceriesVC.m
//  Grab-payments
//
//  Created by Pavan on 07/12/19.
//  Copyright © 2019 Pavan. All rights reserved.
//

#import "GroceriesVC.h"

@interface GroceriesVC () <UITextFieldDelegate>
@property (weak, nonatomic) IBOutlet UITextField *otp1;
@property (weak, nonatomic) IBOutlet UITextField *otp2;
@property (weak, nonatomic) IBOutlet UITextField *otp3;
@property (weak, nonatomic) IBOutlet UITextField *otp4;
@property (weak, nonatomic) IBOutlet UITextField *otp5;
@property (weak, nonatomic) IBOutlet UIButton *submitButton;
@property (weak, nonatomic) IBOutlet UITextField *otp6;

@end

@implementation GroceriesVC

- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.title = @"Groceries";
    
    self.otp1.font = [UIFont fontWithName:@"Helvetica Neue" size:25.0];
    self.otp2.font = [UIFont fontWithName:@"Helvetica Neue" size:25.0];
    self.otp3.font = [UIFont fontWithName:@"Helvetica Neue" size:25.0];
    self.otp4.font = [UIFont fontWithName:@"Helvetica Neue" size:25.0];
    self.otp5.font = [UIFont fontWithName:@"Helvetica Neue" size:25.0];
    self.otp6.font = [UIFont fontWithName:@"Helvetica Neue" size:25.0];
    
    self.otp1.delegate = self;
    self.otp2.delegate = self;
    self.otp3.delegate = self;
    self.otp4.delegate = self;
    self.otp5.delegate = self;
    self.otp6.delegate = self;
    
    self.submitButton.layer.cornerRadius = 5.0;
    [self.submitButton setTitle:@"Submit" forState:UIControlStateNormal];
    
    // Do any additional setup after loading the view from its nib.
}

- (IBAction)submitPressed:(id)sender {
    [self callAPI];
}

- (void)callAPI {
    
    NSString *strOTP = [NSString stringWithFormat:@"%@%@%@%@%@%@",
                        self.otp1.text,
                        self.otp2.text,
                        self.otp3.text,
                        self.otp4.text,
                        self.otp5.text,
                        self.otp6.text];
            
    NSURL *url = [NSURL URLWithString:@"myurll"];
    NSMutableURLRequest *req = [NSMutableURLRequest requestWithURL:url];
    req.HTTPMethod = @"POST";
    req.HTTPBody = [strOTP dataUsingEncoding:NSUTF8StringEncoding];
    
    [[[NSURLSession sharedSession] dataTaskWithRequest:req completionHandler:^(NSData * _Nullable data, NSURLResponse * _Nullable response, NSError * _Nullable error) {
        
        dispatch_async(dispatch_get_main_queue(), ^{
            [self showAlert];
        });
    }] resume];
    
}

- (void)showAlert {
    UIAlertController* alert = [UIAlertController alertControllerWithTitle:@"Grab Payment"
                                                                   message:@"OTP is verified"
                                                            preferredStyle:UIAlertControllerStyleAlert];
    
    UIAlertAction* defaultAction = [UIAlertAction actionWithTitle:@"OK" style:UIAlertActionStyleDefault
                                                          handler:^(UIAlertAction * action) {
                                                              [self.navigationController popToRootViewControllerAnimated:YES];
                                                          }];
    
    [alert addAction:defaultAction];
    [self presentViewController:alert animated:YES completion:nil];
}

- (BOOL)textField:(UITextField *)textField shouldChangeCharactersInRange:(NSRange)range replacementString:(NSString *)string {
    NSString *currentString = textField.text;
    NSString *newString = [currentString stringByReplacingCharactersInRange:range withString:string];
    return newString.length <= 1;
}
@end
