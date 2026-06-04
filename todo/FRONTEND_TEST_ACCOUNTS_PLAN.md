# Plan: Tạo Tài Khoản Test & Cải Thiện Frontend

## 📋 Tóm Tắt Project

**Tên:** E-Commerce Platform (Shopee Clone)
**Tech Stack:**
- Frontend: React 18 + TypeScript + Vite
- Backend: FastAPI (Python)
- Database: PostgreSQL (Supabase)
- Roles: Admin, Shop Owner, Shipper, Customer

---

## 🎯 Phase 1: Tạo Tài Khoản Test Bổ Sung

### Tài Khoản Hiện Có (seed.py)
```
✅ admin@example.com / Admin@123 (ADMIN)
✅ owner1@shop.com / Owner@123 (SHOP_OWNER)
✅ owner2@shop.com / Owner@123 (SHOP_OWNER)
✅ shipper1@example.com / Shipper@123 (SHIPPER)
✅ customer1@example.com / Customer@123 (CUSTOMER)
✅ customer2@example.com / Customer@123 (CUSTOMER)
```

### Tài Khoản Cần Thêm Cho Frontend Testing

#### Nhóm Customer (Người mua)
```
👤 customer3@example.com / Customer@123
   - Full Name: Customer 3 (Premium)
   - Mục đích: Test VIP customer, discount tiers
   - Phone: 0967890123, Address: 404 VIP Lane, Q7, TP.HCM

👤 customer4@example.com / Customer@123
   - Full Name: Customer 4 (New User)
   - Mục đích: Test onboarding, first purchase flow
   - Phone: 0978901234, Address: 505 New Street, Q4, TP.HCM

👤 customer5@example.com / Customer@123
   - Full Name: Customer 5 (Active Shopper)
   - Mục đích: Test repeat purchases, wishlist, reviews
   - Phone: 0989012345, Address: 606 Active Avenue, Q5, TP.HCM
```

#### Nhóm Shop Owner (Người bán)
```
👤 owner3@shop.com / Owner@123
   - Full Name: Shop Owner 3
   - Shop Name: Beauty & Care Hub
   - Mục đích: Test beauty shop, product management
   - Phone: 0923456789, Address: 901 Beauty Street, Q2, TP.HCM

👤 owner4@shop.com / Owner@123
   - Full Name: Shop Owner 4
   - Shop Name: Food & Beverage Store
   - Mục đích: Test food shop, special categories
   - Phone: 0934567890, Address: 1002 Food Lane, Q6, TP.HCM
```

#### Nhóm Shipper (Người giao hàng)
```
👤 shipper2@example.com / Shipper@123
   - Full Name: Shipper 2
   - Vehicle: Xe máy
   - Mục đích: Test multiple shipper scenarios
   - Phone: 0912345670, Address: 110 Shipper Ave, Q8, TP.HCM

👤 shipper3@example.com / Shipper@123
   - Full Name: Shipper 3
   - Vehicle: Xe tải
   - Mục đích: Test bulk delivery
   - Phone: 0901234568, Address: 120 Truck Street, Q9, TP.HCM
```

#### Admin Bổ Sung
```
👤 moderator@example.com / Moderator@123
   - Full Name: Content Moderator
   - Role: ADMIN (với quyền moderation)
   - Mục đích: Test moderation UI, dispute management
   - Phone: 0901112233, Address: 200 Mod Street, Q1, TP.HCM
```

---

## 🔧 Phase 2: Cách Tạo Tài Khoản

### Cách 1: Chỉnh Sửa seed.py (Khuyên dùng)
```bash
# 1. Mở backend/seed.py
# 2. Thêm các account vào users_data (line ~105)
# 3. Thêm shop vào shops_data (line ~198) nếu là owner
# 4. Gán role tại role_map (line ~146)

# Chạy seed
cd backend
python seed.py
```

### Cách 2: Tạo Bằng API
```bash
# Register user
curl -X POST http://localhost:8000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "Password@123",
    "full_name": "New User",
    "phone": "0901234567"
  }'

# Login để lấy token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "Password@123"
  }'
```

### Cách 3: Tạo Trực Tiếp Database
```bash
# SSH vào Supabase hoặc local DB, chạy SQL:
INSERT INTO users (email, password_hash, full_name, phone, address, status)
VALUES (
  'email@example.com',
  '$2b$12$...', -- bcrypt hash của password
  'Full Name',
  '0901234567',
  'Address',
  'active'
);

-- Gán role
INSERT INTO user_roles (user_id, role_id, current_role, status)
VALUES ((SELECT user_id FROM users WHERE email='email@example.com'), 5, true, 'active');
```

---

## 🎨 Phase 3: Cải Thiện Frontend (UI/UX)

### A. Login & Register Page
```typescript
// Frontend/src/pages/Login.tsx
✅ Cần:
  - Modern design (Tailwind/Material UI)
  - Form validation tốt
  - Loading state + error handling
  - "Remember me" option
  - Social login (future: Google, Facebook)
  - Forgot password link
  
❌ Cần Cải:
  - Add background gradient/image
  - Smooth animations khi load
  - Toast notifications instead of alerts
  - Mobile responsive (mobile-first)
```

### B. Home Page / Products Listing
```typescript
// Frontend/src/pages/Home.tsx
✅ Cần:
  - Product grid responsive (3-4 columns)
  - Product card design: image + rating + price
  - Filter & sort options
  - Search bar sticky
  - Pagination / infinite scroll
  
❌ Cần Cải:
  - Product images từ Supabase Storage
  - Star rating display
  - Hover effects (add to cart)
  - Sale badge for discounted products
  - Skeleton loading
```

