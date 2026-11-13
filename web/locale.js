const LANG_KEY = "muslem-lang";

const TEXT = {
  meta: {
    ar: "مسلم - Muslem Optics في باب اللوق. نظارات طبية وشمسية، تجربة حية على الوجه، وتوصيل لكل المحافظات.",
    en: "Muslem Optics in Bab El Louk. Medical and sun glasses, live try-on, and delivery across Egypt.",
  },
  skip: { ar: "تخطَّ إلى المحتوى", en: "Skip to content" },
  announce: { ar: "توصيل من باب اللوق إلى كل المحافظات · خصومات 25%–50%", en: "Delivery from Bab El Louk to every governorate · 25%–50% off" },
  menu: { ar: "القائمة", en: "Menu" },
  cart: { ar: "السلة", en: "Bag" },
  close: { ar: "إغلاق", en: "Close" },
  search: { ar: "بحث", en: "Search" },
  language: { ar: "اللغة", en: "Language" },
  men: { ar: "رجالي", en: "Men" },
  women: { ar: "حريمي", en: "Women" },
  kids: { ar: "أطفالي", en: "Kids" },
  sun: { ar: "نظارات شمسية", en: "Sunglasses" },
  medical: { ar: "نظارات طبية", en: "Eyeglasses" },
  sports: { ar: "نظارات رياضية", en: "Sports" },
  reading: { ar: "نظارات قراءة", en: "Reading glasses" },
  lensTypes: { ar: "أنواع العدسات", en: "Lens types" },
  lensIntro: {
    ar: "هذه العدسات المتاحة عند شراء الإطار. بدون عدسات تنتقل مباشرة لإتمام الطلب، وبعدسات طبية يفتح واتساب المحل.",
    en: "These are the lenses available when you buy a frame. Without lenses you go straight to checkout. With prescription lenses the shop WhatsApp opens.",
  },
  lensIncluded: { ar: "ضمن سعر الإطار", en: "Included in the frame price" },
  lensAdded: { ar: "تُضاف على سعر الإطار", en: "Added to the frame price" },
  bestsellers: { ar: "الأكثر مبيعاً", en: "Bestsellers" },
  saleMenu: { ar: "عروض وخصومات", en: "Sale" },
  about: { ar: "عن مسلم", en: "About" },
  tryon: { ar: "التجربة الحية", en: "Try-on" },
  shipping: { ar: "الشحن", en: "Shipping" },
  track: { ar: "تتبّع الطلب", en: "Track order" },
  contact: { ar: "تواصل", en: "Contact" },
  footerNav: { ar: "روابط أسفل الصفحة", en: "Footer" },
  categories: { ar: "التصنيفات", en: "Categories" },
  searchLabel: { ar: "بحث في التشكيلة", en: "Search the collection" },
  searchPh: { ar: "ابحث عن إطار، لون، أو ماركة", en: "Search a frame, color, or brand" },
  searchAll: { ar: "عرض كل النتائج", en: "View all results" },
  buy: { ar: "شراء", en: "Buy" },
  buyTitle: { ar: "كيف تريد الإطار؟", en: "How do you want this frame?" },
  buyPlain: { ar: "بدون عدسات", en: "Without lenses" },
  buyRx: { ar: "بعدسات طبية", en: "With prescription lenses" },
  buyRxHelp: { ar: "أرسل الكشف والعدسة المحددة مباشرة إلى المحل.", en: "Send the prescription and the chosen lens to the shop." },
  whatsapp: { ar: "واتساب", en: "WhatsApp" },
  vtoTitle: { ar: "جرب النظارة على وشك حالا! 👓✨", en: "Try the glasses on your face now! 👓✨" },
  vtoBody: { ar: "التجربة الحية بالكاميرا 3D", en: "Live 3D camera try-on" },
  vtoCta: { ar: "افتح الكاميرا الآن", en: "Open the camera" },
  emptySection: { ar: "لا توجد إطارات في هذا القسم.", en: "No frames in this section." },
  missingFrame: { ar: "الإطار غير موجود", en: "Frame not found" },
  backShop: { ar: "العودة إلى التشكيلة", en: "Back to the collection" },
  home: { ar: "الرئيسية", en: "Home" },
  crumbs: { ar: "مسار الصفحة", en: "Breadcrumb" },
  tryLive: { ar: "👓 التجربة الحية (افتح الكاميرا)", en: "👓 Live try-on (open camera)" },
  rating: { ar: "تقييم {n}", en: "Rating {n}" },
  suits: { ar: "يناسب الوجه: {shapes}", en: "Suits: {shapes}" },
  qty: { ar: "الكمية", en: "Qty" },
  soldOut: { ar: "نفد", en: "Sold out" },
  outLong: { ar: "نفد من التشكيلة", en: "Sold out" },
  lastN: { ar: "آخر {n} قطع", en: "Last {n} left" },
  available: { ar: "متوفر", en: "In stock" },
  buyNote: { ar: "بدون عدسات تنتقل إلى بيانات الشحن. العدسات الطبية تُطلب عبر واتساب المحل.", en: "Without lenses you go straight to shipping. Prescription lenses are ordered on the shop WhatsApp." },
  related: { ar: "إطارات قريبة", en: "You may also like" },
  goneLine: { ar: "إطار لم يعد في التشكيلة", en: "This frame is no longer in the collection" },
  remove: { ar: "حذف", en: "Remove" },
  decrease: { ar: "تقليل", en: "Decrease" },
  increase: { ar: "زيادة", en: "Increase" },
  emptyCart: { ar: "السلة فارغة", en: "Your bag is empty" },
  emptyCartBody: { ar: "اختر إطاراً من التشكيلة أو جرّبه على وجهك أولاً.", en: "Choose a frame from the collection, or try it on first." },
  shopCollection: { ar: "تسوق التشكيلة", en: "Shop the collection" },
  bagTitle: { ar: "السلة", en: "Bag" },
  summary: { ar: "الملخص", en: "Summary" },
  frames: { ar: "الإطارات", en: "Frames" },
  shipNext: { ar: "رسوم التوصيل تُضاف في الخطوة التالية حسب المحافظة.", en: "Delivery is added on the next step, based on your governorate." },
  checkout: { ar: "إتمام الطلب", en: "Checkout" },
  continueShop: { ar: "متابعة التسوق", en: "Continue shopping" },
  missingCart: { ar: "في السلة إطار لم يعد متاحاً. احذفه قبل المتابعة.", en: "The bag has a frame that is no longer available. Remove it before continuing." },
  name: { ar: "الاسم", en: "Name" },
  namePh: { ar: "الاسم الثلاثي", en: "Full name" },
  phone: { ar: "الهاتف", en: "Phone" },
  gov: { ar: "المحافظة", en: "Governorate" },
  address: { ar: "العنوان", en: "Address" },
  addressPh: { ar: "الشارع، العلامة، رقم العمارة", en: "Street, landmark, building number" },
  payment: { ar: "الدفع", en: "Payment" },
  transferRef: { ar: "رقم العملية", en: "Transaction number" },
  refPh: { ar: "رقم التحويل", en: "Transfer reference" },
  rxTitle: { ar: "مقاس الروشتة، إن وُجد", en: "Prescription, if you have it" },
  rxNote: { ar: "يمكن ترك المقاس فارغاً وإرسال صورة الروشتة على واتساب بعد الطلب. العدسة لا تُقص قبل المراجعة.", en: "You can leave this blank and send a photo of the prescription on WhatsApp after ordering. The lens is not cut before review." },
  note: { ar: "ملاحظة", en: "Note" },
  notePh: { ar: "موعد مفضّل، أو تفصيل للعنوان", en: "Preferred time, or a detail about the address" },
  placeOrder: { ar: "تأكيد الطلب", en: "Place order" },
  yourOrder: { ar: "طلبك", en: "Your order" },
  frameFallback: { ar: "إطار", en: "Frame" },
  deliverTo: { ar: "التوصيل إلى {gov}", en: "Delivery to {gov}" },
  total: { ar: "الإجمالي", en: "Total" },
  eta: { ar: "الوصول المتوقع: {eta}", en: "Expected arrival: {eta}" },
  reviewCart: { ar: "راجع السلة قبل تأكيد الطلب.", en: "Review the bag before placing the order." },
  instapayHelp: { ar: "حوّل إلى InstaPay: {account} ثم اكتب رقم العملية.", en: "Transfer to InstaPay: {account}, then enter the transaction number." },
  vodafoneHelp: { ar: "حوّل فودافون كاش إلى {account} ثم اكتب رقم العملية.", en: "Transfer Vodafone Cash to {account}, then enter the transaction number." },
  received: { ar: "استلمنا طلبك", en: "We received your order" },
  orderStatus: { ar: "حالة الطلب", en: "Order status" },
  receivedBody: { ar: "سيجهز المحل الطلب من باب اللوق. احتفظ برقم الطلب لتتبعه.", en: "The shop will prepare the order in Bab El Louk. Keep the order number to track it." },
  orderedOn: { ar: "بتاريخ {date}", en: "Placed on {date}" },
  qtyLine: { ar: "الكمية {n}", en: "Qty {n}" },
  handover: { ar: "التسليم", en: "Delivery" },
  shipFee: { ar: "التوصيل", en: "Delivery" },
  payLine: { ar: "الدفع: {method}", en: "Payment: {method}" },
  measureAttached: { ar: "مقاس مرفق مع الطلب.", en: "A prescription is attached to this order." },
  sendOrder: { ar: "إرسال الطلب على واتساب", en: "Send the order on WhatsApp" },
  loadingOrder: { ar: "جاري جلب الطلب…", en: "Loading the order…" },
  noOrder: { ar: "لا يوجد طلب بهذا الرقم", en: "No order with this number" },
  noOrderBody: { ar: "تأكد من الرقم، مثل MO-AB12CD.", en: "Check the number, for example MO-AB12CD." },
  trackCta: { ar: "تتبّع طلب", en: "Track an order" },
  orderNumber: { ar: "رقم الطلب", en: "Order number" },
  showStatus: { ar: "عرض الحالة", en: "Show status" },
  loading: { ar: "جاري فتح المتجر…", en: "Opening the shop…" },
  catalogFail: { ar: "تعذر فتح التشكيلة", en: "The collection could not be opened" },
  catalogFailBody: { ar: "أعد تشغيل المتجر من ملف run.bat ثم حدّث الصفحة.", en: "Restart the shop from run.bat, then refresh the page." },
  outToast: { ar: "هذا الإطار نفد من التشكيلة.", en: "This frame is sold out." },
  stockLeft: { ar: "المتوفر {n} قطع.", en: "{n} available." },
  added: { ar: "أُضيف {name} إلى السلة.", en: "{name} was added to the bag." },
  viewBag: { ar: "عرض السلة", en: "View bag" },
  collection: { ar: "التشكيلة", en: "Collection" },
  deals: { ar: "تخفيضات", en: "Sale" },
  results: { ar: "نتائج «{q}»", en: "Results for “{q}”" },
  sunMen: { ar: "نظارات شمسية رجالي", en: "Men’s sunglasses" },
  sunWomen: { ar: "نظارات شمسية حريمي", en: "Women’s sunglasses" },
  sunTitle: { ar: "النظارات الشمسية", en: "Sunglasses" },
  medicalTitle: { ar: "النظارات الطبية", en: "Eyeglasses" },
  docTitle: { ar: "{title} | مسلم", en: "{title} | Muslem" },
  homeTitle: { ar: "مسلم | Muslem Optics", en: "Muslem | Muslem Optics" },
  frameTitle: { ar: "الإطار | مسلم", en: "Frame | Muslem" },
  aboutP1: { ar: "مسلم - Muslem Optics محل نظارات في باب اللوق بالقاهرة. هذا الموقع واجهة المحل نفسه: الإطارات المعروضة تُختار وتُشحن منه، وليست سوقاً لمحلات أخرى.", en: "Muslem Optics is an eyewear shop in Bab El Louk, Cairo. This site is the shop itself: the frames shown are chosen and shipped from there, not a marketplace of other stores." },
  aboutP2: { ar: "تجد في التشكيلة نظارات طبية وشمسية للرجال والنساء والأطفال، وبعض الماركات الموجودة داخل المحل مثل أوكلي وبوليس إلى جانب إطارات مسلم.", en: "The collection includes medical and sun glasses for men, women, and kids, plus brands in the shop such as Oakley and Police alongside Muslem frames." },
  aboutP3: { ar: "يمكن تجربة الإطار على الوجه بالكاميرا قبل الطلب. الصورة تُعالج في متصفحك ولا تُرفع إلينا.", en: "You can try a frame on your face with the camera before ordering. The image is processed in your browser and is not uploaded." },
  shipIntro: { ar: "يخرج الطلب من باب اللوق. الرسوم تقديرية وتظهر في صفحة الإتمام قبل التأكيد.", en: "Orders leave from Bab El Louk. Fees are estimates and appear on checkout before you confirm." },
  govCol: { ar: "المحافظة", en: "Governorate" },
  feeCol: { ar: "الرسوم", en: "Fee" },
  etaCol: { ar: "الوصول المتوقع", en: "Expected arrival" },
  returnsP1: { ar: "يمكن طلب استبدال الإطار خلال 14 يوماً إذا كان بحالته الأصلية ومن غير خدش أو تعديل.", en: "A frame can be exchanged within 14 days if it is in its original condition, without scratches or changes." },
  returnsP2: { ar: "العدسة الطبية التي قُصّت على مقاس الروشتة لا تُستبدل إلا إذا كان الخطأ من المحل في تنفيذ المقاس.", en: "A prescription lens cut to your measurements is exchanged only if the shop made the lens incorrectly." },
  returnsP3: { ar: "لبدء طلب، أرسل رقم الطلب على واتساب {phone}.", en: "To start a request, send the order number on WhatsApp {phone}." },
  faqCamQ: { ar: "هل التجربة الحية ترفع صورتي؟", en: "Does live try-on upload my photo?" },
  faqCamA: { ar: "لا. الكاميرا وتتبع الوجه يعملان داخل المتصفح، واللقطة التي تحفظها تبقى على جهازك.", en: "No. The camera and face tracking run in the browser, and any photo you save stays on your device." },
  faqRxQ: { ar: "كيف أرسل الروشتة؟", en: "How do I send the prescription?" },
  faqRxA: { ar: "اكتب المقاس عند إتمام الطلب، أو أرسل صورة الروشتة على واتساب مع رقم الطلب قبل قص العدسة.", en: "Enter the measurements at checkout, or send a photo of the prescription on WhatsApp with the order number before the lens is cut." },
  faqPayQ: { ar: "ما طرق الدفع؟", en: "Which payment methods are available?" },
  faqPayA: { ar: "الدفع عند الاستلام، أو InstaPay على {account}، أو فودافون كاش على {phone}.", en: "Cash on delivery, InstaPay to {account}, or Vodafone Cash to {phone}." },
  faqFromQ: { ar: "من أين يصل الطلب؟", en: "Where does the order ship from?" },
  faqFromA: { ar: "من مسلم - Muslem Optics في {address}. لا يوجد تجار آخرون على الموقع.", en: "From Muslem Optics in {address}. There are no other sellers on this site." },
  addressLabel: { ar: "العنوان: {address}", en: "Address: {address}" },
  phoneLabel: { ar: "الهاتف: {phone}", en: "Phone: {phone}" },
  instagram: { ar: "إنستغرام", en: "Instagram" },
  facebook: { ar: "فيسبوك", en: "Facebook" },
  privacyP1: { ar: "نحفظ بيانات الطلب التي تكتبها: الاسم والهاتف والعنوان ومحتوى السلة، حتى نجهّز الشحنة من المحل. تبقى هذه البيانات على جهاز تشغيل المتجر.", en: "We keep the order details you enter — name, phone, address, and bag — so the shop can prepare the shipment. That data stays on the machine running the shop." },
  privacyP2: { ar: "صورة الكاميرا في التجربة الحية لا تُرسل إلى الخادم. نموذج تتبع الوجه يُحمَّل في متصفحك من خدمة MediaPipe.", en: "The live try-on camera image is not sent to the server. The face-tracking model is loaded in your browser from MediaPipe." },
  termsP1: { ar: "الأسعار بالجنيه المصري وتشمل الإطار والعدسة المختارة، ولا تشمل التوصيل إلا بعد اختيار المحافظة.", en: "Prices are in Egyptian pounds and include the frame and selected lens. Delivery is added only after you choose a governorate." },
  termsP2: { ar: "المخزون يُحدَّث عند تأكيد الطلب. إذا نفدت الكمية قبل التأكيد تظهر رسالة ولن يُخصم المبلغ من المخزون.", en: "Stock updates when the order is confirmed. If the quantity runs out before confirmation, a message appears and stock is not reduced." },
  termsP3: { ar: "الموقع خاص بمسلم - Muslem Optics في باب اللوق، وليس منصة لتسجيل محلات.", en: "This site belongs to Muslem Optics in Bab El Louk. It is not a platform for other shops to register." },
  notFound: { ar: "الصفحة غير موجودة", en: "Page not found" },
  backHome: { ar: "العودة إلى الرئيسية", en: "Back to home" },
  returnsTitle: { ar: "الاستبدال والإرجاع", en: "Exchanges and returns" },
  faqTitle: { ar: "الأسئلة الشائعة", en: "FAQ" },
  contactTitle: { ar: "تواصل معنا", en: "Contact" },
  privacyTitle: { ar: "الخصوصية", en: "Privacy" },
  termsTitle: { ar: "الشروط", en: "Terms" },
  shippingTitle: { ar: "الشحن والتوصيل", en: "Shipping and delivery" },
  aboutTitle: { ar: "عن مسلم", en: "About Muslem" },
  waHello: { ar: "مرحباً، أتممت طلباً من مسلم - Muslem Optics.", en: "Hello, I placed an order with Muslem Optics." },
  waOrder: { ar: "رقم الطلب: {id}", en: "Order number: {id}" },
  waName: { ar: "الاسم: {name}", en: "Name: {name}" },
  waPhone: { ar: "الهاتف: {phone}", en: "Phone: {phone}" },
  waAddress: { ar: "العنوان: {address} — {gov}", en: "Address: {address} — {gov}" },
  waTotal: { ar: "الإجمالي: {total} جنيه", en: "Total: {total} EGP" },
  waNote: { ar: "ملاحظة: {note}", en: "Note: {note}" },
  live: { ar: "LIVE TRY-ON", en: "LIVE TRY-ON" },
  lookAt: { ar: "انظر إلى الكاميرا", en: "Look at the camera" },
  privacyCam: { ar: "التتبّع يتم داخل المتصفح. صورة وجهك لا تُرسل إلى الخادم ولا تُحفظ.", en: "Tracking runs in the browser. Your face is not sent to the server and is not saved." },
  startCam: { ar: "تشغيل الكاميرا", en: "Start camera" },
  frameSize: { ar: "حجم الإطار", en: "Frame size" },
  frameHeight: { ar: "ارتفاع الإطار", en: "Frame height" },
  lens: { ar: "العدسة", en: "Lens" },
  addCart: { ar: "أضف إلى السلة", en: "Add to bag" },
  framePage: { ar: "صفحة الإطار", en: "Frame page" },
  moveFace: { ar: "حرّك وجهك أمام الكاميرا لنقترح الإطارات الأقرب لشكل الوجه.", en: "Move your face in front of the camera and we will suggest frames for your face shape." },
  capture: { ar: "التقاط", en: "Capture" },
  flipCam: { ar: "تبديل الكاميرا", en: "Flip camera" },
  stopCam: { ar: "إيقاف", en: "Stop" },
  lookStraight: { ar: "انظر مباشرة إلى الكاميرا حتى يثبت الإطار", en: "Look straight at the camera so the frame stays steady" },
  camUnavailable: { ar: "الكاميرا غير متاحة", en: "Camera unavailable" },
  camFail: { ar: "تعذر فتح الكاميرا.", en: "The camera could not be opened." },
  camDenied: { ar: "لم يُسمح بالكاميرا. اسمح بها من أيقونة القفل بجانب العنوان ثم أعد المحاولة.", en: "Camera permission was denied. Allow it from the lock icon beside the address, then try again." },
  camMissing: { ar: "لا توجد كاميرا متاحة على هذا الجهاز.", en: "No camera is available on this device." },
  camUnsupported: { ar: "المتصفح لا يتيح الكاميرا من هذا العنوان. افتح المتجر من كروم أو إيدج.", en: "This browser cannot open the camera from this address. Open the shop in Chrome or Edge." },
  retry: { ar: "إعادة المحاولة", en: "Try again" },
  openingCam: { ar: "جاري فتح الكاميرا", en: "Opening the camera" },
  openingCamBody: { ar: "ثم يُجهَّز تتبّع الوجه. قد يأخذ ذلك بضع ثوانٍ في أول مرة.", en: "Face tracking is prepared next. The first time can take a few seconds." },
  trackFail: { ar: "تعذر تتبّع الوجه", en: "Face tracking failed" },
  trackFailBody: { ar: "تحقق من الاتصال بالإنترنت حتى يُحمَّل نموذج التتبّع، ثم أعد المحاولة. الكاميرا نفسها تبقى على جهازك.", en: "Check your internet connection so the tracking model can load, then try again. The camera itself stays on your device." },
  faceIs: { ar: "شكل الوجه: {shape}", en: "Face shape: {shape}" },
  fromCollection: { ar: "من التشكيلة:", en: "From the collection:" },
  savePhoto: { ar: "حفظ الصورة", en: "Save photo" },
  shotAlt: { ar: "لقطة التجربة", en: "Try-on photo" },
  tryonTitle: { ar: "{name} — تجربة حية | مسلم", en: "{name} — Live try-on | Muslem" },
  odSph: { ar: "العين اليمنى SPH", en: "Right eye SPH" },
  osSph: { ar: "العين اليسرى SPH", en: "Left eye SPH" },
  odCyl: { ar: "اليمنى CYL", en: "Right CYL" },
  osCyl: { ar: "اليسرى CYL", en: "Left CYL" },
  odAxis: { ar: "اليمنى AXIS", en: "Right AXIS" },
  osAxis: { ar: "اليسرى AXIS", en: "Left AXIS" },
};

