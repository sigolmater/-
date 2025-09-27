# Copilot Instructions for Gemini API Client

## Project Overview
This repository contains a Python client for the Gemini cryptocurrency exchange API. The main component is `GeminiClient` which provides a simple, secure interface for interacting with Gemini's REST API endpoints.

## Key Technologies
- **Python 3.x**: Primary programming language
- **requests**: HTTP client library for API calls
- **hmac/hashlib**: Cryptographic signing for API authentication
- **base64/json**: Data encoding and serialization

## Project Structure
```
/
├── gemini_client.py    # Main API client implementation
├── README.md          # Project documentation
└── .gitignore         # Git ignore patterns
```

## Code Style & Conventions

### Python Standards
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Include comprehensive docstrings for all public methods
- Korean comments are acceptable (existing pattern in codebase)

### Security Best Practices
- **Never commit API keys or secrets** - use environment variables or config files
- Always validate input parameters before making API calls
- Implement proper error handling for authentication failures
- Use secure methods for generating signatures (HMAC-SHA384)

### API Client Patterns
- Use session objects for connection pooling and performance
- Implement retry logic with exponential backoff
- Handle rate limiting (HTTP 429) gracefully
- Provide fallback mechanisms for network failures
- Include appropriate timeouts for all HTTP requests

## Development Guidelines

### When Adding New Endpoints
1. Follow the existing pattern in `_make_request()` method
2. Add proper parameter validation
3. Include comprehensive error handling
4. Add descriptive docstrings with parameter descriptions
5. Maintain consistent naming conventions

### Error Handling Standards
- Use specific exception types for different error conditions
- Include meaningful error messages with context
- Implement graceful degradation where possible
- Log errors appropriately (when logging is available)

### Authentication & Security
- All private API endpoints require proper signature generation
- Use the existing `_generate_signature()` method pattern
- Include required headers: `X-GEMINI-APIKEY`, `X-GEMINI-PAYLOAD`, `X-GEMINI-SIGNATURE`
- Ensure nonce values are monotonically increasing

## API Endpoint Categories

### Public Endpoints (No Authentication)
- `/v1/symbols` - Available trading pairs
- `/v1/pubticker/{symbol}` - Public ticker data
- Market data endpoints

### Private Endpoints (Authentication Required)
- `/v1/balances` - Account balances
- `/v1/order/new` - Create new orders
- Account management endpoints

## Testing Considerations
- Mock external API calls in tests
- Test both success and failure scenarios
- Validate signature generation with known test vectors
- Test rate limiting and retry mechanisms
- Include integration tests with sandbox environment

## Common Pitfalls to Avoid
1. **Hardcoded API endpoints** - use base_url property
2. **Missing nonce in POST requests** - required for authentication
3. **Incorrect payload encoding** - must be base64 encoded JSON
4. **Insufficient error handling** - always handle network and API errors
5. **Missing type hints** - maintain consistency with existing code

## Environment Variables
When suggesting environment variable usage:
- `GEMINI_API_KEY` - API key for authentication
- `GEMINI_API_SECRET` - API secret for signature generation
- `GEMINI_SANDBOX` - Boolean flag for sandbox/production environment

## Example Usage Patterns
```python
# Initialize client
client = GeminiClient(api_key="your_key", api_secret="your_secret", sandbox=True)

# Public data (no auth required)
symbols = client.get_symbols()
ticker = client.get_ticker("btcusd")

# Private data (auth required)
balances = client.get_balances()
order = client.new_order("btcusd", "0.01", "50000", "buy")
```

## Performance Considerations
- Reuse session objects for multiple requests
- Implement connection pooling where appropriate
- Cache public data when possible (with appropriate TTL)
- Use batch operations when available in the API
- Monitor and respect rate limits

## Documentation Standards
- Keep README.md updated with new features
- Document all public methods with usage examples
- Include error handling examples in documentation
- Provide configuration examples for different environments