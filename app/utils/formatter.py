from typing import Optional, Union, Dict, List


def formatter(status: bool, message: str, data: Optional[Union[Dict, List]]) -> Dict:
    return {"status": status, "message": message, "data": data}
