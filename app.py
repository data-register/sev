from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
import json
import qrcode
import io
import base64
from pathlib import Path
from config import settings

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return """
    <html>
        <body>
            <h1>Welcome to the Playground Monitoring System</h1>
            <a href="/admin">Admin Panel</a>
        </body>
    </html>
    """

@app.get("/admin", response_class=HTMLResponse)
async def admin_login(request: Request):
    return """
    <html>
        <body>
            <h1>Admin Login</h1>
            <form action="/admin" method="post">
                <input type="password" name="password" placeholder="Password">
                <button type="submit">Login</button>
            </form>
        </body>
    </html>
    """

@app.post("/admin", response_class=HTMLResponse)
async def admin_login_post(request: Request, password: str = Form(...)):
    if password == settings.ADMIN_PASSWORD:
        request.session['admin_logged_in'] = True
        return """
        <html>
            <body>
                <h1>Admin Panel</h1>
                <form action="/admin_panel" method="post">
                    <input type="text" name="cameraUrl" placeholder="Camera URL">
                    <button type="submit">Add Camera</button>
                </form>
            </body>
        </html>
        """
    return "Invalid password"

@app.post("/admin_panel", response_class=HTMLResponse)
async def admin_panel(request: Request, cameraUrl: str = Form(...)):
    if not request.session.get('admin_logged_in'):
        return "Not authorized"
    cameras_path = Path("data/cameras.json")
    with cameras_path.open('r') as f:
        cameras = json.load(f)
    cameras.append(cameraUrl)
    with cameras_path.open('w') as f:
        json.dump(cameras, f)
    return f"Camera {cameraUrl} added."

@app.get("/generate_qr", response_class=HTMLResponse)
async def generate_qr():
    data = {'t': 'your_token', 'e': 'expiration_time'}
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    qr_code_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f"<img src='data:image/png;base64,{qr_code_data}'/>"

@app.get("/logout")
async def logout(request: Request):
    request.session.pop('admin_logged_in', None)
    return "Logged out"
