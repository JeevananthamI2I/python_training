# User Management Commands

This directory contains Django management commands for user administration in the MediTrack360 Hospital Management System.

## Available Commands

### 1. `createsuperuser`

Enhanced superuser creation with validation and multiple options.

**Usage:**
```bash
# Interactive mode
python manage.py createsuperuser

# Non-interactive mode
python manage.py createsuperuser --email admin@example.com --password Admin1234! --non-interactive

# With additional options
python manage.py createsuperuser --email admin@example.com --password Admin1234! --first-name Admin --last-name User --organization "MediTrack Hospital" --non-interactive

# Force creation (even if superuser exists)
python manage.py createsuperuser --email admin@example.com --password Admin1234! --force --non-interactive
```

**Options:**
- `--email`: Email address for the superuser
- `--username`: Username for the superuser
- `--password`: Password for the superuser
- `--first-name`: First name for the superuser
- `--last-name`: Last name for the superuser
- `--phone`: Phone number for the superuser
- `--organization`: Organization name to create or assign
- `--non-interactive`: Run in non-interactive mode
- `--force`: Force creation even if superuser already exists

**Features:**
- Email format validation
- Password strength validation (8+ chars, uppercase, lowercase, digit, special char)
- Phone number validation
- Automatic organization and role creation
- Interactive confirmation

### 2. `listusers`

List users with various filtering and formatting options.

**Usage:**
```bash
# List all users
python manage.py listusers

# Filter by status
python manage.py listusers --status active

# Filter by organization
python manage.py listusers --organization "MediTrack"

# Search users
python manage.py listusers --search "john"

# Show only superusers
python manage.py listusers --superusers

# Show only staff users
python manage.py listusers --staff

# Show soft-deleted users
python manage.py listusers --deleted

# Custom fields
python manage.py listusers --fields email,full_name,role_name,created_at

# Different output formats
python manage.py listusers --format json
python manage.py listusers --format csv
```

**Options:**
- `--status`: Filter by user status (active, inactive, suspended)
- `--organization`: Filter by organization name
- `--role`: Filter by role name
- `--search`: Search in email, first_name, last_name, username
- `--superusers`: Show only superusers
- `--staff`: Show only staff users
- `--deleted`: Show soft-deleted users
- `--format`: Output format (table, json, csv)
- `--fields`: Comma-separated list of fields to display

### 3. `manageuser`

Manage users with various operations.

**Usage:**
```bash
# Activate user
python manage.py manageuser activate --email user@example.com

# Deactivate user
python manage.py manageuser deactivate --email user@example.com

# Soft delete user
python manage.py manageuser delete --email user@example.com

# Restore soft-deleted user
python manage.py manageuser restore --email user@example.com

# Change password
python manage.py manageuser change-password --email user@example.com --password NewPassword123!

# Assign role
python manage.py manageuser assign-role --email user@example.com --role "Doctor"

# Assign organization
python manage.py manageuser assign-org --email user@example.com --organization "MediTrack Hospital"

# Force operation without confirmation
python manage.py manageuser activate --email user@example.com --force

# Apply to all matching users
python manage.py manageuser activate --email "@example.com" --all
```

**Operations:**
- `activate`: Activate users
- `deactivate`: Deactivate users
- `delete`: Soft delete users
- `restore`: Restore soft-deleted users
- `change-password`: Change user password
- `assign-role`: Assign role to users
- `assign-org`: Assign organization to users

**Options:**
- `--email`: User email
- `--username`: User username (alternative to email)
- `--password`: New password (for change-password)
- `--role`: Role name (for assign-role)
- `--organization`: Organization name (for assign-org)
- `--force`: Force operation without confirmation
- `--all`: Apply operation to all matching users

### 4. `setup_initial_data`

Set up initial data for the Hospital Management System.

**Usage:**
```bash
# Setup everything
python manage.py setup_initial_data

# Skip users
python manage.py setup_initial_data --skip-users

# Skip organizations
python manage.py setup_initial_data --skip-organizations

# Skip roles
python manage.py setup_initial_data --skip-roles

# Force recreation of existing data
python manage.py setup_initial_data --force
```

**What it creates:**
- **Organizations:**
  - MediTrack General Hospital
  - MediTrack Clinic
  - MediTrack Laboratory

- **Roles:**
  - Super Admin (level 100)
  - Hospital Admin (level 80)
  - Doctor (level 60)
  - Nurse (level 50)
  - Technician (level 40)
  - Receptionist (level 30)
  - Viewer (level 10)

- **Default Users:**
  - admin@meditrack360.com (Super Admin)
  - hospital.admin@meditrack360.com (Hospital Admin)
  - doctor.smith@meditrack360.com (Doctor)
  - nurse.jones@meditrack360.com (Nurse)
  - tech.wilson@meditrack360.com (Technician)
  - reception.brown@meditrack360.com (Receptionist)

**Options:**
- `--skip-users`: Skip creating default users
- `--skip-organizations`: Skip creating default organizations
- `--skip-roles`: Skip creating default roles
- `--force`: Force recreation of existing data

## Enhanced create_superuser.py Script

The root directory contains an enhanced `create_superuser.py` script that provides additional functionality:

**Usage:**
```bash
# Interactive mode
python create_superuser.py

# Setup initial data
python create_superuser.py --setup

# Non-interactive mode
python create_superuser.py --email admin@example.com --password Admin1234!

# With additional options
python create_superuser.py --email admin@example.com --password Admin1234! --first-name Admin --last-name User --organization "MediTrack Hospital"
```

## Password Requirements

All password creation commands enforce the following requirements:
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character

## Security Features

- **Soft Delete**: Users are soft-deleted by default, preserving data integrity
- **Password Validation**: Strong password requirements enforced
- **Email Validation**: Proper email format validation
- **Transaction Safety**: All operations use database transactions
- **Confirmation Prompts**: Interactive confirmation for destructive operations

## Best Practices

1. **Use the setup command first**: Run `setup_initial_data` to create the basic structure
2. **Use strong passwords**: Always use strong passwords for production
3. **Confirm operations**: Use interactive mode for important operations
4. **Backup before bulk operations**: Always backup before running bulk user operations
5. **Test in development**: Test all commands in development before production

## Troubleshooting

**Common Issues:**

1. **"User not found"**: Check email/username spelling
2. **"Role not found"**: Run `setup_initial_data` to create roles
3. **"Organization not found"**: Run `setup_initial_data` to create organizations
4. **"Password too weak"**: Ensure password meets all requirements
5. **"Email already exists"**: Use `--force` flag or choose different email

**Getting Help:**
```bash
# Get help for any command
python manage.py createsuperuser --help
python manage.py listusers --help
python manage.py manageuser --help
python manage.py setup_initial_data --help
```
