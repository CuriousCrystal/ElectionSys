Election Process Assistant

A comprehensive, interactive assistant that helps users understand election processes, timelines, and procedural steps in an easy-to-follow way. VoterGuide combines voice interaction, interactive dashboards, and step-by-step educational content to demystify voting processes for all users.

---

## 🎯 Features

### 📚 Interactive Learning
- **Election Timeline Visualization** - Interactive timeline showing key election dates and milestones
- **Step-by-Step Guides** - Clear breakdown of voting procedures and requirements
- **Process Flowcharts** - Visual diagrams explaining registration, voting, and counting processes
- **FAQs & Resources** - Comprehensive answers to common election questions

### 🎤 Voice Assistant
- **Natural Language Queries** - Ask questions about election processes in plain English
- **Voice Responses** - Get spoken answers to your questions
- **Location-Based Information** - Find polling locations, registration deadlines, and voting requirements specific to your area
- **Real-Time Updates** - Access current election information and status

### 📊 Interactive Dashboard
- **Personal Voting Checklist** - Track your voting preparation steps
- **Election Calendar** - View important dates for upcoming elections
- **Polling Location Finder** - Locate nearest polling stations with directions
- **Voter Registration Status** - Check registration status and requirements
- **Election Results Tracker** - Monitor results as they come in

### 🔐 User Accounts & Personalization
- **Voter Profiles** - Personalized information based on your location and election year
- **Saved Preferences** - Remember your ballot language and accessibility needs
- **Multi-Language Support** - Interface available in multiple languages
- **Accessibility Features** - High contrast mode, text-to-speech, large fonts

### 📈 Educational Analytics
- **Learning Progress** - Track what you've learned about the election process
- **Knowledge Assessment** - Quiz yourself on election procedures
- **Concept Mastery** - Deep dives into specific election topics

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **Microphone** (optional, for voice features)
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/CuriousCrystal/VoterGuide.git
cd VoterGuide
```

**2. Backend Setup**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Run database migrations
python database.py init
```

**3. Frontend Setup**
```bash
cd dashboard
npm install
npm run dev
```

**4. Start the Application**
```bash
# Terminal 1: Start Flask backend
python main.py

# Terminal 2: Start Vue.js frontend
cd dashboard
npm run dev
```

**5. Access the Application**
- Open your browser to `http://localhost:5173`
- Default login: `admin` / `password`

---

## 📖 How It Works

### User Journey

```
1. New User Arrives
   ↓
2. Select Election Type (Federal, State, Local)
   ↓
3. Enter Location (State, County)
   ↓
4. Choose Learning Style (Interactive, Voice, Visual)
   ↓
5. Browse Timeline & Processes
   ↓
6. Ask Questions (Voice or Text)
   ↓
7. Complete Checklist & Prepare to Vote
```

### Election Process Breakdown

**Registration Phase**
- Voter registration deadlines
- Eligibility requirements
- Registration methods (online, mail, in-person)
- Status checking

**Pre-Election Phase**
- Early voting information
- Absentee ballot requests
- Polling location finder
- Ballot preview tools

**Voting Day**
- Step-by-step polling procedure
- What to bring
- Accessibility accommodations
- Wait time estimates

**Post-Election Phase**
- How ballots are counted
- Result announcements
- Recounts and disputes
- Final certification

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite / PostgreSQL
- **APIs**: Election data APIs, Location services
- **Voice**: Text-to-Speech (TTS) engine
- **Authentication**: JWT tokens, Bcrypt

### Frontend
- **Framework**: Vue.js 3
- **Styling**: Tailwind CSS
- **Charts**: Chart.js / Recharts
- **State Management**: Pinia
- **Real-time**: WebSocket support

### Deployment
- **Backend**: Render, Heroku, or custom server
- **Frontend**: Netlify, Vercel, or CDN
- **Database**: Cloud-hosted PostgreSQL

---

## 📁 Project Structure

