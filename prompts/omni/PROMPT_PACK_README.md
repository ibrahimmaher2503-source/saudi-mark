# Saudi Mark — Omni Gemini Video Generation Pack

هذا هو Prompt Pack الخاص **بتوليد فيديو فعلي** في Omni Gemini. كل ملف يطلب فيديو مستقلًا بمدة محددة وحركة واضحة، وليس صورة Storyboard.

## ترتيب التوليد

| الملف | مدة الفيديو | الناتج |
|---|---:|---|
| `01-generate-video-hook.md` | 3 ثوانٍ | Hook وكثرة المشاوير |
| `02-generate-video-care.md` | 3 ثوانٍ | السيارة تحتاج عناية |
| `03-generate-video-no-trip.md` | 3 ثوانٍ | لا تروح للمغسلة |
| `04-generate-map-route.md` | 4 ثوانٍ | الخريطة والمسار إلى جدة |
| `05-generate-video-booking.md` | 4 ثوانٍ | الحجز والعناية |
| `06-generate-video-final-card.md` | 3 ثوانٍ | النهاية الفاخرة |

الإجمالي: **20 ثانية**.

## طريقة الاستخدام في Omni Gemini

1. افتح ملف Prompt واحدًا فقط في كل مرة.
2. ارفع PNG الخاص بالمشهد كـreference image إذا كان Omni يسمح بالـimage reference.
3. استخدم prompt الفيديو كاملًا كما هو.
4. اختر `vertical 9:16`.
5. ولّد الفيديو، وليس image أو storyboard.
6. افحص أن الناتج فيه حركة فعلية خلال المدة كلها.
7. كرر المشهد إذا غيّر شكل السيارة أو أضاف نصًا مشوهًا.
8. احفظ كل Clip باسم رقمي مطابق للترتيب.

## ملفات PNG المرجعية

كل العناصر الآن PNG بخلفية شفافة داخل:

```text
assets/png/
```

العناصر:

```text
car.png
clock.png
calendar-event.png
droplet.png
bubble.png
sparkles.png
device-mobile.png
map-pin.png
map-route.png
map.png
route.png
building-skyscraper.png
saudi-arabia-location-map.png
```

## النصوص التي تضاف في CapCut فقط

```text
0–3   كثيرة مشاويرك؟
3–6   وسيارتك دايمًا تحتاج عناية؟
6–9   لا تروح للمغسلة
9–13  Saudi Mark تجيك لموقعك
13–17 احجز من جوالك
      وخلي العناية علينا
17–20 غسيل سيارات متنقل في جدة
      احجز الآن
```

لا تطلب من Omni توليد أي نص أو شعار. أضف النص العربي وشعار Saudi Mark في CapCut.

## ثبات الهوية بين المقاطع

استخدم نفس:

- car.png في كل مشهد
- الألوان: navy, aqua, cyan, silver, restrained gold
- أسلوب line-art/vector
- سماكة الخطوط
- نسبة 9:16
- عدم وجود أشخاص أو تصوير حقيقي

## Negative Prompt عام

```text
No still image, no storyboard, no static poster, no readable text, no Arabic letters, no English letters, no generated logo, no fake brand name, no watermark, no prices, no phone numbers, no invented offers, no unapproved coverage claims, no realistic people, no photography, no extra wheels, no changing car design, no object morphing, no flicker, no glitch, no chaotic camera, no random letters, no distorted UI, no unreadable map labels.
```

## CapCut assembly

1. ضع Clips بالترتيب من 01 إلى 06.
2. استخدم cuts قصيرة أو انتقالات 4–6 frames.
3. أضف النصوص العربية يدويًا.
4. أضف شعار Saudi Mark الرسمي في النهاية.
5. أضف صوت clock tick، whoosh، map ping، booking click، water ripple، sparkle.
6. صدّر 1080×1920، 30 fps، H.264.
7. راجع النص العربي واللوجو والـsafe margins قبل النشر.