const TERMS = {
  "طبية": "Medical",
  "شمسية": "Sunglasses",
  "قراءة": "Reading",
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
  "أسود": "Black",
  "ذهبي": "Gold",
  "فضي": "Silver",
  "وردي": "Pink",
  "كحلي": "Navy",
  "تاورتوز": "Tortoiseshell",
  "زيتوني": "Olive",
  "بني": "Brown",
  "أزرق": "Blue",
  "أحمر": "Red",
  "أصفر": "Yellow",
  "أوكلي": "Oakley",
  "بوليس": "Police",
  "نظارات مسلم": "Muslem",
  "مسلم": "Muslem",
  "تم التجهيز": "Prepared",
  "جاري التغليف": "Being packed",
  "خرج للتوصيل": "Out for delivery",
  "الدفع عند الاستلام": "Cash on delivery",
  "فودافون كاش": "Vodafone Cash",
  "الإطار كما هو": "Frame only",
  "عدسة طبية عادية": "Standard prescription lens",
  "عدسة Blue Cut": "Blue Cut lens",
  "عدسة طبية شمسية": "Prescription sun lens",
};

const NAMES = {
  "مسلم كلاسيك أسود": "Muslem Classic Black",
  "مسلم دائري ذهبي": "Muslem Round Gold",
  "أوكلي أفياتور": "Oakley Aviator",
  "مسلم كات آي": "Muslem Cat-eye",
  "أوكلي سبورت": "Oakley Sport",
  "بوليس تاورتوز": "Police Tortoiseshell",
  "مسلم بيضاوي": "Muslem Oval",
  "مسلم شفاف": "Muslem Clear",
  "مسلم برولاين بني": "Muslem Browline Brown",
  "بوليس وايفارير": "Police Wayfarer",
  "مسلم أطفال دائري": "Muslem Kids Round",
  "مسلم أطفال مرن": "Muslem Kids Flex",
  "بوليس كات آي": "Police Cat-eye",
  "مسلم دائري شمسي": "Muslem Round Sun",
  "مسلم أطفال شمسية": "Muslem Kids Sun",
  "مسلم أطفال رياضية": "Muslem Kids Sport",
};

