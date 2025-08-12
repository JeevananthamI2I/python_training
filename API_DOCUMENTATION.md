# 🏥 MediTrack360 - Final API Documentation

## 📋 Table of Contents

1. [Overview](#overview)
2. [Base URLs & Environment](#base-urls--environment)
3. [Authentication](#authentication)
4. [Response Format](#response-format)
5. [Permission & Access Control](#permission--access-control)
6. [HMS API Flow](#hms-api-flow)
7. [API Endpoints](#api-endpoints)
8. [Data Models](#data-models)
9. [Error Codes](#error-codes)
10. [Getting Started](#getting-started)
11. [Testing Guide](#testing-guide)

## 📋 Overview

MediTrack360 is a comprehensive Hospital Management System (HMS) API built with Django REST Framework. The system provides a complete solution for managing hospitals, clinics, patients, staff, and medical visits with role-based access control and secure authentication.

### **Key Features**
- 🔐 JWT-based authentication
- 👥 Role-based access control
- 🏢 Multi-organization support
- 👨‍⚕️ Staff management (doctors, nurses, technicians)
- 🏥 Patient management
- 📅 Visit/appointment scheduling
- 🗺️ Address management
- 🗑️ Soft delete functionality
- 📊 Comprehensive logging and monitoring

## 🔗 Base URLs & Environment

### **Development Environment**
- **Base URL**: `http://localhost:8000`
- **API Version**: `v1`
- **Full API URL**: `http://localhost:8000/api/v1/`

### **API Documentation**
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **API Schema**: `http://localhost:8000/api/schema/`

## 🔐 Authentication

The API uses JWT (JSON Web Token) authentication for protected endpoints.

### **Authentication Header Format**
```http
Authorization: Bearer <access_token>
```

### **Token Types**
- **Access Token**: Short-lived token for API requests
- **Refresh Token**: Long-lived token for renewing access tokens

### **Token Endpoints**
- **Login**: `POST /api/v1/auth/login/`
- **Refresh**: `POST /api/v1/auth/refresh/`
- **Register**: `POST /api/v1/auth/register/`

## 📊 Response Format

All API responses follow a consistent format:

### **Success Response**
```json
{
    "success": true,
    "message": "Operation completed successfully",
    "data": { ... },
    "status_code": 200
}
```

### **Error Response**
```json
{
    "success": false,
    "error": "Error message",
    "code": "ERROR_CODE",
    "details": { ... }
}
```

### **Pagination Response**
```json
{
    "success": true,
    "message": "Data retrieved successfully",
    "data": [ ... ],
    "pagination": {
        "count": 100,
        "next": "http://localhost:8000/api/v1/users/?page=2",
        "previous": null,
        "results": 25
    }
}
```

## 🔍 Filtering, Search & Pagination

### **Global Query Parameters**
All list endpoints support the following query parameters:

#### **Pagination Parameters**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

#### **Search Parameters**
- `search`: Search term across multiple fields (case-insensitive)

#### **Ordering Parameters**
- `ordering`: Sort field with optional prefix:
  - `field_name`: Ascending order
  - `-field_name`: Descending order
  - Example: `ordering=email` or `ordering=-created_at`

### **Filtering Examples**
```http
# Basic pagination
GET /api/v1/users/?page=2&page_size=10

# Search across fields
GET /api/v1/users/?search=john

# Filter by status and order by creation date
GET /api/v1/users/?status=active&ordering=-created_at

# Multiple filters with search
GET /api/v1/users/?status=active&role=doctor&search=cardiology&ordering=email
```

## 🔐 Permission & Access Control

### **Access Levels**
- **🔓 Public**: No authentication required
- **🔑 Authenticated**: Valid JWT token required
- **👑 Admin Only**: Admin role required
- **🏢 Organization Admin**: Organization admin role required
- **👨‍⚕️ Staff**: Any authenticated user with valid role

### **Role-Based Permissions**

| Role | Permissions | Access Level |
|------|-------------|--------------|
| **super_admin** | Full system access | All endpoints |
| **hospital_admin** | Hospital management | Hospital + staff endpoints |
| **admin** | Organization management | Organization + user endpoints |
| **doctor** | Patient & visit management | Patient + visit endpoints |
| **nurse** | Patient care | Patient + visit endpoints |
| **technician** | Equipment & diagnostics | Technical endpoints |
| **receptionist** | Patient registration | Patient + scheduling endpoints |
| **viewer** | Read-only access | View endpoints only |

## 🏥 HMS API Flow

The HMS API implements a specific three-step flow for setting up a hospital management system:

### **Step 1: Admin Registration**
- **Endpoint**: `POST /api/v1/users/`
- **Purpose**: Register the first admin user without organization_id
- **Access**: 🔓 Public
- **Response**: Returns user_id, role_id, and organization_id (null)

### **Step 2: Organization Creation**
- **Endpoint**: `POST /api/v1/organizations/`
- **Purpose**: Create organization and link the admin user
- **Access**: 👑 Admin Only
- **Response**: Returns organization_id

### **Step 3: Additional User Registration**
- **Endpoint**: `POST /api/v1/users/`
- **Purpose**: Register additional users (doctors, nurses, etc.) with organization_id
- **Access**: 🔓 Public
- **Response**: Returns user_id, role_id, and organization_id

## 🚀 API Endpoints

### **Authentication Endpoints**

#### **User Login**
```http
POST /api/v1/auth/login/
```
**Access**: 🔓 Public

**Request Body**:
```json
{
    "email": "admin@meditrack360.com",
    "password": "Admin@2025#Secure!"
}
```

**Response**:
```json
{
    "success": true,
    "message": "Login successful",
    "data": {
        "user": {
            "id": 1,
            "email": "admin@meditrack360.com",
            "username": "admin",
            "phone": "9876543210",
            "status": "active"
        },
        "tokens": {
            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
        }
    }
}
```

#### **Token Refresh**
```http
POST /api/v1/auth/refresh/
```
**Access**: 🔓 Public

**Request Body**:
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### **User Registration**
```http
POST /api/v1/auth/register/
```
**Access**: 🔓 Public

**Request Body**:
```json
{
    "email": "user@meditrack360.com",
    "password": "User@2025#Secure!",
    "password_confirm": "User@2025#Secure!"
}
```

### **User Management Endpoints**

#### **User Registration (HMS Flow)**
```http
POST /api/v1/users/
```
**Access**: 🔓 Public

**Request Body**:
```json
{
    "email": "doctor@meditrack360.com",
    "password": "Doctor@2025#Secure!",
    "password_confirm": "Doctor@2025#Secure!",
    "phone": "9876543211",
    "organization_id": 1,
    "role": {
        "name": "doctor",
        "description": "Medical doctor with patient care access"
    },
    "address": {
        "city": "Salem",
        "state": "Tamil Nadu",
        "pincode": "636007",
        "country": "India"
    },
    "status": "active"
}
```

**Response**:
```json
{
    "success": true,
    "message": "User created successfully",
    "data": {
        "user_id": 2,
        "organization_id": 1,
        "role_id": 2,
        "user": {
            "id": 2,
            "email": "doctor@meditrack360.com",
            "username": "doctor",
            "phone": "9876543211",
            "status": "active",
            "role": {
                "id": 2,
                "name": "doctor",
                "description": "Medical doctor with patient care access"
            },
            "organization": {
                "id": 1,
                "name": "MediTrack General Hospital"
            },
            "address": {
                "city": "Salem",
                "state": "Tamil Nadu",
                "pincode": "636007",
                "country": "India"
            }
        }
    }
}
```

#### **List Users**
```http
GET /api/v1/users/list/
```
**Access**: 👑 Admin Only

**Query Parameters**:
- `status`: Filter by user status (active, inactive, suspended)
- `organization`: Filter by organization name
- `role`: Filter by role name
- `gender`: Filter by gender (M, F, O)
- `search`: Search in email, username, phone
- `ordering`: Sort by field (email, username, created_at, status)
- `page`: Page number for pagination
- `page_size`: Number of items per page

**Filtering Examples**:
```http
# Filter active doctors
GET /api/v1/users/list/?status=active&role=doctor

# Search for users with "john" in email/username/phone
GET /api/v1/users/list/?search=john

# Get users from specific organization, ordered by creation date
GET /api/v1/users/list/?organization=MediTrack&ordering=-created_at

# Paginated results with custom page size
GET /api/v1/users/list/?page=2&page_size=15&status=active
```

**Response with Pagination**:
```json
{
    "success": true,
    "message": "Users retrieved successfully",
    "data": [
        {
            "id": 1,
            "email": "admin@meditrack360.com",
            "username": "admin",
            "phone": "9876543210",
            "status": "active",
            "role_name": "admin",
            "organization_name": "MediTrack General Hospital"
        }
    ],
    "pagination": {
        "count": 25,
        "next": "http://localhost:8000/api/v1/users/list/?page=2",
        "previous": null,
        "results": 20
    }
}
```

#### **Get User Details**
```http
GET /api/v1/users/{id}/
```
**Access**: 👑 Admin Only

#### **Update User**
```http
PUT /api/v1/users/{id}/
```
**Access**: 👑 Admin Only

**Request Body**:
```json
{
    "phone": "9876543212",
    "gender": "M",
    "date_of_birth": "1990-01-01"
}
```

#### **Change User Password**
```http
POST /api/v1/users/{id}/change-password/
```
**Access**: 👑 Admin Only

**Request Body**:
```json
{
    "old_password": "Admin@2025#Secure!",
    "new_password": "NewPassword@2025#Secure!"
}
```

#### **Delete User (Soft Delete)**
```http
DELETE /api/v1/users/{id}/
```
**Access**: 👑 Admin Only

#### **Restore Deleted User**
```http
POST /api/v1/users/{id}/restore/
```
**Access**: 👑 Admin Only

#### **List Deleted Users**
```http
GET /api/v1/users/deleted/
```
**Access**: 👑 Admin Only

### **Organization Management Endpoints**

#### **Create Organization**
```http
POST /api/v1/organizations/
```
**Access**: 👑 Admin Only

**Request Body**:
```json
{
    "name": "MediTrack General Hospital",
    "type": "Hospital",
    "email": "contact@meditrack.com",
    "phone": "+919876543210",
    "address": {
        "city": "Salem",
        "state": "Tamil Nadu",
        "pincode": "636007",
        "country": "India"
    },
    "status": "active"
}
```

**Response**:
```json
{
    "success": true,
    "message": "Organization created successfully",
    "data": {
        "organization_id": 1,
        "organization": {
            "id": 1,
            "name": "MediTrack General Hospital",
            "type": "Hospital",
            "email": "contact@meditrack.com",
            "phone": "+919876543210",
            "status": "active",
            "address": {
                "city": "Salem",
                "state": "Tamil Nadu",
                "pincode": "636007",
                "country": "India"
            },
            "created_at": "2025-08-12T13:30:00Z",
            "updated_at": "2025-08-12T13:30:00Z"
        }
    }
}
```

#### **List Organizations**
```http
GET /api/v1/organizations/list/
```
**Access**: 👑 Admin Only

**Query Parameters**:
- `status`: Filter by organization status (active, inactive, suspended)
- `type`: Filter by organization type (Hospital, Clinic, Laboratory, Pharmacy, Other)
- `search`: Search in name, email, phone
- `ordering`: Sort by field (name, created_at, status, type)
- `page`: Page number for pagination
- `page_size`: Number of items per page

**Filtering Examples**:
```http
# Filter active hospitals
GET /api/v1/organizations/list/?status=active&type=Hospital

# Search for organizations with "clinic" in name/email/phone
GET /api/v1/organizations/list/?search=clinic

# Get organizations ordered by creation date
GET /api/v1/organizations/list/?ordering=-created_at

# Paginated results with custom page size
GET /api/v1/organizations/list/?page=1&page_size=10&status=active
```

**Response with Pagination**:
```json
{
    "success": true,
    "message": "Organizations retrieved successfully",
    "data": [
        {
            "id": 1,
            "name": "MediTrack General Hospital",
            "type": "Hospital",
            "email": "contact@meditrack.com",
            "phone": "+919876543210",
            "status": "active",
            "address": "Salem, Tamil Nadu, India"
        }
    ],
    "pagination": {
        "count": 15,
        "next": "http://localhost:8000/api/v1/organizations/list/?page=2",
        "previous": null,
        "results": 20
    }
}
```

#### **Get Organization Details**
```http
GET /api/v1/organizations/{id}/
```
**Access**: 👑 Admin Only

#### **Update Organization**
```http
PUT /api/v1/organizations/{id}/
```
**Access**: 👑 Admin Only

#### **Get Organization Status**
```http
GET /api/v1/organizations/{id}/status/
```
**Access**: 👑 Admin Only

#### **Delete Organization (Soft Delete)**
```http
DELETE /api/v1/organizations/{id}/
```
**Access**: 👑 Admin Only

#### **Restore Deleted Organization**
```http
POST /api/v1/organizations/{id}/restore/
```
**Access**: 👑 Admin Only

#### **List Deleted Organizations**
```http
GET /api/v1/organizations/deleted/
```
**Access**: 👑 Admin Only

### **Role Management Endpoints**

#### **List Roles**
```http
GET /api/v1/roles/
```
**Access**: 👑 Admin Only

#### **Create Role**
```http
POST /api/v1/roles/create/
```
**Access**: 👑 Admin Only

**Request Body**:
```json
{
    "name": "specialist",
    "description": "Medical specialist with advanced training",
    "permissions": {
        "can_view_patients": true,
        "can_edit_patients": true,
        "can_create_visits": true
    }
}
```

#### **Get Role Details**
```http
GET /api/v1/roles/{id}/
```
**Access**: 👑 Admin Only

#### **Update Role**
```http
PUT /api/v1/roles/{id}/
```
**Access**: 👑 Admin Only

#### **Toggle Role Status**
```http
POST /api/v1/roles/{id}/toggle-status/
```
**Access**: 👑 Admin Only

#### **Delete Role (Soft Delete)**
```http
DELETE /api/v1/roles/{id}/
```
**Access**: 👑 Admin Only

#### **Restore Deleted Role**
```http
POST /api/v1/roles/{id}/restore/
```
**Access**: 👑 Admin Only

#### **List Deleted Roles**
```http
GET /api/v1/roles/deleted/
```
**Access**: 👑 Admin Only

### **Address Management Endpoints**

#### **List Addresses**
```http
GET /api/v1/addresses/
```
**Access**: 👑 Admin Only

#### **Create Address**
```http
POST /api/v1/addresses/create/
```
**Access**: 👑 Admin Only

**Request Body**:
```json
{
    "street_address": "123 Main Street",
    "city": "Salem",
    "state": "Tamil Nadu",
    "pincode": "636007",
    "country": "India"
}
```

#### **Get Address Details**
```http
GET /api/v1/addresses/{id}/
```
**Access**: 👑 Admin Only

#### **Update Address**
```http
PUT /api/v1/addresses/{id}/
```
**Access**: 👑 Admin Only

#### **Delete Address (Soft Delete)**
```http
DELETE /api/v1/addresses/{id}/
```
**Access**: 👑 Admin Only

#### **Restore Deleted Address**
```http
POST /api/v1/addresses/{id}/restore/
```
**Access**: 👑 Admin Only

#### **List Deleted Addresses**
```http
GET /api/v1/addresses/deleted/
```
**Access**: 👑 Admin Only

#### **Get Cities**
```http
GET /api/v1/addresses/cities/
```
**Access**: 🔑 Authenticated

#### **Get States**
```http
GET /api/v1/addresses/states/
```
**Access**: 🔑 Authenticated

### **Patient Management Endpoints**

#### **List Patients**
```http
GET /api/v1/patients/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

**Query Parameters**:
- `status`: Filter by patient status (active, inactive, deceased)
- `gender`: Filter by gender (M, F, O)
- `blood_group`: Filter by blood group (A+, A-, B+, B-, AB+, AB-, O+, O-)
- `organization`: Filter by organization ID
- `age_min`: Filter by minimum age
- `age_max`: Filter by maximum age
- `search`: Search in name, email, phone
- `ordering`: Sort by field (name, age, created_at, status)
- `page`: Page number for pagination
- `page_size`: Number of items per page

**Filtering Examples**:
```http
# Filter active male patients
GET /api/v1/patients/?status=active&gender=M

# Search for patients with "john" in name/email/phone
GET /api/v1/patients/?search=john

# Get patients with specific blood group, ordered by age
GET /api/v1/patients/?blood_group=O+&ordering=age

# Filter patients by age range
GET /api/v1/patients/?age_min=18&age_max=65&status=active

# Paginated results with custom page size
GET /api/v1/patients/?page=1&page_size=15&status=active

# Advanced filtering: Active patients with specific blood group and age range
GET /api/v1/patients/?status=active&blood_group=O+&age_min=18&age_max=65&ordering=age&page=1&page_size=20

# Search patients by medical condition with pagination
GET /api/v1/patients/?search=diabetes&status=active&page=2&page_size=10&ordering=-created_at

# Filter patients by organization and gender
GET /api/v1/patients/?organization=1&gender=F&status=active&page=1&page_size=25
```

**Response with Pagination**:
```json
{
    "success": true,
    "message": "Patients retrieved successfully",
    "data": [
        {
            "id": "uuid-here",
            "name": "John Doe",
            "age": 35,
            "gender": "M",
            "phone": "9876543210",
            "email": "john.doe@email.com",
            "blood_group": "O+",
            "status": "active",
            "organization_name": "MediTrack General Hospital"
        }
    ],
    "pagination": {
        "count": 50,
        "next": "http://localhost:8000/api/v1/patients/?page=2",
        "previous": null,
        "results": 20
    }
}
```

#### **Create Patient**
```http
POST /api/v1/patients/create/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

**Request Body**:
```json
{
    "name": "John Doe",
    "age": 35,
    "gender": "M",
    "phone": "9876543210",
    "email": "john.doe@email.com",
    "date_of_birth": "1990-01-01",
    "blood_group": "O+",
    "medical_history": "No significant medical history",
    "allergies": "None known",
    "organization": 1,
    "address": {
        "city": "Salem",
        "state": "Tamil Nadu",
        "pincode": "636007",
        "country": "India"
    }
}
```

**Response**:
```json
{
    "success": true,
    "message": "Patient created successfully",
    "data": {
        "patient_id": 1,
        "patient": {
            "id": 1,
            "name": "John Doe",
            "age": 35,
            "gender": "M",
            "phone": "9876543210",
            "email": "john.doe@email.com",
            "date_of_birth": "1990-01-01",
            "blood_group": "O+",
            "medical_history": "No significant medical history",
            "allergies": "None known",
            "status": "active",
            "organization": {
                "id": 1,
                "name": "MediTrack General Hospital"
            },
            "address": {
                "id": 5,
                "city": "Salem",
                "state": "Tamil Nadu",
                "pincode": "636007",
                "country": "India"
            },
            "created_by": {
                "id": 2,
                "username": "doctor",
                "email": "doctor@meditrack360.com"
            },
            "created_at": "2025-08-12T14:30:00Z",
            "updated_at": "2025-08-12T14:30:00Z"
        }
    }
}
```

#### **Get Patient Details**
```http
GET /api/v1/patients/{id}/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

#### **Update Patient**
```http
PUT /api/v1/patients/{id}/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

#### **Get Patient Medical History**
```http
GET /api/v1/patients/{id}/medical-history/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses)

#### **Delete Patient (Soft Delete)**
```http
DELETE /api/v1/patients/{id}/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

#### **Restore Deleted Patient**
```http
POST /api/v1/patients/{id}/restore/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

#### **List Deleted Patients**
```http
GET /api/v1/patients/deleted/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

#### **Get Blood Groups**
```http
GET /api/v1/patients/blood-groups/
```
**Access**: 🔑 Authenticated

### **Visit Management Endpoints**

#### **List Visits**
```http
GET /api/v1/visits/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

**Query Parameters**:
- `status`: Filter by visit status (scheduled, in_progress, completed, cancelled, no_show)
- `priority`: Filter by priority (low, medium, high, urgent)
- `doctor`: Filter by doctor ID
- `patient`: Filter by patient ID
- `organization`: Filter by organization ID
- `date_from`: Filter visits from specific date (YYYY-MM-DD)
- `date_to`: Filter visits to specific date (YYYY-MM-DD)
- `search`: Search in patient name, symptoms, notes
- `ordering`: Sort by field (scheduled_date, priority, created_at, status)
- `page`: Page number for pagination
- `page_size`: Number of items per page

**Filtering Examples**:
```http
# Filter scheduled visits for today
GET /api/v1/visits/?status=scheduled&date_from=2025-08-12&date_to=2025-08-12

# Search for visits with "fever" in symptoms/notes
GET /api/v1/visits/?search=fever

# Get urgent visits ordered by scheduled date
GET /api/v1/visits/?priority=urgent&ordering=scheduled_date

# Filter visits by doctor and status
GET /api/v1/visits/?doctor=2&status=completed

# Paginated results with custom page size
GET /api/v1/visits/?page=1&page_size=15&status=scheduled

# Advanced filtering: Today's scheduled visits for specific doctor with pagination
GET /api/v1/visits/?doctor=2&status=scheduled&date_from=2025-08-12&date_to=2025-08-12&page=1&page_size=20&ordering=scheduled_date

# Search visits by patient symptoms with priority filtering
GET /api/v1/visits/?search=diabetes&priority=high&status=scheduled&page=1&page_size=15&ordering=-scheduled_date

# Filter visits by organization and date range
GET /api/v1/visits/?organization=1&date_from=2025-08-01&date_to=2025-08-31&status=completed&page=1&page_size=25&ordering=-actual_date

# Get all visits for specific patient
GET /api/v1/visits/?patient=1&ordering=-scheduled_date&page=1&page_size=10
```

**Response with Pagination**:
```json
{
    "success": true,
    "message": "Visits retrieved successfully",
    "data": [
        {
            "id": "uuid-here",
            "patient_name": "John Doe",
            "doctor_name": "Dr. Smith",
            "scheduled_date": "2025-08-15T10:00:00Z",
            "status": "scheduled",
            "priority": "medium",
            "symptoms": "Fever and headache",
            "organization_name": "MediTrack General Hospital"
        }
    ],
    "pagination": {
        "count": 30,
        "next": "http://localhost:8000/api/v1/visits/?page=2",
        "previous": null,
        "results": 20
    }
}
```

#### **Create Visit**
```http
POST /api/v1/visits/create/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

**Request Body**:
```json
{
    "patient": 1,
    "doctor": 2,
    "technician": 3,
    "organization": 1,
    "scheduled_date": "2025-08-15T10:00:00Z",
    "priority": "medium",
    "symptoms": "Fever and headache",
    "notes": "Patient reports symptoms for 2 days"
}
```

**Response**:
```json
{
    "success": true,
    "message": "Visit created successfully",
    "data": {
        "visit_id": "660e8400-e29b-41d4-a716-446655440001",
        "visit": {
            "id": "660e8400-e29b-41d4-a716-446655440001",
            "patient": {
                "id": 1,
                "name": "John Doe",
                "age": 35,
                "gender": "M"
            },
            "doctor": {
                "id": 2,
                "username": "doctor",
                "email": "doctor@meditrack360.com"
            },
            "technician": {
                "id": 3,
                "username": "technician",
                "email": "technician@meditrack360.com"
            },
            "organization": {
                "id": 1,
                "name": "MediTrack General Hospital"
            },
            "scheduled_date": "2025-08-15T10:00:00Z",
            "actual_date": null,
            "status": "scheduled",
            "priority": "medium",
            "symptoms": "Fever and headache",
            "diagnosis": null,
            "prescription": null,
            "notes": "Patient reports symptoms for 2 days",
            "created_at": "2025-08-12T15:00:00Z",
            "updated_at": "2025-08-12T15:00:00Z"
        }
    }
}
```

#### **Get Visit Details**
```http
GET /api/v1/visits/{id}/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

#### **Update Visit**
```http
PUT /api/v1/visits/{id}/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

#### **Complete Visit**
```http
POST /api/v1/visits/{id}/complete/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses)

**Request Body**:
```json
{
    "diagnosis": "Common cold",
    "prescription": "Rest, fluids, and over-the-counter medication",
    "notes": "Patient should return if symptoms worsen"
}
```

**Response**:
```json
{
    "success": true,
    "message": "Visit completed successfully",
    "data": {
        "visit_id": "660e8400-e29b-41d4-a716-446655440001",
        "visit": {
            "id": "660e8400-e29b-41d4-a716-446655440001",
            "status": "completed",
            "actual_date": "2025-08-12T15:30:00Z",
            "diagnosis": "Common cold",
            "prescription": "Rest, fluids, and over-the-counter medication",
            "notes": "Patient should return if symptoms worsen",
            "updated_at": "2025-08-12T15:30:00Z"
        }
    }
}
```

#### **Assign Visit to Different Doctor**
```http
PUT /api/v1/visits/{id}/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

**Request Body**:
```json
{
    "doctor": 4,
    "notes": "Reassigned to specialist due to complex symptoms"
}
```

**Response**:
```json
{
    "success": true,
    "message": "Visit updated successfully",
    "data": {
        "visit_id": "660e8400-e29b-41d4-a716-446655440001",
        "visit": {
            "id": "660e8400-e29b-41d4-a716-446655440001",
            "doctor": {
                "id": 4,
                "username": "specialist",
                "email": "specialist@meditrack360.com"
            },
            "notes": "Reassigned to specialist due to complex symptoms",
            "updated_at": "2025-08-12T16:00:00Z"
        }
    }
}
```

#### **Cancel Visit**
```http
POST /api/v1/visits/{id}/cancel/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

**Request Body**:
```json
{
    "notes": "Patient requested cancellation"
}
```

#### **Delete Visit (Soft Delete)**
```http
DELETE /api/v1/visits/{id}/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

#### **Restore Deleted Visit**
```http
POST /api/v1/visits/{id}/restore/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

#### **List Deleted Visits**
```http
GET /api/v1/visits/deleted/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

#### **Get Upcoming Visits**
```http
GET /api/v1/visits/upcoming/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

#### **Get Today's Visits**
```http
GET /api/v1/visits/today/
```
**Access**: 👨‍⚕️ Staff (doctors, nurses, receptionists)

## 📝 Data Models

### **User Model**
```python
class User(AbstractUser):
    # Core fields
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)  # Primary login field
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Relationships
    organization = models.ForeignKey('organizations.Organization', null=True, blank=True)
    role = models.ForeignKey('roles.Role', null=True, blank=True)
    address = models.ForeignKey('addresses.Address', null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Field Details**:
- `id`: Auto-increment integer (Primary Key)
- `email`: Email address (unique, used for login)
- `username`: Username (auto-generated from email, optional)
- `phone`: Phone number
- `gender`: Gender (M, F, O)
- `date_of_birth`: Date of birth
- `organization`: Foreign key to Organization
- `role`: Foreign key to Role
- `address`: Foreign key to Address
- `status`: Status (active, inactive, suspended)
- `is_deleted`: Soft delete flag
- `deleted_at`: Deletion timestamp
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### **Organization Model**
```python
class Organization(models.Model):
    # Core fields
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Hospital')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Relationships
    address = models.ForeignKey('addresses.Address')
    
    # Status
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Field Details**:
- `id`: Auto-increment integer (Primary Key)
- `name`: Organization name
- `email`: Organization email (unique)
- `phone`: Organization phone
- `type`: Organization type (Hospital, Clinic, Laboratory, Pharmacy, Other)
- `status`: Status (active, inactive, suspended)
- `address`: Foreign key to Address
- `is_deleted`: Soft delete flag
- `deleted_at`: Deletion timestamp
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### **Role Model**
```python
class Role(models.Model):
    # Core fields
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.JSONField(default=dict, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Field Details**:
- `id`: Auto-increment integer (Primary Key)
- `name`: Role name (unique)
- `description`: Role description
- `permissions`: JSON field for permissions
- `is_active`: Active status
- `is_deleted`: Soft delete flag
- `deleted_at`: Deletion timestamp
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### **Address Model**
```python
class Address(models.Model):
    # Core fields
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    
    # Status
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Field Details**:
- `id`: Auto-increment integer (Primary Key)
- `street_address`: Street address
- `city`: City
- `state`: State
- `pincode`: Pincode
- `country`: Country (default: India)
- `is_deleted`: Soft delete flag
- `deleted_at`: Deletion timestamp
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### **Patient Model**
```python
class Patient(models.Model):
    # Core fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    
    # Relationships
    organization = models.ForeignKey('organizations.Organization')
    created_by = models.ForeignKey('users.User', null=True, blank=True)
    address = models.ForeignKey('addresses.Address', null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Field Details**:
- `id`: UUID (Primary Key)
- `name`: Patient name
- `age`: Patient age
- `gender`: Gender (M, F, O)
- `phone`: Phone number
- `email`: Email address
- `date_of_birth`: Date of birth
- `blood_group`: Blood group
- `medical_history`: Medical history
- `allergies`: Known allergies
- `organization`: Foreign key to Organization
- `created_by`: Foreign key to User (who created the record)
- `address`: Foreign key to Address
- `status`: Status (active, inactive, deceased)
- `is_deleted`: Soft delete flag
- `deleted_at`: Deletion timestamp
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### **Visit Model**
```python
class Visit(models.Model):
    # Core fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    scheduled_date = models.DateTimeField()
    actual_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    symptoms = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    prescription = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Relationships
    patient = models.ForeignKey('patients.Patient')
    doctor = models.ForeignKey('users.User', related_name='doctor_visits')
    technician = models.ForeignKey('users.User', related_name='technician_visits', null=True, blank=True)
    organization = models.ForeignKey('organizations.Organization')
    
    # Status
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Field Details**:
- `id`: UUID (Primary Key)
- `scheduled_date`: Scheduled appointment date/time
- `actual_date`: Actual visit date/time
- `status`: Status (scheduled, in_progress, completed, cancelled, no_show)
- `priority`: Priority (low, medium, high, urgent)
- `symptoms`: Patient symptoms
- `diagnosis`: Medical diagnosis
- `prescription`: Medical prescription
- `notes`: Additional notes
- `patient`: Foreign key to Patient
- `doctor`: Foreign key to User (doctor)
- `technician`: Foreign key to User (technician)
- `organization`: Foreign key to Organization
- `is_deleted`: Soft delete flag
- `deleted_at`: Deletion timestamp
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## 🔧 Error Handling & Exception Management

### **Error Handling Strategy**
The API implements a comprehensive error handling strategy with multiple layers:

1. **Custom Exceptions**: Domain-specific exceptions for business logic
2. **Validation Errors**: Serializer and field validation errors
3. **Database Errors**: Integrity and constraint violations
4. **Authentication Errors**: JWT and permission failures
5. **Base Exception**: Catch-all for unexpected errors

### **Exception Hierarchy**
```
CustomAPIException (Base)
├── ResourceNotFoundException (404)
│   ├── UserNotFoundException
│   ├── OrganizationNotFoundException
│   ├── PatientNotFoundException
│   └── VisitNotFoundException
├── ValidationException (400)
├── AuthenticationException (401)
├── PermissionException (403)
├── BusinessLogicException (400)
│   ├── UserAlreadyExistsException
│   └── OrganizationAlreadyExistsException
├── DatabaseException (500)
├── ExternalServiceException (502)
├── RateLimitException (429)
└── ConfigurationException (500)
```

### **Common Error Codes**

| Error Code | Description | HTTP Status | Exception Type |
|------------|-------------|-------------|----------------|
| `user_creation_validation_error` | User data validation failed | 400 | ValidationException |
| `user_creation_error` | User creation failed | 500 | DatabaseException |
| `organization_creation_validation_error` | Organization data validation failed | 400 | ValidationException |
| `organization_creation_error` | Organization creation failed | 500 | DatabaseException |
| `user_list_error` | Failed to retrieve users | 500 | DatabaseException |
| `organization_list_error` | Failed to retrieve organizations | 500 | DatabaseException |
| `user_detail_error` | Failed to retrieve user details | 500 | DatabaseException |
| `organization_detail_error` | Failed to retrieve organization details | 500 | DatabaseException |
| `user_update_error` | Failed to update user | 500 | DatabaseException |
| `organization_update_error` | Failed to update organization | 500 | DatabaseException |
| `user_delete_error` | Failed to delete user | 500 | DatabaseException |
| `organization_delete_error` | Failed to delete organization | 500 | DatabaseException |
| `user_restore_error` | Failed to restore user | 500 | DatabaseException |
| `organization_restore_error` | Failed to restore organization | 500 | DatabaseException |
| `password_change_error` | Failed to change password | 500 | DatabaseException |
| `invalid_old_password` | Invalid old password provided | 400 | ValidationException |
| `password_change_validation_error` | Password change validation failed | 400 | ValidationException |
| `authentication_failed` | Authentication failed | 401 | AuthenticationException |
| `permission_denied` | Permission denied | 403 | PermissionException |
| `resource_not_found` | Resource not found | 404 | ResourceNotFoundException |
| `validation_error` | Data validation failed | 400 | ValidationException |
| `database_error` | Database operation failed | 500 | DatabaseException |
| `business_logic_error` | Business rule violation | 400 | BusinessLogicException |
| `external_service_error` | External service failure | 502 | ExternalServiceException |
| `rate_limit_exceeded` | Rate limit exceeded | 429 | RateLimitException |
| `configuration_error` | Configuration issue | 500 | ConfigurationException |

### **HTTP Status Codes**

| Status Code | Description | Usage |
|-------------|-------------|-------|
| `200 OK` | Request successful | GET, PUT, DELETE operations |
| `201 Created` | Resource created successfully | POST operations |
| `400 Bad Request` | Invalid request data | Validation errors |
| `401 Unauthorized` | Authentication required | Missing or invalid token |
| `403 Forbidden` | Permission denied | Insufficient privileges |
| `404 Not Found` | Resource not found | Invalid ID or endpoint |
| `429 Too Many Requests` | Rate limit exceeded | Too many requests |
| `500 Internal Server Error` | Server error | Unexpected errors |
| `502 Bad Gateway` | External service error | Third-party service failure |

### **Error Response Examples**

#### **Validation Error (400)**
```json
{
    "success": false,
    "error": "Invalid user data",
    "code": "user_creation_validation_error",
    "details": {
        "email": ["This field is required."],
        "password": ["This password is too common."],
        "phone": ["Enter a valid phone number."]
    }
}
```

#### **Authentication Error (401)**
```json
{
    "success": false,
    "error": "Authentication failed",
    "code": "authentication_error",
    "details": "Invalid or expired token"
}
```

#### **Permission Error (403)**
```json
{
    "success": false,
    "error": "Permission denied",
    "code": "permission_denied",
    "details": "Insufficient privileges to access this resource"
}
```

#### **Resource Not Found (404)**
```json
{
    "success": false,
    "error": "User not found with ID: 999",
    "code": "resource_not_found",
    "details": "The requested user does not exist"
}
```

#### **Database Error (500)**
```json
{
    "success": false,
    "error": "Failed to create user",
    "code": "database_error",
    "details": "Database operation failed due to constraint violation"
}
```

## 🚀 Getting Started

### **1. Prerequisites**
- Python 3.8+
- Django 4.2+
- PostgreSQL (recommended) or SQLite
- Virtual environment

### **2. Installation**
```bash
# Clone the repository
git clone <repository-url>
cd meditrack360

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

### **3. Environment Variables**
Create a `.env` file with the following variables:
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/meditrack360
# or for SQLite: DATABASE_URL=sqlite:///db.sqlite3

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME=5
JWT_REFRESH_TOKEN_LIFETIME=1
```

### **4. Test the HMS API Flow**
1. **Register Admin**: `POST /api/v1/users/`
2. **Login Admin**: `POST /api/v1/auth/login/`
3. **Create Organization**: `POST /api/v1/organizations/`
4. **Register Staff**: `POST /api/v1/users/`

## 🧪 Testing Guide

### **1. Manual Testing with Postman**
- Import the provided Postman collection
- Set up environment variables
- Follow the HMS flow sequence
- Test all endpoints with different user roles

### **2. Sample Data for Testing**

#### **Sample Users for Testing**
```json
{
    "admin_user": {
        "email": "admin@meditrack360.com",
        "password": "Admin@2025#Secure!",
        "phone": "9876543210",
        "status": "active"
    },
    "doctor_user": {
        "email": "doctor@meditrack360.com",
        "password": "Doctor@2025#Secure!",
        "phone": "9876543211",
        "organization_id": 1,
        "role": {"name": "doctor"},
        "status": "active"
    },
    "nurse_user": {
        "email": "nurse@meditrack360.com",
        "password": "Nurse@2025#Secure!",
        "phone": "9876543212",
        "organization_id": 1,
        "role": {"name": "nurse"},
        "status": "active"
    },
    "technician_user": {
        "email": "technician@meditrack360.com",
        "password": "Tech@2025#Secure!",
        "phone": "9876543213",
        "organization_id": 1,
        "role": {"name": "technician"},
        "status": "active"
    }
}
```

#### **Sample Organization for Testing**
```json
{
    "organization": {
        "name": "MediTrack General Hospital",
        "type": "Hospital",
        "email": "contact@meditrack.com",
        "phone": "+919876543210",
        "status": "active",
        "address": {
            "city": "Salem",
            "state": "Tamil Nadu",
            "pincode": "636007",
            "country": "India"
        }
    }
}
```

#### **Sample Patients for Testing**
```json
{
    "patient_1": {
        "name": "John Doe",
        "age": 35,
        "gender": "M",
        "phone": "9876543210",
        "email": "john.doe@email.com",
        "date_of_birth": "1990-01-01",
        "blood_group": "O+",
        "medical_history": "No significant medical history",
        "allergies": "None known",
        "organization": 1
    },
    "patient_2": {
        "name": "Jane Smith",
        "age": 28,
        "gender": "F",
        "phone": "9876543211",
        "email": "jane.smith@email.com",
        "date_of_birth": "1997-05-15",
        "blood_group": "A+",
        "medical_history": "Asthma",
        "allergies": "Peanuts",
        "organization": 1
    },
    "patient_3": {
        "name": "Robert Johnson",
        "age": 45,
        "gender": "M",
        "phone": "9876543212",
        "email": "robert.johnson@email.com",
        "date_of_birth": "1980-12-10",
        "blood_group": "B+",
        "medical_history": "Hypertension",
        "allergies": "None known",
        "organization": 1
    }
}
```

#### **Sample Visits for Testing**
```json
{
    "visit_1": {
        "patient": 1,
        "doctor": 2,
        "technician": 3,
        "organization": 1,
        "scheduled_date": "2025-08-15T10:00:00Z",
        "priority": "medium",
        "symptoms": "Fever and headache",
        "notes": "Patient reports symptoms for 2 days"
    },
    "visit_2": {
        "patient": 2,
        "doctor": 2,
        "organization": 1,
        "scheduled_date": "2025-08-16T14:00:00Z",
        "priority": "high",
        "symptoms": "Chest pain and shortness of breath",
        "notes": "Emergency consultation required"
    },
    "visit_3": {
        "patient": 3,
        "doctor": 2,
        "technician": 3,
        "organization": 1,
        "scheduled_date": "2025-08-17T09:00:00Z",
        "priority": "low",
        "symptoms": "Routine checkup",
        "notes": "Annual health assessment"
    }
}
```

### **2. Automated Testing**
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.users
python manage.py test apps.organizations

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### **3. API Testing Scripts**
- `test_hms_api.py`: Basic HMS flow testing
- `test_hms_api_complete.py`: Comprehensive API testing

### **4. Testing Checklist**
- [ ] Admin registration without organization
- [ ] Admin login and token generation
- [ ] Organization creation
- [ ] Staff registration with organization
- [ ] Role-based access control
- [ ] CRUD operations for all models
- [ ] Soft delete functionality
- [ ] Error handling and validation
- [ ] Pagination and filtering
- [ ] Search functionality

### **5. Complete Testing Workflow**

#### **Step 1: Setup and Authentication**
```bash
# 1. Start the server
python manage.py runserver

# 2. Register admin user
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@meditrack360.com",
    "password": "Admin@2025#Secure!",
    "password_confirm": "Admin@2025#Secure!",
    "phone": "9876543210"
  }'

# 3. Login admin user
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@meditrack360.com",
    "password": "Admin@2025#Secure!"
  }'
```

#### **Step 2: Organization Management**
```bash
# 4. Create organization (use admin token)
curl -X POST http://localhost:8000/api/v1/organizations/ \
  -H "Authorization: Bearer <ADMIN_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MediTrack General Hospital",
    "type": "Hospital",
    "email": "contact@meditrack.com",
    "phone": "+919876543210",
    "address": {
      "city": "Salem",
      "state": "Tamil Nadu",
      "pincode": "636007",
      "country": "India"
    }
  }'

# 5. List organizations with filtering
curl -X GET "http://localhost:8000/api/v1/organizations/list/?status=active&type=Hospital&page=1&page_size=10" \
  -H "Authorization: Bearer <ADMIN_TOKEN>"
```

#### **Step 3: Staff Management**
```bash
# 6. Register doctor
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "doctor@meditrack360.com",
    "password": "Doctor@2025#Secure!",
    "password_confirm": "Doctor@2025#Secure!",
    "phone": "9876543211",
    "organization_id": 1,
    "role": {"name": "doctor"},
    "status": "active"
  }'

# 7. List users with advanced filtering
curl -X GET "http://localhost:8000/api/v1/users/list/?status=active&role=doctor&organization=1&page=1&page_size=20" \
  -H "Authorization: Bearer <ADMIN_TOKEN>"
```

#### **Step 4: Patient Management**
```bash
# 8. Create patient (use doctor token)
curl -X POST http://localhost:8000/api/v1/patients/create/ \
  -H "Authorization: Bearer <DOCTOR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 35,
    "gender": "M",
    "phone": "9876543210",
    "email": "john.doe@email.com",
    "blood_group": "O+",
    "medical_history": "No significant medical history",
    "allergies": "None known",
    "organization": 1
  }'

# 9. List patients with advanced filtering and pagination
curl -X GET "http://localhost:8000/api/v1/patients/?status=active&blood_group=O+&age_min=18&age_max=65&page=1&page_size=15&ordering=age" \
  -H "Authorization: Bearer <DOCTOR_TOKEN>"

# 10. Search patients by medical condition
curl -X GET "http://localhost:8000/api/v1/patients/?search=diabetes&status=active&page=1&page_size=10" \
  -H "Authorization: Bearer <DOCTOR_TOKEN>"
```

#### **Step 5: Visit Management**
```bash
# 11. Create visit
curl -X POST http://localhost:8000/api/v1/visits/create/ \
  -H "Authorization: Bearer <DOCTOR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "patient": 1,
    "doctor": 2,
    "organization": 1,
    "scheduled_date": "2025-08-15T10:00:00Z",
    "priority": "medium",
    "symptoms": "Fever and headache",
    "notes": "Patient reports symptoms for 2 days"
  }'

# 12. List visits with advanced filtering and pagination
curl -X GET "http://localhost:8000/api/v1/visits/?doctor=2&status=scheduled&date_from=2025-08-15&date_to=2025-08-15&page=1&page_size=20&ordering=scheduled_date" \
  -H "Authorization: Bearer <DOCTOR_TOKEN>"

# 13. Search visits by symptoms
curl -X GET "http://localhost:8000/api/v1/visits/?search=fever&priority=medium&page=1&page_size=15" \
  -H "Authorization: Bearer <DOCTOR_TOKEN>"
```

#### **Step 6: Visit Assignment and Management**
```bash
# 14. Assign visit to different doctor
curl -X PUT http://localhost:8000/api/v1/visits/660e8400-e29b-41d4-a716-446655440001/ \
  -H "Authorization: Bearer <DOCTOR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "doctor": 4,
    "notes": "Reassigned to specialist due to complex symptoms"
  }'

# 15. Complete visit
curl -X POST http://localhost:8000/api/v1/visits/660e8400-e29b-41d4-a716-446655440001/complete/ \
  -H "Authorization: Bearer <DOCTOR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "diagnosis": "Common cold",
    "prescription": "Rest, fluids, and over-the-counter medication",
    "notes": "Patient should return if symptoms worsen"
  }'
```

## 🚨 Error Handling Guide

### **1. Error Handling Strategy**
The API implements a multi-layered error handling approach:

#### **Layer 1: Custom Exceptions**
- **Domain-specific exceptions** for business logic violations
- **Resource exceptions** for not found scenarios
- **Validation exceptions** for data validation failures

#### **Layer 2: Serializer Validation**
- **Field-level validation** with detailed error messages
- **Custom validators** for business rules
- **Cross-field validation** for complex relationships

#### **Layer 3: Database Error Handling**
- **Integrity constraint violations** (unique fields, foreign keys)
- **Transaction failures** and rollback handling
- **Connection and timeout errors**

#### **Layer 4: Base Exception Handler**
- **Catch-all for unexpected errors**
- **Logging and monitoring** for debugging
- **Graceful degradation** with user-friendly messages

### **2. Error Handling Best Practices**

#### **Client-Side Error Handling**
```javascript
// Example error handling in JavaScript
try {
    const response = await fetch('/api/v1/users/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    });
    
    const result = await response.json();
    
    if (!result.success) {
        // Handle specific error codes
        switch (result.code) {
            case 'user_creation_validation_error':
                displayValidationErrors(result.details);
                break;
            case 'user_already_exists':
                showUserExistsMessage();
                break;
            default:
                showGenericError(result.error);
        }
    }
} catch (error) {
    handleNetworkError(error);
}
```

#### **Server-Side Error Handling**
```python
# Example error handling in views
try:
    # Business logic
    user = user_service.create_user(data)
    return success_response(data=user)
except ValidationException as e:
    logger.warning(f"Validation failed: {e.details}")
    return error_response(
        error_message=str(e),
        error_code=e.code,
        details=e.details
    )
except UserAlreadyExistsException as e:
    logger.warning(f"User already exists: {e.email}")
    return error_response(
        error_message=str(e),
        error_code=e.code
    )
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}", exc_info=True)
    return error_response(
        error_message="An unexpected error occurred",
        error_code="internal_server_error"
    )
```

### **3. Common Error Scenarios & Solutions**

#### **Validation Errors**
- **Password too common**: Use stronger passwords with special characters
- **Email already exists**: Check for existing users before registration
- **Invalid phone format**: Ensure phone numbers follow country format
- **Missing required fields**: Validate all required fields in frontend

#### **Authentication Errors**
- **Token expired**: Implement automatic token refresh
- **Invalid token**: Clear stored tokens and re-authenticate
- **Permission denied**: Check user role and permissions

#### **Database Errors**
- **Unique constraint violation**: Handle duplicate data gracefully
- **Foreign key constraint**: Ensure referenced resources exist
- **Connection timeout**: Implement retry logic with exponential backoff

### **4. Error Monitoring & Debugging**

#### **Logging Strategy**
- **Structured logging** with trace IDs for request tracking
- **Error categorization** by severity and type
- **Context information** for debugging (user ID, request data)

#### **Monitoring & Alerting**
- **Error rate monitoring** with thresholds
- **Performance metrics** for slow endpoints
- **Real-time alerts** for critical errors

#### **Debugging Tools**
- **Trace ID tracking** across request lifecycle
- **Detailed error logs** with stack traces
- **Request/response logging** for troubleshooting

## 📚 Additional Resources

### **Documentation**
- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **JWT Documentation**: https://django-rest-framework-simplejwt.readthedocs.io/

### **Tools**
- **Postman**: API testing and documentation
- **Swagger UI**: Interactive API documentation
- **ReDoc**: Alternative API documentation view

### **Support**
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check this document for common issues
- **Community**: Django and DRF community forums

## 🔍 Advanced Filtering & Search Reference

### **Filtering Operators**
All list endpoints support advanced filtering with the following operators:

#### **Text Search**
- `search`: Searches across multiple fields (case-insensitive)
- `exact`: Exact match (case-sensitive)
- `icontains`: Contains (case-insensitive)
- `istartswith`: Starts with (case-insensitive)
- `iendswith`: Ends with (case-insensitive)

#### **Numeric Filters**
- `exact`: Exact value match
- `gt`: Greater than
- `gte`: Greater than or equal
- `lt`: Less than
- `lte`: Less than or equal
- `range`: Value range (e.g., `age_min=18&age_max=65`)

#### **Date Filters**
- `date_from`: Filter from specific date
- `date_to`: Filter to specific date
- `year`: Filter by year
- `month`: Filter by month
- `day`: Filter by day

#### **Boolean Filters**
- `is_active`: True/false values
- `is_deleted`: Soft delete status
- `has_organization`: Check if resource has organization

### **Complex Filtering Examples**

#### **User Filtering**
```http
# Active doctors from specific organization, ordered by creation date
GET /api/v1/users/list/?status=active&role=doctor&organization=MediTrack&ordering=-created_at

# Users created in last 30 days with phone number
GET /api/v1/users/list/?created_at__gte=2025-07-12&phone__isnull=false

# Search users with specific email domain
GET /api/v1/users/list/?email__icontains=@meditrack.com&status=active
```

#### **Patient Filtering**
```http
# Patients with specific blood group and age range
GET /api/v1/patients/?blood_group=O+&age_min=18&age_max=65&status=active

# Search patients by medical condition
GET /api/v1/patients/?search=diabetes&status=active

# Patients from specific organization with address
GET /api/v1/patients/?organization=1&address__isnull=false
```

#### **Visit Filtering**
```http
# Today's scheduled visits for specific doctor
GET /api/v1/visits/?doctor=1&status=scheduled&date_from=2025-08-12&date_to=2025-08-12

# Urgent visits in next 24 hours
GET /api/v1/visits/?priority=urgent&scheduled_date__gte=2025-08-12T00:00:00Z&scheduled_date__lte=2025-08-13T00:00:00Z

# Completed visits with specific symptoms
GET /api/v1/visits/?status=completed&search=fever&ordering=-actual_date
```

### **Pagination Best Practices**

#### **Page Size Guidelines**
- **Small datasets**: 10-20 items per page
- **Medium datasets**: 20-50 items per page
- **Large datasets**: 50-100 items per page
- **Maximum**: 100 items per page (API limit)

#### **Performance Optimization**
```http
# Use appropriate page sizes
GET /api/v1/users/list/?page_size=50  # Good for large lists
GET /api/v1/users/list/?page_size=10  # Good for small screens

# Combine with ordering for consistent results
GET /api/v1/users/list/?ordering=id&page=2&page_size=20

# Use search with pagination
GET /api/v1/users/list/?search=doctor&page=1&page_size=15
```

#### **Pagination Response Headers**
```http
X-Total-Count: 150
X-Page-Count: 8
X-Current-Page: 2
X-Page-Size: 20
Link: <http://localhost:8000/api/v1/users/?page=3>; rel="next", <http://localhost:8000/api/v1/users/?page=1>; rel="prev"
```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- **Development Team**: MediTrack360 Development Team
- **API Design**: RESTful API with JWT authentication
- **Database Design**: PostgreSQL/SQLite with soft delete support

---

**Last Updated**: August 2025
**Version**: 1.0.0
**API Version**: v1
