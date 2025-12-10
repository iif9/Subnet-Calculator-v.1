# خطوات رفع المشروع إلى GitHub

## الخطوة 1: إنشاء Repository على GitHub

1. اذهب إلى [github.com](https://github.com)
2. سجل الدخول إلى حسابك (أنشئ حساباً إذا لم يكن لديك)
3. اضغط على "+" في الزاوية العلوية اليمين
4. اختر "New repository"
5. أدخل:
   - **Repository name**: `subnet-calculator`
   - **Description**: `Network calculator application built with Kivy`
   - اختر "Public" أو "Private" حسب تفضيلك
   - تخطى خيارات "Initialize" (سننشئ المحتوى محلياً)
6. اضغط "Create repository"

## الخطوة 2: تثبيت Git

- **Windows**: حمل من [git-scm.com](https://git-scm.com/download/win)
- **macOS**: `brew install git`
- **Linux**: `sudo apt-get install git`

تحقق من التثبيت:
```bash
git --version
```

## الخطوة 3: تكوين Git (مرة واحدة فقط)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## الخطوة 4: رفع المشروع

في مجلد المشروع:

```bash
# تهيئة repository محلي
git init

# إضافة جميع الملفات
git add .

# عمل commit أولي
git commit -m "Initial commit: Subnet Calculator application"

# ربط مع repository البعيد (استبدل USERNAME و REPO)
git remote add origin https://github.com/USERNAME/subnet-calculator.git

# رفع الملفات
git branch -M main
git push -u origin main
```

## الخطوة 5: التحقق

اذهب إلى `https://github.com/USERNAME/subnet-calculator` وتحقق من أن جميع الملفات موجودة!

## ملاحظات مهمة

- تأكد من أن اسم المستخدم والبريد الإلكتروني صحيحين
- إذا طلب منك كلمة السر، استخدم Personal Access Token (ليس كلمة السر العادية)
- لإنشاء PAT: Settings > Developer settings > Personal access tokens > Tokens (classic)

## الملفات التي تم إنشاؤها تلقائياً:

✅ `.gitignore` - يخفي الملفات غير الضرورية
✅ `README.md` - وصف المشروع
✅ `requirements.txt` - المكتبات المطلوبة
✅ `LICENSE` - رخصة MIT

كل شيء جاهز الآن! 🚀