### C. Navigation & Layout
```typescript
// Frontend/src/components/
✅ Cần:
  - Responsive navbar (hamburger menu for mobile)
  - User avatar dropdown menu
  - Shopping cart icon with badge count
  - Breadcrumb navigation
  
❌ Cần Cải:
  - Dark mode toggle
  - Search dropdown (recent searches)
  - Notification bell icon
  - Side categories menu
  - Sticky header
```

### D. Product Detail Page
```typescript
// Frontend/src/pages/shop/ProductDetail.tsx
✅ Cần:
  - Image gallery (thumbnail + main)
  - Product info: name, price, rating, reviews
  - Quantity selector
  - Add to cart / Buy now buttons
  - Similar products section
  
❌ Cần Cải:
  - Image zoom on hover
  - Reviews section with filter
  - Specification tabs
  - Share product (social)
  - Video demo (if available)
```

### E. Shopping Cart
```typescript
// Frontend/src/pages/buyer/Cart.tsx
✅ Cần:
  - Cart items list
  - Quantity adjustment
  - Remove item
  - Checkout button
  
❌ Cần Cải:
  - Empty cart state (nice illustration)
  - Price breakdown (subtotal, shipping, tax, discount)
  - Coupon input
  - Saved items / wishlist
  - Continue shopping button
```

### F. Seller Dashboard
```typescript
// Frontend/src/pages/seller/Dashboard.tsx
✅ Cần:
  - Sales summary (today, week, month)
  - Orders list
  - Product management
  - Analytics charts
  
❌ Cần Cải:
  - Revenue trend chart (Chart.js/Recharts)
  - Top products by sales
  - Customer feedback insights
  - Quick stats cards (responsive)
  - Inventory warnings
```

### G. Admin Panel
```typescript
// Frontend/src/pages/admin/Dashboard.tsx
✅ Cần:
  - User management table
  - Shop approval system
  - Dispute/complaint handling
  - System analytics
  
❌ Cần Cải:
  - Searchable data tables
  - Bulk actions (approve/reject)
  - Date range filters
  - Export to CSV
  - Real-time updates via WebSocket
```

---

## 🎯 Priority 1: Giao Diện Cơ Bản

### 1. Login Page
- [ ] Modern card layout with gradient background
- [ ] Email + Password inputs with icons
- [ ] Forgot password & Register links
- [ ] Remember me checkbox
- [ ] Submit button with loading state
- [ ] Show password toggle

### 2. Products Grid
- [ ] Responsive grid (4 cols desktop, 2 cols tablet, 1 col mobile)
- [ ] Product cards with image, rating, price
- [ ] Add to cart button on hover
- [ ] Sale badge for discounts
- [ ] Loading skeleton

### 3. Navigation
- [ ] Logo + branding
- [ ] Search bar
- [ ] Categories dropdown
- [ ] User menu
- [ ] Cart badge with count
- [ ] Mobile hamburger menu

---

## 🎯 Priority 2: Rich Features

### 1. Product Page
- [ ] Image gallery with thumbnails
- [ ] Star rating + review count
- [ ] Product specifications
- [ ] Similar products carousel
- [ ] Reviews section

### 2. Checkout Flow
- [ ] Shipping address form
- [ ] Shipping method selection
- [ ] Payment method selection
- [ ] Order summary
- [ ] Place order confirmation

### 3. Seller Dashboard
- [ ] Sales chart (Chart.js)
- [ ] Recent orders table
- [ ] Top products stats
- [ ] Revenue breakdown

---

## 📊 Recommended Libraries

```bash
npm install:
  - tailwindcss          (styling)
  - shadcn/ui           (component library)
  - react-hot-toast     (notifications)
  - react-query         (data fetching)
  - recharts            (charts)
  - zustand             (state management)
  - axios               (HTTP client)
```

---

## 🚀 Implementation Order

### Week 1
1. ✅ Create test accounts (all roles)
2. ⬜ Improve Login page UI
3. ⬜ Fix responsive navbar
4. ⬜ Create product grid component

### Week 2
5. ⬜ Product detail page
6. ⬜ Shopping cart improvements
7. ⬜ Checkout flow
8. ⬜ Add toast notifications

### Week 3
9. ⬜ Seller dashboard UI
10. ⬜ Admin panel basic layout
11. ⬜ Add charts for analytics
12. ⬜ Mobile optimization

---

## 🔗 Files to Update

```
backend/
├── seed.py ← Thêm new accounts ở đây

frontend/src/
├── pages/
│   ├── Login.tsx ← Cải thiện UI
│   ├── Home.tsx ← Better product grid
│   └── ...
├── components/
│   ├── Navbar.tsx ← Responsive design
│   ├── ProductCard.tsx ← New component
│   └── ...
└── styles/
    └── globals.css ← Tailwind config
```

---

## ✅ Checklist

- [x] Phân tích project structure
- [x] Xác định test accounts cần thêm
- [x] Tạo kế hoạch UI/UX improvements
- [ ] Cập nhật seed.py với new accounts
- [ ] Chạy seed & verify accounts
- [ ] Bắt đầu cải thiện Login page
- [ ] Test từng role (Customer, Seller, Shipper, Admin)
- [ ] Deploy changes

---

## 💡 Tips

- Luôn test với tất cả roles (khác nhau có khác nhau permissions)
- Dùng Chrome DevTools để debug responsive design
- Mock data trong API responses (CORS issues) nếu cần
- Use Tailwind CSS utility classes for quick prototyping
- Implement dark mode từ sớm (toggle in navbar)

