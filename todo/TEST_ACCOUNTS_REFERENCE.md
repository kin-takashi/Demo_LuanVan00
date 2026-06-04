# Test Accounts Reference Guide

## 🎯 Quick Login Credentials

### Original Test Accounts (from seed.py)
```
✅ ADMIN
   Email: admin@example.com
   Password: Admin@123
   Phone: 0123456789
   Address: 123 Admin Street

✅ SHOP OWNER #1
   Email: owner1@shop.com
   Password: Owner@123
   Phone: 0987654321
   Shop: TechWorld Shop (Tech products)

✅ SHOP OWNER #2
   Email: owner2@shop.com
   Password: Owner@123
   Phone: 0912345678
   Shop: Fashion Hub (Clothing & fashion)

✅ SHIPPER #1
   Email: shipper1@example.com
   Password: Shipper@123
   Phone: 0901234567
   Vehicle: Xe máy

✅ CUSTOMER #1
   Email: customer1@example.com
   Password: Customer@123
   Phone: 0945678901
   Has: Orders, Reviews, Cart

✅ CUSTOMER #2
   Email: customer2@example.com
   Password: Customer@123
   Phone: 0956789012
```

---

## 🆕 Extended Test Accounts (from seed_extended.py)

### Additional Customers (5 more)
```
👤 CUSTOMER #3 (Premium)
   Email: customer3@example.com
   Password: Customer@123
   Phone: 0967890123
   Address: 404 VIP Lane, Q7, TP.HCM

👤 CUSTOMER #4 (New User)
   Email: customer4@example.com
   Password: Customer@123
   Phone: 0978901234
   Address: 505 New Street, Q4, TP.HCM

👤 CUSTOMER #5 (Active Shopper)
   Email: customer5@example.com
   Password: Customer@123
   Phone: 0989012345
   Address: 606 Active Avenue, Q5, TP.HCM

👤 CUSTOMER #6 (Bulk Buyer)
   Email: customer6@example.com
   Password: Customer@123
   Phone: 0990123456
   Address: 707 Bulk Street, Q8, TP.HCM

👤 CUSTOMER #7 (Test Account)
   Email: customer7@example.com
   Password: Customer@123
   Phone: 0901234567
   Address: 808 Test Lane, Q9, TP.HCM
```

### Additional Shop Owners (2 more)
```
🏪 SHOP OWNER #3 (Beauty & Care)
   Email: owner3@shop.com
   Password: Owner@123
   Phone: 0923456789
   Shop: Beauty & Care Hub
   Category: Cosmetics & skincare
   Address: 901 Beauty Street, Q2, TP.HCM

🏪 SHOP OWNER #4 (Food & Beverage)
   Email: owner4@shop.com
   Password: Owner@123
   Phone: 0934567890
   Shop: Food & Beverage Store
   Category: Food & drinks
   Address: 1002 Food Lane, Q6, TP.HCM
```

### Additional Shippers (2 more)
```
🚚 SHIPPER #2
   Email: shipper2@example.com
   Password: Shipper@123
   Phone: 0912345670
   Vehicle: Xe máy (motorcycle)
   Address: 110 Shipper Ave, Q8, TP.HCM
   Rating: 4.5 ⭐

🚚 SHIPPER #3 (Bulk Delivery)
   Email: shipper3@example.com
   Password: Shipper@123
   Phone: 0901234568
   Vehicle: Xe tải (truck)
   Address: 120 Truck Street, Q9, TP.HCM
   Rating: 4.8 ⭐
```

### Moderator / Content Manager
```
🛡️  MODERATOR
   Email: moderator@example.com
   Password: Moderator@123
   Phone: 0901112233
   Role: ADMIN (moderation permissions)
   Address: 200 Mod Street, Q1, TP.HCM
   Purpose: Content moderation, dispute handling
```

---

## 📊 Test Account Summary

| Role | Count | For Testing |
|------|-------|------------|
| ADMIN | 2 | System management, moderation |
| SHOP_OWNER | 4 | Seller dashboard, product management |
| SHIPPER | 3 | Delivery tracking, status updates |
| CUSTOMER | 7 | Shopping, checkout, reviews, wishlists |
| **TOTAL** | **16** | **Full e-commerce workflow** |

---

## 🎭 Testing Scenarios by Role

### As a CUSTOMER
```
1. Browse products by category
2. Search products
3. View product details
4. Add to cart
5. Apply vouchers/discounts
6. Checkout with different payment methods
7. Track order status
8. Leave product review
9. Check order history
10. Manage wishlist
```

