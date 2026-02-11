#!/bin/bash
# Test FastAPI Docker SDK Endpoints

set -e

API_URL="http://localhost:8000"

echo "🧪 Testando FastAPI Docker SDK"
echo "=============================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo -e "${BLUE}1. Health Check${NC}"
curl -s http://localhost:8000/api/v1/health | python -m json.tool
echo ""

# Test 2: List Containers
echo -e "${BLUE}2. Listar Containers${NC}"
curl -s "$API_URL/api/containers" | python -m json.tool | head -20
echo ""

# Test 3: List Images
echo -e "${BLUE}3. Listar Imagens${NC}"
curl -s "$API_URL/api/images" | python -m json.tool | head -20
echo ""

# Test 4: Run Container (Alpine)
echo -e "${BLUE}4. Executar Container (Alpine)${NC}"
RESPONSE=$(curl -s -X POST "$API_URL/api/containers" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "alpine:latest",
    "name": "test-fastapi-' $(date +%s) '",
    "detach": true
  }')

echo "$RESPONSE" | python -m json.tool

CONTAINER_ID=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['data']['container_id'])" 2>/dev/null || echo "")

if [ ! -z "$CONTAINER_ID" ]; then
  echo ""
  CONTAINER_NAME=$(echo "$RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['data'].get('name', 'unknown'))" 2>/dev/null || echo "test-container")
  
  # Test 5: Get Container Info
  echo -e "${BLUE}5. Info do Container${NC}"
  curl -s "$API_URL/api/containers/$CONTAINER_ID" | python -m json.tool | head -20
  echo ""
  
  # Test 6: Get Logs
  echo -e "${BLUE}6. Logs do Container${NC}"
  curl -s "$API_URL/api/containers/$CONTAINER_ID/logs?lines=10" | python -m json.tool
  echo ""
  
  # Test 7: Stop Container
  echo -e "${BLUE}7. Parar Container${NC}"
  curl -s -X POST "$API_URL/api/containers/$CONTAINER_ID/stop" | python -m json.tool
  echo ""
  
  # Test 8: Remove Container
  echo -e "${BLUE}8. Remover Container${NC}"
  curl -s -X DELETE "$API_URL/api/containers/$CONTAINER_ID?force=true" | python -m json.tool
  echo ""
fi

echo -e "${GREEN}✅ Testes Completos!${NC}"
echo ""
echo "📚 Documentação Swagger disponível em:"
echo "   http://localhost:8000/docs"
