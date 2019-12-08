//
//  GroceriesVC.h
//  Grab-payments
//
//  Created by Pavan on 07/12/19.
//  Copyright © 2019 Pavan. All rights reserved.
//

#import <UIKit/UIKit.h>

typedef NS_ENUM(NSInteger, PaymentType) {
    ConfirmMerchant = 0,
    ConfirmBankOtp
};

NS_ASSUME_NONNULL_BEGIN

@interface GroceriesVC : UIViewController
@property (readwrite, nonatomic) PaymentType type;
@end

NS_ASSUME_NONNULL_END
