"""تجربة النظارة الافتراضية عبر MediaPipe Face Mesh."""

from __future__ import annotations

import os
import shutil
import tempfile
import threading
from pathlib import Path
from urllib.request import urlretrieve

import cv2
import numpy as np
from PIL import Image

from paths import model_path

# طوبولوجيا Face Mesh: 478 نقطة مع القزحية.
RIGHT_EYE_OUTER = 33
RIGHT_EYE_INNER = 133
LEFT_EYE_OUTER = 263
LEFT_EYE_INNER = 362
RIGHT_IRIS = 468
LEFT_IRIS = 473
NOSE_TIP = 1
NOSE_BRIDGE = 6

# عرض العدسات بالنسبة للمسافة بين الزاويتين الخارجيتين للعينين.
LENS_TO_EYE = 1.16
FACE_MESH_VERSION = "3"

# نقاط محيط الوجه في Face Mesh.
FOREHEAD_TOP = 10
CHIN = 152
CHEEK_LEFT = 234
CHEEK_RIGHT = 454
TEMPLE_LEFT = 54
TEMPLE_RIGHT = 284
JAW_LEFT = 172
JAW_RIGHT = 397
JAW_CORNER_LEFT = 132
JAW_CORNER_RIGHT = 361

SHAPE_GUIDES = {
    "round": {
        "label": "دائري",
        "categories": ["مربع", "كلاسيك", "كات آي"],
        "advice": (
            "وجهك متقارب الطول والعرض وفكه ناعم. الإطارات الزاوية تضيف تحديداً وتُظهر الوجه أطول. "
            "الأنسب المربع والكلاسيك والكات آي، وابتعد عن الإطارات الدائرية الصغيرة لأنها تزيد الاستدارة."
        ),
    },
    "square": {
        "label": "مربع",
        "categories": ["دائري", "بيضاوي", "أفياتور"],
        "advice": (
            "جبهتك والفك متقاربان والزوايا واضحة. الإطارات الدائرية والأفياتور تنعّم الفك وتوازن الملامح. "
            "تجنّب الإطارات المربعة الثقيلة لأنها تكرر زوايا الوجه."
        ),
    },
    "oval": {
        "label": "بيضاوي",
        "categories": ["كلاسيك", "أفياتور", "كات آي", "شفاف"],
        "advice": (
            "نسب وجهك متوازنة: الخدان أعرض قليلاً من الجبهة والفك. أغلب الإطارات تليق بك إذا كان عرضها قريباً من عرض الوجه. "
            "الكلاسيك والأفياتور والكات آي يظهرون هذا التوازن بأفضل شكل."
        ),
    },
    "rectangle": {
        "label": "مستطيل",
        "categories": ["دائري", "أفياتور", "بيضاوي"],
        "advice": (
            "وجهك أطول من عرضه. الإطارات العريضة والدائرية والأفياتور تضيف عرضاً وتكسر الطول. "
            "تجنّب الإطارات الضيقة لأنها تجعل الوجه أطول."
        ),
    },
    "heart": {
        "label": "قلب",
        "categories": ["دائري", "أفياتور", "بيضاوي"],
        "advice": (
            "جبهتك أعرض من الفك والذقن أضيق. الإطارات الخفيفة والدائرية والأفياتور توازن الذقن دون أن تزيد عرض الجبهة. "
            "تجنّب الإطارات الثقيلة من الأعلى."
        ),
    },
}

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "face_landmarker/face_landmarker/float16/latest/face_landmarker.task"
)
FACE_XML_URL = (
    "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/"
    "haarcascade_frontalface_default.xml"
)
EYE_XML_URL = (
    "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/"
    "haarcascade_eye.xml"
)

_LANDMARKER = None
_LANDMARKER_FAILED = False
_LOCK = threading.Lock()


def _ascii_cache_dir() -> Path:
    root = os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()
    path = Path(root) / "NoorVision"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _download(url: str, dest: Path) -> Path | None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        urlretrieve(url, dest)
        if dest.exists() and dest.stat().st_size > 1000:
            return dest
    except Exception:
        return None
    return dest if dest.exists() else None


