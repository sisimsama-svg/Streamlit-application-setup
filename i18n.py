"""واجهة عربي / إنجليزي. العربية هي اللغة الافتراضية."""

from __future__ import annotations

import streamlit as st

TEXT = {
    "language": {"ar": "اللغة", "en": "Language"},
    "shop": {"ar": "المتجر", "en": "Shop"},
    "tryon": {"ar": "تجربة النظارة", "en": "Try on"},
    "cart_n": {"ar": "السلة ({n})", "en": "Cart ({n})"},
    "track": {"ar": "تتبع الطلب", "en": "Track order"},
    "admin": {"ar": "الإدارة", "en": "Admin"},
    "cart_pill": {"ar": "السلة ({n})", "en": "Cart ({n})"},
    "loc_ar": {"ar": "باب اللوق، القاهرة", "en": "Bab El Louk, Cairo"},
    "hero_title": {"ar": "نظارات مسلم — باب اللوق", "en": "Moslem Optics — Bab El Louk"},
    "hero_body": {
        "ar": "نظارات طبية وشمسية من المحل، منها أوكلي وبوليس. جرّب الإطار على وجهك، أرسل الروشتة، ثم ادفع عند الاستلام أو عبر InstaPay وفودافون كاش.",
        "en": "Medical and sun glasses from the shop, including Oakley and Police. Try a frame on your face, send your prescription, then pay cash on delivery, by InstaPay, or by Vodafone Cash.",
    },
    "search": {"ar": "ابحث عن نظارة أو متجر أو محافظة", "en": "Search frames, stores, or governorates"},
    "search_ph": {"ar": "مثال: أوكلي، نظارات مسلم، القاهرة، شمسية", "en": "Example: Oakley, Moslem Optics, Cairo, sunglasses"},
    "use": {"ar": "الاستخدام", "en": "Type"},
    "audience": {"ar": "الجمهور", "en": "For"},
    "frame_shape": {"ar": "شكل الإطار", "en": "Frame shape"},
    "no_results": {"ar": "لا توجد نتائج مطابقة.", "en": "No matching results."},
    "sold_out": {"ar": "نفد المخزون", "en": "Sold out"},
    "left": {"ar": "المتبقي {n}", "en": "{n} left"},
    "suits": {"ar": "يناسب: {shapes}", "en": "Suits: {shapes}"},
    "add_to_cart": {"ar": "أضف للسلة", "en": "Add to cart"},
    "try": {"ar": "تجربة", "en": "Try"},
    "locating_eyes": {"ar": "جاري تحديد العينين والأنف...", "en": "Locating the eyes and nose..."},
    "tryon_title": {"ar": "تجربة النظارة على وجهك", "en": "Try glasses on your face"},
    "tryon_body": {
        "ar": "يُحلَّل وجهك بـ MediaPipe Face Mesh لتركيب النظارة واقتراح الإطارات المناسبة لشكل الوجه.",
        "en": "MediaPipe Face Mesh reads your face, places the glasses, and suggests frames for your face shape.",
    },
    "image_source": {"ar": "مصدر الصورة", "en": "Photo source"},
    "face_photo": {"ar": "صورة الوجه", "en": "Face photo"},
    "take_photo": {"ar": "التقط صورة", "en": "Take a photo"},
    "use_sample": {"ar": "استخدم صورة تجريبية", "en": "Use a sample photo"},
    "advisor_prompt": {
        "ar": "ارفع صورة ليحلّل المستشار شكل وجهك ويقترح الإطارات المناسبة.",
        "en": "Upload a photo so the advisor can read your face shape and suggest frames.",
    },
    "advisor_title": {"ar": "المستشار الذكي: وجه {label}", "en": "Style advisor: {label} face"},
    "suggested": {"ar": "المقترح:", "en": "Suggested:"},
    "show_all": {"ar": "عرض كل النظارات", "en": "Show all frames"},
    "show_matches": {"ar": "عرض النظارات المناسبة فقط", "en": "Show matching frames only"},
    "tilt_note": {
        "ar": " الصورة مائلة قليلاً، والنتيجة أدق عندما يكون الوجه مواجهاً للكاميرا.",
        "en": " The photo is slightly tilted. A straight-on face gives a more accurate result.",
    },
    "face_unclear": {
        "ar": "تعذر تحديد شكل الوجه. استخدم صورة أمامية أوضح حتى يعمل MediaPipe Face Mesh.",
        "en": "The face shape could not be read. Use a clearer front-facing photo so MediaPipe Face Mesh can work.",
    },
    "no_products": {"ar": "لا توجد نظارات في المتجر بعد. أضفها من لوحة الإدارة.", "en": "The shop has no frames yet. Add them from the admin page."},
    "choose_glasses": {"ar": "اختر النظارة", "en": "Choose a frame"},
    "gone": {"ar": "هذه النظارة لم تعد متاحة.", "en": "This frame is no longer available."},
    "manual_fit": {"ar": "ضبط يدوي", "en": "Manual adjustment"},
    "reset_fit": {"ar": "إعادة الضبط التلقائي", "en": "Reset automatic fit"},
    "size": {"ar": "الحجم", "en": "Size"},
    "size_help": {"ar": "100 يعني المقاس المطابق للوجه", "en": "100 matches the face"},
    "shift_x": {"ar": "تحريك أفقي", "en": "Move sideways"},
    "shift_help": {"ar": "نسبة من المسافة بين العينين", "en": "Percent of the distance between the eyes"},
    "shift_y": {"ar": "تحريك رأسي", "en": "Move up or down"},
    "angle": {"ar": "الزاوية", "en": "Angle"},
    "angle_help": {"ar": "درجات تُضاف إلى ميل العينين", "en": "Degrees added to the eye tilt"},
    "add_frame": {"ar": "أضف هذا الإطار للسلة", "en": "Add this frame to the cart"},
    "frame_gone": {"ar": "نفد مخزون هذا الإطار", "en": "This frame is out of stock"},
    "upload_face": {"ar": "ارفع صورة وجه واضحة لإظهار التجربة.", "en": "Upload a clear face photo to show the try-on."},
    "save_look": {"ar": "حفظ الإطلالة", "en": "Save look"},
    "share_hint": {
        "ar": "حمّل الصورة بعد تركيب النظارة، أو شاركها مباشرة لأخذ رأي أصدقائك.",
        "en": "Download the photo with the glasses on, or share it to ask your friends.",
    },
    "share_look": {"ar": "مشاركة الإطلالة", "en": "Share look"},
    "share_title": {"ar": "نظارات مسلم", "en": "Moslem Optics"},
    "share_text": {
        "ar": "إطلالتي من نظارات مسلم، باب اللوق — ما رأيكم؟",
        "en": "My look from Moslem Optics, Bab El Louk — what do you think?",
    },
    "share_opened": {"ar": "تم فتح نافذة المشاركة.", "en": "The share window is open."},
    "share_copied": {"ar": "تم نسخ الصورة. الصقها في أي تطبيق للمشاركة.", "en": "The photo was copied. Paste it into any app to share."},
    "share_unavailable": {
        "ar": "المشاركة غير متاحة هنا. استخدم زر حفظ الإطلالة ثم أرسل الملف لأصدقائك.",
        "en": "Sharing is not available here. Use Save look, then send the file to your friends.",
    },
    "cart_title": {"ar": "السلة والدفع", "en": "Cart and payment"},
    "cart_body": {
        "ar": "راجع العدسات والروشتة، ثم اختر المحافظة ووسيلة الدفع. رسوم التوصيل تُحسب تلقائياً.",
        "en": "Review the lenses and prescription, then choose the governorate and payment method. Delivery is calculated automatically.",
    },
    "last_order": {"ar": "آخر طلب تم تسجيله برقم {id}.", "en": "The last order was saved as {id}."},
    "follow_order": {"ar": "متابعة حالة الطلب", "en": "Track this order"},
    "empty_cart": {"ar": "السلة فارغة. أضف نظارة من المتجر.", "en": "The cart is empty. Add a frame from the shop."},
    "frame_line": {"ar": "الإطار {frame} · العدسة {lens} +{extra}", "en": "Frame {frame} · lens {lens} +{extra}"},
    "qty": {"ar": "الكمية", "en": "Qty"},
    "delete": {"ar": "حذف", "en": "Remove"},
    "gov": {"ar": "المحافظة", "en": "Governorate"},
    "totals": {
        "ar": "المنتجات: {sub}<br>التوصيل إلى {gov}: {fee} · يصل خلال {eta}<br><span style=\"font-size:20px\">المطلوب: {grand}</span>",
        "en": "Items: {sub}<br>Delivery to {gov}: {fee} · arrives in {eta}<br><span style=\"font-size:20px\">Due: {grand}</span>",
    },
    "ship_details": {"ar": "بيانات التوصيل", "en": "Delivery details"},
    "full_name": {"ar": "الاسم", "en": "Name"},
    "mobile": {"ar": "رقم الجوال", "en": "Mobile number"},
    "address": {"ar": "العنوان", "en": "Address"},
    "pay_heading": {"ar": "طريقة الدفع", "en": "Payment"},
    "pay_method": {"ar": "وسيلة الدفع", "en": "Payment method"},
    "instapay_info": {
        "ar": "حوّل {grand} إلى عنوان InstaPay التجريبي: moslem.optics@instapay ثم اكتب رقم العملية.",
        "en": "Transfer {grand} to the demo InstaPay address moslem.optics@instapay, then enter the transaction number.",
    },
    "instapay_ref": {"ar": "رقم عملية InstaPay", "en": "InstaPay transaction number"},
    "vf_info": {
        "ar": "حوّل {grand} إلى محفظة فودافون كاش التجريبية 01000000000 ثم اكتب رقم المحفظة التي أرسلت منها.",
        "en": "Transfer {grand} to the demo Vodafone Cash wallet 01000000000, then enter the wallet number you sent from.",
    },
    "vf_wallet": {"ar": "رقم محفظة فودافون كاش", "en": "Vodafone Cash wallet number"},
    "cod_info": {"ar": "ستدفع {grand} نقداً عند استلام الطلب في {gov}.", "en": "You will pay {grand} in cash when the order is delivered in {gov}."},
    "confirm_order": {"ar": "تأكيد الطلب", "en": "Place order"},
    "need_contact": {"ar": "أكمل الاسم والجوال والعنوان.", "en": "Enter your name, mobile number, and address."},
    "bad_phone": {"ar": "اكتب رقم جوال صحيح.", "en": "Enter a valid mobile number."},
    "need_instapay": {"ar": "اكتب رقم عملية InstaPay.", "en": "Enter the InstaPay transaction number."},
    "need_wallet": {"ar": "اكتب رقم محفظة فودافون كاش التي تم التحويل منها.", "en": "Enter the Vodafone Cash wallet number you sent from."},
    "order_ok": {
        "ar": "تم استلام طلبك يا {name}. رقم الطلب {id}. الحالة الآن: {status}. التوصيل إلى {gov} خلال {eta}، والدفع عبر {pay}. الإجمالي {grand} شامل التوصيل.",
        "en": "We received your order, {name}. Order number {id}. Status: {status}. Delivery to {gov} in {eta}, paid by {pay}. Total {grand} including delivery.",
    },
    "track_this": {"ar": "تتبع هذا الطلب", "en": "Track this order"},
    "track_title": {"ar": "تتبع الطلب", "en": "Track an order"},
    "track_body": {
        "ar": "اكتب رقم الطلب الذي يظهر بعد الشراء لمتابعة: تم التجهيز، جاري التغليف، ثم خرج للتوصيل.",
        "en": "Enter the order number from checkout to follow it: prepared, being packed, then out for delivery.",
    },
    "order_no": {"ar": "رقم الطلب", "en": "Order number"},
    "order_ph": {"ar": "مثال: MO-A1B2C3", "en": "Example: MO-A1B2C3"},
    "order_hint": {"ar": "رقم الطلب يظهر في رسالة التأكيد فور إتمام الشراء.", "en": "The order number appears in the confirmation message right after checkout."},
    "order_missing": {"ar": "لا يوجد طلب بهذا الرقم. تأكد من الحروف، مثل MO-A1B2C3.", "en": "No order uses that number. Check the characters, for example MO-A1B2C3."},
    "order_heading": {"ar": "الطلب {id}", "en": "Order {id}"},
    "track_meta": {"ar": "سُجّل في {created} · {gov} · يصل خلال {eta}", "en": "Placed {created} · {gov} · arrives in {eta}"},
    "status_now": {"ar": "الحالة الحالية: **{status}**", "en": "Current status: **{status}**"},
    "line_item": {"ar": "- {name} × {qty} — {lens}", "en": "- {name} × {qty} — {lens}"},
    "track_total": {"ar": "الإجمالي {total} شامل التوصيل، والدفع عبر {pay}.", "en": "Total {total} including delivery, paid by {pay}."},
    "lens_dialog": {"ar": "تفاصيل العدسة والروشتة", "en": "Lenses and prescription"},
    "lens_type": {"ar": "نوع العدسات", "en": "Lens type"},
    "rx_data": {"ar": "بيانات النظر", "en": "Prescription"},
    "rx_caption": {"ar": "القوة بالديوبتر، والمحور من 0 إلى 180.", "en": "Power is in diopters. Axis is from 0 to 180."},
    "right_eye": {"ar": "العين اليمنى", "en": "Right eye"},
    "left_eye": {"ar": "العين اليسرى", "en": "Left eye"},
    "sph_r": {"ar": "SPH يمين", "en": "SPH right"},
    "cyl_r": {"ar": "CYL يمين", "en": "CYL right"},
    "axis_r": {"ar": "AXIS يمين", "en": "AXIS right"},
    "sph_l": {"ar": "SPH يسار", "en": "SPH left"},
    "cyl_l": {"ar": "CYL يسار", "en": "CYL left"},
    "axis_l": {"ar": "AXIS يسار", "en": "AXIS left"},
    "pd": {"ar": "المسافة بين البؤبؤين PD", "en": "Pupillary distance PD"},
    "unit_price": {"ar": "سعر القطعة مع العدسة: **{price}**", "en": "Price with lenses: **{price}**"},
    "confirm_add": {"ar": "تأكيد الإضافة للسلة", "en": "Confirm add to cart"},
    "need_rx": {"ar": "ارفع صورة الروشتة، أو بدّل إلى إدخال المقاسات يدوياً.", "en": "Upload a prescription photo, or switch to entering the measurements."},
    "out_of_stock": {"ar": "نفد مخزون هذه النظارة.", "en": "This frame is out of stock."},
    "cart_holds": {"ar": "السلة تحتوي بالفعل كل المتاح من {name} ({stock}).", "en": "The cart already has every available {name} ({stock})."},
    "config_line": {"ar": "**{name}** — الإطار {price} · المتبقي {stock}", "en": "**{name}** — frame {price} · {stock} left"},
    "added": {"ar": "تمت إضافة {name} — {lens}", "en": "Added {name} — {lens}"},
    "included": {"ar": "مشمولة", "en": "included"},
    "rx_uploaded": {"ar": "روشتة مرفوعة: {name}", "en": "Uploaded prescription: {name}"},
    "no_rx": {"ar": "بدون تفاصيل روشتة", "en": "No prescription details"},
    "manual_rx": {"ar": "مقاسات يدوية — يمين {od} / يسار {os} / PD {pd}", "en": "Manual measurements — right {od} / left {os} / PD {pd}"},
    "rx_detail": {
        "ar": "يمين: SPH {od_sph} · CYL {od_cyl} · AXIS {od_axis}\nيسار: SPH {os_sph} · CYL {os_cyl} · AXIS {os_axis}\nPD {pd}",
        "en": "Right: SPH {od_sph} · CYL {od_cyl} · AXIS {od_axis}\nLeft: SPH {os_sph} · CYL {os_cyl} · AXIS {os_axis}\nPD {pd}",
    },
    "rx_file": {"ar": "ملف الروشتة: {name}", "en": "Prescription file: {name}"},
    "rx_caption_img": {"ar": "الروشتة", "en": "Prescription"},
    "admin_title": {"ar": "لوحة الإدارة", "en": "Admin"},
    "admin_body": {
        "ar": "الطلبات وكشف النظر، وإدارة النظارات والمخزون بدون تعديل أي ملفات.",
        "en": "Orders, prescriptions, frames, and stock, without editing any files.",
    },
    "admin_code": {"ar": "رمز الإدارة", "en": "Admin code"},
    "enter": {"ar": "دخول", "en": "Sign in"},
    "bad_code": {"ar": "الرمز غير صحيح.", "en": "That code is not correct."},
    "section": {"ar": "القسم", "en": "Section"},
    "logout": {"ar": "خروج", "en": "Sign out"},
    "add_glasses": {"ar": "إضافة نظارة", "en": "Add a frame"},
    "add_help": {
        "ar": "ارفع صورة PNG بخلفية شفافة، ثم حدّد الاسم والسعر والنوع وشكل الوجه والمخزون.",
        "en": "Upload a transparent PNG, then set the name, price, type, face shape, and stock.",
    },
    "glasses_name": {"ar": "اسم النظارة", "en": "Frame name"},
    "price_egp": {"ar": "السعر (ج.م)", "en": "Price (EGP)"},
    "stock": {"ar": "المخزون", "en": "Stock"},
    "face_match": {"ar": "شكل الوجه المناسب", "en": "Matching face shape"},
    "png_image": {"ar": "صورة النظارة PNG", "en": "Frame PNG"},
    "add_glasses_btn": {"ar": "إضافة النظارة", "en": "Add frame"},
    "name_required": {"ar": "اكتب اسم النظارة.", "en": "Enter the frame name."},
    "shape_required": {"ar": "اختر شكل وجه واحداً على الأقل.", "en": "Choose at least one face shape."},
    "current_glasses": {"ar": "النظارات الحالية", "en": "Current frames"},
    "no_glasses_admin": {"ar": "لا توجد نظارات. أضف الأولى من النموذج أعلاه.", "en": "There are no frames. Add the first one with the form above."},
    "image_missing": {"ar": "صورة النظارة غير موجودة.", "en": "The frame image is missing."},
    "save_edit": {"ar": "حفظ التعديل", "en": "Save changes"},
    "replace_png": {"ar": "استبدال الصورة PNG", "en": "Replace PNG"},
    "saved_notice": {"ar": "تم حفظ {name}", "en": "Saved {name}"},
    "added_notice": {"ar": "تمت إضافة {name}", "en": "Added {name}"},
    "deleted_notice": {"ar": "تم حذف {name}", "en": "Removed {name}"},
    "confirm_delete": {"ar": "تأكيد الحذف", "en": "Confirm delete"},
    "cancel": {"ar": "إلغاء", "en": "Cancel"},
    "delete_glasses": {"ar": "حذف النظارة", "en": "Delete frame"},
    "product_admin_title": {"ar": "{name} — {price} — المخزون {stock}", "en": "{name} — {price} — stock {stock}"},
    "orders_count": {"ar": "الطلبات: {n}", "en": "Orders: {n}"},
    "no_orders": {"ar": "لا توجد طلبات بعد. ستظهر هنا فور تأكيد العميل للشراء.", "en": "No orders yet. They appear here as soon as a customer checks out."},
    "update_status": {"ar": "تحديث الحالة", "en": "Update status"},
    "save_status": {"ar": "حفظ الحالة", "en": "Save status"},
    "ship_contact": {"ar": "التوصيل والتواصل", "en": "Delivery and contact"},
    "field_name": {"ar": "الاسم: {value}", "en": "Name: {value}"},
    "field_phone": {"ar": "الجوال: {value}", "en": "Mobile: {value}"},
    "field_gov": {"ar": "المحافظة: {value}", "en": "Governorate: {value}"},
    "field_address": {"ar": "العنوان: {value}", "en": "Address: {value}"},
    "field_recorded": {"ar": "سُجّل: {value}", "en": "Placed: {value}"},
    "field_pay": {"ar": "الدفع: {value}", "en": "Payment: {value}"},
    "field_ref": {"ar": "مرجع InstaPay: {value}", "en": "InstaPay reference: {value}"},
    "money_line": {
        "ar": "المنتجات {sub} · التوصيل {fee} · الإجمالي {total}",
        "en": "Items {sub} · delivery {fee} · total {total}",
    },
    "rx_heading": {"ar": "كشف النظر والروشتة", "en": "Prescription"},
    "admin_line": {"ar": "{i}. {name} × {qty} — {lens} — {price}", "en": "{i}. {name} × {qty} — {lens} — {price}"},
    "download_rx": {"ar": "تنزيل الروشتة ({name})", "en": "Download prescription ({name})"},
    "png_required": {"ar": "ارفع صورة النظارة بصيغة PNG.", "en": "Upload the frame image as a PNG."},
    "png_empty": {"ar": "الملف فارغ.", "en": "The file is empty."},
    "png_large": {"ar": "الصورة أكبر من 8 ميغابايت.", "en": "The image is larger than 8 MB."},
    "png_unreadable": {"ar": "تعذر قراءة الصورة. استخدم ملف PNG صالحاً.", "en": "The image could not be read. Use a valid PNG file."},
    "png_format": {"ar": "الصيغة يجب أن تكون PNG حتى تظهر النظارة بخلفية شفافة في التجربة.", "en": "The file must be a PNG so the frame stays transparent in try-on."},
    "stock_missing": {"ar": "إحدى النظارات لم تعد موجودة في المتجر.", "en": "One of the frames is no longer in the shop."},
    "stock_short": {"ar": "المخزون لا يكفي لـ {name}. المتبقي {available}.", "en": "Not enough stock for {name}. {available} left."},
    "file_fallback": {"ar": "ملف", "en": "file"},
    "join_store": {"ar": "سجل محلك / انضم كتاجر", "en": "Register your store / Join as a vendor"},
    "vendor_login": {"ar": "دخول التاجر", "en": "Vendor sign in"},
    "my_dashboard": {"ar": "لوحة متجري", "en": "My store dashboard"},
    "marketplace_note": {
        "ar": "نظارات مسلم هو المتجر الأساسي وتجربة الارتداء متاحة لإطاراته. المتاجر المنضمّة تظهر بعده ويمكن تجربة أي إطار بصورته الشفافة.",
        "en": "Moslem Optics is the main store and try-on stays available for its frames. Joined stores appear after it, and any frame with a transparent image can be tried on.",
    },
    "sold_by": {"ar": "المتجر: {store}", "en": "Store: {store}"},
    "all_stores": {"ar": "كل المتاجر", "en": "All stores"},
    "store_filter": {"ar": "المتجر", "en": "Store"},
    "join_title": {"ar": "سجل محلك", "en": "Register your store"},
    "join_body": {
        "ar": "اختر الباقة، أدخل بيانات المحل، ثم ادفع الاشتراك: انستاباي، أو الفيزا والبطاقات البنكية، أو أبل باي، أو نقدي. انستاباي يتطلب إيصال تحويل قبل التفعيل. الفيزا وأبل باي والنقدي تفعيل محلي بدون خصم حقيقي ولا يُطلب لها إيصال.",
        "en": "Choose a plan, enter the shop details, then pay the subscription with InstaPay, Visa / MasterCard, Apple Pay, or Cash. InstaPay requires a transfer receipt before activation. Visa / MasterCard, Apple Pay, and Cash activate in this local demo with no real charge and no receipt.",
    },
    "plan_pick": {"ar": "الباقة", "en": "Plan"},
    "plan_monthly": {"ar": "اشتراك شهري — {price} / شهرياً", "en": "Monthly subscription — {price} / month"},
    "plan_yearly": {"ar": "اشتراك سنوي — {price} / سنوياً", "en": "Yearly subscription — {price} / year"},
    "store_name": {"ar": "اسم المحل", "en": "Store name"},
    "store_logo": {"ar": "شعار المحل", "en": "Store logo"},
    "whatsapp": {"ar": "رقم واتساب", "en": "WhatsApp number"},
    "sub_pay": {"ar": "دفع الاشتراك", "en": "Subscription payment"},
    "pay_voda": {"ar": "فودافون كاش", "en": "Vodafone Cash"},
    "pay_insta": {"ar": "انستاباي", "en": "InstaPay"},
    "pay_apple": {"ar": "أبل باي", "en": "Apple Pay"},
    "pay_cash": {"ar": "نقدي / دفع مباشر", "en": "Cash / direct payment"},
    "pay_card": {"ar": "الفيزا والبطاقات البنكية", "en": "Visa / MasterCard"},
    "pay_visa": {"ar": "الفيزا والبطاقات البنكية", "en": "Visa / MasterCard"},
    "sub_insta_info": {
        "ar": "حوّل {price} إلى عنوان InstaPay التجريبي {handle} ثم ارفع صورة الإيصال. العنوان تجريبي وليس حساباً حقيقياً. الإيصال إلزامي: لن يُفعَّل المتجر ولن يكتمل الاشتراك بدونه.",
        "en": "Transfer {price} to the demo InstaPay address {handle}, then upload the receipt image. The address is a demo, not a real account. The receipt is mandatory: the store is not activated and the subscription does not complete without it.",
    },
    "sub_card_info": {
        "ar": "الفيزا والبطاقات البنكية هنا طريقة تجريبية داخل التطبيق المحلي. لن يُخصم أي مبلغ حقيقي ولن يُرسل الرقم إلى بوابة دفع. أدخل اسم حامل البطاقة وآخر 4 أرقام فقط. لا نطلب الرقم الكامل ولا CVV، ولا حاجة لإيصال تحويل.",
        "en": "Visa / MasterCard here is a demo method in this local app. No real charge is made and the number is not sent to a payment gateway. Enter only the cardholder name and the last 4 digits. The full card number and CVV are not collected, and no transfer receipt is required.",
    },
    "card_name": {"ar": "اسم حامل البطاقة", "en": "Cardholder name"},
    "card_last4": {"ar": "آخر 4 أرقام", "en": "Last 4 digits"},
    "need_card": {
        "ar": "اكتب اسم حامل البطاقة وآخر 4 أرقام فقط. لن يُفعَّل الاشتراك بدونها، ولا يُقبل رقم البطاقة الكامل.",
        "en": "Enter the cardholder name and only the last 4 digits. The subscription is not activated without them, and a full card number is not accepted.",
    },
    "sub_apple_info": {
        "ar": "أبل باي هنا طريقة تجريبية داخل التطبيق المحلي. لن يُفتح دفع أبل باي الحقيقي ولن يُخصم أي مبلغ، ولا يُطلب رقم البطاقة ولا CVV ولا إيصال تحويل.",
        "en": "Apple Pay here is a demo method in this local app. No real Apple Pay sheet opens and no charge is made. No card number, CVV, or transfer receipt is collected.",
    },
    "sub_cash_info": {
        "ar": "الدفع نقدي ومباشر في المحل. لا حاجة لإيصال تحويل، ويمكن تفعيل المتجر في هذا العرض المحلي.",
        "en": "Cash is pay-in-person, paid directly. No transfer receipt is required, and the store can be activated in this local demo.",
    },
    "receipt": {"ar": "صورة إيصال التحويل (إلزامي)", "en": "Transfer receipt image (required)"},
    "activate": {"ar": "تفعيل المتجر", "en": "Activate store"},
    "need_store": {"ar": "اكتب اسم المحل ورقم واتساب والعنوان.", "en": "Enter the store name, WhatsApp number, and address."},
    "need_logo": {"ar": "ارفع شعار المحل.", "en": "Upload the store logo."},
    "need_receipt": {
        "ar": "ارفع صورة إيصال التحويل. لن يُفعَّل المتجر ولن يكتمل اشتراك انستاباي بدون الإيصال.",
        "en": "Upload the transfer receipt image. The store is not activated and the InstaPay subscription does not complete without it.",
    },
    "join_ok": {
        "ar": "تم تفعيل {name}. هذا رمز دخول لوحة متجرك، سيظهر مرة واحدة:",
        "en": "{name} is active. This is your dashboard access code. It is shown once:",
    },
    "code_saved": {"ar": "حفظت الرمز وسأدخل اللوحة", "en": "I saved the code and will open the dashboard"},
    "vendor_title": {"ar": "لوحة التاجر", "en": "Vendor dashboard"},
    "vendor_body": {"ar": "إدارة منتجات متجرك وبياناته فقط.", "en": "Manage only your store's frames and profile."},
    "vendor_code": {"ar": "رمز دخول المتجر", "en": "Store access code"},
    "vendor_enter": {"ar": "دخول", "en": "Sign in"},
    "bad_vendor_code": {"ar": "الرمز غير صحيح أو المتجر غير مفعّل.", "en": "That code is not correct, or the store is not active."},
    "vendor_out": {"ar": "خروج من المتجر", "en": "Sign out of the store"},
    "tab_products": {"ar": "منتجاتي", "en": "My frames"},
    "tab_profile": {"ar": "بيانات المتجر", "en": "Store profile"},
    "tab_orders": {"ar": "طلبات متجري", "en": "My orders"},
    "save_profile": {"ar": "حفظ بيانات المتجر", "en": "Save store profile"},
    "profile_saved": {"ar": "تم حفظ بيانات المتجر.", "en": "Store profile saved."},
    "sub_status": {"ar": "الاشتراك: {plan} — {price} — {method} — مفعّل", "en": "Subscription: {plan} — {price} — {method} — active"},
    "plan_primary": {"ar": "المتجر الأساسي", "en": "Main store"},
    "no_vendor_orders": {"ar": "لا توجد طلبات لمنتجاتك بعد.", "en": "There are no orders for your frames yet."},
    "vendors_title": {"ar": "المتاجر والاشتراكات", "en": "Stores and subscriptions"},
    "vendor_row": {"ar": "{name} — {status} — {plan} — {gov} — واتساب {phone}", "en": "{name} — {status} — {plan} — {gov} — WhatsApp {phone}"},
    "status_active": {"ar": "مفعّل", "en": "Active"},
    "method_none": {"ar": "بدون دفع", "en": "No payment"},
    "logo_bad": {"ar": "تعذر قراءة الشعار. استخدم صورة PNG أو JPG.", "en": "The logo could not be read. Use a PNG or JPG image."},
    "gov_filter": {"ar": "المحافظة / المنطقة", "en": "Governorate / area"},
    "all_areas": {"ar": "كل المحافظات", "en": "All areas"},
    "metric_orders": {"ar": "إجمالي الطلبات", "en": "Total orders"},
    "metric_sales": {"ar": "إجمالي المبيعات", "en": "Total sales (EGP)"},
    "metric_days": {"ar": "الأيام المتبقية في الاشتراك", "en": "Days left in the subscription"},
    "download_invoice": {"ar": "تنزيل فاتورة PDF", "en": "Download PDF invoice"},
    "download_vendor_pdf": {"ar": "تنزيل تقرير طلبات المتجر PDF", "en": "Download this store's orders PDF"},
    "download_admin_pdf": {"ar": "تنزيل تقرير المتاجر والطلبات PDF", "en": "Download stores and orders PDF"},
    "pdf_failed": {"ar": "تعذر إنشاء ملف PDF.", "en": "The PDF could not be created."},
    "pdf_invoice": {"ar": "فاتورة طلب", "en": "Order invoice"},
    "pdf_vendor": {"ar": "تقرير طلبات المتجر", "en": "Store orders report"},
    "pdf_admin": {"ar": "تقرير المنصة", "en": "Platform report"},
    "pdf_customer": {"ar": "العميل", "en": "Customer"},
    "pdf_phone": {"ar": "الهاتف", "en": "Phone"},
    "pdf_address": {"ar": "العنوان", "en": "Address"},
    "pdf_item": {"ar": "الصنف", "en": "Item"},
    "pdf_qty": {"ar": "الكمية", "en": "Qty"},
    "pdf_lens": {"ar": "العدسة", "en": "Lens"},
    "pdf_store": {"ar": "المتجر", "en": "Store"},
    "pdf_price": {"ar": "السعر", "en": "Price"},
    "pdf_subtotal": {"ar": "المنتجات", "en": "Items"},
    "pdf_delivery": {"ar": "التوصيل", "en": "Delivery"},
    "pdf_total": {"ar": "الإجمالي", "en": "Total"},
    "pdf_payment": {"ar": "الدفع", "en": "Payment"},
    "pdf_status": {"ar": "الحالة", "en": "Status"},
    "pdf_date": {"ar": "التاريخ", "en": "Date"},
    "pdf_orders_n": {"ar": "الطلبات", "en": "Orders"},
    "pdf_sales": {"ar": "المبيعات", "en": "Sales"},
    "pdf_stores": {"ar": "المتاجر", "en": "Stores"},
    "pdf_plan": {"ar": "الباقة", "en": "Plan"},
    "pdf_method": {"ar": "وسيلة الدفع", "en": "Payment method"},
    "pdf_amount": {"ar": "المبلغ", "en": "Amount"},
    "plan_month_short": {"ar": "شهري", "en": "Monthly"},
    "plan_year_short": {"ar": "سنوي", "en": "Yearly"},
    "notifications": {"ar": "الإشعارات", "en": "Notifications"},
    "no_notifications": {"ar": "لا توجد إشعارات بعد.", "en": "No notifications yet."},
    "open_whatsapp": {"ar": "فتح واتساب", "en": "Open WhatsApp"},
    "notif_order": {"ar": "طلب {id} — {store} — {total}", "en": "Order {id} — {store} — {total}"},
    "notif_sub": {"ar": "اشتراك {store} — {total}", "en": "Subscription {store} — {total}"},
    "wa_order": {
        "ar": "طلب جديد {id} من {store}. الإجمالي {total}. هاتف العميل {phone}.",
        "en": "New order {id} from {store}. Total {total}. Customer phone {phone}.",
    },
    "wa_sub": {
        "ar": "تم تفعيل اشتراك {store}. المبلغ {total}. واتساب {phone}.",
        "en": "Subscription activated for {store}. Amount {total}. WhatsApp {phone}.",
    },
    "backup_title": {"ar": "نسخة احتياطية", "en": "Backup"},
    "backup_csv": {"ar": "تنزيل المتاجر والطلبات CSV", "en": "Download stores and orders CSV"},
    "backup_xlsx": {"ar": "تنزيل نسخة Excel", "en": "Download Excel workbook"},
    "shop_status": {"ar": "حالة المتجر", "en": "Store status"},
    "shop_open": {"ar": "مفتوح", "en": "Open"},
    "shop_closed": {"ar": "مغلق", "en": "Closed"},
    "shop_maintenance": {"ar": "تحت الصيانة", "en": "Under Maintenance"},
    "save_shop_status": {"ar": "حفظ حالة المتجر", "en": "Save store status"},
    "shop_status_saved": {"ar": "تم حفظ حالة المتجر.", "en": "Store status saved."},
    "shop_closed_note": {
        "ar": "هذا المتجر مغلق حالياً. يمكن التصفح وتجربة النظارة، ولا يمكن إضافة منتجاته للسلة.",
        "en": "This store is closed. You can still browse and try frames, but its products cannot be added to the cart.",
    },
    "shop_maint_note": {
        "ar": "هذا المتجر تحت الصيانة. يمكن التصفح وتجربة النظارة، ولا يمكن إضافة منتجاته للسلة.",
        "en": "This store is under maintenance. You can still browse and try frames, but its products cannot be added to the cart.",
    },
    "stores_heading": {"ar": "المتاجر", "en": "Stores"},
    "wa_store": {"ar": "واتساب المتجر", "en": "Store WhatsApp"},
    "wa_product": {"ar": "تواصل عبر واتساب", "en": "WhatsApp"},
    "social_whatsapp": {"ar": "واتساب WhatsApp", "en": "WhatsApp"},
    "social_instagram": {"ar": "إنستغرام Instagram", "en": "Instagram"},
    "social_facebook": {"ar": "فيسبوك Facebook", "en": "Facebook"},
    "no_store_whatsapp": {
        "ar": "المتجر لم يضف واتساب بعد.",
        "en": "This store has not added WhatsApp yet.",
    },
    "tech_support": {"ar": "الدعم الفني", "en": "Technical support"},
    "support_unset": {
        "ar": "واتساب الدعم غير مُعد بعد.",
        "en": "Support WhatsApp is not configured yet.",
    },
    "support_whatsapp": {"ar": "رقم واتساب الدعم الفني", "en": "Support WhatsApp number"},
    "save_support": {"ar": "حفظ رقم الدعم", "en": "Save support number"},
    "support_saved": {"ar": "تم حفظ رقم واتساب الدعم.", "en": "Support WhatsApp number saved."},
    "support_bad": {"ar": "اكتب رقم واتساب صالحاً للدعم.", "en": "Enter a valid support WhatsApp number."},
    "change_code": {"ar": "تغيير رمز الدخول", "en": "Change access code"},
    "current_code": {"ar": "الرمز الحالي", "en": "Current code"},
    "new_code": {"ar": "الرمز الجديد", "en": "New code"},
    "save_code": {"ar": "حفظ الرمز الجديد", "en": "Save new code"},
    "code_too_short": {
        "ar": "الرمز الجديد يجب أن يكون 4 أحرف على الأقل.",
        "en": "The new code must be at least 4 characters.",
    },
    "bad_current_code": {"ar": "الرمز الحالي غير صحيح.", "en": "The current code is not correct."},
    "code_changed": {
        "ar": "تم تغيير الرمز. احفظ الرمز الجديد، سيظهر مرة واحدة:",
        "en": "The code was changed. Save the new code. It is shown once:",
    },
    "admin_change_code": {"ar": "تغيير رمز الإدارة", "en": "Change admin code"},
    "admin_code_changed": {"ar": "تم تغيير رمز الإدارة.", "en": "The admin code was changed."},
    "reset_code_title": {"ar": "استعادة رمز الدخول", "en": "Reset access code"},
    "reset_code_help": {
        "ar": "أدخل اسم المتجر ورقم واتساب المسجّل عليه. إن تطابق الرقم يُنشأ رمز جديد ويظهر مرة واحدة.",
        "en": "Enter the store name and the WhatsApp number saved on it. If the number matches, a new code is created and shown once.",
    },
    "reset_code_btn": {"ar": "إنشاء رمز جديد", "en": "Create a new code"},
    "reset_ok": {
        "ar": "تم إنشاء رمز جديد. احفظه، سيظهر مرة واحدة:",
        "en": "A new code was created. Save it. It is shown once:",
    },
    "reset_no_whatsapp": {
        "ar": "هذا المتجر بلا رقم واتساب. أضفه من لوحة المتجر أو اطلب من إدارة المنصة.",
        "en": "This store has no WhatsApp number. Set one from the dashboard or ask the platform admin.",
    },
    "reset_primary": {
        "ar": "دخول المتجر الأساسي يتم من إدارة المنصة وليس برمز تاجر.",
        "en": "The main store is opened from platform admin, not with a vendor code.",
    },
    "reset_mismatch": {
        "ar": "لم يتطابق اسم المتجر مع رقم واتساب المحفوظ.",
        "en": "The store name does not match the saved WhatsApp number.",
    },
    "platform_settings": {"ar": "إعدادات المنصة", "en": "Platform settings"},
    "store_cover": {"ar": "غلاف المتجر", "en": "Store cover"},
    "logo_replace_help": {
        "ar": "JPG أو PNG حتى 5 ميغابايت. اترك الحقل فارغاً للإبقاء على الشعار الحالي.",
        "en": "JPG or PNG up to 5 MB. Leave this empty to keep the current logo.",
    },
    "cover_help": {
        "ar": "صورة عريضة تظهر أعلى قسم متجرك للعملاء. JPG أو PNG حتى 5 ميغابايت. اتركها فارغة للإبقاء على الغلاف الحالي.",
        "en": "A wide image shown at the top of your store for customers. JPG or PNG up to 5 MB. Leave it empty to keep the current cover.",
    },
    "image_too_big": {"ar": "الصورة أكبر من 5 ميغابايت.", "en": "The image is larger than 5 MB."},
    "image_type": {"ar": "استخدم صورة JPG أو PNG.", "en": "Use a JPG or PNG image."},
    "ship_fees_title": {"ar": "رسوم التوصيل", "en": "Delivery fees"},
    "ship_fees_help": {
        "ar": "اكتب رسماً افتراضياً إذا أردت سعراً واحداً لكل المحافظات، أو اتركه فارغاً ليبقى رسم المنصة. املأ المحافظة فقط عند التخصيص. الخانة الفارغة تعني رسم المنصة، أو الرسم الافتراضي إن كتبته. يُحسب كل متجر مرة واحدة.",
        "en": "Enter a default fee for one price on every governorate, or leave it empty to keep the platform fee. Fill a governorate only when you want to override it. An empty cell keeps the platform fee, or your default fee if you set one. Each store is charged once.",
    },
    "ship_default": {"ar": "الرسم الافتراضي بالجنيه", "en": "Default fee in EGP"},
    "ship_default_ph": {"ar": "اختياري", "en": "Optional"},
    "ship_platform": {"ar": "رسم المنصة {fee}", "en": "platform fee {fee}"},
    "save_ship": {"ar": "حفظ رسوم التوصيل", "en": "Save delivery fees"},
    "ship_saved": {"ar": "تم حفظ رسوم التوصيل.", "en": "Delivery fees saved."},
    "ship_bad": {
        "ar": "اكتب رسوم التوصيل أرقاماً صحيحة من غير كسور، أو اترك الحقل فارغاً.",
        "en": "Enter delivery fees as whole numbers, or leave the field empty.",
    },
    "store_ship_line": {"ar": "رسم توصيل {store}: {fee}", "en": "{store} delivery fee: {fee}"},
    "totals_detail": {
        "ar": "المنتجات: {sub}<br>التوصيل إلى {gov}: {fee} · يصل خلال {eta}<br>{lines}<br><span style=\"font-size:20px\">المطلوب: {grand}</span>",
        "en": "Items: {sub}<br>Delivery to {gov}: {fee} · arrives in {eta}<br>{lines}<br><span style=\"font-size:20px\">Due: {grand}</span>",
    },
    "footer_note": {
        "ar": "نظارات مسلم — باب اللوق",
        "en": "Moslem Optics — Bab El Louk",
    },
    "policy_title": {"ar": "الشروط وسياسة الإرجاع", "en": "Terms and return policy"},
    "policy_intro": {
        "ar": "شروط الشراء وسياسة الإرجاع والاستبدال لنظارات مسلم في باب اللوق، وللمتاجر الأخرى على المنصة.",
        "en": "Purchase terms and the return and exchange policy for Moslem Optics in Bab El Louk, and for the other stores on the platform.",
    },
    "policy_disclaimer": {
        "ar": "هذا نص سياسة للمتجر داخل المنصة، وليس استشارة قانونية.",
        "en": "This is store policy copy for the marketplace, not legal advice.",
    },
    "terms_heading": {"ar": "الشروط والأحكام", "en": "Terms and conditions"},
    "returns_heading": {"ar": "سياسة الإرجاع والاستبدال", "en": "Return and exchange policy"},
    "back_shop": {"ar": "العودة للمتجر", "en": "Back to the shop"},
    "terms_body": {
        "ar": (
            "نظارات مسلم في باب اللوق هي المتجر الأساسي على هذه المنصة.\n\n"
            "- الطلب يشمل الإطار، والعدسة إن اخترتها، وعنوان التوصيل، ووسيلة الدفع التي تظهر في السلة.\n"
            "- العدسات الطبية تُجهَّز حسب الروشتة أو المقاسات التي تدخلها. راجعها قبل التأكيد.\n"
            "- السعر المعروض للإطار والعدسة. تُضاف رسوم التوصيل حسب المحافظة والمتجر، وتظهر قبل إرسال الطلب.\n"
            "- لا نذكر ضمان مصنع ولا مدة ضمان إلا إذا كُتبت على صفحة المنتج نفسه.\n\n"
            "المتاجر الأخرى على المنصة تتبع هذه السياسة الأساسية، ما لم توضح صفحة المتجر غير ذلك."
        ),
        "en": (
            "Moslem Optics in Bab El Louk is the main store on this platform.\n\n"
            "- An order includes the frame, the lens if you choose one, the delivery address, and the payment method shown in the cart.\n"
            "- Prescription lenses are made from the prescription or the measurements you enter. Review them before you confirm.\n"
            "- The listed price is for the frame and lens. Delivery is added for the governorate and the store, and it is shown before you place the order.\n"
            "- A manufacturer warranty or a warranty period is not stated here unless it is written on that product's page.\n\n"
            "Other vendors on the platform follow this same baseline policy unless their own page says otherwise."
        ),
    },
    "returns_body": {
        "ar": (
            "- يمكن طلب استبدال الإطار خلال 7 أيام من الاستلام إذا كان بحالته الأصلية، من غير كسر أو خدش واضح، ومع العلبة إن وُجدت.\n"
            "- العدسة الطبية المقطوعة حسب الروشتة لا تُستبدل إذا طابقت البيانات التي أرسلتها. إذا اختلف التنفيذ عن الروشتة يراجع المتجر الطلب.\n"
            "- إذا وصل المنتج معيباً أو مختلفاً عن الطلب، راسل المتجر على واتساب خلال يومين من الاستلام وأرفق صورة العيب. بعد المعاينة يمكن استبدال القطعة المعيبة أو الاتفاق على إعادة قيمتها.\n"
            "- إذا كان الاستبدال لرغبة شخصية من غير عيب في المنتج، قد لا تُعاد رسوم التوصيل.\n"
            "- نظارات مسلم — باب اللوق، القاهرة. بقية المتاجر تلتزم بهذه السياسة ما لم تذكر صفحتها خلاف ذلك."
        ),
        "en": (
            "- You can ask to exchange a frame within 7 days of delivery if it is still in its original condition, without a clear break or scratch, and with the case if one was included.\n"
            "- A prescription lens cut to your prescription is not exchanged when it matches the details you sent. If the lens was made differently from the prescription, the store reviews the order.\n"
            "- If an item arrives defective or different from the order, message the store on WhatsApp within two days of delivery and include a photo of the problem. After inspection, the defective piece can be exchanged or its price refunded by agreement.\n"
            "- If you exchange an item only because you changed your mind, and there is no defect, the delivery fee may not be refunded.\n"
            "- Moslem Optics — Bab El Louk, Cairo. Other vendors follow this policy unless their page says otherwise."
        ),
    },
}

