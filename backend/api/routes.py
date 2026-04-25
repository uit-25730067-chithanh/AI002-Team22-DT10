from fastapi import APIRouter, HTTPException

# Import schema và service; fallback để chạy được cả từ root và từ thư mục backend
try:
    from backend.schemas.prediction import PredictionRequest, PredictionResponse
    from backend.services.predictor import PredictorService
except ModuleNotFoundError:
    from schemas.prediction import PredictionRequest, PredictionResponse
    from services.predictor import PredictorService

router = APIRouter()

# Khởi tạo predictor và load model ngay khi module import (module-level singleton)
predictor = PredictorService()
predictor.load_model()


@router.get("/health")
def health() -> dict:
    """Kiểm tra trạng thái API và xem model đã load thành công chưa."""
    return {"status": "ok", "model_loaded": predictor.is_loaded()}


@router.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest) -> PredictionResponse:
    """
    Dự báo giá cà phê dựa trên đầu vào thời tiết + giá lịch sử.
    Tự động validate bởi Pydantic (Trụ cột Robustness).
    """
    try:
        result = predictor.predict(payload)
        return PredictionResponse(**result)
    except RuntimeError as exc:
        # Model chưa sẵn sàng (ví dụ file .pkl chưa có)
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        # Lỗi không mong muốn khác
        raise HTTPException(status_code=500, detail=f"Lỗi không mong muốn: {exc}") from exc


@router.get("/model/info")
def model_info() -> dict:
    """Trả về thông tin model: version, danh sách features, thời gian train."""
    return predictor.get_model_info()
