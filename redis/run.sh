docker run -d \
  --name redis \
  -p 6379:6379 \
  -v ./data:/data \
  --network mynetwork \
  redis:6.0.8