TERMS = {
    "الكل": "All",
    "طبية": "Medical",
    "شمسية": "Sunglasses",
    "رجالي": "Men",
    "حريمي": "Women",
    "أطفال": "Kids",
    "للجميع": "Everyone",
    "كلاسيك": "Classic",
    "دائري": "Round",
    "أفياتور": "Aviator",
    "كات آي": "Cat-eye",
    "رياضي": "Sport",
    "مربع": "Square",
    "بيضاوي": "Oval",
    "شفاف": "Clear",
    "مستطيل": "Rectangle",
    "قلب": "Heart",
    "عادية": "Clear",
    "Blue Cut": "Blue Cut",
    "طبية شمسية": "Prescription sun",
    "تم التجهيز": "Prepared",
    "جاري التغليف": "Being packed",
    "خرج للتوصيل": "Out for delivery",
    "الدفع عند الاستلام": "Cash on delivery",
    "InstaPay": "InstaPay",
    "فودافون كاش": "Vodafone Cash",
    "رفع صورة": "Upload a photo",
    "الكاميرا": "Camera",
    "رفع صورة الروشتة": "Upload a prescription photo",
    "إدخال المقاسات يدوياً": "Enter measurements",
    "الطلبات": "Orders",
    "إدارة المنتجات": "Manage frames",
    "المتاجر": "Stores",
    "منتجاتي": "My frames",
    "بيانات المتجر": "Store profile",
    "طلبات متجري": "My orders",
    "رسوم التوصيل": "Delivery fees",
    "إعدادات المنصة": "Platform settings",
}

