# Payment Flow Test Instructions

## Test Case 1: Razorpay Payment
1. Add items to basket
2. Go to checkout → shipping address → shipping method → payment details
3. Select "Online Payment (Razorpay)" 
4. Click "Pay Now" and complete payment with test card
5. Should redirect to preview page and show successful payment
6. Click "Place Order" - should complete successfully

## Test Case 2: Cash on Delivery (COD)
1. Add items to basket
2. Go to checkout → shipping address → shipping method → payment details
3. Select "Cash on Delivery (COD)"
4. Click "Continue to Review Order"
5. Should redirect to preview page showing COD method
6. Click "Place Order" - should complete successfully

## Test Case 3: Razorpay without payment
1. Add items to basket
2. Go to checkout → shipping address → shipping method → payment details
3. Select "Online Payment (Razorpay)" 
4. Do NOT click "Pay Now" - instead manually navigate to preview
5. Should show error message indicating payment is required

## Expected Behavior:
- Payment method selection should persist during checkout
- COD orders should complete without payment ID
- Razorpay orders should require valid payment ID
- Preview page should show correct payment method
- No more "The id provided does not exist" errors