### As a SHOP OWNER
```
1. Login to seller dashboard
2. View shop analytics
3. Manage product inventory
4. Add/edit products
5. View orders from customers
6. Update order status
7. Manage promotions/vouchers
8. View shop reviews & ratings
9. Handle customer disputes
10. Export sales reports
```

### As a SHIPPER
```
1. Login to shipper dashboard
2. View assigned deliveries
3. Update delivery status
4. Input location/coordinates
5. Mark delivery as completed
6. View earnings/statistics
7. Manage availability
8. View customer feedback
9. Check route optimization
10. Report issues with delivery
```

### As an ADMIN
```
1. View system analytics
2. Manage users (approve/ban)
3. Approve shops for operation
4. Handle disputes/complaints
5. Manage promotions/vouchers
6. View financial reports
7. Monitor seller activities
8. Content moderation
9. System logs & audit trail
10. Configure platform settings
```

---

## 🚀 How to Use

### Setup (First Time)

```bash
# 1. Go to backend directory
cd backend

# 2. Run original seed
python seed.py

# 3. Run extended seed (adds new accounts)
python seed_extended.py

# 4. Start backend
uvicorn app.main:socket_app --reload --port 8000
```

### Login to Frontend

```bash
# 1. Go to frontend directory
cd frontend

# 2. Install & run
npm install
npm run dev

# 3. Open browser: http://localhost:5173
# 4. Click Login
# 5. Use any credentials from above
```

### Test Specific Feature

**Example: Test Customer Checkout**
```
1. Login as: customer3@example.com / Customer@123
2. Browse products (TechWorld Shop or Fashion Hub)
3. Add items to cart
4. Go to checkout
5. Fill shipping address
6. Select payment method
7. Apply voucher (SUMMER2024, FLASH50K, WELCOME10, etc.)
8. Place order
9. See order confirmation
10. Go to Orders page, see status updates
```

**Example: Test Seller Dashboard**
```
1. Login as: owner1@shop.com / Owner@123
2. Go to Seller Dashboard
3. View sales analytics
4. See recent orders
5. Update order status (pending → confirmed → shipped → delivered)
6. Check shop ratings/reviews
7. Manage products
8. View earnings
```

---

## 💾 Sample Data Created

### Products
- TechWorld Shop (Electronics)
  - Tai nghe không dây (Wireless earbuds) - 1.5M VND
  - Cáp USB-C (USB-C cable) - 150K VND
  - Ốp lưng điện thoại (Phone case) - 200K VND
  - Bàn phím cơ (Mechanical keyboard) - 2.5M VND

- Fashion Hub (Clothing)
  - Áo thun cotton (Cotton t-shirt) - 250K VND
  - Quần jeans (Jeans) - 500K VND
  - Váy hoa nhí (Floral dress) - 350K VND
  - Áo khoác dù (Windbreaker) - 750K VND

### Vouchers (Promotional codes)
- `SUMMER2024` - 20% discount
- `FLASH50K` - 50K VND fixed
- `WELCOME10` - 10% discount
- `VIP100K` - 100K VND fixed
- `NEWYEAR30` - 30% discount (inactive)

### Orders (Sample)
- 5 orders from customer1 with different statuses
  - 1 delivered
  - 1 pending
  - 1 shipped
  - 1 confirmed
  - 1 delivered

---

## ✅ Verification

After running seeds, verify in browser:

```bash
# Check API docs
http://localhost:8000/docs

# Try login endpoint
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer1@example.com",
    "password": "Customer@123"
  }'

# Should return JWT token + user info
```

---

## 🔐 Security Notes

- ⚠️  These are TEST ACCOUNTS ONLY
- Do NOT use in production
- Passwords are simple for testing (should be stronger in prod)
- All phone numbers are fake/test data
- All addresses are fictitious

---

## 📝 Notes

- Each time you run `seed.py` or `seed_extended.py`, they check for duplicates
- Running multiple times is safe (won't create duplicates)
- To reset: Drop all tables and re-run seeds
- For database reset: `alembic downgrade base` then `alembic upgrade head`

---

## 🆘 Troubleshooting

**Issue: "User already exists" error**
- Solution: The account was already created. Just use the existing credentials.

**Issue: Can't login**
- Check: Email is spelled correctly
- Check: Password is exactly as shown (case-sensitive)
- Check: Backend is running on port 8000
- Check: Database is connected properly

**Issue: Shop products not showing**
- Run: `python seed.py` first to create products
- Check: Products have "active" status
- Check: Shop has "approved" verification_status

**Issue: Can't create new account via API**
- Check: Email doesn't already exist
- Check: Password meets requirements
- Check: Backend is accepting connections