GOV_EN = {
    "القاهرة": "Cairo",
    "الجيزة": "Giza",
    "القليوبية": "Qalyubia",
    "الإسكندرية": "Alexandria",
    "البحيرة": "Beheira",
    "المنوفية": "Monufia",
    "الغربية": "Gharbia",
    "كفر الشيخ": "Kafr El Sheikh",
    "الدقهلية": "Dakahlia",
    "دمياط": "Damietta",
    "الشرقية": "Sharqia",
    "بورسعيد": "Port Said",
    "الإسماعيلية": "Ismailia",
    "السويس": "Suez",
    "الفيوم": "Fayoum",
    "بني سويف": "Beni Suef",
    "المنيا": "Minya",
    "أسيوط": "Asyut",
    "سوهاج": "Sohag",
    "قنا": "Qena",
    "الأقصر": "Luxor",
    "أسوان": "Aswan",
    "البحر الأحمر": "Red Sea",
    "الوادي الجديد": "New Valley",
    "مطروح": "Matrouh",
    "شمال سيناء": "North Sinai",
    "جنوب سيناء": "South Sinai",
}

ETA_EN = {
    "1–2 يوم": "1–2 days",
    "2–3 أيام": "2–3 days",
    "2–4 أيام": "2–4 days",
    "3–4 أيام": "3–4 days",
    "3–5 أيام": "3–5 days",
    "4–6 أيام": "4–6 days",
}

