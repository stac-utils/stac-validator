import json
import os
import tempfile
from typing import Any, Dict

import uvicorn
from fastapi import Body, FastAPI, HTTPException

from stac_validator.fast_validator import FastValidator

app = FastAPI(
    title="STAC-Valid API",
    description="High-performance STAC validation as a service using fastjsonschema.",
    version="4.2.0",
)


@app.post("/validate")
async def validate_stac(data: Dict[str, Any] = Body(...)):
    """
    Validates a STAC Item, Collection, or FeatureCollection provided in the request body.
    Returns a detailed validation summary including performance metrics and error breakdowns.
    """
    # Create a temporary file because FastValidator currently reads from disk
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            json.dump(data, tmp)
            tmp_path = tmp.name

        # Initialize and run the FastValidator in quiet mode
        fv = FastValidator(stac_file=tmp_path, quiet=True, verbose=False)
        fv.run()

        # Check if the result message was populated.
        # With the fix in FastValidator, fv.message[0] should contain the 'valid' key.
        if not fv.message or len(fv.message) == 0:
            raise HTTPException(
                status_code=500, detail="Validator failed to produce a result summary."
            )

        # Extract the validation dictionary
        response = fv.message[0]

        # Cleanup: Hide internal temp paths from API consumers
        response["path"] = "request_body"

        return response

    except Exception as e:
        # Catch unexpected errors and return a 500
        raise HTTPException(status_code=500, detail=f"Validation crashed: {str(e)}")

    finally:
        # Ensure cleanup of the temporary file regardless of success or failure
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.get("/health")
async def health_check():
    """Simple health check endpoint for monitoring."""
    return {"status": "online", "engine": "fastjsonschema"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
