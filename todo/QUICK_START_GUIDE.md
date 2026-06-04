# Quick Start: Create Test Accounts & Improve Frontend

## 🎯 3-Step Quick Start

### Step 1️⃣: Create Test Accounts

```bash
# Navigate to backend
cd backend

# Run the extended seed script
python seed_extended.py
```

**What it does:**
- ✅ Creates 5 additional CUSTOMERS
- ✅ Creates 2 additional SHOP OWNERS
- ✅ Creates 2 additional SHIPPERS
- ✅ Creates 1 MODERATOR/ADMIN
- ✅ Total: 16 test accounts for comprehensive testing

**Output:** List of all new test accounts with credentials

---

### Step 2️⃣: Start the Backend

```bash
# Still in backend directory
uvicorn app.main:socket_app --reload --port 8000
```

**Verify:** Open http://localhost:8000/docs (Swagger API docs)

---

### Step 3️⃣: Start the Frontend

```bash
# In a new terminal, navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Run development server
npm run dev
```

**Verify:** Open http://localhost:5173 and try logging in

---

## 📋 Test Accounts (After Seed)

### Customer Accounts (7 total)
| Email | Password | Notes |
|-------|----------|-------|
| customer1@example.com | Customer@123 | Original - has orders |
| customer2@example.com | Customer@123 | Original |
| customer3@example.com | Customer@123 | **NEW** - Premium user |
| customer4@example.com | Customer@123 | **NEW** - New user |
| customer5@example.com | Customer@123 | **NEW** - Active shopper |
| customer6@example.com | Customer@123 | **NEW** - Bulk buyer |
| customer7@example.com | Customer@123 | **NEW** - Test account |

### Shop Owner Accounts (4 total)
| Email | Shop Name | Password |
|-------|-----------|----------|
| owner1@shop.com | TechWorld Shop | Owner@123 |
| owner2@shop.com | Fashion Hub | Owner@123 |
| owner3@shop.com | Beauty & Care Hub | **NEW** Owner@123 |
| owner4@shop.com | Food & Beverage Store | **NEW** Owner@123 |

### Shipper Accounts (3 total)
| Email | Vehicle | Password |
|-------|---------|----------|
| shipper1@example.com | Xe máy | Shipper@123 |
| shipper2@example.com | **NEW** Xe máy | Shipper@123 |
| shipper3@example.com | **NEW** Xe tải | Shipper@123 |

### Admin / Moderator (2 total)
| Email | Role | Password |
|-------|------|----------|
| admin@example.com | ADMIN | Admin@123 |
| moderator@example.com | **NEW** ADMIN (Moderation) | Moderator@123 |

---

## 🎨 Frontend Improvements Roadmap

### Priority 1: Core Pages (Appearance)
- [ ] **Login Page** - Modern card design, gradient background
- [ ] **Home/Products Grid** - Responsive layout, product cards
- [ ] **Navigation Bar** - Better layout, mobile menu
- [ ] **Product Detail** - Image gallery, specifications

### Priority 2: User Experience
- [ ] **Shopping Cart** - Better visual hierarchy
- [ ] **Checkout Flow** - Step-by-step, form validation
- [ ] **Order History** - Table with filters
- [ ] **Notifications** - Toast messages instead of alerts

### Priority 3: Role-Specific UIs
- [ ] **Seller Dashboard** - Analytics charts
- [ ] **Shipper Panel** - Delivery tracking UI
- [ ] **Admin Panel** - User/shop management tables

### Priority 4: Polish
- [ ] Dark mode toggle
- [ ] Loading skeletons
- [ ] Animations & transitions
- [ ] Mobile responsiveness

---

## 🚀 Recommended Tech Stack

### Install these libraries:
```bash
cd frontend

npm install:
  npm install -D tailwindcss postcss autoprefixer
  npm install react-hot-toast
  npm install recharts
  npm install @hookform/react
  npm install zustand
```

### Already in project:
- Redux Toolkit
- TypeScript
- Vite

---

## 📁 Key Files to Work On

### Frontend Pages to Improve
```
frontend/src/pages/
├── Login.tsx ← Start here (simple, high impact)
├── Home.tsx ← Product grid
├── ProfilePage.tsx ← User account
├── shop/
│   └── ProductDetail.tsx ← Product page
├── buyer/
│   ├── Cart.tsx ← Shopping cart
│   └── Checkout.tsx ← Order placement
├── seller/
│   ├── Dashboard.tsx ← Sales analytics
│   └── Products.tsx ← Inventory
├── admin/
│   └── Dashboard.tsx ← System admin
└── shipper/
    └── Dashboard.tsx ← Delivery tracking
```

