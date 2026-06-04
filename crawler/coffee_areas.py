"""Shared area metadata for coffee price, weather, and soil crawlers."""

from __future__ import annotations

import re
import unicodedata


COFFEE_TYPE = "Robusta / ca phe nhan xo noi dia"


AREAS = [
    {
        "area": "Di Linh",
        "province": "Lam Dong",
        "latitude": 11.5814,
        "longitude": 108.0727,
        "dominant_soil_type": "Dat do vang tren bazan",
        "soil_note": "Vung trong ca phe quan trong cua Lam Dong; gan nhom dat bazan/dat do vang phu hop ca phe.",
        "soil_score": 4,
        "soil_data_confidence": "medium",
        "source_url": "https://open-meteo.com/en/docs/historical-weather-api",
    },
    {
        "area": "Lam Ha",
        "province": "Lam Dong",
        "latitude": 11.7996,
        "longitude": 108.2260,
        "dominant_soil_type": "Dat do vang tren bazan",
        "soil_note": "Vung san xuat ca phe Lam Dong; dung loai dat tong quat cap khu vuc khi thieu thong ke chi tiet.",
        "soil_score": 4,
        "soil_data_confidence": "low",
        "source_url": "https://open-meteo.com/en/docs/historical-weather-api",
    },
    {
        "area": "Bao Loc",
        "province": "Lam Dong",
        "latitude": 11.5480,
        "longitude": 107.8077,
        "dominant_soil_type": "Dat do vang tren bazan",
        "soil_note": "Vung cao nguyen Lam Dong phu hop cay cong nghiep lau nam, trong do co ca phe.",
        "soil_score": 4,
        "soil_data_confidence": "low",
        "source_url": "https://open-meteo.com/en/docs/historical-weather-api",
    },
    {
        "area": "Cu M'gar",
        "province": "Dak Lak",
        "latitude": 12.8089,
        "longitude": 108.0459,
        "dominant_soil_type": "Dat do bazan",
        "soil_note": "Nguon nghien cuu cap huyen ve hieu qua su dung dat trong ca phe tai Cu M'gar; dat bazan rat phu hop ca phe.",
        "soil_score": 5,
        "soil_data_confidence": "high",
        "source_url": "https://vie.vjas.vn/index.php/vjasvn/article/view/2256",
    },
    {
        "area": "Ea H'leo",
        "province": "Dak Lak",
        "latitude": 13.2237,
        "longitude": 108.2109,
        "dominant_soil_type": "Dat do bazan",
        "soil_note": "Dak Lak co dien tich dat do bazan lon va Ea H'leo la vung ca phe trong diem; dung thong tin cap tinh/huyen.",
        "soil_score": 5,
        "soil_data_confidence": "medium",
        "source_url": "https://www.vista.gov.vn/vi/news/cac-linh-vuc-khoa-hoc-va-cong-nghe/nghien-cuu-xac-dinh-dong-ca-phe-voi-chat-luong-cao-phu-hop-voi-mot-so-vung-trong-chinh-o-tinh-dak-lak-11640.html",
    },
    {
        "area": "Buon Ho",
        "province": "Dak Lak",
        "latitude": 12.9172,
        "longitude": 108.2662,
        "dominant_soil_type": "Dat do bazan",
        "soil_note": "Khu vuc Dak Lak trong vung dat bazan, phu hop ca phe Robusta.",
        "soil_score": 5,
        "soil_data_confidence": "medium",
        "source_url": "https://www.vista.gov.vn/vi/news/cac-linh-vuc-khoa-hoc-va-cong-nghe/nghien-cuu-xac-dinh-dong-ca-phe-voi-chat-luong-cao-phu-hop-voi-mot-so-vung-trong-chinh-o-tinh-dak-lak-11640.html",
    },
    {
        "area": "Gia Nghia",
        "province": "Dak Nong",
        "latitude": 12.0042,
        "longitude": 107.6907,
        "dominant_soil_type": "Dat do bazan",
        "soil_note": "Dak Nong thuoc Tay Nguyen, nhom dat bazan/dat do vang pho bien cho cay ca phe.",
        "soil_score": 4,
        "soil_data_confidence": "low",
        "source_url": "https://open-meteo.com/en/docs/historical-weather-api",
    },
    {
        "area": "Dak R'lap",
        "province": "Dak Nong",
        "latitude": 11.8795,
        "longitude": 107.5228,
        "dominant_soil_type": "Dat do bazan",
        "soil_note": "Khu vuc Dak Nong co dat bazan phu hop ca phe; dung loai dat tong quat khi thieu thong ke cap huyen.",
        "soil_score": 4,
        "soil_data_confidence": "low",
        "source_url": "https://open-meteo.com/en/docs/historical-weather-api",
    },
    {
        "area": "Chu Prong",
        "province": "Gia Lai",
        "latitude": 13.7529,
        "longitude": 107.8845,
        "dominant_soil_type": "Dat do bazan",
        "soil_note": "Vung Tay Nguyen co dat bazan phu hop ca phe; thong tin chi tiet cap huyen can bo sung neu co nguon moi.",
        "soil_score": 4,
        "soil_data_confidence": "low",
        "source_url": "https://open-meteo.com/en/docs/historical-weather-api",
    },
    {
        "area": "Pleiku",
        "province": "Gia Lai",
        "latitude": 13.9718,
        "longitude": 108.0151,
        "dominant_soil_type": "Dat do bazan",
        "soil_note": "Cao nguyen Pleiku co dieu kien dat bazan phu hop cay cong nghiep lau nam.",
        "soil_score": 4,
        "soil_data_confidence": "low",
        "source_url": "https://open-meteo.com/en/docs/historical-weather-api",
    },
    {
        "area": "Ia Grai",
        "province": "Gia Lai",
        "latitude": 13.9889,
        "longitude": 107.7370,
        "dominant_soil_type": "Dat do bazan",
        "soil_note": "Khu vuc Gia Lai, dung loai dat bazan tong quat cho vung ca phe.",
        "soil_score": 4,
        "soil_data_confidence": "low",
        "source_url": "https://open-meteo.com/en/docs/historical-weather-api",
    },
    {
        "area": "Kon Tum",
        "province": "Kon Tum",
        "latitude": 14.3497,
        "longitude": 108.0005,
        "dominant_soil_type": "Dat do vang / dat bazan cuc bo",
        "soil_note": "Khu vuc co ca phe nhung thieu thong ke thich nghi cap dia phuong trong crawler mac dinh.",
        "soil_score": 3,
        "soil_data_confidence": "low",
        "source_url": "https://open-meteo.com/en/docs/historical-weather-api",
    },
]


def strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value)
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")


def normalize_name(value: str) -> str:
    value = strip_accents(value).lower()
    value = value.replace("đ", "d")
    value = value.replace("’", "'").replace("`", "'").replace("´", "'")
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def slugify(value: str) -> str:
    value = normalize_name(value)
    return re.sub(r"[^a-z0-9]+", "_", value).strip("_")


AREA_BY_NORMALIZED = {normalize_name(item["area"]): item for item in AREAS}
