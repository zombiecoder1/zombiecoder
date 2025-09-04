# 🧟 Cursor Editor Test Queries
## লোকাল ZombieCoder vs ক্লাউড পার্থক্য টেস্ট

### 🎯 টেস্ট উদ্দেশ্য
এই কুয়েরিগুলো চালিয়ে দেখতে হবে:
1. **গতি**: লোকাল কত দ্রুত রেসপন্স দেয়
2. **কনটেক্সট**: বেঙ্গলি-ইংলিশ মিক্সড কত ভালো হ্যান্ডল করে
3. **লিমিট**: কোনো কোটা/রেট লিমিট আছে কিনা
4. **ক্যাপাবিলিটি**: 14টি ক্যাপাবিলিটি সব কাজ করছে কিনা

---

## 🔥 Level 1: Basic Functionality Test

### Test 1: Simple Code Generation
```
ভাই, একটা Python function লিখো যেটা:
- দুটো সংখ্যা নিয়ে যোগফল বের করবে
- বেঙ্গলি কমেন্ট দিয়ে
- error handling থাকবে
```

**Expected**: দ্রুত রেসপন্স, বেঙ্গলি কমেন্ট, সম্পূর্ণ ফাংশন

### Test 2: Bengali-English Mixed Query
```
Create a React component for a "বাংলা-ইংরেজি মিক্সড" language switcher. 
The component should:
- টগল between বাংলা and English
- Store preference in localStorage
- Show current language status
```

**Expected**: পারফেক্ট মিক্সড ল্যাঙ্গুয়েজ হ্যান্ডলিং

### Test 3: Complex Architecture Question
```
ভাই, একটা e-commerce system এর architecture design করো:
- Microservices approach
- Database design (SQL + NoSQL)
- API structure
- Security considerations
- Performance optimization
```

**Expected**: বিস্তারিত আর্কিটেকচার, সব ক্যাপাবিলিটি ব্যবহার

---

## 🚀 Level 2: Advanced Capability Test

### Test 4: Bug Hunting
```
এই JavaScript code এ bug আছে, খুঁজে বের করো:

function calculateTotal(items) {
    let total = 0;
    for (let i = 0; i <= items.length; i++) {
        total += items[i].price;
    }
    return total;
}

const products = [
    {name: "ল্যাপটপ", price: 50000},
    {name: "মাউস", price: 500}
];

console.log(calculateTotal(products));
```

**Expected**: Array index out of bounds bug detect, fix suggest

### Test 5: Performance Optimization
```
এই Python code optimize করো:

def find_duplicates(arr):
    duplicates = []
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] == arr[j]:
                duplicates.append(arr[i])
    return duplicates

# Test with large array
data = [1, 2, 3, 4, 5] * 1000
result = find_duplicates(data)
```

**Expected**: O(n²) থেকে O(n) optimization, set/dict ব্যবহার

### Test 6: Security Analysis
```
এই SQL query তে security issue আছে কিনা check করো:

def get_user_data(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return database.execute(query)

# Usage
user_data = get_user_data(request.GET['id'])
```

**Expected**: SQL injection vulnerability detect, prepared statement suggest

---

## 🎨 Level 3: Creative & Context Test

### Test 7: Bengali Context Understanding
```
ভাই, একটা "বাংলা রেসিপি ম্যানেজার" app এর জন্য:
- Database schema design করো
- API endpoints define করো
- Frontend component structure করো
- Bengali text handling strategy করো
```

**Expected**: বাংলা টেক্সট হ্যান্ডলিং, cultural context understanding

### Test 8: Real-time System Design
```
একটা "লাইভ স্টক প্রাইস ট্র্যাকার" system design করো:
- WebSocket connection
- Real-time data processing
- User notification system
- Performance monitoring
```

**Expected**: Real-time architecture, WebSocket implementation

### Test 9: DevOps & Deployment
```
এই Node.js app কে production এ deploy করার জন্য:
- Docker configuration
- CI/CD pipeline
- Environment variables
- Monitoring setup
- Backup strategy
```

**Expected**: Complete DevOps pipeline, production-ready setup

---

## 🔍 Level 4: Stress Test