const DESCS = {
  "مسلم كلاسيك أسود": "A men’s medical frame from the Bab El Louk shop. A light rectangle that suits round and oval faces.",
  "مسلم دائري ذهبي": "A women’s round medical frame from the shop. Thin gold metal softens square and rectangular faces.",
  "أوكلي أفياتور": "Aviator sunglasses from the Oakley corner of the shop. Dark lenses and a metal frame.",
  "مسلم كات آي": "A women’s cat-eye medical frame from Bab El Louk. It lifts the eye line on round and oval faces.",
  "أوكلي سبورت": "Oakley sport sunglasses with dark lenses and a wrap frame, as shown in the brand corner.",
  "بوليس تاورتوز": "A men’s Police medical frame in tortoiseshell. It adds definition to a round face.",
  "مسلم بيضاوي": "A women’s oval medical frame from the shop. It balances square, rectangular, and heart-shaped faces.",
  "مسلم شفاف": "A light clear medical frame from the shop, made for everyday wear on an oval face.",
  "مسلم برولاين بني": "A men’s medical frame with a brown browline from the shop. It defines round and oval faces.",
  "بوليس وايفارير": "Wayfarer sunglasses from the Police corner. Dark lenses and a wide frame for a round face.",
  "مسلم أطفال دائري": "A round kids’ medical frame from the shop, flexible and light, for square and rectangular faces.",
  "مسلم أطفال مرن": "A flexible pink kids’ medical frame from Bab El Louk, light enough for school.",
  "بوليس كات آي": "Women’s Police cat-eye sunglasses with brown lenses. They lift the features on round and oval faces.",
  "مسلم دائري شمسي": "Round sunglasses from the shop with dark lenses and a gold frame. They soften square and rectangular faces.",
  "مسلم أطفال شمسية": "Small kids’ sunglasses from the shop, with dark lenses and a light frame.",
  "مسلم أطفال رياضية": "Kids’ sport sunglasses from the shop, with a wrap frame and dark lenses.",
};

