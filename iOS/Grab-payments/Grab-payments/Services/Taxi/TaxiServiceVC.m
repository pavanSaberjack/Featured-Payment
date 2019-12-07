//
//  TaxiServiceVC.m
//  Grab-payments
//
//  Created by Pavan on 07/12/19.
//  Copyright © 2019 Pavan. All rights reserved.
//

#import "TaxiServiceVC.h"
#import "PaymentVC.h"

typedef NS_ENUM(NSInteger, RideStatus) {
    None = 0,
    Started,
    Finished
};

@interface TaxiServiceVC ()
@property (weak, nonatomic) IBOutlet UIButton *rideStatusButton;
@property (readwrite, nonatomic) RideStatus rideStatus;
@end

@implementation TaxiServiceVC

- (void)viewDidLoad {
    [super viewDidLoad];
    
    self.title = @"Taxi";
    self.rideStatus = None;
    [self updateButtonTitle];
    self.rideStatusButton.layer.cornerRadius = 5.0;
}

- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:animated];
    
    self.rideStatus = None;
    [self updateButtonTitle];
}

- (IBAction)buttonPressed:(id)sender {
    
    if (self.rideStatus == Finished) {
        PaymentVC *paymentVC = [[PaymentVC alloc] initWithNibName:@"PaymentVC" bundle:nil];
        [self.navigationController pushViewController:paymentVC animated:YES];
    }
    
    [self updateRideStatus];
    [self updateButtonTitle];
}

#pragma mark: Custom methods
- (NSString *)getButtonTitle {
    switch (self.rideStatus) {
        case None:
            return @"Start Ride";
            
        case Started:
            return @"In Progress";
            
        case Finished:
            return @"Make Payment";
    }
}

- (void)updateRideStatus {
    switch (self.rideStatus) {
        case None:
            self.rideStatus = Started;
            break;
            
        case Started:
            self.rideStatus = Finished;
            break;
            
        case Finished:
            self.rideStatus = None;
            break;
    }
}

- (void)updateButtonTitle {
    [self.rideStatusButton setTitle:[self getButtonTitle] forState:UIControlStateNormal];
    
    if (self.rideStatus == Started) {
        CABasicAnimation *theAnimation;
        
        theAnimation=[CABasicAnimation animationWithKeyPath:@"opacity"];
        theAnimation.duration=1.0;
        theAnimation.repeatCount=HUGE_VALF;
        theAnimation.autoreverses=YES;
        theAnimation.fromValue=[NSNumber numberWithFloat:1.0];
        theAnimation.toValue=[NSNumber numberWithFloat:0.0];
        [self.rideStatusButton.layer addAnimation:theAnimation forKey:@"animateOpacity"];
        
        dispatch_after(dispatch_time(DISPATCH_TIME_NOW, (int64_t)(5.0 * NSEC_PER_SEC)), dispatch_get_main_queue(), ^{
            self.rideStatus = Finished;
            [self.rideStatusButton.layer removeAnimationForKey:@"animateOpacity"];
            [self updateButtonTitle];
        });
    }
}
@end