def _cached_file(name: str, source: Path | None, url: str) -> Path | None:
    cached = _ascii_cache_dir() / name
    if cached.exists() and cached.stat().st_size > 1000:
        return cached
    if source and source.exists() and source.stat().st_size > 1000:
        shutil.copy2(source, cached)
        return cached
    return _download(url, cached)


def _ensure_model() -> Path | None:
    return _cached_file("face_landmarker.task", model_path(), MODEL_URL)


def _create_landmarker(with_matrix: bool):
    import mediapipe as mp
    from mediapipe.tasks.python import BaseOptions
    from mediapipe.tasks.python.vision import FaceLandmarker, FaceLandmarkerOptions

    model = _ensure_model()
    if model is None:
        return None
    options = FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=str(model)),
        num_faces=1,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        output_facial_transformation_matrixes=with_matrix,
    )
    landmarker = FaceLandmarker.create_from_options(options)
    return landmarker, mp


def _get_landmarker():
    global _LANDMARKER, _LANDMARKER_FAILED
    if _LANDMARKER_FAILED:
        return None
    if _LANDMARKER is not None:
        return _LANDMARKER
    try:
        created = _create_landmarker(True)
    except Exception:
        created = None
    if created is None:
        try:
            created = _create_landmarker(False)
        except Exception:
            created = None
    if created is None:
        _LANDMARKER_FAILED = True
        return None
    _LANDMARKER = created
    return _LANDMARKER


def _xy(point, width: int, height: int) -> list[float]:
    return [float(point.x * width), float(point.y * height)]


def _pair_by_x(a: list[float], b: list[float]) -> tuple[list[float], list[float]]:
    if a[0] <= b[0]:
        return a, b
    return b, a


def _distance(a, b) -> float:
    return float(np.linalg.norm(np.asarray(a, dtype=np.float64) - np.asarray(b, dtype=np.float64)))


def _corner_angle(a, b, c) -> float:
    ba = np.asarray(a, dtype=np.float64) - np.asarray(b, dtype=np.float64)
    bc = np.asarray(c, dtype=np.float64) - np.asarray(b, dtype=np.float64)
    denom = float(np.linalg.norm(ba) * np.linalg.norm(bc))
    if denom < 1e-6:
        return 180.0
    cosine = float(np.dot(ba, bc) / denom)
    return float(np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0))))


def _classify_shape(length_ratio: float, temple_ratio: float, jaw_ratio: float, jaw_angle: float) -> str:
    taper = temple_ratio - jaw_ratio
    if taper >= 0.12 and jaw_ratio < 0.80:
        return "heart"
    if length_ratio >= 1.40:
        return "rectangle"
    if length_ratio < 1.34 and jaw_ratio >= 0.86 and jaw_angle <= 150:
        return "square"
    if length_ratio < 1.20 and jaw_ratio >= 0.80 and jaw_angle >= 130:
        return "round"
    return "oval"


def _shape_from_mesh(points, width: int, height: int, yaw: float) -> dict | None:
    if len(points) <= JAW_RIGHT:
        return None

    def xy(index: int) -> list[float]:
        return [points[index].x * width, points[index].y * height]

    cheek = _distance(xy(CHEEK_LEFT), xy(CHEEK_RIGHT))
    if cheek < 8:
        return None
    length_ratio = _distance(xy(FOREHEAD_TOP), xy(CHIN)) / cheek
    temple_ratio = _distance(xy(TEMPLE_LEFT), xy(TEMPLE_RIGHT)) / cheek
    jaw_ratio = _distance(xy(JAW_LEFT), xy(JAW_RIGHT)) / cheek
    jaw_angle = (
        _corner_angle(xy(CHEEK_LEFT), xy(JAW_CORNER_LEFT), xy(JAW_LEFT))
        + _corner_angle(xy(CHEEK_RIGHT), xy(JAW_CORNER_RIGHT), xy(JAW_RIGHT))
    ) / 2.0
    yaw_scale = max(0.72, abs(float(np.cos(np.radians(yaw)))))
    length_ratio *= yaw_scale
    key = _classify_shape(length_ratio, temple_ratio, jaw_ratio, jaw_angle)
    guide = SHAPE_GUIDES[key]
    return {
        "key": key,
        "label": guide["label"],
        "categories": list(guide["categories"]),
        "advice": guide["advice"],
        "length_ratio": round(float(length_ratio), 3),
        "jaw_angle": round(float(jaw_angle), 1),
        "yaw": round(float(yaw), 1),
    }


