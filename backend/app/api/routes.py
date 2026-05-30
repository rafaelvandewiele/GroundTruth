from fastapi import APIRouter, HTTPException, status
from app.models.schemas import CheckRequest, CheckResponse
from app.services.fact_check_service import run_fact_check

router = APIRouter()


@router.post(
    "/check",
    response_model=CheckResponse,
    summary="Fact-check a claim or piece of text",
)
async def check(request: CheckRequest):
    """
    Submit text (or a base64 screenshot) for fact-checking.
    Returns verdicts for each extracted claim with sources.
    """
    if not request.text and not request.image_base64:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Provide either 'text' or 'image_base64'.",
        )

    try:
        result = await run_fact_check(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}",
        )


@router.get("/check/{check_id}", summary="Get a previous fact-check by ID")
async def get_check(check_id: str):
    """Retrieve a stored fact-check result by its ID."""
    # TODO: implement lookup by UUID from Supabase
    raise HTTPException(status_code=404, detail="Not implemented yet")