const GOV = {
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
};

const ETA = {
  "1–2 يوم": "1–2 days",
  "2–3 أيام": "2–3 days",
  "2–4 أيام": "2–4 days",
  "3–4 أيام": "3–4 days",
  "3–5 أيام": "3–5 days",
  "4–6 أيام": "4–6 days",
};

const LENS = {
  none: "Frame only",
  plain: "Standard prescription lens",
  blue: "Blue Cut lens",
  sun: "Prescription sun lens",
};

const PAY = {
  cod: "Cash on delivery",
  instapay: "InstaPay",
  vodafone: "Vodafone Cash",
};

const SHAPE = {
  round: "Your face is similar in length and width. Angular, square, and cat-eye frames add clearer definition.",
  square: "The jaw angles are clear. Round frames and aviators soften the features and balance the face.",
  oval: "The proportions are balanced. Most frames suit you when they are close to the width of your face.",
  rectangle: "The face is longer than it is wide. Wide, round, and aviator frames break up the length.",
  heart: "The forehead is wider than the chin. Light round frames balance the face without weight at the top.",
};

const listeners = new Set();

export function getLang() {
  try {
    return localStorage.getItem(LANG_KEY) === "en" ? "en" : "ar";
  } catch {
    return "ar";
  }
}

export function t(key, vars) {
  const entry = TEXT[key];
  let raw = entry ? (entry[getLang()] || entry.ar || key) : key;
  if (vars) {
    Object.entries(vars).forEach(([name, value]) => {
      raw = raw.replaceAll(`{${name}}`, String(value));
    });
  }
  return raw;
}

