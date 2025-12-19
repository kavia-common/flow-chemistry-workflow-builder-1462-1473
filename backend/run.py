import os
from app import app

if __name__ == "__main__":
    # Bind host/port; platform proxy may map to 3001 but we set default here
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "3001"))
    app.run(host=host, port=port)