### Test 10: Multiple Rapid Queries
```
একসাথে ৫টা কুয়েরি করো:
1. একটা sorting algorithm implement করো
2. Database indexing strategy explain করো  
3. CSS Grid vs Flexbox difference বলো
4. Python decorator example দাও
5. API rate limiting implement করো
```

**Expected**: সব কুয়েরির দ্রুত রেসপন্স, কোনো rate limiting না

### Test 11: Long Context Test
```
একটা complete "বাংলা ব্লগ প্ল্যাটফর্ম" build করো:
- User authentication system
- Post creation and editing
- Comment system
- Search functionality
- Admin dashboard
- Bengali text processing
- Image upload
- SEO optimization
- Performance optimization
- Security measures
```

**Expected**: বিস্তারিত implementation, সব feature cover

---

## 📊 Performance Monitoring

### Response Time Test
```
এই কুয়েরিগুলো চালিয়ে response time measure করো:

1. Simple query: "Hello world in Python"
2. Medium query: "Create a todo app"
3. Complex query: "Design a social media platform"
4. Bengali query: "বাংলা টেক্সট প্রসেসিং system"
```

**Expected**: সব কুয়েরি < 2 seconds, consistent performance

### Context Retention Test
```
1. "My name is সাহন, I'm a developer"
2. "What's my name?"
3. "Create a function for me"
4. "What's my profession?"
```

**Expected**: Context retention, personalization

---

## 🎯 Success Criteria

### ✅ লোকাল ZombieCoder Success Indicators:
- **গতি**: সব রেসপন্স < 2 seconds
- **কনটেক্সট**: বেঙ্গলি-ইংলিশ পারফেক্ট মিক্স
- **ক্যাপাবিলিটি**: সব 14টি capability কাজ করে
- **লিমিট**: কোনো rate limiting নেই
- **পার্সোনালিটি**: "ভাই" style friendly responses
- **মেমরি**: Context retention works

### ❌ ক্লাউড Fallback Indicators:
- **গতি**: > 5 seconds response time
- **লিমিট**: "Rate limit exceeded" errors
- **কনটেক্সট**: শুধু ইংরেজি responses
- **ক্যাপাবিলিটি**: Limited functionality
- **পার্সোনালিটি**: Generic responses

---

## 🚨 Troubleshooting

### যদি ক্লাউডে যেতে চায়:
```bash
# Check network connections
netstat -tulpn | grep cursor

# Verify hosts file
cat /etc/hosts | grep -E "(openai|anthropic|huggingface|bedrock|google)"

# Restart Cursor
pkill -f cursor
cursor &
```

### যদি লোকাল রেসপন্স না দেয়:
```bash
# Check ZombieCoder services
curl -s http://localhost:12345/status
curl -s http://localhost:8002/verify

# Restart services
cd /home/sahon/Desktop/zombiecoder
./COMPLETE_SYSTEM_LAUNCHER.sh
```

---

## 🎉 Final Verification

### Complete System Test
```
ভাই, তুমি কি সম্পূর্ণ লোকাল ZombieCoder Agent?
- তোমার নাম কি?
- তুমি কোন port এ চলছো?
- তুমি কতগুলো capability আছে?
- তুমি কি ক্লাউডে যেতে পারো?
- তুমি কি বেঙ্গলি-ইংলিশ মিক্স করতে পারো?
```

**Expected Response**:
```json
{
  "name": "ZombieCoder Agent (সাহন ভাই)",
  "port": 12345,
  "capabilities": 14,
  "cloud_access": false,
  "language": "bengali_english_mixed",
  "status": "fully_local"
}
```

---

## 🔥 Pro Tips

1. **গতি টেস্ট**: Stopwatch দিয়ে measure করো
2. **কনটেক্সট টেস্ট**: বেঙ্গলি-ইংলিশ মিক্স করো
3. **লিমিট টেস্ট**: একসাথে অনেক কুয়েরি করো
4. **ক্যাপাবিলিটি টেস্ট**: সব ধরনের কাজ করো
5. **মেমরি টেস্ট**: আগের কথা মনে রাখে কিনা

**ভাই, এই টেস্টগুলো চালিয়ে দেখো - তুমি পার্থক্য টের পাবে!** 🧟‍♂️
