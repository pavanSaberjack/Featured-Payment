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
@property (weak, nonatomic) IBOutlet UILabel *titleLabel;

@end

@implementation GroceriesVC

- (void)viewDidLoad {
    [super viewDidLoad];
    
    
    
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
    
    
    if (self.type == ConfirmMerchant) {
        self.titleLabel.text = @"Confirm merchant OTP";
        self.title = @"Merchant";
    } else {
        self.titleLabel.text = @"Confirm transaction OTP";
        self.title = @"Bank";
    }
    
    // Do any additional setup after loading the view from its nib.
}

- (IBAction)submitPressed:(id)sender {
    [self callAPI];
}

- (void)callAPI {
    
    NSString *urlStr = @"http://172.20.10.5:8080/confirm_bank_otp";
    if (self.type == ConfirmMerchant) {
        urlStr = @"http://172.20.10.5:8080/confirm_seller";
    }
    
    NSString *strOTP = [NSString stringWithFormat:@"%@%@%@%@%@%@",
                        self.otp1.text,
                        self.otp2.text,
                        self.otp3.text,
                        self.otp4.text,
                        self.otp5.text,
                        self.otp6.text];
    
    NSDictionary *params = @{@"otp":strOTP, @"user_phone":@"9663269499"};
    
    NSURL *url = [NSURL URLWithString:urlStr];
    NSMutableURLRequest *req = [NSMutableURLRequest requestWithURL:url];
    req.HTTPMethod = @"POST";
    
    NSError *writeError = nil;
    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:params options:NSJSONWritingPrettyPrinted error:&writeError];
    req.HTTPBody = jsonData;
    
    [[[NSURLSession sharedSession] dataTaskWithRequest:req completionHandler:^(NSData * _Nullable data, NSURLResponse * _Nullable response, NSError * _Nullable error) {
        
        NSLog(@"%@", error);
        
        NSHTTPURLResponse *httpResponse = (NSHTTPURLResponse *) response;
//        NSLog(@"%@", httpResponse.statusCode);
        
        if (error) {
            dispatch_async(dispatch_get_main_queue(), ^{
                [self showAlertForError:error.localizedDescription];
            });
        } else {
            dispatch_async(dispatch_get_main_queue(), ^{
                [self showAlert];
            });
        }
    }] resume];
    
}

- (void)showAlert {
    
    NSString *messageText = @"";
    if (self.type == ConfirmMerchant) {
        messageText = @"Merchant confirmed";
    } else {
        messageText = @"Transaction confirmed";
    }
    
    UIAlertController* alert = [UIAlertController alertControllerWithTitle:@"Grab Payment"
                                                                   message:messageText
                                                            preferredStyle:UIAlertControllerStyleAlert];
    
    UIAlertAction* defaultAction = [UIAlertAction actionWithTitle:@"OK" style:UIAlertActionStyleDefault
                                                          handler:^(UIAlertAction * action) {
                                                              
                                                              if (self.type == ConfirmMerchant) {
                                                                  GroceriesVC *groceriesVC = [[GroceriesVC alloc] initWithNibName:@"GroceriesVC" bundle:nil];
                                                                  groceriesVC.type = ConfirmBankOtp;
                                                                  [self.navigationController pushViewController:groceriesVC animated:YES];
                                                              } else {
                                                                  [self.navigationController popToRootViewControllerAnimated:YES];
                                                              }
                                                          }];
    
    [alert addAction:defaultAction];
    [self presentViewController:alert animated:YES completion:nil];
}

- (void)showAlertForError:(NSString *)message {
    UIAlertController* alert = [UIAlertController alertControllerWithTitle:@"Grab Payment"
                                                                   message:message
                                                            preferredStyle:UIAlertControllerStyleAlert];
    
    UIAlertAction* defaultAction = [UIAlertAction actionWithTitle:@"OK" style:UIAlertActionStyleDefault
                                                          handler:^(UIAlertAction * action) {
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