def _yaw_degrees(matrix) -> float:
    if matrix is None:
        return 0.0
    rotation = np.asarray(matrix, dtype=np.float64)
    if rotation.shape[0] < 3 or rotation.shape[1] < 3:
        return 0.0
    return float(np.degrees(np.arctan2(rotation[0, 2], rotation[2, 2])))


def _pack_anchor(
    left_outer,
    right_outer,
    left_inner,
    right_inner,
    left_iris,
    right_iris,
    nose_bridge,
    nose_tip,
    yaw: float,
    method: str,
) -> dict | None:
    left_outer, right_outer = _pair_by_x(left_outer, right_outer)
    left_inner, right_inner = _pair_by_x(left_inner, right_inner)
    if left_iris is not None and right_iris is not None:
        left_iris, right_iris = _pair_by_x(left_iris, right_iris)
        aim_left, aim_right = left_iris, right_iris
    else:
        aim_left, aim_right = left_outer, right_outer
    delta = np.asarray(aim_right, dtype=np.float64) - np.asarray(aim_left, dtype=np.float64)
    eye_span = float(np.linalg.norm(np.asarray(right_outer) - np.asarray(left_outer)))
    if eye_span < 8:
        return None
    eye_y = (aim_left[1] + aim_right[1]) / 2.0
    if nose_tip[1] < eye_y - 0.45 * eye_span:
        return None
    roll = float(np.degrees(np.arctan2(delta[1], delta[0])))
    return {
        "left_outer": left_outer,
        "right_outer": right_outer,
        "left_inner": left_inner,
        "right_inner": right_inner,
        "left_iris": left_iris,
        "right_iris": right_iris,
        "nose_bridge": nose_bridge,
        "nose_tip": nose_tip,
        "roll": roll,
        "yaw": float(yaw),
        "eye_span": eye_span,
        "method": method,
    }


def _landmarks_mediapipe(rgb: np.ndarray) -> dict | None:
    loaded = _get_landmarker()
    if loaded is None:
        return None
    landmarker, mp = loaded
    try:
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb))
        result = landmarker.detect(image)
        if not result.face_landmarks:
            return None
        points = result.face_landmarks[0]
        height, width = rgb.shape[:2]
        if len(points) <= NOSE_BRIDGE:
            return None
        left_iris = _xy(points[LEFT_IRIS], width, height) if len(points) > LEFT_IRIS else None
        right_iris = _xy(points[RIGHT_IRIS], width, height) if len(points) > RIGHT_IRIS else None
        matrices = getattr(result, "facial_transformation_matrixes", None) or []
        yaw = _yaw_degrees(matrices[0]) if matrices else 0.0
        anchor = _pack_anchor(
            _xy(points[LEFT_EYE_OUTER], width, height),
            _xy(points[RIGHT_EYE_OUTER], width, height),
            _xy(points[LEFT_EYE_INNER], width, height),
            _xy(points[RIGHT_EYE_INNER], width, height),
            left_iris,
            right_iris,
            _xy(points[NOSE_BRIDGE], width, height),
            _xy(points[NOSE_TIP], width, height),
            yaw,
            "facemesh",
        )
        if anchor is None:
            return None
        try:
            anchor["shape"] = _shape_from_mesh(points, width, height, yaw)
        except Exception:
            anchor["shape"] = None
        return anchor
    except Exception:
        return None