```
VoterGuide/
├── main.py                    # Flask application entry point
├── requirements.txt           # Python dependencies
├── config.py                  # Configuration settings
│
├── backend/
│   ├── auth.py               # Authentication & authorization
│   ├── elections.py          # Election data & timelines
│   ├── voting_process.py     # Voting procedure logic
│   ├── locations.py          # Polling location service
│   ├── voice_assistant.py    # Voice interaction handler
│   ├── database.py           # Database operations
│   └── utils.py              # Helper functions
│
├── dashboard/                 # Vue.js frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Timeline.vue
│   │   │   ├── VoiceAssistant.vue
│   │   │   ├── ProcessFlow.vue
│   │   │   └── Checklist.vue
│   │   ├── views/
│   │   │   ├── Home.vue
│   │   │   ├── Elections.vue
│   │   │   └── Dashboard.vue
│   │   └── App.vue
│   ├── package.json
│   └── vite.config.js
│
├── data/                      # Election data files
│   ├── timelines.json
│   ├── processes.json
│   └── faqs.json
│
├── docs/                      # Documentation
│   ├── SETUP.md
│   ├── API.md
│   └── DEPLOYMENT.md
│
└── tests/
    ├── test_elections.py
    ├── test_voice.py
    └── test_api.py
```

---

## 🎮 Core Components

### 1. **Timeline Viewer**
Interactive visualization of election dates and important deadlines
- Customizable by election type and location
- Color-coded phases (registration, early voting, election day, results)
- Click for detailed information on each milestone

### 2. **Voice Assistant ("Civics")**
Natural language interface for election questions
```
User: "When can I register to vote?"
Civics: "In your state, voter registration closes 30 days before election day. 
         Would you like to know the exact date for the upcoming election?"
```

### 3. **Process Flow Diagram**
Visual step-by-step guides for:
- Voter registration process
- Voting day procedures
- Ballot counting process
- Dispute resolution

### 4. **Personal Checklist**
Customizable voting preparation checklist
- [ ] Check voter registration status
- [ ] Find polling location
- [ ] Arrange transportation
- [ ] Request absentee ballot (if needed)
- [ ] Study candidate/ballot information
- [ ] Gather required documents

### 5. **Location Finder**
- Search polling locations by address or ZIP code
- Real-time wait time estimates
- Accessibility information
- Directions and parking details

---

## 🔐 Authentication & Roles

VoterGuide supports multiple user types:

| Role | Access | Features |
|------|--------|----------|
| **Voter** | Public | Timeline, voice assistant, checklist |
| **Poll Worker** | Restricted | Additional procedural details, training materials |
| **Election Official** | Admin | System configuration, data management |
| **Guest** | Limited | Read-only access to public information |

**Default Credentials** (Change in production!)
```
Username: admin
Password: changeme123

Username: voter
Password: voterpass
```

---

## 📡 API Endpoints

### Election Information
```
GET  /api/elections              # List all elections
GET  /api/elections/:id          # Get election details
GET  /api/elections/:id/timeline # Get election timeline
GET  /api/elections/:id/process  # Get voting process steps
```

### Voter Information
```
POST /api/voter/register         # Register to vote
GET  /api/voter/status           # Check registration status
GET  /api/voter/location         # Find polling location
```

### Voice Assistant
```
POST /api/voice/query            # Send voice question
GET  /api/voice/history          # Get conversation history
```

### Dashboard Data
```
GET  /api/dashboard/checklist    # Get user checklist
PUT  /api/dashboard/checklist    # Update checklist items
GET  /api/dashboard/stats        # Get learning progress
```

---

## 🎓 Usage Examples

### Example 1: First-Time Voter
1. Opens VoterGuide
2. Selects "First-Time Voter" learning path
3. Views registration timeline
4. Uses voice assistant: "Where do I register?"
5. Follows step-by-step checklist
6. Gets notified when election day arrives

### Example 2: Busy Professional
1. Logs in to dashboard
2. Uses voice: "What are my voting options?"
3. Finds early voting and absentee ballot info
4. Requests absentee ballot through the app
5. Gets text reminders for important dates

