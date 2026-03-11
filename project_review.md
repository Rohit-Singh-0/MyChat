# Project Review & Assessment: MyChat Application

## Is this a good project for a resume?
**Yes, absolutely.** A real-time video and audio streaming application is highly technical and stands out on a resume. It demonstrates competencies in multiple advanced domains:
- **Real-Time Communication (RTC):** Understanding WebRTC concepts, publish/subscribe models, and handling remote data streams via the Agora SDK.
- **Client-Server Architecture:** Bridging a Django python backend (for token generation and state management) with an asynchronous JavaScript frontend.
- **Security Best Practices:** Minting expiring tokens on a secure server rather than trusting the client, preventing unauthorized room access.
- **Asynchronous JavaScript:** Heavy use of `async`/`await` in `streams.js` to handle promises from media devices.

This project shows you can integrate third-party APIs (Agora) into a full-stack framework (Django) to create a synchronous, real-time user experience. 

---

## Software Development Fundamentals Assessment

### Where the Project Excels ✅
1. **Separation of Concerns (MVT):** The project properly follows Django's Model-View-Template architecture. Logic is segmented into `views.py`, UI into `templates`, and database schemas into `models.py`.
2. **Frontend Modularity:** JavaScript logic isn't crammed inline into HTML. It is cleanly separated into `streams.js`, keeping the HTML templates semantic and clean.
3. **Security:** By utilizing `.env` variables and `.gitignore` (which we just fixed), you strictly adhere to the Twelve-Factor App methodology concerning configuration.
4. **Resilience:** Your backend explicitly handles database collisons (e.g., identical usernames jumping into the same room) by uniquely filtering based on `UID`s. Use of `get_or_create` ensures idempotent database operations.
5. **Testing Foundation:** Your `tests.py` has excellent coverage of your views and database logic. You correctly mock/stub your environment variables during the test suite execution.

### Areas for Improvement / Constructive Feedback 🛑
1. **Bloated `requirements.txt`:** 
   - Your `requirements.txt` contains many packages that aren't actually used by your project (e.g., `mysqlclient`, `Pyrebase4`, `beautifulsoup4`, `oauth2client`). 
   - **Fix:** It looks like this was generated from a dirty global Python environment. You should regenerate it inside a clean Virtual Environment using only `django`, `agora-token-builder`, `django-cors-headers` and `python-dotenv`.
2. **"Zombie" Database Records:**
   - Currently, if a user clicks the "Leave" button, `deleteMember` is called and their record is removed from the DB. 
   - However, if the user forcefully closes their browser tab or loses internet connection, the Javascript `unload` event is not guaranteed to fire. This means their `RoomMember` object will stay in your SQLite database forever (Zombie Data). 
   - **Fix:** Implement a server-side cleanup mechanism. For instance, a periodic Celery task, or utilize WebSockets (`Django Channels`) where the server instantly detects a socket disconnect and cleans up the DB automatically.
3. **Lack of Authentication:**
   - Anyone can type any name into the Lobby and join. If John wants to pretend to be Rohit, he can.
   - **Fix:** Link the `RoomMember` model directly to Django's built-in `User` authentication system. Require users to log in before they can see the Lobby.
4. **Hardcoded CSS Assets:**
   - The UI looks good but the CSS (`main.css`) is monolithic and relies highly on fixed viewport heights (`vh`, `vw`). This can scale poorly on mobile screens.
   - **Fix:** Migrate to a utility-first CSS framework like Tailwind CSS or utilize CSS Flexbox/Grid more thoroughly using fractional (`fr`) units instead of strict viewports.

## Next Steps Suggestions
If you want to take this project from "Good" to "**Exceptional**" for your portfolio, I highly recommend looking into **Django Channels** to transition from HTTP Polling/REST to WebSockets. This will allow your backend database to magically stay in total sync with who is *actually* connected to Agora without relying on the browser to tell the truth!
