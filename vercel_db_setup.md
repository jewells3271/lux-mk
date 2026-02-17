# Database Connection String for Vercel

Vercel **does not** create a database for you (unless you add a marketplace integration). 
We will use your **Hostinger MySQL** database.

## Your Connection String
Based on your credentials:

`DATABASE_URL="mysql+pymysql://u649168233_lux:Revolution_100@sql.freedb.tech/u649168233_revolution"`

**IMPORTANT:** 
1. Replace `sql.freedb.tech` with your **actual Hostinger MySQL Host** (e.g., `mysql.hostinger.com`).
2. **Add this to Vercel:**
   - Go to Project Settings -> Environment Variables.
   - Key: `DATABASE_URL`
   - Value: (The string above)
   - Click **Save**.