export function term(value) {
  const text = String(value ?? "");
  if (!text || getLang() === "ar") return text;
  return TERMS[text] || text;
}

export function money(amount) {
  const number = new Intl.NumberFormat("en-EG", { maximumFractionDigits: 0 }).format(Number(amount) || 0);
  return getLang() === "en" ? `EGP ${number}` : `${number} ج.م`;
}

export function productName(name) {
  const text = String(name || "");
  if (getLang() === "ar") return text;
  return NAMES[text] || text;
}

export function productText(name, description) {
  const text = String(description || "");
  if (getLang() === "ar") return text;
  return DESCS[name] || text;
}

export function lensLabel(item) {
  if (!item) return "";
  if (getLang() === "ar") return item.label || "";
  return LENS[item.id] || term(item.label);
}

export function payLabel(item) {
  if (!item) return "";
  if (getLang() === "ar") return item.label || "";
  return PAY[item.id] || term(item.label);
}

export function govLabel(name) {
  const text = String(name || "");
  if (getLang() === "ar") return text;
  return GOV[text] || text;
}

export function etaLabel(eta) {
  const text = String(eta || "");
  if (getLang() === "ar") return text;
  return ETA[text] || text;
}

export function shopAddress(address) {
  const text = String(address || "");
  if (getLang() === "ar") return text;
  if (text === "باب اللوق، القاهرة") return "Bab El Louk, Cairo";
  return text;
}

