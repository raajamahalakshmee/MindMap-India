API Reference
=============

This document provides detailed information about the Mindmap India API, including available endpoints, request/response formats, and usage examples.

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2

   Overview <#overview>
   Authentication <#authentication>
   Rate Limiting <#rate-limiting>
   Endpoints <#endpoints>
   Error Handling <#error-handling>
   Examples <#examples>
   Client Libraries <#client-libraries>

Overview
--------

The Mindmap India API provides programmatic access to career data, recommendations, and analysis features. The API follows RESTful principles and returns JSON-encoded responses.

Base URL
--------

All API endpoints are relative to the base URL:

```
https://api.mindmapindia.example.com/v1
```

Authentication
--------------

Most API endpoints require authentication. Include your API key in the `Authorization` header:

```http
Authorization: Bearer YOUR_API_KEY
```

### Getting an API Key

1. Sign up for an account at [Mindmap India](https://mindmapindia.example.com)
2. Go to Account Settings > API Access
3. Generate a new API key

### Rate Limiting

- **Free Tier**: 100 requests per hour
- **Pro Tier**: 1,000 requests per hour
- **Enterprise**: Custom limits available

Headers indicating rate limits are included in all responses:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1614556800  # Unix timestamp
```

Endpoints
---------

### Careers

#### List All Careers

```http
GET /careers
```

**Query Parameters:**

- `page` (integer, optional): Page number (default: 1)
- `per_page` (integer, optional): Items per page (default: 20, max: 100)
- `q` (string, optional): Search query
- `domain` (string, optional): Filter by domain
- `min_salary` (number, optional): Minimum salary
- `education_level` (string, optional): Required education level

**Example Response:**

```json
{
  "data": [
    {
      "id": "data-scientist",
      "title": "Data Scientist",
      "description": "Analyzes complex data to extract insights...",
      "domain": "Technology",
      "avg_salary": 120000,
      "education_required": "Master's Degree",
      "job_growth": 16,
      "skills": ["Python", "Machine Learning", "Statistics"]
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_items": 150,
    "total_pages": 8
  }
}
```

#### Get Career by ID

```http
GET /careers/{career_id}
```

**Path Parameters:**

- `career_id` (string, required): The ID of the career to retrieve

**Example Response:**

```json
{
  "id": "data-scientist",
  "title": "Data Scientist",
  "description": "Analyzes complex data to extract insights...",
  "detailed_description": "A Data Scientist is responsible for...",
  "domain": "Technology",
  "avg_salary": 120000,
  "salary_range": {
    "low": 90000,
    "median": 120000,
    "high": 160000
  },
  "education_required": "Master's Degree",
  "job_growth": 16,
  "skills": [
    {
      "name": "Python",
      "importance": 0.95,
      "level_required": "Advanced"
    },
    {
      "name": "Machine Learning",
      "importance": 0.90,
      "level_required": "Advanced"
    }
  ],
  "related_careers": [
    {
      "id": "machine-learning-engineer",
      "title": "Machine Learning Engineer",
      "similarity_score": 0.85
    }
  ],
  "education_pathways": [
    {
      "degree": "Bachelor's in Computer Science",
      "institutions": ["IITs", "NITs", "Top Universities"]
    }
  ],
  "job_responsibilities": [
    "Develop machine learning models",
    "Clean and analyze large datasets",
    "Create data visualizations"
  ],
  "work_environment": {
    "work_schedule": "Full-time",
    "remote_possible": true,
    "work_life_balance": "Moderate"
  },
  "job_outlook": {
    "growth_rate": 16,
    "employment_change": 5600,
    "prospects": "Excellent"
  },
  "certifications": [
    {
      "name": "Google Data Analytics Professional Certificate",
      "issuer": "Google",
      "duration": "6 months"
    }
  ],
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Recommendations

#### Get Career Recommendations

```http
POST /recommendations
```

**Request Body:**

```json
{
  "interests": ["technology", "data analysis"],
  "skills": ["Python", "SQL"],
  "education_level": "Bachelor's Degree",
  "experience_years": 3,
  "preferred_domains": ["Technology", "Finance"],
  "salary_expectations": {
    "min": 80000,
    "preferred": 100000
  },
  "work_preferences": {
    "remote": true,
    "relocation": false
  },
  "limit": 5
}
```

**Response:**

```json
{
  "recommendations": [
    {
      "career_id": "data-scientist",
      "title": "Data Scientist",
      "match_score": 0.92,
      "reason": "Matches your skills in Python and interest in data analysis",
      "avg_salary": 120000,
      "education_required": "Master's Degree"
    },
    {
      "career_id": "data-analyst",
      "title": "Data Analyst",
      "match_score": 0.88,
      "reason": "Aligns with your SQL skills and interest in data",
      "avg_salary": 85000,
      "education_required": "Bachelor's Degree"
    }
  ],
  "skill_gaps": [
    {
      "skill": "Machine Learning",
      "importance": 0.85,
      "suggested_learning": [
        {
          "resource": "Coursera - Machine Learning by Andrew Ng",
          "type": "online_course",
          "duration": "11 weeks"
        }
      ]
    }
  ]
}
```

### Skills

#### Search Skills

```http
GET /skills
```

**Query Parameters:**

- `q` (string, optional): Search query
- `page` (integer, optional): Page number
- `per_page` (integer, optional): Items per page

**Response:**

```json
{
  "data": [
    {
      "id": "python",
      "name": "Python",
      "category": "Programming Languages",
      "description": "A high-level programming language...",
      "related_skills": ["Pandas", "NumPy", "Scikit-learn"],
      "in_demand": true,
      "trending": true
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total_items": 150,
    "total_pages": 8
  }
}
```

### Domains

#### List All Domains

```http
GET /domains
```

**Response:**

```json
{
  "data": [
    {
      "id": "technology",
      "name": "Technology",
      "description": "Careers in software development, IT, and technology services",
      "total_careers": 45,
      "avg_salary": 95000,
      "growth_rate": 15
    },
    {
      "id": "healthcare",
      "name": "Healthcare",
      "description": "Medical and healthcare professions",
      "total_careers": 38,
      "avg_salary": 85000,
      "growth_rate": 18
    }
  ]
}
```

Error Handling
-------------

### Error Response Format

```json
{
  "error": {
    "code": "invalid_request",
    "message": "The request is missing a required parameter",
    "details": {
      "parameter": "career_id"
    },
    "documentation_url": "https://docs.mindmapindia.example.com/errors/invalid-request"
  }
}
```

### Common Error Codes

| Status Code | Error Code | Description |
|-------------|------------|-------------|
| 400 | invalid_request | The request is missing required parameters |
| 401 | unauthorized | Invalid or missing API key |
| 403 | forbidden | Insufficient permissions |
| 404 | not_found | The requested resource doesn't exist |
| 429 | rate_limit_exceeded | Rate limit exceeded |
| 500 | server_error | Internal server error |
| 503 | service_unavailable | Service temporarily unavailable |

Examples
--------

### Python Example

```python
import requests

API_KEY = "your_api_key_here"
BASE_URL = "https://api.mindmapindia.example.com/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Get career by ID
response = requests.get(
    f"{BASE_URL}/careers/data-scientist",
    headers=headers
)
career = response.json()
print(career["title"])  # Data Scientist

# Get recommendations
payload = {
    "skills": ["Python", "SQL"],
    "interests": ["data analysis"],
    "limit": 3
}
response = requests.post(
    f"{BASE_URL}/recommendations",
    headers=headers,
    json=payload
)
recommendations = response.json()
for rec in recommendations["recommendations"]:
    print(f"{rec['title']} - Match: {rec['match_score']:.0%}")
```

### JavaScript Example

```javascript
const API_KEY = 'your_api_key_here';
const BASE_URL = 'https://api.mindmapindia.example.com/v1';

const headers = {
  'Authorization': `Bearer ${API_KEY}`,
  'Content-Type': 'application/json'
};

// Get career by ID
fetch(`${BASE_URL}/careers/data-scientist`, { headers })
  .then(response => response.json())
  .then(career => console.log(career.title));

// Get recommendations
const payload = {
  skills: ['Python', 'SQL'],
  interests: ['data analysis'],
  limit: 3
};

fetch(`${BASE_URL}/recommendations`, {
  method: 'POST',
  headers,
  body: JSON.stringify(payload)
})
  .then(response => response.json())
  .then(data => {
    data.recommendations.forEach(rec => {
      console.log(`${rec.title} - Match: ${(rec.match_score * 100).toFixed(0)}%`);
    });
  });
```

Client Libraries
---------------

### Official Libraries

- **Python**: `pip install mindmap-india`
  ```python
  from mindmap import MindmapClient
  
  client = MindmapClient(api_key="your_api_key")
  career = client.get_career("data-scientist")
  recommendations = client.get_recommendations(
      skills=["Python"],
      interests=["data analysis"]
  )
  ```

- **JavaScript/Node.js**: `npm install mindmap-india`
  ```javascript
  const MindmapClient = require('mindmap-india');
  
  const client = new MindmapClient('your_api_key');
  client.getCareer('data-scientist')
    .then(career => console.log(career.title));
  ```

### Community Libraries

- **Ruby**: `gem install mindmap-india`
- **PHP**: `composer require mindmap/mindmap-india`
- **Go**: `go get github.com/community/mindmap-go`

Changelog
---------

### v1.0.0 (2024-06-01)
- Initial public release of the Mindmap India API
- Added careers, recommendations, skills, and domains endpoints

### v1.1.0 (Planned)
- Add user authentication endpoints
- Add saved careers and career paths features
- Enhanced recommendations with more personalization options

Support
-------

For API support, please contact:

- Email: api-support@mindmapindia.example.com
- GitHub Issues: https://github.com/yourusername/mindmap-india/issues
- Documentation: https://docs.mindmapindia.example.com