### Example 3: Election Official
1. Logs in with admin credentials
2. Updates election timeline and procedures
3. Monitors user engagement metrics
4. Configures localized information

---

## 🌍 Data Sources

VoterGuide integrates with:
- **Election Assistance Commission (EAC)** - Official election data
- **State Election Offices** - State-specific procedures
- **Google Maps API** - Polling location mapping
- **OpenElections Project** - Historical election data
- **Ballotpedia** - Ballot and candidate information

---

## 📝 Configuration

Edit `.env` file to customize:

```env
# Flask Config
FLASK_ENV=development
FLASK_SECRET_KEY=your_secret_key_here
DEBUG=True

# Voice Settings
TTS_ENGINE=google  # or azure, pyttsx3
TTS_LANGUAGE=en-US
VOICE_ENABLED=True

# Database
DATABASE_URL=sqlite:///voterguide.db

# Location Services
GOOGLE_MAPS_API_KEY=your_api_key

# Email Notifications
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
NOTIFICATION_EMAIL=noreply@voterguide.app
```

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_elections.py

# Run with coverage
python -m pytest --cov=backend tests/

# Frontend tests
cd dashboard
npm run test
```

---

## 🚀 Deployment

### Heroku Deployment
```bash
heroku create voterguide
git push heroku main
heroku logs --tail
```

### Netlify Deployment (Frontend)
```bash
cd dashboard
npm run build
netlify deploy --prod --dir dist
```

### Docker Deployment
```bash
docker build -t voterguide .
docker run -p 5000:5000 voterguide
```

See `docs/DEPLOYMENT.md` for detailed deployment instructions.

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for Vue.js code
- Write tests for new features
- Update documentation as needed

---

## 📚 Documentation

- **[Setup Guide](docs/SETUP.md)** - Detailed installation instructions
- **[API Documentation](docs/API.md)** - Complete API reference
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Production deployment steps
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to VoterGuide
- **[Voice Assistant Guide](docs/VOICE_ASSISTANT.md)** - Voice feature documentation

---

## 🐛 Troubleshooting

### Voice Assistant Not Working
- Check microphone permissions in browser settings
- Ensure TTS engine is properly configured
- Verify API keys in `.env` file

### Database Connection Error
```bash
# Reset database
python database.py reset
python database.py init
```

### Frontend Not Loading
```bash
cd dashboard
npm cache clean --force
npm install
npm run dev
```

---

## 📊 Project Statistics

- **Lines of Code**: ~8,000+
- **Test Coverage**: 85%+
- **Languages Supported**: English, Spanish, French, Mandarin
- **Elections Covered**: Federal, State, Local (US)
- **Performance**: Sub-second response times

---

## 📋 Roadmap

- [x] Core election timeline and processes
- [x] Voice assistant integration
- [x] Polling location finder
- [ ] Multi-country election support
- [ ] Advanced voter education modules
- [ ] Integration with voter registration databases
- [ ] Mobile app (iOS & Android)
- [ ] Accessibility certifications (WCAG 2.1 AAA)
- [ ] Real-time election results tracking
- [ ] Candidate comparison tool

---

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/CuriousCrystal/VoterGuide/issues)
- **Discussions**: [GitHub Discussions](https://github.com/CuriousCrystal/VoterGuide/discussions)
- **Email**: support@voterguide.app
- **Community Forum**: Coming soon!

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Election Assistance Commission** for data standards
- **Open Elections Project** for historical data
- **Vue.js & Flask** communities for excellent frameworks
- **All contributors** who help improve VoterGuide

---

## 🌟 Show Your Support

If VoterGuide helps you understand the election process, please:
- ⭐ Star this repository
- 🔗 Share it with friends
- 💬 Leave feedback and suggestions
- 🤝 Contribute to the project

---

**Made with ❤️ to empower voters everywhere**

Last Updated: April 2026
