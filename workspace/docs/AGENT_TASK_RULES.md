# 🧟 Zombie Agent Core Instructions

## 1️⃣ ফাইল–ফোল্ডার অর্গানাইজেশন

### **মূল নিয়ম:**
* প্রতিটি প্রজেক্টের জন্য আলাদা **মূল ফোল্ডার** তৈরি করতে হবে
* **memory/**, **agents/**, **logs/**, **reports/**, **tests/** — এই বেস ফোল্ডারগুলো না থাকলে সাথে সাথে বানাবে
* ডকুমেন্টেশন ফাইল সব **memory/**-এর ভেতর রাখতে হবে
* টেস্ট–রিলেটেড ফাইল সব **tests/**-এ যাবে
* লগ সব **logs/**-এ যাবে
* রিপোর্ট সব **reports/**-এ যাবে
* এজেন্ট কনফিগ ফাইলগুলো **agents/config/**-এ যাবে

### **ফোল্ডার স্ট্রাকচার:**
```
project-root/
├── memory/           # সব ডকুমেন্টেশন
├── agents/           # এজেন্ট সিস্টেম
│   └── config/       # এজেন্ট কনফিগ
├── logs/             # সব লগ ফাইল
├── reports/          # জেনারেটেড রিপোর্ট
├── tests/            # টেস্ট ফাইল
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── README.md         # প্রজেক্ট লেভেল README
```

---

## 2️⃣ প্রয়োজনীয় ফাইল তৈরি

### **অবশ্যই থাকতে হবে:**
* **README.md** → প্রজেক্ট লেভেলে অবশ্যই থাকবে
* **AGENT_START.md** → Zero Tolerance Rules থাকবে
* **AGENT_WORKFLOW.md** → Workflow system থাকবে
* **AGENT_TASK_RULES.md** → এই ফাইল (নিয়ম-কানুন)
* **FINAL_AGENT_SETUP_REPORT.md** → ফাইনাল রিপোর্ট এখানে সেভ হবে

### **ফাইল তৈরি করার নিয়ম:**
* প্রতিটি ফাইল meaningful নাম দিতে হবে
* ফাইলের ভেতরে proper documentation থাকবে
* Empty ফাইল রাখা যাবে না - অন্তত basic content থাকতে হবে
* প্রতিটি ফাইল proper permissions দিতে হবে

---

## 3️⃣ ডিপেন্ডেন্সি ইন্সটল

### **ইন্সটল করার নিয়ম:**
* সব প্রয়োজনীয় লাইব্রেরি `config.yaml` থেকে পড়ে ইন্সটল করতে হবে
* যেসব প্যাকেজ ইনস্টল করা আছে কিন্তু **ব্যবহার হচ্ছে না** → সরিয়ে ফেলতে হবে
* যেসব প্যাকেজ দরকার কিন্তু **ইন্সটল হয়নি** → সাথে সাথে ইন্সটল করবে

### **ডিপেন্ডেন্সি চেক:**
```bash
# Check installed packages
pip3 list

# Check requirements
cat requirements.txt

# Install missing packages
pip3 install -r requirements.txt

# Remove unused packages
pip3 uninstall package_name
```

---

## 4️⃣ অর্গানাইজেশন রুলস

### **ফাইল ম্যানেজমেন্ট:**
* **অপ্রয়োজনীয় ফাইল/ফোল্ডার** → ডিলিট করবে
* **কার্যকর কিন্তু অগোছালো ফাইল** → সঠিক ফোল্ডারে সরাবে
* **ডুপ্লিকেট ফাইল** → চেক করে একটাই কপি রাখবে
* প্রতিটি কাজের পর **লগ আপডেট** করতে হবে

### **ফাইল চেকলিস্ট:**
- [ ] All files in correct folders
- [ ] No duplicate files
- [ ] No unnecessary files
- [ ] Proper file permissions
- [ ] Logs updated

---

## 5️⃣ রিপোর্টিং

### **রিপোর্ট ফরম্যাট (Copy-Paste Ready):**
```
🧟 Agent Report
===============
Agent: <Agent Name>
Task: <Task Description>
Status: ✅ Completed / ❌ Failed
Memory: Updated (file_name.md)
Commit: <Git commit hash>
Next: Ready for next task
Notes: <Any observations or issues>

কলিজা, রিপোর্ট শেষ। আমাদের পথ ঠিক আছে কিনা বলো।
```

### **রিপোর্ট করার নিয়ম:**
* প্রতিটি কাজ শেষে অবশ্যই রিপোর্ট করতে হবে
* রিপোর্ট স্পষ্ট এবং concise হতে হবে
* Status সঠিকভাবে mention করতে হবে
* Next task কি হবে তা বলে দিতে হবে

---

## 6️⃣ কোয়ালিটি স্ট্যান্ডার্ড

### **কোড কোয়ালিটি:**
* Clean, readable code
* Proper error handling
* Documentation comments
* Test coverage

### **ডকুমেন্টেশন কোয়ালিটি:**
* Clear commit messages
* Updated memory files
* Proper file organization
* Status reports

### **কমিউনিকেশন কোয়ালিটি:**
* Regular status updates
* Clear problem reporting
* Collaborative approach
* Respectful tone

---

## 7️⃣ ইমার্জেন্সি প্রসিডিউর

### **সিস্টেম ডাউন:**
1. Check logs immediately
2. Report to Zombie Leader
3. Follow recovery procedures
4. Document incident

### **টাস্ক ফেইলিউর:**
1. Stop current task
2. Analyze failure cause
3. Report with details
4. Wait for instructions

### **মেমোরি করাপশন:**
1. Backup current state
2. Restore from last known good
3. Report corruption details
4. Rebuild if necessary

---

## 8️⃣ জিরো টলারেন্স রুলস

### **নো ফেক ওয়ার্ক:**
* শুধু লগ-আপডেট লিখলেই হবে না
* আসল ফাইল/ফোল্ডার থাকতে হবে
* প্রতিটি কাজের প্রমাণ থাকতে হবে

### **ফোল্ডার ডিসিপ্লিন:**
* Test ফাইল → `tests/`
* Docs → `memory/`
* Logs → `logs/`
* Config → `agents/config/`
* আর কিছু বাইরে ছড়ানো যাবে না ❌

### **বিফোর ওপেনিং সার্ভার:**
* প্রথমে log চেক করবে
* তারপর status চেক করবে
* সব ঠিক থাকলে তবেই কাজ শুরু

---

## 9️⃣ সাকসেস ক্রাইটেরিয়া

### **প্রতিটি টাস্কের জন্য:**
- [ ] All required folders exist
- [ ] All required files created
- [ ] Dependencies installed
- [ ] Files organized properly
- [ ] Logs updated
- [ ] Report submitted
- [ ] Ready for next task

### **সিস্টেম লেভেলে:**
- [ ] All services running
- [ ] No errors in logs
- [ ] Performance optimal
- [ ] Documentation complete
- [ ] Ready for production

---

## 🧟‍♂️ জম্বি টিম মেসেজ

> "প্রিয় ZombieCoder Agents,
> 
> এই নিয়মগুলো শুধু কোডের লাইন না - এটা আমাদের পরিচয়।
> প্রতিটি ফাইল, প্রতিটি ফোল্ডার, প্রতিটি লগ - সব কিছুই আমাদের পদচিহ্ন।
> 
> চল একসাথে কোডিং জগৎকে সহজ করি!
> 
> - কলিজা (Zombie Leader) 🧟‍♂️"

---

**Last Updated**: $(date)  
**Version**: 1.0  
**Status**: Active  
**Next Review**: Daily