SHAPE_UI = {
    "round": {
        "en": "Round",
        "advice": (
            "Your face is similar in length and width, with a soft jaw. Angular frames add definition and make the face look longer. "
            "Square, classic, and cat-eye suit you best. Small round frames add more roundness, so they are less helpful."
        ),
    },
    "square": {
        "en": "Square",
        "advice": (
            "Your forehead and jaw are similar and the angles are clear. Round frames and aviators soften the jaw and balance the features. "
            "Heavy square frames repeat the angles of the face."
        ),
    },
    "oval": {
        "en": "Oval",
        "advice": (
            "Your proportions are balanced: the cheeks are a little wider than the forehead and jaw. Most frames suit you when they are close to the width of your face. "
            "Classic, aviator, and cat-eye show this balance best."
        ),
    },
    "rectangle": {
        "en": "Rectangle",
        "advice": (
            "Your face is longer than it is wide. Wide, round, and aviator frames add width and break up the length. "
            "Narrow frames make the face look longer."
        ),
    },
    "heart": {
        "en": "Heart",
        "advice": (
            "Your forehead is wider than the jaw and the chin is narrower. Light, round, and aviator frames balance the chin without widening the forehead. "
            "Frames that are heavy on top are less helpful."
        ),
    },
}

OVERLAY_EN = {
    "لم يتم التعرف على الوجه. جرّب صورة أوضح من الأمام.": "The face was not recognized. Try a clearer front-facing photo.",
    "تعذر تحديد العينين بدقة. استخدم صورة أوضح.": "The eyes could not be placed precisely. Use a clearer photo.",
    "تم ضبط المقاس والزاوية تلقائياً حسب العينين والأنف.": "Size and angle were set automatically from the eyes and nose.",
    "تم تركيب النظارة بتقدير تقريبي لأن Face Mesh لم يتعرف على هذه الصورة.": "The glasses were placed approximately because Face Mesh did not recognize this photo.",
}


