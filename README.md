# SageWire Voice Service v1.0

Permanent standalone TTS infrastructure service owned by SageWire Syndicate.

This service is not HerdMate, Hazel, DAVE, or headset-specific.

## Rule

A product may depend on a service.  
A service must never depend on a product.

## Public API

### Health

GET /health

### Speak

POST /speak

Input:

```json
{
  "text": "Hello world"
}