def _landmarks_haar(bgr: np.ndarray) -> dict | None:
    face_xml = _cached_file("haarcascade_frontalface_default.xml", None, FACE_XML_URL)
    eye_xml = _cached_file("haarcascade_eye.xml", None, EYE_XML_URL)
    if face_xml is None:
        return None
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(str(face_xml))
    if face_cascade.empty():
        return None
    faces = face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(40, 40))
    if len(faces) == 0:
        return None
    x, y, w, h = sorted(faces, key=lambda item: item[2] * item[3], reverse=True)[0]
    roi = gray[y : y + int(h * 0.65), x : x + w]
    eyes = []
    if eye_xml is not None:
        eye_cascade = cv2.CascadeClassifier(str(eye_xml))
        if not eye_cascade.empty():
            eyes = eye_cascade.detectMultiScale(roi, 1.1, 4, minSize=(12, 12))
    if len(eyes) < 2:
        left_outer = [x + w * 0.22, y + h * 0.38]
        right_outer = [x + w * 0.78, y + h * 0.38]
        left_inner = [x + w * 0.42, y + h * 0.38]
        right_inner = [x + w * 0.58, y + h * 0.38]
        left_iris = [x + w * 0.32, y + h * 0.38]
        right_iris = [x + w * 0.68, y + h * 0.38]
    else:
        found = sorted(eyes, key=lambda item: item[0])[:2]
        centers = []
        for ex, ey, ew, eh in found:
            centers.append([x + ex + ew / 2.0, y + ey + eh / 2.0])
        if centers[0][0] > centers[1][0]:
            centers = centers[::-1]
        left_c, right_c = centers
        span = float(np.linalg.norm(np.asarray(right_c) - np.asarray(left_c)))
        direction = (np.asarray(right_c) - np.asarray(left_c)) / max(span, 1.0)
        left_iris = left_c
        right_iris = right_c
        left_outer = (np.asarray(left_c) - direction * span * 0.42).tolist()
        right_outer = (np.asarray(right_c) + direction * span * 0.42).tolist()
        left_inner = (np.asarray(left_c) + direction * span * 0.22).tolist()
        right_inner = (np.asarray(right_c) - direction * span * 0.22).tolist()
    nose_bridge = [
        (left_inner[0] + right_inner[0]) / 2.0,
        (left_inner[1] + right_inner[1]) / 2.0 + h * 0.04,
    ]
    nose_tip = [nose_bridge[0], nose_bridge[1] + h * 0.12]
    return _pack_anchor(
        left_outer,
        right_outer,
        left_inner,
        right_inner,
        left_iris,
        right_iris,
        nose_bridge,
        nose_tip,
        0.0,
        "haar",
    )


def detect_face_anchor(image: Image.Image) -> dict | None:
    """يحدد العينين والأنف. يعيد قاموساً قابلاً للتخزين أو None."""
    rgb = np.array(image.convert("RGB"))
    with _LOCK:
        anchor = _landmarks_mediapipe(rgb)
    if anchor is not None:
        return anchor
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    return _landmarks_haar(bgr)


def detect_eye_anchor(image: Image.Image) -> dict | None:
    return detect_face_anchor(image)


def _point(value) -> np.ndarray | None:
    if value is None:
        return None
    return np.asarray(value, dtype=np.float64)


def _placement(anchor: dict) -> np.ndarray:
    left_iris = _point(anchor.get("left_iris"))
    right_iris = _point(anchor.get("right_iris"))
    if left_iris is not None and right_iris is not None:
        eyes = (left_iris + right_iris) / 2.0
    else:
        eyes = (_point(anchor["left_outer"]) + _point(anchor["right_outer"])) / 2.0
    nose = _point(anchor["nose_bridge"])
    # جسر الإطار يتبع الأنف أفقياً، ومركز العدسة يبقى على القزحية.
    return np.array([0.55 * eyes[0] + 0.45 * nose[0], eyes[1]], dtype=np.float64)


def _frame_metrics(glasses: Image.Image) -> tuple[float, float]:
    alpha = np.array(glasses.getchannel("A"))
    height, width = alpha.shape
    columns = (alpha > 30).sum(axis=0)
    threshold = max(8, int(height * 0.12))
    xs = np.where(columns > threshold)[0]
    if len(xs) < 2:
        return 0.73, 0.48
    lens_ratio = float(np.clip((xs[-1] - xs[0]) / float(width), 0.45, 0.95))
    region = alpha[:, int(xs[0]) : int(xs[-1]) + 1]
    ys = np.where(region > 30)[0]
    center_y = float(ys.mean()) / float(height) if len(ys) else 0.48
    return lens_ratio, center_y


