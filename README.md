# PyMeet-Google-Meet-Clone
PyMeet – Google Meet Clone


pymeet/
├── app/
│   ├── main.py                # FastAPI app entry point
│   ├── routers/
│   │   ├── auth.py            # Login, Register APIs
│   │   ├── meeting.py         # Create/Join meeting
│   │   └── websocket.py       # Real-time chat + signaling
│   ├── models/
│   │   └── models.py          # SQLAlchemy models
│   ├── db/
│   │   └── database.py        # SQLite setup
│   ├── utils/
│   │   ├── auth.py            # JWT handling
│   │   └── rtc.py             # WebRTC signaling helpers
│   └── templates/
│       ├── index.html         # Login/Register UI
│       ├── dashboard.html     # Dashboard to create/join rooms
│       └── meeting.html       # WebRTC video chat page
├── static/
│   ├── css/
│   └── js/
├── .env                       # Secrets like JWT_SECRET
├── requirements.txt
└── README.md
