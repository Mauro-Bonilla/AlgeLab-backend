# AlgeLab

![Static Badge](https://img.shields.io/badge/Python-3.11-blue)
![GitHub](https://img.shields.io/badge/license-MIT-green)
[![Discord](https://img.shields.io/discord/YOUR_SERVER_ID?color=7289da&label=Discord&logo=discord&logoColor=white)](https://discord.gg/4SRmKVZb8V)

AlgeLab is an open-source web platform designed to enhance linear algebra learning through virtual laboratories, multimedia learning principles, and gamification strategies.

## Overview

AlgeLab combines interactive learning modules with practical exercises in a digital environment, implementing Richard Mayer's multimedia learning theory to improve student retention and understanding of algebraic concepts.

### Key Features

- Virtual laboratories for hands-on practice
- Interactive multimedia learning modules
- GitHub-based authentication system
- Progress tracking and gamification elements
- Containerized development environments
- Open-source architecture for STEM education

## Tech Stack

- **Frontend**: React.js
- **Backend**: FastAPI (migrated from Django REST Framework)
- **Database**: PostgreSQL (via Supabase)
- **Authentication**: GitHub OAuth
- **Container**: Docker
- **Deployment**: Azure Web Apps

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/your-username/algelab.git
cd algelab
```

2. Set up environment variables:

-  (see `docs/env_vars.md`)

3. Run with Docker:
```bash
docker compose up
```

4. Or run directly with Python:
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Run the application
python -m src.main
```

## Documentation

Detailed documentation is available in the `docs` directory:

- `database.md` - Database configuration guide
- `deployment.md` - Deployment instructions
- `env_vars.md` - Environment variables setup
- `github_auth.md` - GitHub authentication configuration

## API Endpoints

The FastAPI backend provides the following key endpoints:

- **Authentication**:
  - `POST /api/auth/github` - Get GitHub OAuth login URL
  - `GET /api/auth/github/callback` - GitHub OAuth callback
  - `POST /api/auth/logout` - Logout user
  - `GET /api/auth/token` - Get JWT token info
  - `POST /api/auth/validate-token` - Validate token
  - `POST /api/auth/refresh-token` - Refresh JWT token

- **User Management**:
  - `GET /api/user/` - Get current user info

- **Utility**:
  - `GET /health` - Health check endpoint
  - `GET /` - API information

## Related Repositories

- [Frontend (React)](https://github.com/Mauro-Bonilla/practicum-2-react)
- [Animations](https://github.com/Mauro-Bonilla/practicum-II-animations)

## Community

Join our Discord server for discussions, support, and contributions:
[AlgeLab Discord](https://discord.gg/Q8F6xm7U)

## Development

### Project Structure

```
algelab/
├── docs/                # Documentation
├── src/                 # Source code
│   ├── api/             # API endpoints
│   ├── auth/            # Authentication logic
│   ├── config/          # Application configuration
│   ├── db/              # Database interactions
│   ├── schemas/         # Pydantic models
│   └── main.py          # Application entry point
├── .env.development     # Development environment variables
├── .env.production      # Production environment variables
├── Dockerfile           # Docker configuration
└── requirements.txt     # Python dependencies
```

### Setting Up for Development

1. Configure GitHub OAuth:
   - Create a GitHub OAuth App (see `docs/github_auth.md`)
   - Set the callback URL to `http://localhost:8000/api/auth/github/callback`
   - Update `.env.development` with your GitHub credentials

2. Configure Supabase:
   - Create a Supabase project
   - Set up the database schema
   - Add Supabase credentials to `.env.development`

## Contributing

We welcome contributions! Please read our documentation for contribution guidelines and setup instructions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For project inquiries:
- Email: maurobonillaolea@outlook.com
- Discord: [AlgeLab Server](https://discord.gg/Q8F6xm7U)