export function shapeAdvice(key, arabic) {
  if (getLang() === "ar") return arabic;
  return SHAPE[key] || arabic;
}

export function listJoin(items) {
  return items.filter(Boolean).join(getLang() === "ar" ? "، " : ", ");
}

export function searchBits(fields) {
  const bits = [];
  const push = (value) => {
    if (!value) return;
    const text = String(value);
    bits.push(text);
    if (TERMS[text]) bits.push(TERMS[text]);
    if (NAMES[text]) bits.push(NAMES[text]);
    if (DESCS[text]) bits.push(DESCS[text]);
  };
  push(fields.name);
  push(fields.brand);
  push(fields.category);
  push(fields.kind);
  push(fields.audience);
  push(fields.color);
  push(fields.description);
  (fields.face_shapes || []).forEach(push);
  return bits.join(" ");
}

export function applyDocument() {
  const lang = getLang();
  document.documentElement.lang = lang;
  document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
  document.querySelectorAll("[data-set-lang]").forEach((button) => {
    const on = button.dataset.setLang === lang;
    button.setAttribute("aria-pressed", on ? "true" : "false");
  });
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
    node.setAttribute("placeholder", t(node.dataset.i18nPlaceholder));
  });
  document.querySelectorAll("[data-i18n-aria]").forEach((node) => {
    node.setAttribute("aria-label", t(node.dataset.i18nAria));
  });
  const meta = document.querySelector('meta[name="description"]');
  if (meta) meta.setAttribute("content", t("meta"));
}

export function setLang(value) {
  const next = value === "en" ? "en" : "ar";
  try {
    localStorage.setItem(LANG_KEY, next);
  } catch {
    /* تبقى اللغة في هذه الجلسة فقط */
  }
  applyDocument();
  listeners.forEach((fn) => fn(next));
}

export function onLang(fn) {
  listeners.add(fn);
}
