# Amazon Product Advertising API Setup Guide

## 🔑 Getting Your Amazon API Credentials

### Step 1: Join Amazon Associates Program
1. Visit [Amazon Associates](https://affiliate-program.amazon.com/)
2. Sign up for the Amazon Associates program
3. Complete the application process
4. Wait for approval (can take 24-48 hours)

### Step 2: Register for Product Advertising API
1. Sign in to your Amazon Associates account
2. Go to **Tools** → **Product Advertising API**
3. Click **"Join"** or **"Request Access"**
4. Accept the license agreement
5. Wait for API access approval

### Step 3: Create API Credentials
1. In Associates Central, go to **Tools** → **Product Advertising API**
2. Click **"Manage your credentials"**
3. Click **"Add Credentials"** 
4. Download your credentials (Access Key ID and Secret Access Key)
5. Note your Associate Tag (from your Associates account)

### Step 4: Configure Your Application
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```env
   AMAZON_API_KEY=AKIAIOSFODNN7EXAMPLE
   AMAZON_API_SECRET=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
   AMAZON_ASSOCIATE_TAG=yourtag-20
   AMAZON_COUNTRY=US
   ```

## 🌍 Supported Countries
- **US** - United States (amazon.com)
- **UK** - United Kingdom (amazon.co.uk)
- **DE** - Germany (amazon.de)
- **FR** - France (amazon.fr)
- **IT** - Italy (amazon.it)
- **ES** - Spain (amazon.es)
- **CA** - Canada (amazon.ca)
- **JP** - Japan (amazon.co.jp)
- **IN** - India (amazon.in)
- **BR** - Brazil (amazon.com.br)
- **MX** - Mexico (amazon.com.mx)
- **AU** - Australia (amazon.com.au)

## ⚠️ Important Requirements

### API Access Requirements
- **Active Amazon Associates Account**: Must be approved
- **Sales Threshold**: Some regions require a minimum number of qualifying sales within 180 days
- **Compliance**: Must follow Amazon's operating agreement and content guidelines

### Rate Limits
- **Requests per second**: 1 request per second (enforced by our throttling)
- **Daily requests**: 8,640 requests per day maximum
- **Burst requests**: Up to 10 requests in burst, then back to 1/second

## 🔧 Installation & Testing

### Install Dependencies
```bash
cd backend
pip install -r enhanced_requirements.txt
```

### Test API Connection
```bash
python3 -c "from amazon_api import amazon_api; print(amazon_api.get_api_status())"
```

### Run Enhanced Backend
```bash
python3 enhanced_api.py
```

## 📊 Monitoring & Debugging

### Check API Status
Visit: `http://localhost:8000/amazon-status`

### View Logs
The application logs all API calls, errors, and performance metrics.

### Common Issues

1. **"Credentials not found"**
   - Ensure `.env` file exists with correct credentials
   - Check environment variable names

2. **"Access denied"**
   - Verify Associate Tag is correct
   - Ensure API access is approved
   - Check if account meets sales requirements

3. **"Rate limited"**
   - Our throttling prevents this, but if it occurs, increase `API_THROTTLE_DELAY`

4. **"No products found"**
   - Try broader search terms
   - Check if budget range is reasonable
   - Verify country marketplace has relevant products

## 🚀 Production Deployment

### Environment Variables for Production
```bash
export AMAZON_API_KEY="your_key"
export AMAZON_API_SECRET="your_secret"
export AMAZON_ASSOCIATE_TAG="your_tag"
export AMAZON_COUNTRY="US"
```

### Security Best Practices
- Never commit `.env` files to version control
- Use secure environment variable management in production
- Rotate credentials periodically
- Monitor API usage and costs

## 💰 Monetization

With Amazon Associates integration:
- Earn 1-10% commission on qualifying purchases
- Track clicks and conversions through your Associate Tag
- Access detailed reporting in Associates Central

## 📚 Additional Resources

- [Amazon PA-API Documentation](https://webservices.amazon.com/paapi5/documentation/)
- [Associates Program Policies](https://affiliate-program.amazon.com/help/operating)
- [API Best Practices](https://webservices.amazon.com/paapi5/documentation/best-practices.html)
- [Troubleshooting Guide](https://webservices.amazon.com/paapi5/documentation/troubleshooting.html)