def _apply_yaw(glasses: Image.Image, yaw_deg: float) -> Image.Image:
    yaw = float(np.clip(yaw_deg, -35, 35))
    if abs(yaw) < 4:
        return glasses
    canvas = np.array(glasses)
    height, width = canvas.shape[:2]
    src = np.float32([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]])
    shrink = abs(yaw) / 35.0 * 0.18 * height
    if yaw >= 0:
        dst = np.float32(
            [[0, 0], [width - 1, shrink], [width - 1, height - 1 - shrink], [0, height - 1]]
        )
    else:
        dst = np.float32(
            [[0, shrink], [width - 1, 0], [width - 1, height - 1], [0, height - 1 - shrink]]
        )
    matrix = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(
        canvas,
        matrix,
        (width, height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0, 0),
    )
    return Image.fromarray(warped)


def _rotate_about(image: Image.Image, angle_deg: float, pivot: tuple[float, float]) -> Image.Image:
    canvas = np.array(image)
    height, width = canvas.shape[:2]
    matrix = cv2.getRotationMatrix2D((float(pivot[0]), float(pivot[1])), float(angle_deg), 1.0)
    cos = abs(matrix[0, 0])
    sin = abs(matrix[0, 1])
    new_w = max(1, int(round(height * sin + width * cos)))
    new_h = max(1, int(round(height * cos + width * sin)))
    matrix[0, 2] += new_w / 2.0 - pivot[0]
    matrix[1, 2] += new_h / 2.0 - pivot[1]
    warped = cv2.warpAffine(
        canvas,
        matrix,
        (new_w, new_h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(0, 0, 0, 0),
    )
    return Image.fromarray(warped)


def overlay_glasses(
    face_image: Image.Image,
    glasses_path: str | Path,
    scale: float = 1.0,
    offset_x: float = 0.0,
    offset_y: float = 0.0,
    angle_delta: float = 0.0,
    anchor: dict | None = None,
) -> tuple[Image.Image, str, str]:
    """يركب النظارة على الوجه.

    scale: مضاعف المقاس التلقائي (1 = مطابق للوجه).
    offset_x/offset_y: إزاحة كنسبة من المسافة بين العينين.
    angle_delta: درجات تُضاف إلى ميل العينين.
    """
    face = face_image.convert("RGBA")
    glasses = Image.open(glasses_path).convert("RGBA")
    if anchor is None:
        anchor = detect_face_anchor(face)
    if anchor is None:
        return face.convert("RGB"), "لم يتم التعرف على الوجه. جرّب صورة أوضح من الأمام.", ""

    eye_span = float(anchor["eye_span"])
    if eye_span < 8:
        return face.convert("RGB"), "تعذر تحديد العينين بدقة. استخدم صورة أوضح.", anchor.get("method", "")

    lens_ratio, center_y = _frame_metrics(glasses)
    yaw = float(anchor.get("yaw") or 0.0)
    yaw_scale = 1.0 / max(0.75, abs(float(np.cos(np.radians(yaw)))))
    yaw_scale = float(min(yaw_scale, 1.3))
    target_w = eye_span * LENS_TO_EYE * float(scale) * yaw_scale / lens_ratio
    target_w = int(max(32, min(target_w, face.width * 1.45)))
    target_h = max(12, int(round(glasses.height * (target_w / glasses.width))))

    glasses = _apply_yaw(glasses, yaw)
    glasses = glasses.resize((target_w, target_h), Image.Resampling.LANCZOS)
    roll = float(anchor["roll"]) + float(angle_delta)
    glasses = _rotate_about(glasses, -roll, (glasses.width / 2.0, center_y * glasses.height))

    spot = _placement(anchor)
    spot = spot + np.array([float(offset_x), float(offset_y)], dtype=np.float64) * eye_span
    paste_x = int(round(spot[0] - glasses.width / 2.0))
    paste_y = int(round(spot[1] - glasses.height / 2.0))

    layer = Image.new("RGBA", face.size, (0, 0, 0, 0))
    layer.paste(glasses, (paste_x, paste_y), glasses)
    composed = Image.alpha_composite(face, layer).convert("RGB")
    if anchor.get("method") == "facemesh":
        message = "تم ضبط المقاس والزاوية تلقائياً حسب العينين والأنف."
    else:
        message = "تم تركيب النظارة بتقدير تقريبي لأن Face Mesh لم يتعرف على هذه الصورة."
    return composed, message, str(anchor.get("method") or "")
