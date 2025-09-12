import requests
import time
import hmac
import hashlib
import base64
import json
from typing import Dict, Optional, List


class GeminiClient:
    """
    Gemini API Client - 사람처럼 생각하고 기계처럼 일하는 API 클라이언트
    단계별로 체계적인 API 인터페이스 제공
    """
    
    def __init__(self, api_key: str, api_secret: str, sandbox: bool = False):
        """
        초기화 - 한걸음씩 신중하게 설정
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.sandbox.gemini.com" if sandbox else "https://api.gemini.com"
        self.session = requests.Session()
        
    def _generate_signature(self, payload: str) -> str:
        """보안 시그니처 생성"""
        message = base64.b64encode(payload.encode()).decode()
        signature = hmac.new(
            self.api_secret.encode(), 
            message.encode(), 
            hashlib.sha384
        ).hexdigest()
        return signature
        
    def _make_request(self, endpoint: str, payload: Dict = None, method: str = "GET") -> Dict:
        """창의적 요청 처리 - 문제 발생시 우회 경로 포함"""
        url = f"{self.base_url}{endpoint}"
        
        if method == "GET":
            try:
                response = self.session.get(url, timeout=30)
                return self._handle_response(response)
            except Exception as e:
                return self._fallback_request(url, method)
                
        elif method == "POST":
            if payload is None:
                payload = {}
                
            payload["request"] = endpoint
            payload["nonce"] = str(int(time.time() * 1000))
            
            encoded_payload = json.dumps(payload)
            b64_payload = base64.b64encode(encoded_payload.encode()).decode()
            signature = self._generate_signature(encoded_payload)
            
            headers = {
                'Content-Type': 'text/plain',
                'Content-Length': '0',
                'X-GEMINI-APIKEY': self.api_key,
                'X-GEMINI-PAYLOAD': b64_payload,
                'X-GEMINI-SIGNATURE': signature,
                'Cache-Control': 'no-cache'
            }
            
            try:
                response = self.session.post(url, headers=headers, timeout=30)
                return self._handle_response(response)
            except Exception as e:
                return self._fallback_request(url, method, headers=headers)
    
    def _handle_response(self, response: requests.Response) -> Dict:
        """꼼꼼한 응답 처리"""
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            time.sleep(1)
            raise Exception("Rate limit exceeded")
        else:
            error_msg = f"API Error {response.status_code}: {response.text}"
            raise Exception(error_msg)
    
    def _fallback_request(self, url: str, method: str, headers: Dict = None) -> Dict:
        """우회적 대안 요청 방법"""
        for attempt in range(3):
            try:
                time.sleep(attempt * 2)
                if method == "GET":
                    response = requests.get(url, timeout=45)
                else:
                    response = requests.post(url, headers=headers, timeout=45)
                return self._handle_response(response)
            except Exception as e:
                if attempt == 2:
                    raise Exception(f"All attempts failed: {str(e)}")
                continue
    
    def get_symbols(self) -> List[str]:
        """사용 가능한 심볼 목록"""
        return self._make_request("/v1/symbols")
    
    def get_ticker(self, symbol: str) -> Dict:
        """티커 정보"""
        return self._make_request(f"/v1/pubticker/{symbol}")
    
    def get_balances(self) -> List[Dict]:
        """계정 잔고"""
        return self._make_request("/v1/balances", method="POST")
    
    def new_order(self, symbol: str, amount: str, price: str, side: str) -> Dict:
        """주문 생성"""
        payload = {
            "symbol": symbol,
            "amount": amount,
            "price": price,
            "side": side,
            "type": "exchange limit"
        }
        return self._make_request("/v1/order/new", payload, "POST")