### Backend Files Reference
```
backend/
├── seed.py ← Original test accounts
├── seed_extended.py ← NEW - Additional accounts
└── app/
    ├── models/ ← Database schemas
    ├── routes/ ← API endpoints
    └── services/ ← Business logic
```

---

## 💡 Example Task: Improve Login Page

**Current:** Basic form, no styling
**Goal:** Modern login card with gradient background

```typescript
// frontend/src/pages/Login.tsx

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      // API call here
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      
      if (res.ok) {
        const data = await res.json();
        localStorage.setItem('token', data.access_token);
        toast.success('Login successful!');
        navigate('/dashboard');
      } else {
        toast.error('Login failed');
      }
    } catch (error) {
      toast.error('Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-2xl p-8 w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
          Login
        </h1>
        
        <form onSubmit={handleLogin} className="space-y-4">
          {/* Email input */}
          <div>
            <label className="block text-gray-700 font-medium mb-2">
              Email Address
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          {/* Password input */}
          <div>
            <label className="block text-gray-700 font-medium mb-2">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          {/* Login button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition duration-200 disabled:opacity-50"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        {/* Demo accounts */}
        <div className="mt-6 p-4 bg-blue-50 rounded-lg text-sm">
          <p className="font-bold text-gray-700 mb-2">Test Accounts:</p>
          <p className="text-gray-600">customer1@example.com / Customer@123</p>
          <p className="text-gray-600">owner1@shop.com / Owner@123</p>
          <p className="text-gray-600">admin@example.com / Admin@123</p>
        </div>

        {/* Register link */}
        <div className="text-center mt-4">
          <p className="text-gray-600">
            Don't have an account?{' '}
            <a href="/register" className="text-blue-500 hover:underline font-medium">
              Register here
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
```

---

## 🔄 Development Workflow

```mermaid
1. Run seed_extended.py (backend) → Create test accounts
2. Start backend (uvicorn) → API ready on :8000
3. Start frontend (npm run dev) → App ready on :5173
4. Login with test account → Test specific feature
5. Make changes → Auto reload with Vite HMR
6. Verify across all roles → Customer, Seller, Shipper, Admin
```

---

## ✅ Testing Checklist

After creating accounts, test each role:

### As Customer
- [ ] Login works
- [ ] Can browse products
- [ ] Can add to cart
- [ ] Can checkout

### As Shop Owner
- [ ] Login works
- [ ] Can see dashboard
- [ ] Can view orders
- [ ] Can manage products

### As Shipper
- [ ] Login works
- [ ] Can see deliveries
- [ ] Can update status

### As Admin
- [ ] Login works
- [ ] Can access admin panel
- [ ] Can view all users

---

## 📞 Need Help?

### Common Issues:

**Issue:** `python seed_extended.py` fails with "DIRECT_URL not found"
```bash
# Solution: Set environment variables
cd backend
cp .env.example .env
# Edit .env with your DATABASE_URL
python seed_extended.py
```

**Issue:** Frontend won't connect to backend
```bash
# Check: Backend running on port 8000
# Check: VITE_API_URL in frontend/.env.local
VITE_API_URL=http://localhost:8000
```

**Issue:** "Duplicate key value violates unique constraint"
```bash
# Solution: Account already exists, just use it
# Or reset: python seed.py --reset (if implemented)
```

---

## 📚 Documentation Files Created

1. **FRONTEND_TEST_ACCOUNTS_PLAN.md** - Detailed 3-phase plan
2. **TEST_ACCOUNTS_REFERENCE.md** - All account credentials & scenarios
3. **seed_extended.py** - Script to create additional test accounts
4. **QUICK_START_GUIDE.md** - This file (you are here)

---

## 🎯 Next Steps (Today)

1. ✅ Run `python seed_extended.py` - Create 10+ test accounts
2. ✅ Start backend & frontend
3. ✅ Login with different accounts, test each role
4. ✅ Identify which page looks worst (start there)
5. 🔄 Improve Login page UI (Tailwind + gradients)
6. 🔄 Improve Products grid
7. 🔄 Add toast notifications
8. 🔄 Mobile responsiveness

---

Bạn sẵn sàng chưa? 🚀

