- **User API**
  - List/Create: `http://localhost:8000/api/user/`
  - Retrieve/Update/Delete: `http://localhost:8000/api/user/{id}/`

- **Tag API**
  - List/Create: `http://localhost:8000/api/tag/`
  - Retrieve/Update/Delete: `http://localhost:8000/api/tag/{id}/`

- **Project API**
  - List/Create: `http://localhost:8000/api/project/`
  - Retrieve/Update/Delete: `http://localhost:8000/api/project/{id}/`

- **Rate API**
  - List/Create: `http://localhost:8000/api/rate/`
  - Retrieve/Update/Delete: `http://localhost:8000/api/rate/{id}/`

- **Project Image API**
  - List/Create: `http://localhost:8000/api/project-images/`
  - Retrieve/Update/Delete: `http://localhost:8000/api/project-images/project-images/{id}/`
  To get all images for project :'http://localhost:8000/api/project-images/for-project/{id}/'

- **Comments API**
  - List/Create: `http://localhost:8000/api/comments/`
  - Retrieve/Update/Delete: `http://localhost:8000/api/comments/{id}/`
  To create a reply to a comment, use the following:
	HTTP Method: POST
	URL: /api/comments/
	Request Body Example:
	{
	  "content": "This is a reply",
	  "parent": 1
	}

- **Project Reports API**
  - List/Create: `http://localhost:8000/api/project-reports/`
  - Retrieve/Update/Delete: `http://localhost:8000/api/project-reports/{id}/`
  - By Project: `http://localhost:8000/api/project-reports/by-project/{project_id}/`

- **Comment Reports API**
  - List/Create: `http://localhost:8000/api/comment-reports/`
  - Retrieve/Update/Delete: `http://localhost:8000/api/comment-reports/{id}/`

- **Donations API**
  - List/Create: `http://localhost:8000/api/donation/`
  - Retrieve/Update/Delete: `http://localhost:8000/api/donation/{id}/`

- **Categories API**
  - List/Create: `http://localhost:8000/api/categories/`
  - Retrieve/Update/Delete: `http://localhost:8000/api/categories/{id}/`

- **Project Tags API**
  - List/Create: `http://localhost:8000/api/project_tags/`
  - Retrieve/Update/Delete: `http://localhost:8000/api/project_tags/{id}/`