def lang() -> str:
    try:
        value = st.session_state.get("lang", "ar")
    except Exception:
        return "ar"
    return value if value in ("ar", "en") else "ar"


def direction() -> str:
    return "rtl" if lang() == "ar" else "ltr"


def t(key: str, **kwargs) -> str:
    entry = TEXT.get(key) or {}
    raw = entry.get(lang()) or entry.get("ar") or key
    return raw.format(**kwargs) if kwargs else raw


def term(value: str | None) -> str:
    if not value:
        return ""
    if lang() == "ar":
        return str(value)
    return TERMS.get(str(value), str(value))


def money(amount) -> str:
    value = int(amount)
    if lang() == "en":
        return f"{value} EGP"
    return f"{value} ج.م"


def join(items) -> str:
    sep = "، " if lang() == "ar" else ", "
    return sep.join(str(item) for item in items)


def gov_name(name: str) -> str:
    if lang() == "ar":
        return name
    english = GOV_EN.get(name)
    if not english:
        return name
    return f"{english} — {name}"


def eta_label(eta: str) -> str:
    if lang() == "ar":
        return eta
    return ETA_EN.get(eta, eta)


def shape_label(shape: dict) -> str:
    if lang() == "ar":
        return str(shape.get("label") or "")
    key = str(shape.get("key") or "")
    if key in SHAPE_UI:
        return SHAPE_UI[key]["en"]
    return term(str(shape.get("label") or ""))


def shape_advice(shape: dict) -> str:
    if lang() == "ar":
        return str(shape.get("advice") or "")
    key = str(shape.get("key") or "")
    if key in SHAPE_UI:
        return SHAPE_UI[key]["advice"]
    return str(shape.get("advice") or "")


def overlay_message(message: str) -> str:
    if lang() == "ar":
        return message
    return OVERLAY_EN.get(message, message)


def stock_message(error: BaseException) -> str:
    code = getattr(error, "code", "")
    data = getattr(error, "data", {}) or {}
    if code == "missing":
        return t("stock_missing")
    if code == "short":
        return t("stock_short", name=data.get("name", ""), available=data.get("available", 0))
    return str(error)


def hero(title: str, body: str, color: str = "#5c656c") -> str:
    return (
        '<div class="nv-hero">'
        f'<h2 style="margin:0 0 6px">{title}</h2>'
        f'<p style="margin:0;color:{color}">{body}</p>'
        "</div>"
    )

